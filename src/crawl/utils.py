def correct_channel_name(name: str) -> str:
    if name[0] != "@":
        new_name = "@"+name
        return new_name
