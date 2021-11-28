from flask import Flask, render_template, request, jsonify
import sys

app = Flask(__name__,
            template_folder='../public/template',
            static_folder='../public/static'
            )

sys.path.insert(0,'../..') # parent-parent path

from tikTokDownloader import TikTokDownloader
from VideoDb import VideoDB

tiktok = TikTokDownloader()

@app.route('/index.html')
@app.route('/')
def my_app():
    return render_template('index.html')

@app.route('/api/download-video')
def downloaded_videos():

    url = request.args.get('url')

    try:
    
        videoDb = VideoDB('VideoDB.db')
        
        html = tiktok.get_html(url)
        video_info = tiktok.get_video_info(html)
        videoLink, user, videoCover, description = video_info["videoLink"], video_info["user"], video_info["videoCover"], video_info["description"]
        path = tiktok.download(videoLink, user, "videos")["video_path"]

        videoDb.add_video({"user": user, "videoLink":videoLink, "videoCover": videoCover, "description": description, "videoPath": path})

        return jsonify({'status': 'ok', 'message': 'successfuly downloaded'})

    except:
    
        return jsonify({'status':'error', 'message': 'something went wrong'})   

@app.route('/api/all-downloaded')
def all_downloaded():

    videoDb = VideoDB('VideoDB.db')
    videos = videoDb.show_videos()
    videos.reverse()

    if len(videos) > 0:
        return jsonify({'status': 'ok', 'videos': videos})
    return jsonify({'status': 'error'})

@app.route('/api/remove-video')
def remove_video():

    videoId = request.args.get('id')

    videoDb = VideoDB('VideoDB.db')
    videoDb.delete_video(videoId)  
    

    return jsonify({'status': 'ok'})    

if "__main__" == __name__:
    app.run(port=3333, debug=True)