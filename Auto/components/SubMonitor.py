"""
    Send Request to subtitle server and return the result.
"""
import requests
import Bot.blibot.global_var as gl
class SubMonitor:
    def __init__(self, url:str,paras:dict):
        r = requests.get(url,params=paras)
        r.json()


if __name__ == "__main__":
    SubMonitor()