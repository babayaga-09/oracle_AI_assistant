import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import requests
import json
import random

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak out the given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to greet the user
def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am Jarvis. How can I assist you today?")

# Function to take voice input from the user
def take_command():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-us')
        print(f"User said: {query}\n")
    except Exception as e:
        print("I'm sorry, I couldn't understand what you said.")
        query = None
    return query

# Function to send email
def send_email(to, subject, content):
    # Configure your email credentials and server
    email_address = 'aryangrang@gmail.com'
    password = 'Agrang190905'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email_address, password)
    message = f"Subject: {subject}\n\n{content}"
    server.sendmail(email_address, to, message)
    server.close()

# Function to get weather updates
def get_weather(city):
    api_key = 'your_openweathermap_api_key'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    if data['cod'] == 200:
        weather_desc = data['weather'][0]['description']
        temperature = data['main']['temp']
        speak(f"The weather in {city} is {weather_desc}. The temperature is {temperature} degrees Celsius.")
    else:
        speak("Sorry, I couldn't retrieve the weather information for that city.")

# Main function to execute Jarvis
def main():
    greet()
    while True:
        query = take_command().lower()

        if query:
            if 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
            elif 'open youtube' in query:
                webbrowser.open("youtube.com")
            elif 'open google' in query:
                webbrowser.open("google.com")
            elif 'play music' in query:
                music_dir = 'path_to_your_music_directory'
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, random.choice(songs)))
            elif 'what is the time' in query:
                time = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The current time is {time}")
            elif 'send email' in query:
                try:
                    speak("What should I say in the email?")
                    content = take_command()
                    speak("Who should I send it to?")
                    to = input("Recipient: ")
                    send_email(to, "Subject", content)
                    speak("Email has been sent!")
                except Exception as e:
                    print(e)
                    speak("Sorry, I couldn't send the email.")
            elif 'weather' in query:
                speak("Sure, which city?")
                city = take_command()
                get_weather(city)
            elif 'exit' in query:
                speak("Goodbye!")
                break
            else:
                speak("I'm sorry, I didn't understand that command.")

if __name__ == "__main__":
    main()