from tkinter import *
from tkinter import messagebox
import math
import os
import pygame
import time
from selenium import webdriver

#Add geckodriver to PATH
os.system("export PATH=$PATH:" + os.path.realpath("geckodriver").removesuffix("/geckodriver"))
pygame.mixer.init()
tk = Tk("Arcade Automation - GIT Management, Slack calls, Timer")
tk.geometry("500x500")
frame = Frame(tk, width=500, height=500)
frame.pack()
sessionDescription = StringVar(tk)
remoteOrigin = StringVar(tk)
timeRemaining = StringVar(tk)
directory = StringVar(tk)
arcadeLink ="https://hackclub.slack.com/archives/C06SBHMQU8G"
username = StringVar(tk)
password = StringVar(tk)
secondsRemaining = 10#3600
driver = webdriver.Firefox()




#Main Menu
def drawMainMenu():
    Label(frame, text= "Arcade Automation Tool").grid(row=0, column=0)
    Button(frame, text= "Start megasession", command= drawStartSession).grid(row=1, column=0)

def drawStartSession():
    playSound("restartSession.mp3")
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text= "Describe your session's goals:").grid(row=0, column=0)
    Entry(frame, textvariable=sessionDescription).grid(row = 0, column= 1)
    Label(frame, text= "Enter your GitHub Repo's remote origin:").grid(row=1, column=0)
    Entry(frame, textvariable=remoteOrigin).grid(row = 1, column= 1)
    Label(frame, text= "Enter your files' parent directory: ").grid(row=2, column=0)
    Entry(frame, textvariable=directory).grid(row = 2, column= 1)
    Label(frame, text= "Enter your slack Username: ").grid(row=4, column=0)
    Entry(frame, textvariable=username).grid(row = 4, column= 1)
    Label(frame, text= "Enter your slack Password: ").grid(row=5, column=0)
    Entry(frame, textvariable=password).grid(row = 5, column= 1)
    Button(frame, text= "Start Session!", command=drawTimer).grid(row = 6, column= 0, columnspan = 2, sticky = W+E)

def drawTimer():
    for widget in frame.winfo_children():
        widget.destroy()
    secondsRemaining = 10#3600
    #send /arcade to slack
    driver.get(arcadeLink)
    time.sleep(0.1)
    usernamebox = driver.find_element_by_id("signup_email")
    usernamebox.send_keys(username.get())
    messagebox.showinfo("Check your e-mail for sign in credentials on and check your terminal for an input statement that asks for the code")
    code = input("What is your login code? (no dash)")
    driver.maximize_window()
    driver.get_screenshot_as_file("test.png")


    

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

    #Upload stuff to Slack

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
                messagebox.showerror("File " + os.path.realpath(file) + " is larger than GitHub's 100MB file limit. Please shrink file or upload manually.")
        else:
            searchPath(os.path.realpath(file))

def playSound(sound):
    pygame.mixer.music.load(os.getcwd() + "/" + sound)
    pygame.mixer.music.play(loops=0)
drawMainMenu()
tk.mainloop()