# PySimpleGUI-Root-App

工作上经常需要与外国友人邮件沟通，奈何工作电脑没有安装有道词典一类的翻译软件，结合自己的需要，自己撸一个桌面翻译神器。

> >💖💖💖💕💕💕欢迎来到本博客💕💕💕💖💖💖
> >
> >🎁支持：如果觉得博主的文章写得还说得过去或者博客对您有帮助的话，可以关注一下博主，如果三连收藏支持就更好啦！这就是给予我最大的支持！
> >
>> 🎉🎉Welcome to my blog!🎉🎉
> 
> 📃个人CSDN博客主页：[热爱科技的刘同学](https://studentliu.blog.csdn.net)🌈🌈🌈


@[TOC](项目目录)

# 一、基本思路

基于PySimpleGUI开发桌面GUI→获取键盘输入→接入谷歌翻译API→爬虫获取翻译结果【其中涉及到正则表达式匹配翻译结果输出翻译结果口翻译完成。


# 二、PySimpleGUI是什么

创建图形用户界面（GUI)可能很困难，有许多不同的PythonGUI工具包可供选择。最常提到的前三名是 Tkinter,wxPython和PyQt .但是PySimpleGUI的较新工具包，其目的是使创建GUI更加容易。

# 三、代码分析

废话不能多，上分析！


## 1、引入包

可能有点儿多，但是下面的每一个包都必须用`pip`安装：

```python
from optparse import Values
import re
import html
from tkinter import font
from urllib import parse
import requests
import PySimpleGUI as sg
```

## 2、谷歌翻译网址

该处使用的ur网络请求的数据，这里用到了字符串格式化方法需要用到三个参数：

text—需要翻译的内容、to_language—日标语音类型、text_Language—当前话言类型。

```python
url = 'http://translate.google.cn/m?q=%s&tl=%s&sl=%s'
```

## 3、构建翻译函数

```python
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
```

## 4、GUI构建

```python
g.theme('bluepurple')
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

```
