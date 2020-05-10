import requests
import re
import time
import logging

def getAudioName(url):
    if len(url)==0:
        logging.error('URL为空，请检查URL的数值！')
        return 0
    regex=re.compile(r"[A-Z]*[\.\w]*mp3")
    test_str = url
    matches=regex.search(test_str)
    return matches.group()

def getAudio(url):
    if len(url)==0:
        logging.error('URL为空，请检查URL的数值！')
        return 0
    logging.debug('current URL: ' + url)
    time.sleep(5)
    res = requests.get(url)
    
    filePath=r'D:\E.EF\AnkiDataFolder'
    audioName=getAudioName(url)
    intact_path=filePath + '\\' + audioName

    with open(intact_path, 'wb') as mp3:
        mp3.write(res.content)
        print('成功写入音频文件: '+audioName)
    return '[sound:'+audioName+']'

if __name__ == "__main__":
    # 要注意这个音频网页是不是能用
    pass