import tkinter as tk
from tkinter import ttk
from urllib.request import urlopen
from newsapi import NewsApiClient
from PIL import Image, ImageTk
import webbrowser
import io
import urllib

prev_step = 'next'


def back(_event=None):
    global cur, prev_step
    if cur != 0:
        cur -= 1
        prev_step = 'back'
        update()


def next(_event=None):
    global cur, prev_step
    cur += 1
    prev_step = 'next'
    update()


def update():
    global title, img, description, original_site, cur
    title.config(text='Updating..........')
    image = ImageTk.PhotoImage(Image.open(r'res\loading_img.png'))
    img.configure(image=image)
    img.image = image
    description.config(text='')
    root.update()
    while True:
        try:
            #req = urllib.request.Request(articles[cur]['urlToImage'], headers=hdr)
            raw_data = urlopen(articles[cur]['urlToImage'], timeout=5).read()
            im = Image.open(io.BytesIO(raw_data))
            tk.Label(root).grid(row=1, column=0, columnspan=2)
            image = ImageTk.PhotoImage(im)
            break
        except urllib.error.HTTPError:
            if prev_step == 'next':
                cur += 1
            elif prev_step == 'back':
                cur -= 1
        except IndexError:
            image = ImageTk.PhotoImage(Image.open(r'res\end.jpg'))
            break
        except Exception:
            if prev_step == 'next':
                cur += 1
                print(cur)
            elif prev_step == 'back':
                cur -= 1
    img.configure(image=image)
    img.image = image
    try:
        title.config(text=articles[cur]["title"])
        description.config(text=articles[cur]["description"])
    except IndexError:
        title.config(text='Out of news articles come back later')


newsapi = NewsApiClient(api_key='GET_THIS_BY_SIGNIN_UP')

top_headlines = newsapi.get_top_headlines(sources='google-news-in, the-times-of-india ,bbc-news, the-verge')
articles = top_headlines['articles']
cur = 0
root = tk.Tk()
root.title('NEWS | Top Headlines')
root.wm_iconbitmap(r'res\icon.ico')
title = ttk.Label(root, text=articles[cur]['title'], font=('Helvetica', 20, 'bold'), wraplengt=720, justify='center')
title.grid(row=0, column=0, columnspan=2)


while True:
    try:
        #req = urllib.request.Request(articles[cur]['urlToImage'], headers=hdr)
        raw_data = urlopen(articles[cur]['urlToImage']).read()
        im = Image.open(io.BytesIO(raw_data))
        tk.Label(root).grid(row=1, column=0, columnspan=2)
        image = ImageTk.PhotoImage(im)
        break
    except Exception:
        if prev_step == 'next':
            cur += 1
            print(cur)
        elif prev_step == 'back':
            cur -= 1

img = tk.Label(root, image=image, width=720, height=480)
img.grid(row=2, column=0, columnspan=2)

tk.Label(root).grid(row=3, column=0, columnspan=2)

description = ttk.Label(root, text=articles[cur]['description'], font=30, wraplengt=720, justify='center')
description.grid(row=4, column=0, columnspan=2)

original_site = ttk.Button(root, text='Read More', command=lambda: webbrowser.open(articles[cur]['url'], new=2))
original_site.grid(row=5, column=0, columnspan=2)

back_btn = ttk.Button(root, text='Back', command=back)
next_btn = ttk.Button(root, text='Next', command=next)
back_btn.grid(row=6, column=0)
next_btn.grid(row=6, column=1)
ttk.Label(root).grid(row=7, column=0, columnspan=2)
root.bind('<Right>', next)
root.bind('<Left>', back)

root.mainloop()
