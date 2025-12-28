import requests


def get_size(bytes_count):
    """
    converts byte to make we readable
    """
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes_count < 1024:
            return f"{bytes_count:.2f}{unit}B"
        bytes_count /= 1024
    return f"{bytes_count:.2f}PB"


def get_public_ip():
    """
    get ip for the 'show ip button'
    """
    try:
        return requests.get("https://api.ipify.org").text
    except Exception:
        return "Error"
