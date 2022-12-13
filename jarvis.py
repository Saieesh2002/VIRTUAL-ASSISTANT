import ctypes
import operator
import subprocess
import PyPDF2
import instaloader
import psutil
import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random
import os.path
from pywikihow import WikiHow
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import sys
import time
import pyjokes
import requests
import pyautogui
from googletrans import Translator
from nltk.app.wordnet_app import pg
from prompt_toolkit.clipboard import pyperclip
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders



engine = pyttsx3.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('volume', 1)



# text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# change voice
def voice_change(v):
    x = int(v)
    engine.setProperty('voice', voices[x].id)
    speak("done karthik")


# To convert voice into text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.energy_threshold = 4000
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")

    except Exception as e:
        #speak("Say that again please...")
        return "none"

    query = query.lower()
    return query


# to wish
def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if hour >= 0 and hour < 12:
        speak(f"good morning, its {tt}")
    elif hour >= 12 and hour < 18:
        speak(f"good afternoon, its {tt}")
    else:
        speak(f"good evening, its {tt}")

    speak("i am jarvis sir. please tell me how may i help you")


# screenshot function
def screenshot():
    img = pyautogui.screenshot()
    img.save("C:\\Users\\ASUS\\OneDrive\\Pictures\\Screenshots\\ss.png")


# To read PDF files
def pdf_reader():
    book = open('ENTER BOOK', 'rb')#here rb is binary mode
    pdfReader = PyPDF2.PdfFileReader(book) #pip install PyPDF2
    pages = pdfReader.numPages
    speak(f"Total numbers of pages in this book {pages}")
    speak("sir please enter the page number i have to read")
    Pg= int(input("Please enter the page number: "))
    page= pdfReader.getPage(pg)
    text = page.extractText()
    speak (text)


# date function
def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak("The current date is")
    speak(date)
    speak(month)
    speak(year)


# battery and cpu usage
def cpu():
    usage = str(psutil.cpu_percent())
    speak('CPU usage is at ' + usage)
    print('CPU usage is at ' + usage)

    battery = psutil.sensors_battery()
    percentage = battery.percent
    print("battery is at : " + str(battery.percent))
    speak(f"sir our system has {percentage} percent battery")

    if percentage>=75:
        speak("we have enough power to continue our work sir. lets go sir.")

    elif percentage>=40 and percentage<=75:
        speak("we should connect our system to charging point to charge our battery sir.")

    elif percentage>=15 and percentage<=30:
        speak("we don't have enough power to work, please connect to charging sir.")

    elif percentage<=15:
        speak("sir, we have very low power, please charge the system or the system will shutdown soon")


# notes
def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe", file_name])


# weather
def weather_info():
    api_key = "eece000de5e319b3c94c04b2d1bc9b15"  # generate your own api key from open weather
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    speak("tell me which city")
    city_name = takecommand()
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        r = ("in " + city_name + " Temperature is " +
                 str(int(current_temperature - 273.15)) + " degree celsius " +
                 ", atmospheric pressure " + str(current_pressure) + " hpa unit" +
                 ", humidity is " + str(current_humidiy) + " percent"
                                                           " and " + str(weather_description))
        print(r)
        speak(r)
    else:
        speak(" City Not Found ")


# translate
def translate():
    try:
        trans=Translator()
        speak("Say the language to translate in")
        language=takecommand().replace(" ","")
        pyautogui.keyDown("ctrl")
        pyautogui.press("c")
        pyautogui.keyUp("ctrl")
        tobespoken=pyperclip.paste()
        content=tobespoken
        t=trans.translate(text=content,dest=language)
        speak(f"{t.origin} in {t.dest} is{t.text}")

    except:
        speak("Unable to translate")


# send email
def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttl('YOUR EMAIL ID@gmail.com', 'PASSWORD')
    server.sendmail('YOUR EMAIL ID@gmail.com', to, content)
    server.close()


# for news updates
def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=d0cb2b6508464402845cb5e109a409c0'

    main_page = requests.get(main_url).json()
    #print(main_page)
    articles = main_page["articles"]
    #print(articles)
    head = []
    day=["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(day)):
        # print(f"today's {day[i]} news is: ", head[i])
        speak(f"today's {day[i]} news is: {head[i]}")


# to search/do anything
def search_wikihow(query, max_results=10, lang="en"):
    return list(WikiHow.search(query, max_results, lang))


def TaskExecution():
    wish()
    while True:

        query = takecommand().lower()

# date
        if ('date' in query):
            date()


# time
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")


# internet connection
        elif ('check my internet connection' in query or 'am I connected to internet' in query):
            hostname = "google.co.in"
            response = os.system("ping -c 1" + hostname)
            if response == 0:
                speak("Sir Internet is disconnected")
            else:
                speak("sir you are connected to internet")


# music
        elif "play music" in query:
            music_dir = "C:\\Users\\ASUS\\Music\\Music\\songs3"
            songs = os.listdir(music_dir)
            # rd = random.choice(songs)
            for song in songs:
                if song.endswith('.mp3'):
                    os.startfile(os.path.join(music_dir, song))


# reminder
        elif ("create a reminder list" in query or "reminder" in query):
            speak("What is the reminder?")
            data = takecommand()
            speak("You said to remember that" + data)
            reminder_file = open("data.txt", 'a')
            reminder_file.write('\n')
            reminder_file.write(data)
            reminder_file.close()


# read reminder list
        elif ("do you know anything" in query or "remember" in query or " our plans " in query):
            reminder_file = open("data.txt", 'r')
            speak("You said me to remember that: " + reminder_file.read())


# make a note
        elif 'make a note' in query or 'write down' in query:
            speak("What would you like me to note down?")
            note_text = takecommand()
            note(note_text)
            speak("I've made a note of that. Anything else?")
            query = takecommand()
            if "no" in query:
                speak('ok sir')
            if "yes" in query:
                speak('Go on sir')


# screenshot
        elif ("take screenshot" in query):
            speak("sir, please tell me the name for this screenshot file")
            name = takecommand().lower()
            screenshot()
            speak("Done sir, waiting for the next command")


# To read PDF files
        elif "read pdf" in query:
            pdf_reader()


#To hide all files and folders
        elif "hide all files" in query or "hide this folder" in query or "visible for everyone" in query:
            speak("sir please tell me you want to hide this folder or make it visible for everyone")
            condition = takecommand().lower()
            if ("hide" in condition):
                os.system("attrib +h /s /d")  # os module
                speak("sir, all the files in this folder are now hidden.")

            elif ("visible" in condition):
                os.system("attrib -h /s /d")
                speak("sir, all the files in this folder are now visible to everyone.")

            elif ("leave it" in condition or "leave for now" in condition):
                speak("Ok sir")


# cpu and battery usage
        elif ("cpu and battery" in query or "battery" in query or "cpu" in query or "system status" in query):
            cpu()


# ip address
        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"your IP address is {ip}")


# Google Search
        elif ('wikipedia' in query or 'what' in query or 'who' in query or 'when' in query):
            speak("searching...")
            query = query.replace("searching", "")
            result = wikipedia.summary(query, sentences=2)
            print(query)

            speak('Here is What I found for')
            speak(result)


# open sites / apps
        elif "open facebook" in query:
            webbrowser.open("www.facebook.com")

        elif "open stackoverflow" in query:
            webbrowser.open("www.stackoverflow.com")

        elif "open notepad" in query:
            npath = "C:\\Windows\\system32\\notepad.exe"
            os.startfile(npath)

        elif "open command prompt" in query:
            os.system("start cmd")

        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k==27:
                    break;
            cap.release()
            cv2.destroyAllWindows()

        elif "open google" in query:
            speak("sir, what should i search on google")
            cm = takecommand().lower()
            webbrowser.open(f"{cm}")

        elif 'open youtube' in query:
            speak('Ok sir Opening Youtube')
            webbrowser.open("https://youtube.com/")
            speak("Sir what would u like to Watch on youtube?")
            query = takecommand()
            if 'search' in query:
                query = query.replace("search", "")
                url = f"https://www.youtube.com/results?search_query={query}"
                webbrowser.open(url)
                speak("I've searched for" + query + "in youtube")
            if 'will do it myself' in query or 'leave it' in query or 'no':
                speak("As You like sir!")


# close sites
        elif 'close chrome' in query:
            os.system("taskkill /f /im chrome.exe")
            speak('chrome has been closed')

        elif "close notepad" in query:
            os.system("taskkill /f /im notepad.exe")
            speak("notepad has been closed")

        elif "close command prompt" in query:
            os.system("taskkill /f /im cmd.exe")
            speak("command prompt has been closed")


# Send Whatsapp message
        elif "send message" in query:
            kit.sendwhatmsg("+919052289784", "this is testing protocol",14,52)
            time.sleep(120)
            speak("message has been sent")


# translate
        elif 'translate' in query:
            translate()


# timer
        elif 'timer' in query or 'stopwatch' in query:
            speak("For how many minutes?")
            timing = takecommand()
            timing =timing.replace('minutes', '')
            timing = timing.replace('minute', '')
            timing = timing.replace('for', '')
            timing = float(timing)
            timing = timing * 60
            speak(f'I will remind you in {timing} seconds')
            time.sleep(timing)
            speak('Your time has been finished sir')


# next window
        elif 'next window' in query or 'switch back' in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")
            speak("window switched")


# previous window
        elif 'previous window' in query or 'last window' in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")
            speak("anything else sir?")


# switch window
        elif 'switch window' in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            speak("which one")
            query = takecommand()
            if 'next' in query:
                pyautogui.press("right")
                pyautogui.keyUp("alt")
                speak('window switched')
            if "don't switch" in query or 'go back' in query:
                pyautogui.press("left")
                pyautogui.keyUp("alt")
                speak("window switched")


# close window
        elif 'close current window' in query:
            pyautogui.keyDown("alt")
            pyautogui.press("f4")
            pyautogui.keyUp("alt")


# Minimize current window
        elif 'minimise this window' in query or 'minimize current window' in query or 'minimize this' in query:
            pyautogui.keyDown("win")
            pyautogui.press("down")
            pyautogui.keyUp("win")
            speak("Current window has been minimized")


# Minimize all
        elif 'minimize all windows' in query or 'minimize all' in query:
            try:
                os.system('''powershell -command "(new-object -com shell.application).minimizeall()"''')
                speak("all windows minimized")
            except Exception as e:
                speak("Sir there are no windows to minimize")


# Maximize
        elif 'maximize window' in query or 'fullscreen' in query or 'maximise window' in query or 'maximise' in query:
            try:
                pyautogui.keyDown("win")
                pyautogui.press("up")
                pyautogui.keyUp("win")
                speak("This window is now on fullscreen")
            except Exception as e:
                speak("No windows to maximize")


# lock windows
        elif 'lock window' in query or 'lock the system' in query:
            try:
                speak("locking the device")
                ctypes.windll.user32.LockWorkStation()
            except Exception as e:
                speak("Sir windows is already locked")


# to set an alarm
        elif "set alarm" in query:
            nn = int(datetime.datetime.now().hour)
            if nn==22: 
                music_dir = 'C:\\Users\\ASUS\\Music\\Music\\songs'
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, songs[0]))

# shutdown
        elif "shut down the system" in query:
             os.system("shutdown /s /t 5")

# restart
        elif "restart the system" in query:
            os.system("shutdown /r /t 5")

# sleep
        elif "sleep the system" in query:
             os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


# tells jokes
        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)


# changing voice
        elif ("voice" in query or 'change voice' in query):
            speak("for female say female and, for male say male")
            q = takecommand()
            if ("female" in q):
                voice_change(1)
            elif ("male" in q):
                voice_change(0)


# To find your current location
        elif "where am i" in query or "where are we" in query:
           speak("wait sir, let me check")
           try:
               ipAdd = requests.get('https://api.ipify.org').text
               print(ipAdd)
               url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + 'json'
               geo_requests = requests.get(url)
               geo_data = geo_requests.json()
               # print(geo_data)
               city = geo_data["city"]
               # state= geo_data['state']
               country = geo_data['country']
               speak(f"sir i am not sure, but i think we are in {city} city of {country} country")


           except Exception as e:
               speak("sorry sir, Due to network issue i am not able to find where we are.")
               pass


# To check a instagram profile
        elif "instagram profile" in query or "profile on instagram" in query:
            speak("sir please enter the username correctly")
            name = input("Enter username here:")
            webbrowser.open(f"www.instagram.com/{name}")
            speak(f"Sir here is the profile of the user {name}")
            time.sleep(5)
            speak("sir would you like to download profile picture of this account.")
            condition = takecommand().lower()
            if "yes" in condition:
                mod = instaloader.Instaloader()  # pip install instadownloader
                mod.download_profile(name, profile_pic_only=True)
                speak("i am done sir, profile picture is saved in our main folder. now i am ready")
            else:
                pass


# To calculate
        elif "do some calculations" in query or "can you calculate" in query or 'calculate' in query:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                speak("Say what you want to calculate")
                print("listening.....")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)

            my_string = r.recognize_google(audio)
            print(my_string)

            def get_operator_fn(op):
                return {
                    '+' : operator.add, # plus

                    '-' : operator.sub,  # minus

                    'x' : operator.mul,  # multiplied by

                    'divided by' : operator.__truediv__, #divided
                     }[op]


            def eval_binary_expr(op1, oper, op2):  # 5 plus 8
                op1, op2 = int(op1), int(op2)
                return get_operator_fn(oper)(op1, op2)
            speak("your result is")
            speak(eval_binary_expr(*(my_string.split())))


# weather
        elif 'weather' in query or 'temperature' in query:
            weather_info()


# news
        elif "tell me news" in query:
            speak("please wait sir, feteching the latest news")
            news()


# email
        elif "email to karthik" in query or 'send email' in query:
            speak("sir what should i say")
            query = takecommand().lower()
            if "send a file" in query:
                email = 'your@gmail.com'  # Your email
                password = 'your_pass'  # Your email account password
                send_to_email = 'To_person@gmail.com'  # Whom you are sending the message to
                speak("okay sir, what is the subject for this email")
                query = takecommand().lower()
                subject = query  # The Subject in the email
                speak("and sir, what is the message for this email")
                query2 = takecommand().lower()
                message = query2  # The message in the email
                speak("sir please enter the correct path of the file into the shell")
                file_location = input("please enter the path here")  # The File attachment in the email

                speak("please wait,i am sending email now")

                msg = MIMEMultipart()
                msg['From'] = email
                msg['To'] = send_to_email
                msg['Subject'] = subject

                msg.attach(MIMEText(message, 'plain'))

                # Setup the attachment
                filename = os.path.basename(file_location)
                attachment = open(file_location, "rb")
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

                # Attach the attachment to the MIMEMultipart object
                msg.attach(part)

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email, password)
                text = msg.as_string()
                server.sendmail(email, send_to_email, text)
                server.quit()
                speak("email has been sent to karthik")

            else:
                email = 'your@gmail.com'  # Your email
                password = 'your_pass'  # Your email account password
                send_to_email = 'To_person@gmail.com'  # Whom you are sending the message to
                message = query  # The message in the email

                server = smtplib.SMTP('smtp.gmail.com', 587)  # Connect to the server
                server.starttls()  # Use TLS
                server.login(email, password)  # Login to the email server
                server.sendmail(email, send_to_email, message)  # Send the email
                server.quit()  # Logout of the email server
                speak("email has been sent to karthik")


# formal chatting
        elif 'how are you' in query or 'how are you doing' in query:
            speak("am fine sir, what about you?")
            query = takecommand()
            if 'am also good' in query or 'am also fine' in query or 'healthy' in query or 'fine' in query:
                speak("wow")
            if 'not fine' in query or 'not well' in query or 'not good' in query or 'felling low' in query or 'not in mood' in query:
                speak("sad to hear that sir, how may I change your mood, May i play music for You?")
                query = takecommand()
                if 'ok' in query or 'sure' in query or 'hmm' in query or 'alright' in query or 'yeah' in query or 'play music' in query:
                    speak('ok sir playing music for you')
                    music_dir = "C:\\Users\\ASUS\\Music\\Music\\songs3"
                    songs = os.listdir(music_dir)
                    rd = random.choice(songs)
                    print(songs)
                    for songs in songs:
                        if songs.endswith('.mp3'):
                            os.startfile(os.path.join(music_dir, songs))
                elif "no" in query or "it's ok" in query or "don't play" in query or 'nope' in query:
                    speak("Ok sir as You like!")


# take a break
        elif 'take a break' in query or 'get some rest' in query or 'jarvis down' in query or 'keep quiet' in query:
            speak("Do You want me to take a break sir")
            query = takecommand()
            if 'no' in query or 'cancel' in query:
                speak("Process cancelled")
            if 'yes' in query or 'yep' in query:
                hour = int(datetime.datetime.now().hour)
                if hour >= 0 and hour < 18:
                    speak("Have a Nice day sir!")
                    break
                elif hour >= 18 and hour < 24:
                    speak("Ok, good Night sir. I will be on standby for you")
                    break


# to search/do anything
        elif "activate how to do mod" in query:
            speak("How to do mode is activated")
            while True:
                speak("please tell me what you want to know")
                how = takecommand()

                try:
                    if "exit" in how or "close" in how:
                        speak("okay sir, exiting from how to do mode")
                        break
                    else:
                        max_results = 1
                        how_to = search_wikihow(how, max_results)
                        assert len(how_to) == 1
                        how_to[0].print()
                        speak(how_to[0].summary)

                except Exception as e:
                    speak("sorry sir, i am unable to find this")



if __name__ == "__main__": #main program
    while True:
        permission = takecommand()
        if "wake up" in permission or "hey jarvis" in permission:
            TaskExecution()

        elif "goodnight" in permission or "thank you" in permission:
            speak("Thank you for having me sir")
            sys.exit()