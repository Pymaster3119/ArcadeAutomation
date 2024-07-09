from tkinter import *
import math
import os
import pygame

pygame.mixer.init()
tk = Tk("Arcade Automation - GIT Management, Slack calls, Timer")
tk.geometry("500x500")
frame = Frame(tk, width=500, height=500)
frame.pack()
sessionDescription = StringVar(tk)
remoteOrigin = StringVar(tk)
timeRemaining = StringVar(tk)
directory = StringVar(tk)
secondsRemaining = 10#3600

#Main Menu
def drawMainMenu():
    Label(frame, text= "Arcade Automation Tool").grid(row=0, column=0)
    Button(frame, text= "Start megasession", command= drawStartSession).grid(row=1, column=0)

def drawStartSession():
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text= "Describe your session's goals:").grid(row=0, column=0)
    Entry(frame, textvariable=sessionDescription).grid(row = 0, column= 1)
    Label(frame, text= "Enter your GitHub Repo's remote origin:").grid(row=1, column=0)
    Entry(frame, textvariable=remoteOrigin).grid(row = 1, column= 1)
    Label(frame, text= "Enter your files' parent directory").grid(row=2, column=0)
    Entry(frame, textvariable=directory).grid(row = 2, column= 1)
    Button(frame, text= "Start Session!", command=drawTimer).grid(row = 3, column= 0, columnspan = 2, sticky = W+E)

def drawTimer():
    for widget in frame.winfo_children():
        widget.destroy()
    secondsRemaining = 10#3600
    Label(frame, textvariable=timeRemaining).grid(row=0,column=0)
    updateTimer()

def updateTimer():
    global secondsRemaining
    minutes = math.floor(secondsRemaining/60)
    seconds = secondsRemaining % 60
    timeRemaining.set(f"{minutes}:{seconds} remaining! You got this!")
    secondsRemaining -= 1
    if (secondsRemaining != 0):
        tk.after(1250, updateTimer)
    else:
        endSession()

def endSession():
    #Git commit
    os.system("git init")
    searchPath(directory.get())
    os.system("git commit -m \"" + sessionDescription.get() + "\"")
    os.system("git branch -M main")
    os.system("git remote add origin " + remoteOrigin.get())
    os.system("git push -u origin main")

    
    #Upload stuff to Slack and git commit, etc
    drawStartSession()
    
def searchPath(pathname):
    if "/." in pathname:
        return
    for file in os.listdir(path=pathname):
        if os.path.isfile(file):
            if os.path.getsize(file) < 100000000:
                os.system(f"git add " + os.path.realpath(file))
            else:
                playSound('fileTooLarge.mp3')
        else:
            searchPath(os.path.realpath(file))

def playSound(sound):
    pygame.mixer.music.load(os.getcwd() + "/" + sound)
    pygame.mixer.music.play(loops=0)
drawMainMenu()
tk.mainloop()