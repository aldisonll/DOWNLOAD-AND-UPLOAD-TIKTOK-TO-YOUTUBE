import re

tikTokRegex = {
    "videoLink": r'(downloadAddr\":\")(.*?)(vr=)',
    "user": r'(uniqueId\":\").[a-zA-Z0-9._]+',
    "videoCover": r'(\"cover\":\").*(\",\"originCover\")',
    "description": r'\"desc\":\"(.*?)\"createTime'
}

unwantedStrings = {
    "videoLink": ['downloadAddr":"'],
    "user": ['uniqueId":"'],
    "videoCover": ['"cover":"', '","originCover"'],
    "description": ['"desc":"', '","createTime']
}