from optparse import Values
import re
import html
from tkinter import font
from urllib import parse
import requests
import PySimpleGUI as sg

url = 'http://translate.google.cn/m?q=%s&tl=%s&sl=%s'

def translate(text, to_language="en", text_language="auto"):
    text = parse.quote(text)
    urll = url % (text, to_language ,text_language)
    response = requests.get(urll)
    data = response.text
    expr = r'(?s)class = "(?:t0|result-container)">(.*?)<'
    result = re.findall(expr, data)
    print (result)
    if (len(result) == 0):
        return ""
    return html.unescape(result[0])

sg.theme('bluepurple')
font = {"fangsong", 12}
menu = [["Help", ["About", "Item", "Author"]]]
value = ['汉语', '英语', '日语', '法语', '俄语', '自动']

var = ['zh', 'en', 'ja', 'fr', 'ru', 'auto']
dic = dict(zip(value, var))
layout = [[sg.Menu(menu, tearoff = False)],
          [sg.Text(text='Input', size=(26, 1)),
           sg.Text(text='将', size=(2, 1), justification='center'),
           sg.Combo(values=value, key='from', size=(10, 1)),
           sg.Text(text='翻译为', size=(5, 1), justification='center'),
           sg.Combo(values=value, key='to', size=(10, 1))],
          [sg.Multiline(key='-IN-', size=(60, 0), font=font)],
          [sg.Text(text='Output', size=(30, 1))],
          [sg.Multiline(key="-OUT-", size=(60, 8), font=font)],
          [sg.Text(text='', size=(36, 1)),
           sg.Button("翻译", size=(6, 1)),
           sg.Button("清除", size=(6, 1)),
           sg.Button("退出", size=(6, 1))]
          ]

window = sg.Window("自制桌面翻译器", layout, icon="CT.ico")

while True:
    event, value = window.read()
    if event in (None, "退出"):
        break
    if event == "翻译":
        if Values["to"] == '' or Values["from"] == '':
            sg.Popup("请尝试选择语言类型后尝试，谢谢！")
        else:
            tar = translate(Values["-IN-"], dic[Values["to"]], dic[Values["from"]])
            window["-OUT-"].Update(tar)
    if event == "清除":
        window["-IN-"].Update("")
        window["-OUT-"].Update("")
    if event == "About":
        sg.Popup("使用方法：",
                 "'翻译'确认输入，并输出翻译结果"
                 "'清除'清除已有输入，清空翻译结果",
                 "'退出'取消,并退出App", title='', font=font, auto_close=1)
    if event == "Item":
        sg.Popup("翻译类型：",
                 "'输入类型'输入的语言类型",
                 "'输出类型',输出语言类型", title='', font=font, auto_close=1)
    if event == "Author":
        sg.Popup("作者简介：",
                 "姓名：刘镇鸣",
                 "微信/电话:17734258540",
                 "E-mail:2124619132@qq.com", title='', font=font, auto_close=1)
window.close()
