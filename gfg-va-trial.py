from trello import TrelloClient
import subprocess
import wolframalpha
import pyttsx3
import json
import speech_recognition as sr
import datetime

import wikipedia
import webbrowser
import os

import winshell
import pyjokes
import smtplib
import ctypes
import time
import requests
import shutil

from twilio.rest import Client
from clint.textui import progress
from ecapture import ecapture as ec
from urllib.request import urlopen

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

vaname = "Alice"

from dotenv import load_dotenv

load_dotenv()

trello_api_key = os.getenv("TRELLO_API_KEY")
trello_token = os.getenv("TRELLO_TOKEN")
trello_token_secret = os.getenv("TRELLO_TOKEN_SECRET")

# print(trello_api_key, trello_token)

client = TrelloClient(
    api_key=trello_api_key,
    token=trello_token,
    token_secret=trello_token_secret,
)

# print(pyttsx3.voice.Voice)


def open_board(client):
    """
    This function will print the name, id, and url of all the boards that the user has access to

    :param client: TrelloClient object
    """
    boards = client.list_boards()

    for board in boards:
        print(board.name)
        print(board.id)
        print(board.url)


def speak(audio):
    """
    The function takes in a string of text, converts it to speech, and plays it back to the user

    :param audio: The audio to be played
    """
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    """
    It takes the current hour and if it's between 0 and 12, it says "Good Morning", if it's between 12
    and 18, it says "Good Afternoon", and if it's between 18 and 24, it says "Good Evening".
    """
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Nigga !")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Nigga !")

    else:
        speak("Good Evening Nigga !")

    speak(f"I am {vaname}")


def username():
    """
    It asks the user for a name, then greets the user with that name.
    """
    speak("What should i call you sir")
    uname = takeCommand()
    speak("Welcome Mister")
    speak(uname)
    columns = shutil.get_terminal_size().columns

    print("#####################".center(columns))
    print("Welcome Mr.", uname.center(columns))
    print("#####################".center(columns))

    speak("How can i Help you, Sir")


def takeCommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "None"

    return query


def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()

    # Enable low security in gmail
    server.login("your email id", "your email password")
    server.sendmail("your email id", to, content)
    server.close()


def main(client, open_board, speak, wishMe, takeCommand, sendEmail):
    query = takeCommand().lower()

    # All the commands said by user will be
    # stored here in 'query' and will be
    # converted to lower case for easily
    # recognition of command
    if "wikipedia" in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=3)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    elif "open board" in query:
        open_board(client)

    elif "open trello" in query:
        webbrowser.open("https://trello.com/")

    elif "open youtube" in query:
        speak("Here you go to Youtube\n")
        webbrowser.open("youtube.com")

    elif "open google" in query:
        speak("Here you go to Google\n")
        webbrowser.open("google.com")

    elif "open stackoverflow" in query:
        speak("Here you go to Stack Over flow.Happy coding")
        webbrowser.open("stackoverflow.com")

    elif "play music" in query or "play song" in query:
        speak("Here you go with music")
        # music_dir = "G:\\Song"
        music_dir = "D:\Music\Soggfy"
        songs = os.listdir(music_dir)
        print(songs)
        os.startfile(os.path.join(music_dir, songs[1]))

    elif "the time" in query:
        strTime = datetime.datetime.now().strftime("% H:% M:% S")
        speak(f"Sir, the time is {strTime}")

    elif "open opera" in query:
        codePath = r"C:\\Users\\GAURAV\\AppData\\Local\\Programs\\Opera\\launcher.exe"
        os.startfile(codePath)

    elif "email to gaurav" in query:
        try:
            speak("What should I say?")
            content = takeCommand()
            to = "Receiver email address"
            sendEmail(to, content)
            speak("Email has been sent !")
        except Exception as e:
            print(e)
            speak("I am not able to send this email")

    elif "send a mail" in query:
        try:
            speak("What should I say?")
            content = takeCommand()
            speak("whome should i send")
            to = input()
            sendEmail(to, content)
            speak("Email has been sent !")
        except Exception as e:
            print(e)
            speak("I am not able to send this email")

    elif "how are you" in query:
        speak("I am fine, Thank you")
        speak("How are you, Sir")

    elif "fine" in query or "good" in query:
        speak("It's good to know that your fine")

    elif "change my name to" in query:
        query = query.replace("change my name to", "")
        vaname = query

    elif "change name" in query:
        speak("What would you like to call me, Sir ")
        vaname = takeCommand()
        speak("Thanks for naming me")

    elif "what's your name" in query or "what is your name" in query:
        speak(f"My name is {vaname}")
        # print("My friends call me", vaname)

    elif "exit" in query:
        speak("Thanks for giving me your time")
        exit()

    elif "who made you" in query or "who created you" in query:
        speak("I have been created by Achsah & Mayur.")

    elif "joke" in query:
        # speak(pyjokes.get_joke())
        print(pyjokes.get_joke())

    elif "calculate" in query:
        app_id = "Wolframalpha api id"
        client = wolframalpha.Client(app_id)
        indx = query.lower().split().index("calculate")
        query = query.split()[indx + 1 :]
        res = client.query(" ".join(query))
        answer = next(res.results).text
        print(f"The answer is {answer}")
        speak(f"The answer is {answer}")

    elif "search" in query or "play" in query:
        query = query.replace("search", "")
        query = query.replace("play", "")
        webbrowser.open(query)

    elif "who i am" in query:
        speak("If you talk then definitely your human.")

    elif "why you came to world" in query:
        speak("Thanks to Gaurav. further It's a secret")

    elif "power point presentation" in query:
        speak("opening Power Point presentation")
        power = r"C:\\Users\\GAURAV\\Desktop\\Minor Project\\Presentation\\Voice Assistant.pptx"
        os.startfile(power)

    elif "is love" in query:
        speak("It is 7th sense that destroy all other senses")

    elif "who are you" in query:
        speak("I am your virtual assistant created by Gaurav")

    elif "reason for you" in query:
        speak("I was created as a Minor project by Mister Gaurav ")

    elif "change background" in query:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, "Location of wallpaper", 0)
        speak("Background changed successfully")

    elif "open bluestack" in query:
        appli = r"C:\\ProgramData\\BlueStacks\\Client\\Bluestacks.exe"
        os.startfile(appli)

    elif "news" in query:
        try:
            jsonObj = urlopen(
                """https://newsapi.org / v1 / articles?source = the-times-of-india&sortBy = top&apiKey =\\times of India Api key\\"""
            )
            data = json.load(jsonObj)
            speak("here are some top news from the times of india")
            print("""=============== TIMES OF INDIA ============""" + "\n")

            for i, item in enumerate(data["articles"], start=1):
                print(f"{str(i)}. " + item["title"] + "\n")
                print(item["description"] + "\n")
                speak(f"{str(i)}. " + item["title"] + "\n")
        except Exception as e:
            print(e)

    elif "lock window" in query:
        speak("locking the device")
        ctypes.windll.user32.LockWorkStation()

    elif "shutdown system" in query:
        speak("Hold On a Sec ! Your system is on its way to shut down")
        subprocess.call("shutdown / p /f")

    elif "empty recycle bin" in query:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
        speak("Recycle Bin Recycled")

    elif "don't listen" in query or "stop listening" in query:
        speak("for how much time you want to stop jarvis from listening commands")
        a = int(takeCommand())
        time.sleep(a)
        print(a)

    elif "where is" in query:
        query = query.replace("where is", "")
        location = query
        speak("User asked to Locate")
        speak(location)
        webbrowser.open(f"https://www.google.com / maps / place/{location}")

    elif "camera" in query or "take a photo" in query:
        ec.capture(0, "Jarvis Camera ", "img.jpg")

    elif "restart" in query:
        subprocess.call(["shutdown", "/r"])

    elif "hibernate" in query or "sleep" in query:
        speak("Hibernating")
        subprocess.call("shutdown / h")

    elif "log off" in query or "sign out" in query:
        speak("Make sure all the application are closed before sign-out")
        time.sleep(5)
        subprocess.call(["shutdown", "/l"])

    elif "write a note" in query:
        speak("What should i write, sir")
        note = takeCommand()
        file = open("jarvis.txt", "w")
        speak("Sir, Should i include date and time")
        snfm = takeCommand()
        if "yes" in snfm or "sure" in snfm:
            strTime = datetime.datetime.now().strftime("% H:% M:% S")
            file.write(strTime)
            file.write(" :- ")
        file.write(note)
    elif "show note" in query:
        speak("Showing Notes")
        file = open("jarvis.txt", "r")
        print(file.read())
        speak(file.read(6))

    elif "update assistant" in query:
        speak("After downloading file please replace this file with the downloaded one")
        url = "# url after uploading file"
        r = requests.get(url, stream=True)

        with open("Voice.py", "wb") as Pypdf:
            total_length = int(r.headers.get("content-length"))

            for ch in progress.bar(
                r.iter_content(chunk_size=2391975),
                expected_size=(total_length / 1024) + 1,
            ):
                if ch:
                    Pypdf.write(ch)

        # NPPR9-FWDCX-D2C8J-H872K-2YT43
    elif "jarvis" in query:
        wishMe()
        speak("Jarvis 1 point 0 in your service Mister")
        speak(vaname)

    elif "weather" in query:
        base_url = "http://api.openweathermap.org / data / 2.5 / weather?"
        speak(" City name ")
        print("City name : ")
        city_name = takeCommand()
        api_key = "Api key"
        complete_url = f"{base_url}appid ={api_key}&q ={city_name}"
        response = requests.get(complete_url)
        x = response.json()

        if x["code"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_pressure = y["pressure"]
            current_humidiy = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            print(
                f" Temperature (in kelvin unit) = {str(current_temperature)}"
                + "\n atmospheric pressure (in hPa unit) ="
                + str(current_pressure)
                + "\n humidity (in percentage) = "
                + str(current_humidiy)
                + "\n description = "
                + str(weather_description)
            )

        else:
            speak(" City Not Found ")

    elif "send message " in query:
        # You need to create an account on Twilio to use this service
        account_sid = "Account Sid key"
        auth_token = "Auth token"
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=takeCommand(), from_="Sender No", to="Receiver No"
        )

        print(message.sid)

    elif "Good Morning" in query:
        speak(f"A warm{query}")
        speak("How are you Mister")
        speak(vaname)

        # most asked question from google Assistant
    elif "will you be my gf" in query or "will you be my bf" in query:
        speak("I'm not sure about, may be you should give me some time")

    elif "i love you" in query:
        speak("It's hard to understand")


if __name__ == "__main__":

    def clear():
        return os.system("cls")

    # This Function will clean any
    # command before execution of this python file
    clear()
    wishMe()
    username()

    while True:

        main(client, open_board, speak, wishMe, takeCommand, sendEmail)

        # elif "what is" in query or "who is" in query:

        #     # Use the same API key
        #     # that we have generated earlier
        #     client = wolframalpha.Client("API_ID")
        #     res = client.query(query)

        #     try:
        #         print(next(res.results).text)
        #         speak(next(res.results).text)
        #     except StopIteration:
        #         print("No results")

        # elif "" in query:
        # Command go here
        # For adding more commands