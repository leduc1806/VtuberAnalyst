from googleapiclient.http import HttpRequest

from googleapiclient.discovery import build

from .utils import correct_channel_name


class YTService:
    def __init__(self,
                 developer_key: str,
                 max_result: int = 5):
        self.service = build(
            'youtube', 'v3', developerKey=developer_key
        )
        self.max_result = max_result

    def get_channelID_from_name(self, name: str) -> str:
        name = correct_channel_name(name)
        request: HttpRequest = self.service.search().list(
            q=name,
            part='id',
            type='channel',
            maxResults=1
        )
        response = request.execute()
        channel_id = response['items'][0]['id']['channelId']

        return channel_id
