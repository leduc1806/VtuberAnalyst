from typing import List, Optional

import re
import warnings


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