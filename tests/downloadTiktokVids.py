import sys
sys.path.insert(0,'..')

from tikTokDownloader import TikTokDownloader

tiktok = TikTokDownloader()

# # get html of tiktok link
# html = tiktok.get_html('https://www.tiktok.com/@eurovision.albania/video/7035017824565218566?sender_device=pc&sender_web_id=6966645226976183813&is_from_webapp=v1&is_copy_url=0')
# # get all infos from the link
# video_info = tiktok.get_video_info(html)
# # get videoLink, user, videoCover, description from html
# videoLink, user, videoCover, description = video_info["videoLink"], video_info["user"], video_info["videoCover"], video_info["description"]

# # download this video 
# downloaded_video_path = tiktok.download(videoLink, user, "videos")
# # # print path of this video
# print(downloaded_video_path)