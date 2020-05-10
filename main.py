# 两种文件类型：
#   1. "templateCode": "LanguagePresentationNew"；
#   2. "templateCode": "LngComp"。

import lngComp
import presentationNew
import getAudio
import ankiFormat

import json
import logging

if __name__ == "__main__":
    # set the log file format
    logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
                    filename='new.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )

    # open the json file
    jsonpath=r'EF-presentationNew\jsondir\basic.json'
    with open(jsonpath, 'r', encoding='utf-8') as f:
        content = json.loads(f.read())

    for item in content:
        # the first type of question
        if item[0]['templateCode'] == 'LanguagePresentationNew':
            text=presentationNew.getSiglePage(item)
            # logging.debug(content)
            ankiFormat.writeToTxt(text)
            # ask=input('是否要继续Y/F：')
            # if ask=='Y':
            #     continue
            # else:
            #     break   
        elif item[0]['templateCode'] == 'LngComp':
            text=lngComp.getPage(item)
            ankiFormat.writeToTxt(text)
    
    
    # write to Anki support file
    
    # 问题：
    #  <td style=width> 没有办法完全匹配替换