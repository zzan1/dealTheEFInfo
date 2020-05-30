import lxml.etree as let
import re
import getAudio
import ankiFormat
import logging


def getStrFormat(str):
    text = str.strip().replace('\n', '').replace('\t', '').strip()
    return text

# 正则匹配lxml的元素对象


def textExtraction(regrex, HTMLElement):
    content = let.tostring(HTMLElement, encoding='utf-8').decode("utf-8")
    matches = re.findall(regrex, content)
    return matches

# 用选出来的元素对象新建一个lxml的元素树对象


def buildNewElementTree(HTMLElement):
    content = let.tostring(HTMLElement, encoding='utf-8').decode("utf-8")
    newTree = let.HTML(content)
    return newTree


def getTitle(htmlObj):
    # 所有 td 属性 colspan=3 的都是标题
    # 大标题，以 <strong> 标签包裹
    # 目的： 提取所有的大标题和小标题，大标题当作标签，大标题+小标题作为笔记
    # 输入，单页DOM数队形
    # 返回（tag, note）本页上面的大标题，小标题，如果没有，则返回空

    # 这里存在一个 bug 有的时候 这个 Colspan="4" 不知道该怎么解决
    titleList = htmlObj.xpath('//td[@colspan="4"]')
    bigTitleList = htmlObj.xpath('//td[@colspan="4"]/strong')
    tags = ''
    notes = ''

    for bigTitle in bigTitleList:
        tag = getStrFormat(bigTitle.text)
        if tag:
            tags = tags+tag
            tags = '<strong>' + tags + '</strong>'
            # logging.debug('Get the single tags: ' + tags)

    for title in titleList:
        # 因为大标题下面有strong标签，所以直接获取内容的结果是空字符串，这部分可以认为只获取副标题
        note = getStrFormat(title.text)
        if note:
            notes = notes+note
            # logging.debug('Get the single notes: ' + notes)

    return tags, notes


def getContent(tdList, tags, notes):

    def getEnglish(td):
        tdText = let.tostring(td, encoding='utf-8').decode('utf-8')
        tdText = getStrFormat(tdText)
        # 替换掉所有的</em><em><td></td>
        tdText = re.sub(r'<[^s].{1,2}>', '', tdText)
        tdText = re.sub(r'<td style="width: \d*%;">', '', tdText)
        return tdText

    def getEnglishFocus(line):
        tdObj = let.HTML(line)
        focusList = tdObj.xpath('//strong')
        # logging.debug(len(focusList))
        if len(focusList) != 0:
            logging.debug(let.tostring(
                focusList[0], encoding='utf-8').decode("utf-8"))
            logging.debug("this focus is:" + focusList[0].text)
            return getStrFormat(focusList[0].text)
        else:
            return ''

    content = []
    logging.debug('the totla td numbers is: ' + str(len(tdList)))
    for i in range(len(tdList)):
        # 以一个 url 开始处理，
        lineContent = [j for j in range(7)]
        logging.debug('the i number is: ' + str(i))
        if getStrFormat(tdList[i].text)[:5] == 'https':
            logging.debug('There is a new infor source raw: ' + str(i))
            # the first is url
            lineContent[0] = getStrFormat(tdList[i].text)
            lineContent[0] = getAudio.getAudio(lineContent[0])

            # the second is english
            lineContent[4] = getEnglish(tdList[i+1])
            logging.debug('current english is: ' + lineContent[4])

            # the third is chinese
            lineContent[3] = getStrFormat(tdList[i+2].text)
            if not lineContent[3]:
                lineContent[3] =getStrFormat(tdList[i+3].text)

            # the foucus phase
            if getEnglishFocus(lineContent[4]):
                lineContent[2] = getEnglishFocus(lineContent[4])
            else:
                lineContent[2] = ''

            # the cloze sentence
            focus = lineContent[2]
            if focus:
                cloze = '{{c1::'+focus+'}}'
                lineContent[1] = lineContent[4].replace(focus, cloze, 1)
            else:
                lineContent[1] = lineContent[4]

            # the tags
            lineContent[6] = tags

            # the notes
            lineContent[5] = tags+notes

            # focus on the special page
            try:
                if getStrFormat(tdList[i+3].text)[0:2] == 'B:':
                    # 把英语拼接起来
                    lineContent[4] = lineContent[4] + \
                        '<br>'+getEnglish(tdList[i+3])
                    lineContent[1] = lineContent[1] + \
                        '<br> '+getEnglish(tdList[i+3])
                    lineContent[3] = lineContent[3] + \
                        '<br> '+getStrFormat(tdList[i+4].text)
            except IndexError:
                logging.debug('The i was in the end and I number is ' +
                              str(i)+' total I number is ' + str(len(tdList)))

            content.append(lineContent)
            logging.debug('now the single page raws are: ' + str(len(content)))
        else:
            continue

    return content


def getSiglePage(item):
    # 单个单元
    htmlArray = item["presentations"]

    # ============= 处理得到 notes 和  tag 两个部分 ==============
    # 每个单元的大标题和小标题的初始化
    tags = ''
    notes = ''
    content = []
    # 前后多页的那种
    # 把多页的小标题和大标题都拼在一起
    for item in htmlArray:
        htmlContent = item['text']
        htmlObj = let.HTML(htmlContent)
        # ============= 处理得到 notes 和  tag 两个部分 ==============
        tag, note = getTitle(htmlObj)
        tags = tags+tag
        notes = notes+note

    logging.info('the final tags is: ' + tags)
    logging.info('the final notes is: ' + notes)
    # ============= 处理得到 mp3 和  eng and zn 三个部分 ==============
    # 必须先把多页的所有的笔记都收集起来，再去做一行一行的统计
    for item in htmlArray:
        htmlContent = item['text']
        htmlObj = let.HTML(htmlContent)
        tdList = htmlObj.xpath('//td')
        content = content+getContent(tdList, tags, notes)
    return content


# xpath 只能从 最开始的 ElementTreeObj 中搜索，不是依赖.前面的, 搜索表达式也是从最开始的html开始的
    # with open('jsondir\\test.html','r',encoding='utf-8') as f:
    #     html=f.read()


if __name__ == "__main__":
    pass
