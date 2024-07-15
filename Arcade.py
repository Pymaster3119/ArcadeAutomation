from tkinter import *
from tkinter import messagebox
import math
import os
import pygame
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service;
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument('--headless')

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
gitUsername = StringVar(tk)
gitPassword = StringVar(tk)
secondsRemaining = 3600
service = Service(executable_path=os.path.realpath("geckodriver"))
driver = webdriver.Firefox(service=service)#, options=options)
loggedIn = False
addToSlack = BooleanVar(tk)


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
    Label(frame, text= "Enter your files' Parent Directory: ").grid(row=2, column=0)
    Entry(frame, textvariable=directory).grid(row = 2, column= 1)
    Label(frame, text= "Enter your slack Username: ").grid(row=4, column=0)
    Entry(frame, textvariable=username).grid(row = 4, column= 1)
    Label(frame, text= "Enter your gitHub username: ").grid(row=5, column=0)
    Entry(frame, textvariable=gitUsername).grid(row = 5, column= 1)
    Label(frame, text= "Enter your gitHub password: ").grid(row=6, column=0)
    Entry(frame, textvariable=gitPassword).grid(row = 6, column= 1)
    Checkbutton(frame, text= "Upload to slack", variable=addToSlack).grid(row = 7, column= 0)
    Button(frame, text= "Start Session!", command=drawTimer).grid(row = 8, column= 0, columnspan = 2, sticky = W+E)

def drawTimer():
    global loggedIn, secondsRemaining
    for widget in frame.winfo_children():
        widget.destroy()
    secondsRemaining = 10
    if (addToSlack.get()):
        if (not loggedIn):
            #open arcade
            driver.get(arcadeLink)
            time.sleep(0.1)

            #signin using email authentication
            usernamebox = driver.find_element(By.ID, "signup_email")
            usernamebox.send_keys(username.get())
            submitbutton = driver.find_element(By.ID, "submit_btn")
            submitbutton.click()
            code = input("What is your login code? (no dash)")
            codeEntry = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/form/div/fieldset/div/div[1]/div[1]/input")
            codeEntry.send_keys(code)

            #Redirections
            wait = WebDriverWait(driver, 60)
            redirect = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/p/a[2]")))
            redirect.click()
        else:
            arcadebutton = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[4]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div[5]/div/span[1]/span")
            ActionChains().click(arcadebutton)
        
        messagebox = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[4]/div[2]/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/div/div[2]/div/div/div/div[2]/div/div[1]")))

        #Send the message
        messagebox.send_keys("/arcade " + sessionDescription.get() + "\n")
        sendbutton = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[4]/div[2]/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/div/div[2]/div/div/div/div[3]/div[3]/span/button[1]")
        sendbutton.click()

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
    os.system("cd " + directory.get())
    os.system("git init")
    os.system("git add --all")
    #searchPath(directory.get())
    os.system("git commit -m \"" + sessionDescription.get() + "\"")
    os.system("git branch -M main")
    os.system("git remote add origin " + remoteOrigin.get())
    os.system("git push -u origin main")

    if (addToSlack.get()):
        #Find link to commit
        if not loggedIn:
            actions = ActionChains(driver)
            driver.execute_script("window.open('');") 
            driver.switch_to.window(driver.window_handles[1]) 
            driver.get("https://www.github.com/login")
            time.sleep(0.2)
            username = driver.find_element(By.XPATH, '//*[@id="login_field"]')
            username.send_keys(gitUsername.get())
            password = driver.find_element(By.XPATH, '//*[@id="password"]')
            password.send_keys(gitPassword.get())
            signinbutton = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div[4]/form/div/input[13]')
            signinbutton.click()
            verify = input("Enter your verification code from GitHub: ")
            input = driver.find_element(By.XPATH, '//*[@id="otp"]')
            input.send_keys(verify)
            driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/main/div/div[3]/div[2]/div[2]/form/button").click()
            time.sleep(1.5)
            repo = driver.find_element(By.LINK_TEXT, remoteOrigin.get().removeprefix("https://github.com/").removesuffix(".git"))
            repo.click()
            loggedIn = True
        driver.switch_to.window(driver.window_handles[1]) 
        time.sleep(2)
        commitButton = driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div/main/turbo-frame/div/div/div/div[2]/div[1]/react-partial/div/div/div[3]/div[1]/table/tbody/tr[1]/td/div/div[2]/div[2]/a")
        commitButton.click()
        time.sleep(0.5)
        commit = driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div/main/turbo-frame/div/react-app/div/div/div/div/div/div[2]/div/div[2]/div[2]/div/ul/li[1]/div[1]/h4/span/a")
        commit.click()
        time.sleep(0.5)
        gitLink = driver.current_url
        driver.switch_to.window(driver.window_handles[0]) 

        #Upload stuff to Slack
        threads = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[4]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div[1]/div")
        threads.click()
        wait = WebDriverWait(driver, 10)
       
        reply = wait.until(expected_conditions.visibility_of_any_elements_located((By.CSS_SELECTOR, "[data-qa=\"message_input\"]")))
        reply = driver.find_element(By.CSS_SELECTOR, "[data-qa=\"message_input\"]")
        actions.click(on_element=reply)
        actions.send_keys(gitLink + "\n").perform()
        sendbutton = driver.find_element(By.CSS_SELECTOR,"[data-qa='texty_send_button']")
        sendbutton.click()
    drawStartSession()
    
def searchPath(pathname):
    if "/." in pathname:
        return
    try:
        for file in os.listdir(path=pathname):
            if os.path.isfile(file):
                if os.path.getsize(file) < 100000000:
                    os.system(f"git add " + os.path.realpath(file))
                else:
                    playSound('fileTooLarge.mp3')
                    messagebox.showerror("File " + os.path.realpath(file) + " is larger than GitHub's 100MB file limit. Please shrink file or upload manually.")
            else:
                searchPath(os.path.realpath(file))
    except:
        os.system(f"git add " + os.path.realpath(file))

def playSound(sound):
    pygame.mixer.music.load(os.getcwd() + "/" + sound)
    pygame.mixer.music.play(loops=0)
drawMainMenu()
tk.mainloop()