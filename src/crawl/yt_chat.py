from typing import Optional, List

from tqdm import tqdm
import re

from chat_downloader.sites.common import Chat as BaseChat
from chat_downloader.sites import YouTubeChatDownloader
from chat_downloader.formatting.format import ItemFormatter

from .utils import replace_emoji_in_string


__all__ = ['Chat', 'YTChat']


class Chat(BaseChat):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formatter = ItemFormatter()

    def format(self, item):
        return self.formatter.format(item, format_name='youtube')


class YTChat(YouTubeChatDownloader):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.default_params = dict(
            max_attempts=15,
            message_groups=['messages'],
            buffer_size=4096,
            message_receive_timeout=0.1
        )

    def get_chat_by_video_id(self,
                             video_id,
                             params: Optional[dict] = None) -> List[dict]:
        """Get chat messages for a YouTube video, given its ID.

        :param video_id: YouTube video ID
        :type video_id: str
        :return: Chat object for the corresponding YouTube video
        :rtype: Chat
        """

        if params is None:
            params = self.default_params

        initial_info, ytcfg = self._get_initial_video_info(video_id, params)

        chat_object = Chat(
            self._get_chat_messages(initial_info, ytcfg, params),
            id=video_id,
            **initial_info
        )

        chat_infos = []
        for mess in tqdm(chat_object, desc=f"Getting chat from {video_id}"):
            text = chat_object.format(mess)
            text = replace_emoji_in_string(text)
            chat_info = self._text_to_chat_data(text)
            if chat_info:
                chat_infos.append(chat_info)

        return chat_infos

    def _text_to_chat_data(self, line: str) -> dict:
        """
        Parse the text to a dict with specified fields
        """
        timestamp_pattern = re.compile(
            r'(?P<timestamp>-?(\d+:)?\d+:\d+) \|'
        )
        timestamp_match = re.match(timestamp_pattern, line)
        timestamp = None
        if timestamp_match:
            timestamp = timestamp_match.group("timestamp")

        mbs_match = re.search(r'\((New\s+member)|(Member\s*\(\d+\s*((years?)|(months?))\))\)', line)
        mbs_status = "Not Member"
        if mbs_match:
            mbs_status = mbs_match.group().strip()
            # Cuz regex sux
            if mbs_status[0] == "(":
                mbs_status = mbs_status[1:]
            if mbs_status[-1] == ")":
                mbs_status = mbs_status[:-1]

        account_line = line.split('|')[1]
        account_line = re.sub(
            r"\((New\s+member)|(Member\s*\(\d+\s*((years?)|(months?))\))\)",
            '', account_line)
        account_line = re.sub(r"\(|\)", '', account_line)
        yt_account = account_line.strip().split(':')[0]
        chat_content = account_line.strip().split(':')[1]

        data_dict = {
            "timestamp": timestamp if timestamp else "N/A",
            "mbs_status": mbs_status,
            "yt_account": yt_account,
            "chat_content": chat_content
        }

        return data_dict
