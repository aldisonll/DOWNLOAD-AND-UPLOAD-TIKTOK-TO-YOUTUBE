import os, re, time, requests
from fake_useragent import UserAgent
from helpers import tikTokRegex, unwantedStrings

class TikTokDownloader():
    def __init__(self):
        self.ua = UserAgent()
        self.cookies = self.generated_cookies
    
    @property
    def generated_cookies(self):
        return requests.get('https://www.tiktok.com/').headers['Set-Cookie']

    @property
    def __tiktokInfo__headers__(self):
        return {
            'user-agent': self.ua.random,
            'cookie': self.cookies,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }
        
    def __tiktokVideo__headers__(self, ref: str):
        return  {
            'Referer': ref,
            'User-Agent': self.ua.random,
            'Range': 'bytes=0-',
        } 

    def unicode_escape(self, str: str):
        return str.encode().decode('unicode-escape')

    def rem_unwantedStrings(self, str: str, rm: list):
        for r in rm:
            str = str.replace(r, '')
        return str    

    def get_html(self, url: str):
        return requests.get(url, headers=self.__tiktokInfo__headers__).text

    def get_video_info(self, html: str):
        videoLink = self.rem_unwantedStrings(re.search(tikTokRegex["videoLink"], html)[0], unwantedStrings["videoLink"])
        user = self.rem_unwantedStrings(re.search(tikTokRegex["user"], html)[0], unwantedStrings["user"])
        videoCover = self.rem_unwantedStrings(re.search(tikTokRegex["videoCover"], html)[0], unwantedStrings["videoCover"])
        description = self.rem_unwantedStrings(re.search(tikTokRegex["description"], html)[0], unwantedStrings["description"])

        return dict({
            "videoLink": self.unicode_escape(videoLink), 
            "user": self.unicode_escape(user),
            "videoCover": self.unicode_escape(videoCover),
            "description": description
        })
        
    def download(self, url: str, videoName: str, path: str):
        if not os.path.isdir(path):
            os.mkdir(path)

        video_path = f"{path}/{videoName}_{int(time.time())}.mp4" 

        req = requests.get(url, headers=self.__tiktokVideo__headers__(url))
        
        with open(video_path, "wb") as video:
            video.write(req.content)

        return { "video_path": video_path }    
