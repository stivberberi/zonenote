import tkinter
import time
from queue import Queue
from threading import Thread


##Progressbar.start(interval=600)
##Progressbar.step(amount=2)

stop = True

window = tkinter.Tk()

window.title("ZoneNote")
window.wm_iconbitmap('Icon.ico')

window.geometry("180x75")

var = tkinter.IntVar()
cmd_queue = Queue()

def enter_text():
    btn.destroy()
    text = ent.get()
    content = tkinter.StringVar()
    entry = tkinter.Entry(textvariable=content)
    text = content.get()
    content.set(text)
    ent.destroy()
    lbl.destroy()
    window.geometry("180x30")
    btn2.pack()
    f = open("subject_name.txt", "w")
    f.write(text)
    f.close()
    global cmd_queue
    cmd_queue.put("TEXT")

def start_recording():
    lbl2 = tkinter.Label(window,text = "Recording started")
    lbl2.pack()
    window.geometry("180x30")
    btn2.destroy()
    btn3.pack()
    global cmd_queue
    cmd_queue.put("START")

def stop_recording():
    lbl3 = tkinter.Label(window,text = "Recording stopped")
    lbl3.pack()
    window.geometry("180x30")
    btn3.destroy()
    global cmd_queue
    cmd_queue.put("STOP")
    
lbl = tkinter.Label(window, width = 20,text="Enter lecture name: ")

ent = tkinter.Entry(window)

btn = tkinter.Button(window, text="Enter Text",command=enter_text)

btn2 = tkinter.Button(window,text="Start recording",command=start_recording)

btn3 = tkinter.Button(window,text="Stop recording",command=stop_recording)

lbl.pack()
ent.pack()
btn.pack()

class WindowThread(Thread):
    def run(self):
        global window
        window.mainloop()

WindowThread().start()

from threaded import Recorder
recorder = Recorder(cmd_queue)
recorder.start()
