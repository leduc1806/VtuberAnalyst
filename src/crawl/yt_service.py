from typing import List, Union
from googleapiclient.http import HttpRequest

from googleapiclient.discovery import build

import logging
logging.basicConfig(level=logging.INFO)

from .utils import correct_channel_name


class YTService:
    def __init__(self,
                 developer_key: str):
        self.service = build(
            'youtube', 'v3', developerKey=developer_key
        )
        self.yt_chat = None

    def get_channel_id_from_name(self, name: str) -> str:
        name = correct_channel_name(name)
        request: HttpRequest = self.service.search().list(
            q=name,
            part='id',
            type='channel',
            maxResults=1,
            fields='items(id(channelId))'
        )
        response = request.execute()
        channel_id = response['items'][0]['id']['channelId']

        return channel_id

    def channel_info_from_channel_id(self, channel_id: str) -> dict:
        request: HttpRequest = self.service.channels().list(
            part='brandingSettings, snippet, statistics',
            id=channel_id,
            fields='items('
                   'snippet(thumbnails(high)),'
                   'brandingSettings(channel(title,unsubscribedTrailer,country), image(bannerExternalUrl)),'
                   'statistics)'
        )
        response = request.execute()

        return response

    def get_all_streamIDs_from_channel_id(self, channel_id: str) -> List[str]:
        stream_ids = []
        page_token = ""
        while True:
            request: HttpRequest = self.service.search().list(
                part='id',
                channelId=channel_id,
                maxResults=50,
                order="date",
                type="video",
                eventType="completed",
                pageToken=page_token
            )
            response = request.execute()
            current_stream_ids = [item['id']['videoId'] for item in response['items']]
            stream_ids.extend(current_stream_ids)

            num_results = len(response['items'])
            logging.info(f"Found {num_results} streams on page token {page_token}")

            if 'nextPageToken' in response.keys():
                page_token = response['nextPageToken']
            else:
                break

        num_streams = len(stream_ids)
        logging.info(f"Found {num_streams} streams from channel {channel_id}")

        return stream_ids

    def get_video_info_from_video_ids(
            self,
            video_ids: Union[str, List[str]],
            infos: List[str] = ['snippet', 'statistics', 'contentDetails',
                                'liveStreamingDetails', 'topicDetails']) -> dict:
        part = ",".join(info for info in infos)
        if isinstance(video_ids, list):
            video_ids = ",".join(video_id for video_id in video_ids)
        request: HttpRequest = self.service.videos().list(
            part=part,
            id=video_ids
        )
        response = request.execute()
        return response
