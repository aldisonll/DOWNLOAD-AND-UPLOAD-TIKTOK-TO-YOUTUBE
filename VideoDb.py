import sqlite3 
import time

class VideoDB:

    def __init__(self, db_name):
        self.db_name = db_name
        
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

        self.c.execute('''
        CREATE TABLE IF NOT EXISTS VIDEOS
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            user                CHAR(30)  NOT NULL,
            videoLink           CHAR(60)  NOT NULL,
            videoCover          CHAR(60)  NOT NULL,
            description         CHAR(500) NOT NULL,
            videoPath           CHAR(100) NOT NULL,
            time                INT(11)   NOT NULL);
        ''')
            
        self.conn.commit()

    def show_videos(self):
        self.c.execute('''
            SELECT * FROM 'VIDEOS' 
        ''')

        return self.c.fetchall()

    def add_video(self, videoInfo):
        user = videoInfo.get('user')
        videoLink = videoInfo.get('videoLink')
        videoCover = videoInfo.get('videoCover')
        description = videoInfo.get('description')
        videoPath = videoInfo.get('videoPath')


        self.c.execute('''
            INSERT INTO VIDEOS 
                    (ID, user, videoLink, videoCover ,description, videoPath, time)
            VALUES 
                    (NULL, ?, ?, ?, ?, ?, ?);
            ''', (user, videoLink, videoCover, description, videoPath, int(time.time()),)
        )

        self.conn.commit()
        self.conn.close()


    def delete_video(self, ID):
        self.c.execute('''
            DELETE FROM 'VIDEOS' WHERE ID = ?;
        ''', (ID,))

        self.conn.commit()
        self.conn.close()
