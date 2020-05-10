import datetime

def formatAnki(array):
    sigleRow=''
    for item in array:
        sigleRow=sigleRow+item+'`'
    sigleRow=sigleRow+'\n'
    return(sigleRow)

def writeToTxt(array):
    text=[]
    for item in array:
        text.append(formatAnki(item))
    now_time = datetime.datetime.now().strftime(' %m-%d-%H-%M-%S')
    fileName='card'+now_time+'.txt'
    with open(fileName,'w+',encoding='utf-8') as wholecard:
        wholecard.writelines(text)   
    