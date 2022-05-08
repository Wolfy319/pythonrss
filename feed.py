import os
import time
import tkinter as tk
from turtle import color
import feedparser
import webbrowser
import tkinter.font as tkFont

import threading


sem = threading.Semaphore()


#http://feeds.bbci.co.uk/news/world/rss.xml


            
class App(threading.Thread):
    def __init__(self):
        self.width = 300
        sem.acquire()
        threading.Thread.__init__(self, name = "GUI")
        self.thread = threading.currentThread()
        self.start()
        
    def getTime(self) :
        return time.localtime().tm_hour * 100 + time.localtime().tm_min

    def link(self, event, url):
        webbrowser.open_new(url)

    def on_enter(self, event, id) :
        self.canvas.itemconfigure(id, fill = "#F000F0", font = self.font2)
        self.canvas.config(cursor="hand2")

    def on_exit(self, event, id) :
        self.canvas.itemconfig(id, fill = "#000000", font = self.font1)
        self.canvas.config(cursor="arrow")

    def press(self, event, var) :
        self.url = self.input.get()
        var.set(1)

    def updateEntries(self, canvas, url) :
        feed = feedparser.parse(url)

        titles = []
        for i, entry in enumerate(feed.entries) :
            tag = "text" + str(i)
            t = entry["title"]
            self.text = self.canvas.create_text(self.width + 10, 1, anchor = "nw",text = t, font=self.font1, tags = tag)
            self.space = self.canvas.create_text(self.width + 10, 1, anchor = "nw",text = "   |   ", font=self.font1)
            self.canvas.tag_bind(tag, "<Button-1>", func = lambda event, url = entry["link"], : self.link(event, url))
            self.canvas.tag_bind(tag, "<Enter>", func = lambda event, num = self.text: self.on_enter(event, num))
            self.canvas.tag_bind(tag, "<Leave>", func = lambda event, num = self.text: self.on_exit(event, num))
            titles.append(self.text)
            titles.append(self.space)
        return titles
        

    def checkUpdate(self, currTime, prevTime, titles): 
        if currTime - prevTime >= 2 or currTime <= 2 :
            print("updating...")
            titles = self.updateEntries(self.canvas)
            prevTime = currTime
            currTime = self.getTime
        return titles
    
    def run(self):
        self.root=tk.Tk()
        self.var = tk.IntVar()
        self.root.attributes('-topmost',True)
        self.root.title("")
        self.root.iconbitmap("Projects\Rss feed\\transparent.ico")
        self.f1 = tk.Frame(self.root)
        self.f1.grid(row=0, column=0, sticky='news')
        self.f2 = tk.Frame(self.root)
        self.f2.grid(row=0, column=0, sticky='news')
        
        self.f1.tkraise()
        self.label = tk.Label(self.f1, text= "Enter RSS feed URL",font=('Helvetica bold', 15)).pack(pady=20)
        self.input = tk.Entry(self.f1)
        self.button = tk.Button(self.f1, text = "Start", command=lambda v = self.var: self.press(tk.Event, v))

        self.input.pack()
        self.button.pack()
        self.button.wait_variable(self.var)
        self.font1 = tkFont.Font(font=("Verdana 15"))
        self.font2 = tkFont.Font(font =("Verdana 15 underline"))


        self.canvas = tk.Canvas(self.f2, height=30, width = 300)
        self.canvas.pack()

        self.f2.tkraise()
        self.root.geometry("{}x{}".format(300, 30))

        self.prevTime = self.getTime()
        self.titles = self.updateEntries(self.canvas, self.url)
        self.queue = [self.titles[0]]
        self.currTime = self.getTime()
        self.titles = self.checkUpdate(self.currTime, self.prevTime, self.titles)
        sem.release()
        self.root.mainloop()
        stop.set()

        


def moveit(app) :
    hasmoved = {}
    for i, item in enumerate(app.queue) :
        coords = app.canvas.bbox(item)
        if coords[2] < -5 :
            app.queue.append(app.queue.pop())
        if coords[2] < 300 and i < len(app.queue) - 1:
            if not i + 1 in hasmoved.keys() :
                app.canvas.move(app.queue[i + 1], -2, 0)
                hasmoved[i + 1] = True
        if not i in hasmoved.keys() :
            app.canvas.move(item, -1, 0)
            hasmoved[i] = True
    return


stop = threading.Event()

app = App()
sem.acquire()
# width = 300
# root = tk.Tk()
# root.attributes('-topmost',True)
# root.title("")
# root.iconbitmap("Projects\Rss feed\\transparent.ico")
# text_width = 40
# duration = 5
# font1 = tkFont.Font(font=("Verdana 15"))
# font2 = tkFont.Font(font =("Verdana 15 underline"))

# f1 = tk.Frame(root)
# f1.grid(row=0, column=0, sticky='news')
# f2 = tk.Frame(root)
# f2.grid(row=0, column=0, sticky='news')

# f1.tkraise()
# label = tk.Label(f1, text= "Enter RSS feed URL",font=('Helvetica bold', 15)).pack(pady=20)
# input = tk.Entry(f1)
# button = tk.Button(f1, text = "Start", command=lambda v = var: press(v))

# input.pack()
# button.pack()
# button.wait_variable(var)



# canvas = tk.Canvas(f2, height=30, width = width)
# canvas.pack()

# f2.tkraise()
# root.geometry("{}x{}".format(width, 30))

# prevTime = getTime()
# titles = updateEntries(canvas, url)
# queue = [titles[0]]
# currTime = getTime()
# if currTime - prevTime >= 2 or currTime <= 2 :
#     print("updating...")
#     titles = updateEntries(canvas)
#     prevTime = currTime
#     currTime = getTime
sem.release()
print(threading.activeCount())
appThread = app.thread
while not threading.active_count() < 2 :
    time.sleep(.02)
    if stop.is_set() :
        break
    moveit(app)
    for i in range(len(app.titles)) : 
        coords = app.canvas.bbox(app.titles[i])
        if coords[2] < app.width and i < len(app.titles) :
            if app.titles[i+1] in app.queue :
                continue
            app.queue.append(app.titles[i+1])
os._exit()
    # while coords[2] > 0 :
    #     coords = canvas.bbox(titles[i])
    #     if coords[2] < width and i < len(titles):
    #         canvas.move(titles[i + 1], -1, 0)
    #     canvas.move(titles[i], -1, 0)
    #     canvas.update()
    #     canvas.after(10)






