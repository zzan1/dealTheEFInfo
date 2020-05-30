import requests
import re
import time
import logging
import random
import os


def getAudioName(url):
    if len(url) == 0:
        logging.error('URL为空，请检查URL的数值！')
        return 0
    regex = re.compile(r"[A-Z]*[\.\w]*mp3")
    test_str = url
    matches = regex.search(test_str)
    return matches.group()


def getAudio(url):
    if len(url) == 0:
        logging.error('URL为空，请检查URL的数值！')
        return 0
    logging.debug('current URL: ' + url)
    

    filePath = r'D:\E.EF\AnkiDataFolder'
    audioName = getAudioName(url)
    intact_path = filePath + '\\' + audioName
    if not os.path.isfile(intact_path):
        sleep_time = random.randint(1, 5)
        time.sleep(sleep_time)
        res = requests.get(url)
    
        with open(intact_path, 'wb') as mp3:
            mp3.write(res.content)
            print('成功写入音频文件: '+audioName)
    else:
        print(f'{audioName}文件已经存在!')
        
    return '[sound:'+audioName+']'


if __name__ == "__main__":
    # 要注意这个音频网页是不是能用
    pass
