from typing import List, Optional

import re
import warnings
import datetime


def correct_channel_name(name: str) -> str:
    if name[0] != "@":
        new_name = "@"+name
        return new_name


def extract_urls_from_string(string: str) -> List[str]:
    urls = re.findall(r'(https?://[^\s]+)', string)
    if len(urls) == 0:
        warnings.warn("Can't find any url")
    return urls


def extract_name_from_url(url: str) -> Optional[str]:
    match = re.search(r'/@([^/]+)', url)
    if match:
        name = match.group(1)
        return name
    return None


def parse_iso_duration(iso_duration: str) -> str:
    pass


def parse_iso_datetime(iso_datetime: str) -> str:
    iso_datetime = iso_datetime.strip()
    if iso_datetime[-1] == "Z": # Denoting UTC
        iso_datetime = iso_datetime[:-1]
    try:
        dt_obj = datetime.datetime.fromisoformat(iso_datetime)
        readable_time = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
        return readable_time
    except ValueError as e:
        warnings.warn(f"Error: {e}")
        return "N/A"


def replace_emoji_in_string(string: str, tag: str = "<emoji>") -> str:
    emoji_pattern = re.compile(r':[a-zA-Z_][a-zA-Z0-9_-]*:')
    modified_string = re.sub(emoji_pattern, tag, string)
    return modified_string


# ----------- Example -----------
if __name__ == '__main__':
    string = ("- Lunaby: https://www.youtube.com/@LUNABY_HOJO\n"
              "- Sim Chan: https://www.youtube.com/@simchan_hojo")
    print(string)
    vtuber_urls = extract_urls_from_string(string)
    vtuber_names = []
    for url in vtuber_urls:
        vtuber_names.append(
            correct_channel_name(extract_name_from_url(url))
        )
    print(vtuber_names)
