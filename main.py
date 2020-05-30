# 两种文件类型：
#   1. "templateCode": "LanguagePresentationNew"；
#   2. "templateCode": "LngComp"。

import lngComp
import presentationNew
import getAudio
import ankiFormat

import json
import logging
import time


def main(jsonpath):
    # set the log file format
    logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                        filename=r'EF-presentationNew/new.log',
                        filemode='w',  # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                        # a是追加模式，默认如果不写的话，就是追加模式
                        format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                        # 日志格式
                        )

    # open the json file
    jsonpath = jsonpath

    with open(jsonpath, 'r', encoding='utf-8') as f:
        content = json.loads(f.read())

    if(not content):
        logging.error("文件路径错误，请检查")
        return 0

    for item in content:
        # 此时的 Item 是每张单页（近似一个话题）
        length = len(item)
        for i in range(length):
            try:
                if(item[i]['templateCode'] == 'LanguagePresentationNew'):
                    text = presentationNew.getSiglePage(item[i]['content'])
                    ankiFormat.writeToTxt(text)
                    break
                elif item[i]['templateCode'] == 'LngComp':
                    text = lngComp.getPage(item[i]['content'])
                    ankiFormat.writeToTxt(text)
                    break
            except KeyError:
                continue
         # 发现一个 bug， 当程序执行很快的时候，文件写的 就不对了
        time.sleep(5)

if __name__ == "__main__":
    main(r'EF-presentationNew\jsondir\Talking-about-awkward-situations\basic.json')
