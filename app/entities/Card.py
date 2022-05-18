class Card(object):
    title = ''
    smallContent = ''
    content = ''
    imgUrl = ''
    buttonAction = ''
    buttonText = ''
    requestButtonText = ''
    def __init__(self, title:str, smallContent:str, content:list, imgUrl:str, buttonAction:str, requestButtonText:str, buttonText:str):
        self.title = title
        self.smallContent = smallContent
        self.content = content
        self.imgUrl = imgUrl
        self.buttonAction = buttonAction
        self.requestButtonText = requestButtonText
        self.buttonText = buttonText