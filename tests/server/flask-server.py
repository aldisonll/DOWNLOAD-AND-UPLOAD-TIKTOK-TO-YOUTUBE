from flask import Flask, render_template, request, jsonify

import sys
from threading import Thread

app = Flask(__name__,
            template_folder='../public/template',
            static_folder='../public/static'
            )

sys.path.insert(0,'../..') # parent-parent path

from tikTokDownloader import TikTokDownloader
from VideoDb import VideoDB
from youtubeSearchSuggestions import YouTubeTagGenerator
from youtubeUploader import upload

tiktok = TikTokDownloader()
Tags = YouTubeTagGenerator()

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

        videoDb.add_video({"user": user, "videoLink": videoLink, "videoCover": videoCover, "description": description, "videoPath": path})

        return jsonify({'status': 'ok', 'message': 'successfuly downloaded'})

    except:
    
        return jsonify({'status':'error', 'message': 'something went wrong'})   

@app.route('/api/all-downloaded')
def all_downloaded():

    videoDb = VideoDB('VideoDB.db')
    videos = videoDb.show_videos()
    videos.reverse()

    return jsonify({'status': 'ok', 'videos': videos}) if len(videos) > 0 else jsonify({'status': 'error'})

@app.route('/api/remove-video')
def remove_video():

    videoId = request.args.get('id')

    videoDb = VideoDB('VideoDB.db')
    videoDb.delete_video(videoId)  

    return jsonify({'status': 'ok'})    

@app.route('/api/tags-suggestions')
def tag_suggestions():

    query = request.args.get('query')
    tags = Tags.show_tags(query)

    return jsonify({'status': 'ok', 'tags': tags})

@app.route('/api/upload-video')
def upload_video():

    file = request.args.get('file') 
    title = request.args.get('title') 
    description = request.args.get('description') 
    keywords = request.args.get('keywords')
    
    Thread(target=upload,kwargs={'file': file, 'title': title, 'description': description, 'keywords': keywords}).start()
    return "done"

if "__main__" == __name__:
    app.run(port=3333, debug=True)