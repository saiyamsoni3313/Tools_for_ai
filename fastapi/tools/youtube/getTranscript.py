from proxy import ProxyManager
from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse as urlparse
from tools.youtube.models import (
    Language,
    Transcription,
    TranscriptionResponse,
    TranscriptionObject,
    TranscriptionResponseVideo,
)
from typing import List
from tools.openAI import process_search_results
from pytube import Playlist
import re


def get_youtube_playlist_urls(playlist_url):
    try:
        playlist = Playlist(playlist_url)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        video_urls = list(playlist.video_urls)
        return video_urls
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def getVideoId(URL):
    """
    Extract the YouTube video ID from various URL formats, including YouTube Shorts.

    Examples:
    - https://www.youtube.com/shorts/Fwy4_Q4lTZE
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse.urlparse(URL)
    if query.hostname == "youtu.be":
        return query.path[1:]
    if query.hostname in ("www.youtube.com", "youtube.com"):
        if query.path.startswith("/shorts/"):
            return query.path.split("/")[2]
        if query.path == "/watch":
            p = urlparse.parse_qs(query.query)
            return p["v"][0]
        if query.path.startswith("/embed/"):
            return query.path.split("/")[2]
        if query.path.startswith("/v/"):
            return query.path.split("/")[2]
    return None


def extract_video_ids(url):
    """
    Accepts either a YouTube video URL or a playlist URL and returns a list of video IDs.

    :param url: str - The URL of a YouTube video or playlist.
    :return: list - A list of YouTube video IDs.
    """
    video_ids = []
    urls = []
    if "playlist" in url:
        # It's a playlist
        video_urls = get_youtube_playlist_urls(url)
        for video_url in video_urls:
            video_id = getVideoId(video_url)
            if video_id:
                video_ids.append(video_id)
                urls.append(video_url)
    else:
        # It's a single video
        video_id = getVideoId(url)
        if video_id:
            video_ids.append(video_id)
            urls.append(url)

    return video_ids, urls


def makeSlots(transcription, summarize, entities) -> List[TranscriptionObject]:
    result: List[TranscriptionObject] = []

    if summarize:
        parsed_content = process_search_results(None, str(transcription), entities)
        for obj in transcription:
            last_start = obj["start"]
            last_duration = obj["duration"]

        # Calculate the total duration
        total_duration = last_start + last_duration

        return [
            TranscriptionObject(text=parsed_content, start=0, duration=total_duration)
        ]

    text = ""
    dur = 0
    start = 0
    for obj in transcription:
        text += " " + obj["text"]
        dur += obj["duration"]
        start = min(start, obj["start"])

        if dur > 30:
            result.append(TranscriptionObject(text=text, start=start, duration=dur))
            text = ""
            start = start + dur
            dur = 0

    result.append(TranscriptionObject(text=text, start=start, duration=dur))
    return result


def getTranscription(data: Transcription) -> TranscriptionResponse:

    proxy_manager = ProxyManager()
    proxy = proxy_manager.get_proxy()
    response: List[TranscriptionResponseVideo] = []
    responseURLs = []
    for url in data.urls:
        try:
            print(f"Getting Video Ids for {url}")
            videoIds, videoURL = extract_video_ids(url)
            for videoId, url in zip(videoIds, videoURL):
                print(f"Getting transcription for {url}")
                transcription = YouTubeTranscriptApi.get_transcript(
                    video_id=videoId,
                    languages=[data.language.value, Language.English_US.value],
                    proxies=proxy,
                )
                response.append(
                    TranscriptionResponseVideo(
                        transcript=makeSlots(
                            transcription, data.summarize, data.entities
                        )
                    )
                )
                responseURLs.append(url)
        except Exception as e:
            print(f"Error getting transcription for {url}: {e}")
            proxy_manager.remove_and_update_proxy(proxy)
            response.append(TranscriptionResponseVideo(transcript=[]))
            continue
    return TranscriptionResponse(urls=responseURLs, transcripts=response)
