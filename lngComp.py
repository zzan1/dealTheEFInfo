import getAudio


def getPage(item):
    contentList=item[0]['content']['phrases']
    text=[]
    for content in contentList:
        singleRow=[j for j in range(7)]
        # audio
        url=content['audio']['url']
        singleRow[0]=getAudio.getAudio(url)

        # Sentence
        singleRow[1]=content['text']

        # Focus
        singleRow[2]=''

        # Chinese
        singleRow[3]=content['translation']

        # completeSentence
        singleRow[4]=content['text']

        # notes and tags
        singleRow[5]=''
        singleRow[6]=''

        text.append(singleRow)

    return text
    
if __name__ == "__main__":
    pass