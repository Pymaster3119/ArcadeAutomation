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
from selenium.webdriver.common.actions.action_builder import ActionBuilder
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
sessionLength = StringVar(tk)
sessionLength.set("3600")
driver.set_window_size(1000,1000)

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
    Entry(frame, textvariable=gitPassword, show="*").grid(row = 6, column= 1)
    Checkbutton(frame, text= "Upload to slack", variable=addToSlack).grid(row = 7, column= 0)
    Button(frame, text= "Start Session!", command=drawTimer).grid(row = 8, column= 0, columnspan = 2, sticky = W+E)
    Label(frame, text="Custom Session Length: ").grid(row=9, column=0)
    Entry(frame, textvariable=sessionLength).grid(row=9, column=1)

def drawTimer():
    global loggedIn, secondsRemaining
    for widget in frame.winfo_children():
        widget.destroy()
    try:
        secondsRemaining = int(sessionLength.get())
    except Exception:
        playSound("fileTooLarge.mp3")
    wait = WebDriverWait(driver, 60)
    if (addToSlack.get()):
        try:
            if (not loggedIn):
                #open arcade
                driver.get(arcadeLink)
                WebDriverWait(driver, 60).until(expected_conditions.visibility_of_any_elements_located((By.ID, "signup_email")))

                #signin using email authentication
                usernamebox = driver.find_element(By.ID, "signup_email")
                usernamebox.send_keys(username.get())
                submitbutton = driver.find_element(By.ID, "submit_btn")
                submitbutton.click()
                code = input("What is your login code? (no dash)")
                codeEntry = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/form/div/fieldset/div/div[1]/div[1]/input")
                codeEntry.send_keys(code)

                #Redirections
                redirect = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/p/a[2]")))
                redirect.click()
            
            messagebox = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[4]/div[2]/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/div/div[2]/div/div/div/div[2]/div/div[1]")))

            #Send the message
            messagebox.send_keys("/arcade " + sessionDescription.get() + "\n")
            sendbutton = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[4]/div[2]/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/div/div[2]/div/div/div/div[3]/div[3]/span/button[1]")
            sendbutton.click()
        except:
            playSound("fileTooLarge.mp3")
    else:
        if not loggedIn:
            driver.quit()
            loggedIn = True

    Label(frame, textvariable=timeRemaining).grid(row=0,column=0)
    Button(frame, text="Emergency commit", command=commitfn).grid(row=1, column=0)
    Label(frame, text="Commit Message: ").grid(row=2, column=0)
    Entry(frame, textvariable=sessionDescription).grid(row=2, column=1)
    updateTimer()

def updateTimer():
    global secondsRemaining
    minutes = math.floor(secondsRemaining/60)
    seconds = secondsRemaining % 60
    timeRemaining.set(f"{minutes}:{seconds} remaining! You got this!")
    secondsRemaining -= 1
    if (secondsRemaining != 0):
        tk.after(1000, updateTimer)
    else:
        endSession()

def commitfn():
    #Git commit
    os.system("cd \"" + directory.get() + "\"")
    currdir = os.getcwd()
    os.chdir(directory.get())
    print("init")
    os.system("git init")
    os.system("git add --all")
    #searchPath(directory.get())
    print("commit")
    os.system("git commit -m \"" + sessionDescription.get() + "\"")
    print("branch")
    os.system("git branch -M main")
    print("origin")
    os.system("git remote add origin " + remoteOrigin.get())
    print("push")
    os.system("git push -u origin main")
    os.chdir(currdir)

def endSession():
    global loggedIn
    playSound("restartSession.mp3")
    commitfn()

    if (addToSlack.get()):
        try:
            #Find link to commit
            actions = ActionChains(driver)
            if not loggedIn:
                
                driver.execute_script("window.open('');") 
                driver.switch_to.window(driver.window_handles[1]) 
                driver.get("https://www.github.com/login")
                WebDriverWait(driver, 60).until(expected_conditions.visibility_of_any_elements_located((By.XPATH, '//*[@id="login_field"]')))
                username = driver.find_element(By.XPATH, '//*[@id="login_field"]')
                username.send_keys(gitUsername.get())
                password = driver.find_element(By.XPATH, '//*[@id="password"]')
                password.send_keys(gitPassword.get())
                signinbutton = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div[4]/form/div/input[13]')
                signinbutton.click()
                try:
                    playSound("notification.mp3")
                    verify = input("Enter your verification code from GitHub: ")
                    verification = driver.find_element(By.XPATH, '//*[@id="otp"]')
                    verification.send_keys(verify)
                    driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/main/div/div[3]/div[2]/div[2]/form/button").click()
                except:
                    print("No verification detected")
                
                loggedIn = True
            
            driver.switch_to.window(driver.window_handles[1])
            print("https://github.com/" + remoteOrigin.get().removeprefix("https://github.com/").removesuffix(".git") + "/commits/main")
            driver.get("https://github.com/" + remoteOrigin.get().removeprefix("https://github.com/").removesuffix(".git") + "/commits/main")
            WebDriverWait(driver, 60).until(expected_conditions.visibility_of_any_elements_located((By.XPATH, "/html/body/div[1]/div[5]/div/main/turbo-frame/div/react-app/div/div/div/div/div/div[2]/div/div[2]/div[2]/div/ul/li[1]/div[1]/h4/span/a")))
            commit = driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div/main/turbo-frame/div/react-app/div/div/div/div/div/div[2]/div/div[2]/div[2]/div/ul/li[1]/div[1]/h4/span/a")
            commit.click()
            time.sleep(1)
            gitLink = driver.current_url
            driver.switch_to.window(driver.window_handles[0]) 
            #Upload stuff to Slack
            actionbuilder = ActionBuilder(driver)
            actionbuilder.pointer_action.move_to_location(78, 101)
            actionbuilder.pointer_action.click()
            actionbuilder.perform()

            wait = WebDriverWait(driver, 60)
            reply = wait.until(expected_conditions.visibility_of_any_elements_located((By.CSS_SELECTOR, "[data-qa=\"message_input\"]")))
            reply = wait.until(expected_conditions.visibility_of_any_elements_located((By.CSS_SELECTOR, "[data-qa=\"message_input\"]")))
            reply = wait.until(expected_conditions.visibility_of_any_elements_located((By.CSS_SELECTOR, "[data-qa=\"message_input\"]")))
            reply = wait.until(expected_conditions.visibility_of_any_elements_located((By.CSS_SELECTOR, "[data-qa=\"message_input\"]")))
            reply = wait.until(expected_conditions.visibility_of_any_elements_located((By.CSS_SELECTOR, "[data-qa=\"message_input\"]")))
            reply = driver.find_element(By.CSS_SELECTOR, "[data-qa=\"message_input\"]")
            actions.click(on_element=reply)
            actions.send_keys(gitLink + "\n").perform()
            sendbutton = driver.find_element(By.CSS_SELECTOR,"[data-qa='texty_send_button']")
            sendbutton.click()

            #Reset to the arcade
            time.sleep(3)
            driver.get(driver.current_url + "/C06SBHMQU8G")
        except:
            playSound("fileTooLarge.mp3")

    drawStartSession()
    

def playSound(sound):
    pygame.mixer.music.load(os.getcwd() + "/" + sound)
    pygame.mixer.music.play(loops=0)
drawMainMenu()
tk.mainloop()