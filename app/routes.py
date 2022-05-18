from re import I
from app import app
from flask import render_template, request
from flask_mail import Mail, Message
from app.entities import *
import json
import re

mail = Mail(app)
contentFile = json.load(open('app\\static\\content.json', encoding='utf-8'))

languages = list(map(lambda x: x,contentFile.keys()))

mail_re = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
phone_re = "(?:\+\d{2})?\d{3,4}\D?\d{3}\D?\d{3}"
def check(reg,form):   
    if(re.search(reg,form)):   
        return True  
    else:   
        return False

nav = dict(map(lambda i:(
    i[0],
    list(map(
        lambda x: Link(
            x[0],
            x[1]
        ),
    i[1]["nav"].items())) 
    ),
    contentFile.items()))

packetCards = dict(
                map(
                    lambda i:(
                        i[0],
                        list(
                            map(            
                                lambda x:Card(
                                    title = x["title"],
                                    smallContent = x["smallContent"],
                                    content = x["content"],
                                    imgUrl = x["imgUrl"],
                                    buttonAction = x["buttonAction"],
                                    requestButtonText = x["requestButtonText"],
                                    buttonText = x["buttonText"]
                                ),
                                i[1]["packetCards"].values()
                            )
                        )
                    ),
                    contentFile.items()
                )
            )

serviceCards = dict(
                map(
                    lambda i:(
                        i[0],
                        list(
                            map(            
                                lambda x:Card(
                                    title = x["title"],
                                    smallContent = x["smallContent"],
                                    content = x["content"],
                                    imgUrl = x["imgUrl"],
                                    buttonAction = x["buttonAction"],
                                    requestButtonText = x["requestButtonText"],
                                    buttonText = x["buttonText"]
                                ),
                                i[1]["serviceCards"].values()
                            )
                        )
                    ),
                    contentFile.items()
                )
            )

pageMain = dict(map(lambda i:(i[0],i[1]["pageMain"]),contentFile.items()))
pageAbout = dict(map(lambda i:(i[0],i[1]["pageAbout"]),contentFile.items()))
pageServices = dict(map(lambda i:(i[0],i[1]["pageServices"]),contentFile.items()))
pagePackets = dict(map(lambda i:(i[0],i[1]["pagePackets"]),contentFile.items()))
pageForm = dict(map(lambda i:(i[0],i[1]["pageForm"]),contentFile.items()))


footer = dict(map(lambda i:(i[0],i[1]["footer"]),contentFile.items()))

@app.route('/')
@app.route('/<lang>/')
@app.route('/<lang>/index')
def index(lang = 'en'):
    return render_template(
        'index.html',
        nav=nav[lang],
        languages=languages,
        currentLang = lang,
        
        content=pageMain[lang],
        packetCards=packetCards[lang][:3],
        serviceCards=serviceCards[lang][:3],
        footer=footer[lang]
    )

@app.route('/<lang>/services')
def services(lang = 'en'):
    return render_template(
        'services.html',
        nav=nav[lang],
        languages=languages,
        currentLang = lang,
        content=pageServices[lang],
        cards=serviceCards[lang],
        footer=footer[lang]
    )

@app.route('/<lang>/packets')
def packets(lang = 'en'):
    return render_template(
        'packets.html',
        nav=nav[lang],
        languages=languages,
        currentLang = lang,
        content=pagePackets[lang],
        cards=packetCards[lang],
        footer=footer[lang]
    )

@app.route('/<lang>/about')
def about(lang = 'en'):
    return render_template(
        'about.html',
        nav=nav[lang],
        languages=languages,
        currentLang = lang,
        content=pageAbout[lang],
        footer=footer[lang]
    )

@app.route('/<lang>/form', methods=['POST', 'GET'])
def form(lang = 'en'):
    preSelect = request.args.get("item", default='', type=str)
    fieldsList = list(pageForm[lang]["formMustFields"].items())

    productList = list(map(lambda x: x.title, packetCards[lang])) 
    productList += [pagePackets[lang]["extraPacketTitle"]]
    productList += list(map(lambda x: x.title, serviceCards[lang]))

    formOk = dict(zip(list(pageForm[lang]["formMustFields"].keys()),[True] * len(pageForm[lang]["formMustFields"])))
    if request.method == 'POST':
        form = []
        for i in pageForm[lang]["formMustFields"].keys():
            if request.form.get(i) != "":
                formOk[i] = False
            form.append(request.form.get(i)) 
        form[0] = request.form.get("items")

        if not check(mail_re,form[1]):
            formOk["email"] = True
            form[1] = ''
        
        if not check(phone_re,form[3]):
            formOk["phone"] = True
            form[3] = ''
        print(formOk)
        if '' not in form:    

            print(form)
            msg = Message("Новый заказ", recipients=[app.config['MAIL_USERNAME']])
            msg.body = "пакет: "+form[0]+"\nпочта: " +form[1]+"\nимя: "+form[2]+"\nтелефон: "+form[3]
            mail.send(msg)
    return render_template(
        'form.html',
        nav=nav[lang],
        languages=languages,
        currentLang = lang,
        content=pageForm[lang],
        fieldsList = fieldsList,
        productList = productList,
        preSelect = preSelect,
        formOk = formOk,
        footer=footer[lang]
    )