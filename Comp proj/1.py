import tkinter as tk
import cv2
from PIL import Image, ImageTk
import threading
from functools import partial
import imutils
import time

# width and height of main screen
Set_Width = 650
Set_Height = 380

stream = cv2.VideoCapture('clip.mp4')
flag = True


def Play(speed):
    global flag
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1+speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()

    frame = imutils.resize(frame, width=Set_Width, height=Set_Height)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tk.NW)

    # we want to blink a decision pending on screen
    if flag:
        canvas.create_text(150, 30, font='times 30 italic bold',
                           fill='black', text='Decision Pending')
    flag = not flag



def pending(decision):

    # 1. display decision pending and wait for 2 sec
    frame = cv2.cvtColor(cv2.imread('pending.png'), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=Set_Width, height=Set_Height)
    frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tk.NW)

    time.sleep(2)

    # 2. display sponser wait for 1 sec

    frame = cv2.cvtColor(cv2.imread('sponser.png'), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=Set_Width, height=Set_Height)
    frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tk.NW)

    time.sleep(1)
    # 3. display result wait 3 sec
    if decision == 'out':
        decision_img = 'out.png'
    else:
        decision_img = 'not_out.png'

    frame = cv2.cvtColor(cv2.imread(decision_img), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=Set_Width, height=Set_Height)
    frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tk.NW)


def not_out():
    thred = threading.Thread(target=pending, args=('not out',))
    thred.daemon = 1
    thred.start()


def out():
    thred = threading.Thread(target=pending, args=('out',))
    thred.daemon = 1
    thred.start()


window = tk.Tk()

cv_img = cv2.cvtColor(cv2.imread('Welcome.png'), cv2.COLOR_BGR2RGB)
cv_img = imutils.resize(cv_img, width=Set_Width, height=Set_Height)
window.title('Ravinder Third Umpire Review Tool Kit')
canvas = tk.Canvas(window, width=Set_Width, height=Set_Height)
photo = ImageTk.PhotoImage(Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, anchor=tk.NW, image=photo)
canvas.pack()


# Buttons to control playback
btn = tk.Button(window, text=" <<  Previous (Fast) ",
                width=50, command=partial(Play, -10))
btn.pack()

btn = tk.Button(window, text=" <<  Previous (slow) ",
                width=50, command=partial(Play, -2))
btn.pack()

btn = tk.Button(window, text=" Next (slow) >>",
                width=50, command=partial(Play, 1))
btn.pack()

btn = tk.Button(window, text=" Next (Fast) >>",
                width=50, command=partial(Play, 10))
btn.pack()

btn = tk.Button(window, text="Give Out", width=50, command=out)
btn.pack()

btn = tk.Button(window, text="Give Not Out", width=50, command=not_out)
btn.pack()


window.mainloop()
