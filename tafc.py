import sys
from threading import Thread
import tkinter
from tkinter import *
from tkinter import ttk 
from tkinter.ttk import Combobox
import tkinter.colorchooser 
import json

class tkin(Thread):
        def cvetobv(self):
            (rgb, hx) = tkinter.colorchooser.askcolor()
            cvetobv=hx
            parameters = json.loads(open('config.json','r').read())
            parameters["line"] = str(hx)
            f = open('config.json','w')
            f.write(json.dumps(parameters))
            f.close()

        def increase_w(self):  
            parameters = json.loads(open('config.json','r').read())
            width = int(parameters["tall"])
            parameters["tall"] = str(width+1)
            f = open('config.json','w')
            f.write(json.dumps(parameters))
            f.close()
        def decrease_w(self):
            parameters = json.loads(open('config.json','r').read())
            width = int(parameters["tall"])
            parameters["tall"] = str(width-1)
            f = open('config.json','w')
            f.write(json.dumps(parameters))
            f.close()
        def decrease_t(self):
            parameters = json.loads(open('config.json','r').read())
            width = int(parameters["width"])
            parameters["width"] = str(width-1)
            f = open('config.json','w')
            f.write(json.dumps(parameters))
            f.close()
        def increase_t(self):
            parameters = json.loads(open('config.json','r').read())
            width = int(parameters["width"])
            parameters["width"] = str(width+1)
            f = open('config.json','w')
            f.write(json.dumps(parameters))
            f.close()
            
        def run(self):
            window = Tk()  
            window.title("Панель управления")  
            window.geometry('400x150')
            iw = Button(window, text="     +    ", command=self.increase_w)  
            iw.grid(column=0, row=0)
            lbl = Label(window, text=" Толщина ")  
            lbl.grid(column=1, row=0)
            dw = Button(window, text="     -      ", command=self.decrease_w)  
            dw.grid(column=2, row=0)
            l = Label(window, text="--------------------")  
            l.grid(column=1, row=1)
            it = Button(window, text="     +   ", command=self.increase_t)  
            it.grid(column=0, row=2)
            lb = Label(window, text=" Радиус ")
            lb.grid(column=1, row=2)
            dt = Button(window, text="      -      ", command=self.decrease_t)  
            dt.grid(column=2, row=2)
            ll = Label(window, text = "--------------------")
            ll.grid(column=1,row=3)
            choc = Button(window, text=" Выберите цвет ", command=self.cvetobv)
            choc.grid(column=1, row=4)
            window.mainloop()

import cv2

valid_cams=[]
for i in range(8):
    cap = cv2.VideoCapture(i)
    if cap is None or not cap.isOpened():
        print('Warning: unable to open video source: ', i)
    else:
        valid_cams.append(i)

def getSel():
  selection = listing.curselection()
  chosen_cam = [listing.get(i) for i in selection]
  print(chosen_cam[0])
  chosen_cam = chosen_cam[0]
  chosen = int(chosen_cam.replace('Cam ',''))
  f = open('camnum.txt','w')
  f.write(str(chosen))
  f.close()
  window.destroy()

window = Tk()  
#listing = window.Listbox()
window.title("Камера")  
window.geometry('400x300')
ll = Label(window, text = "  Выберите камеру:  ")
ll.grid(column=0,row=0)
listing = Listbox(window)
for item in valid_cams:
  listing.insert(item, 'Cam '+str(item))
listing.grid(column=0,row=1)
btn = Button(window, text="  Выбрал  ", command=getSel)  
btn.grid(column=0, row=3)
window.mainloop()


try:
    t1 = tkin()
    t1.start()
    pass
except Exception as e:
    print(e)
    pass

try:
    parameters = json.loads(open('config.json','r').read())
    width = int(parameters["width"])
    parameters["width"] = str(width+1)
    f = open('config.json','w')
    f.write(json.dumps(parameters))
    f.close()
    pass
except:
    f = open('config.json','w')
    f.write('{"line": "white", "width": "123", "tall": "4"}')
    f.close()
    pass
    

from PIL import Image, ImageDraw
import numpy as np

def get_x(height):
  height = int(height)
  y = height/2
  return (height)

def get_y(width):
  width = int(width)
  x = width/2
  return (width)

#try:
#    a = 0
#    capture = cv2.VideoCapture(a)
#    pass
#except:
#    capture = cv2.VideoCapture(1)
#    pass


go = int(open('camnum.txt','r').read())
capture = cv2.VideoCapture(go)

while True:
    try:
        ret, img = capture.read()
        config = json.loads(open('config.json','r').read())
        elp = int(config["width"])
        tall = int(config["tall"])
        colours = str(config["line"])
        eX = elp
        eY = elp
        height, width, channels = img.shape
        sample = Image.new("RGBA", (width,height), (0,0,0,0))
        #sample = Image.open('all.png')
        mass = (str(sample.size).replace(')','').replace('(','').replace(' ','').split(','))
        x = get_x(mass[0])
        y = get_y(mass[1])

        draw = ImageDraw.Draw(sample)
        #рисуем горизонтальную линию
        draw.line((x,y/2,0,y/2), fill=(colours),width=tall)
        #рисуем вертикальную линию
        draw.line((x/2,0,x/2,y), fill=(colours),width=tall)
        #делаем круг по середине радиусом
        bbox =  (x/2 - eX/2, y/2 - eY/2, x/2 + eX/2, y/2 + eY/2)
        #draw.ellipse ((0,0,elp,elp), fill=('yellow'))
        draw.ellipse(bbox, width=tall, outline =colours)
        # Читать изображение1
        sample.save("ME.png", "PNG")
        mountain = cv2.imread('ME.png', 1)


          
        # Читать изображение2

        #dog = cv2.imread('F:\dog.jpg', 1)

          
        # Добавить изображения

        image = cv2.add(img, mountain)

          
        # Показать изображение

        cv2.imshow('AIMFinder Cam', image)

          
        key = cv2.waitKey(30)
        if key == 27:
            break
    except KeyboardInterrupt:
        capture.release()
        capture.distroyAllWindows()
        sys.exit()

capture.release()
# Разбить все окна открытыми
cv2.distroyAllWindows()
