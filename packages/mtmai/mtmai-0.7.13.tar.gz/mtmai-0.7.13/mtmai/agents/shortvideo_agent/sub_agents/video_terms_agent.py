import json
import os
import random
from typing import List
from urllib.parse import urlencode

import requests
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.events import Event
from google.genai import types  # noqa
from json_repair import repair_json
from loguru import logger
from moviepy.video.io.VideoFileClip import VideoFileClip
from mtmai.core.config import settings
from mtmai.model_client import get_default_litellm_model
from mtmai.NarratoAI import config
from mtmai.NarratoAI.schema import MaterialInfo, VideoAspect, VideoConcatMode
from mtmai.NarratoAI.utils import mpt_utils as utils


def search_videos_pexels(
    search_term: str,
    minimum_duration: int,
    video_aspect: VideoAspect = VideoAspect.portrait,
) -> List[MaterialInfo]:
    aspect = VideoAspect(video_aspect)
    video_orientation = aspect.name
    video_width, video_height = aspect.to_resolution()
    # api_key = get_api_key("pexels_api_keys")
    api_key = settings.PEXELS_API_KEYS[0]
    headers = {
        "Authorization": api_key,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    }
    # Build URL
    params = {"query": search_term, "per_page": 20, "orientation": video_orientation}
    query_url = f"https://api.pexels.com/videos/search?{urlencode(params)}"
    logger.info(f"searching videos: {query_url}, with proxies: {config.proxy}")

    try:
        r = requests.get(
            query_url,
            headers=headers,
            proxies=config.proxy,
            verify=False,
            timeout=(30, 60),
        )
        response = r.json()
        video_items = []
        if "videos" not in response:
            logger.error(f"search videos failed: {response}")
            return video_items
        videos = response["videos"]
        # loop through each video in the result
        for v in videos:
            duration = v["duration"]
            # check if video has desired minimum duration
            if duration < minimum_duration:
                continue
            video_files = v["video_files"]
            # loop through each url to determine the best quality
            for video in video_files:
                w = int(video["width"])
                h = int(video["height"])
                if w == video_width and h == video_height:
                    item = MaterialInfo()
                    item.provider = "pexels"
                    item.url = video["link"]
                    item.duration = duration
                    video_items.append(item)
                    break
        return video_items
    except Exception as e:
        logger.error(f"search videos failed: {str(e)}")

    return []


def search_videos_pixabay(
    search_term: str,
    minimum_duration: int,
    video_aspect: VideoAspect = VideoAspect.portrait,
) -> List[MaterialInfo]:
    aspect = VideoAspect(video_aspect)

    video_width, video_height = aspect.to_resolution()

    # api_key = get_api_key("pixabay_api_keys")
    api_key = settings.PIXABAY_API_KEYS[0]
    # Build URL
    params = {
        "q": search_term,
        "video_type": "all",  # Accepted values: "all", "film", "animation"
        "per_page": 50,
        "key": api_key,
    }
    query_url = f"https://pixabay.com/api/videos/?{urlencode(params)}"
    logger.info(f"searching videos: {query_url}, with proxies: {config.proxy}")

    try:
        r = requests.get(
            query_url, proxies=config.proxy, verify=False, timeout=(30, 60)
        )
        response = r.json()
        video_items = []
        if "hits" not in response:
            logger.error(f"search videos failed: {response}")
            return video_items
        videos = response["hits"]
        # loop through each video in the result
        for v in videos:
            duration = v["duration"]
            # check if video has desired minimum duration
            if duration < minimum_duration:
                continue
            video_files = v["videos"]
            # loop through each url to determine the best quality
            for video_type in video_files:
                video = video_files[video_type]
                w = int(video["width"])
                # h = int(video["height"])
                if w >= video_width:
                    item = MaterialInfo()
                    item.provider = "pixabay"
                    item.url = video["url"]
                    item.duration = duration
                    video_items.append(item)
                    break
        return video_items
    except Exception as e:
        logger.error(f"search videos failed: {str(e)}")

    return []


def save_video(video_url: str, save_dir: str = "") -> str:
    if not save_dir:
        save_dir = utils.storage_dir("cache_videos")

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    url_without_query = video_url.split("?")[0]
    url_hash = utils.md5(url_without_query)
    video_id = f"vid-{url_hash}"
    video_path = f"{save_dir}/{video_id}.mp4"

    # if video already exists, return the path
    if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
        logger.info(f"video already exists: {video_path}")
        return video_path

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    # if video does not exist, download it
    with open(video_path, "wb") as f:
        f.write(
            requests.get(
                video_url,
                headers=headers,
                proxies=config.proxy,
                verify=False,
                timeout=(60, 240),
            ).content
        )

    if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
        try:
            clip = VideoFileClip(video_path)
            duration = clip.duration
            fps = clip.fps
            clip.close()
            if duration > 0 and fps > 0:
                return video_path
        except Exception as e:
            try:
                os.remove(video_path)
            except Exception:
                pass
            logger.warning(f"invalid video file: {video_path} => {str(e)}")
    return ""


def download_videos(
    output_dir: str,
    search_terms: List[str],
    # 音频时长
    audio_duration: float,
    source: str = "pexels",
    video_aspect: VideoAspect = VideoAspect.portrait,
    video_contact_mode: VideoConcatMode = VideoConcatMode.random,
    # 最大剪辑时长
    max_clip_duration: int = 5,
) -> List[str]:
    valid_video_items = []
    valid_video_urls = []
    found_duration = 0.0
    search_videos = search_videos_pexels
    if source == "pixabay":
        search_videos = search_videos_pixabay

    if audio_duration <= 0:
        raise ValueError("audio_duration must be greater than 0")

    for search_term in search_terms:
        video_items = search_videos(
            search_term=search_term,
            minimum_duration=max_clip_duration,
            video_aspect=video_aspect,
        )
        logger.info(f"found {len(video_items)} videos for '{search_term}'")

        for item in video_items:
            if item.url not in valid_video_urls:
                valid_video_items.append(item)
                valid_video_urls.append(item.url)
                found_duration += item.duration

    logger.info(
        f"found total videos: {len(valid_video_items)}, required duration: {audio_duration} seconds, found duration: {found_duration} seconds"
    )
    video_paths = []

    material_directory = config.app.get("material_directory", "").strip()
    if material_directory == "task":
        material_directory = output_dir
    elif material_directory and not os.path.isdir(material_directory):
        material_directory = ""

    if video_contact_mode.value == VideoConcatMode.random.value:
        random.shuffle(valid_video_items)

    total_duration = 0.0
    for item in valid_video_items:
        logger.info(f"downloading video: {item.url}")
        saved_video_path = save_video(video_url=item.url, save_dir=material_directory)
        if saved_video_path:
            logger.info(f"video saved: {saved_video_path}")
            video_paths.append(saved_video_path)
            seconds = min(max_clip_duration, item.duration)
            total_duration += seconds
            if total_duration > audio_duration:
                logger.info(
                    f"total duration of downloaded videos: {total_duration} seconds, skip downloading more"
                )
                break
    return video_paths


def after_agent_callback(callback_context: CallbackContext):
    # 修正 video_terms 的类型, 确保为json array
    video_terms = callback_context.state.get("video_terms")
    if video_terms:
        if isinstance(video_terms, str):
            video_terms = json.loads(repair_json(video_terms))
        callback_context.state["video_terms"] = video_terms
    # 下载素材
    output_dir = callback_context.state["output_dir"]

    video_terms = callback_context.state["video_terms"]

    downloaded_videos = download_videos(
        output_dir=output_dir,
        search_terms=video_terms,
        audio_duration=callback_context.state["audio_duration"],
    )
    if not downloaded_videos:
        return Event(
            author=callback_context.agent.name,
            content=types.Content(
                role="assistant",
                parts=[types.Part(text="素材收集失败")],
            ),
        )
    callback_context.state["downloaded_videos"] = downloaded_videos
    return Event(
        author=callback_context.agent_name,
        content=types.Content(
            role="assistant",
            parts=[
                types.Part(
                    text="素材收集完成, 素材数量: {}".format(len(downloaded_videos))
                )
            ],
        ),
        actions={
            "state_delta": {
                "downloaded_videos": downloaded_videos,
            },
        },
    )


video_terms_agent = LlmAgent(
    name="video_terms_generator",
    model=get_default_litellm_model(),
    instruction="""
    # Role: Video Search Terms Generator

    ## Goals:
    Generate {video_terms_amount} search terms for stock videos, depending on the subject of a video.

    ## Constrains:
    1. the search terms are to be returned as a json-array of strings.
    2. each search term should consist of 1-3 words, always add the main subject of the video.
    3. you must only return the json-array of strings. you must not return anything else. you must not return the script.
    4. the search terms must be related to the subject of the video.
    5. reply with english search terms only.

    ## Output Example:
    ["search term 1", "search term 2", "search term 3","search term 4","search term 5"]

    ## Context:
    ### Video Subject
    {video_subject}

    ### Video Script
    {video_script}

    Please note that you must use English for generating video search terms; Chinese is not accepted.
    """.strip(),
    # input_schema=None,
    output_key="video_terms",
    after_agent_callback=after_agent_callback,
)
