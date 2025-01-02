import os
import webbrowser
import datetime
import speech_recognition as sr
import pyttsx3
import openai
import os
import wikipedia
import subprocess

# Initialize the speech recognition and text-to-speech engines  
r = sr.Recognizer()  
engine = pyttsx3.init()  

def speak(text):
    engine.say(text)
    engine.runAndWait()

openai.api_key = 'paste your api key here'

print("API Key:", "Present" if openai.api_key else "Missing")

def get_chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def recognize_speech():  
    with sr.Microphone() as source:  
        print("Listening...")  
        audio = r.listen(source)  
        try:  
            print("Recognizing...")  
            query = r.recognize_google(audio, language='en-US')  
            print(f"User  said: {query}")  
            return query  
        except sr.UnknownValueError:  
            print("Sorry, I didn't catch that.") 
            speak("Sorry, I didn't catch that.") 
            return None  
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None

def perform_task(query):  
    if query is None:  
        return  

    # Basic tasks  
    if "hello" in query.lower():  
        engine.say("Hello! How can I assist you today?")  
        engine.runAndWait()  

    elif "what's your name" in query.lower():  
        engine.say("My name is Viky, and I'm here to help you with any questions or tasks you may have.")  
        engine.runAndWait()  

    elif "what is the time" in query.lower():  
        current_time = datetime.datetime.now().strftime("%I:%M %p")  
        engine.say(f"The current time is {current_time}.")  
        engine.runAndWait()

    elif "open google" in query.lower():  
        webbrowser.open("https://www.google.com")

    elif "open notepad" in query.lower():
        subprocess.Popen("notepad.exe")
        speak("Opening Notepad")

    elif "open calculator" in query.lower():
        subprocess.Popen("calc.exe")
        speak("Opening Calculator")

    elif "open word" in query.lower():
        try:
            subprocess.Popen(["winword.exe"])
            speak("Opening Microsoft Word")
        except FileNotFoundError:
            speak("Microsoft Word is not installed on this computer")

    elif "open excel" in query.lower():
        try:
            subprocess.Popen(["excel.exe"])
            speak("Opening Microsoft Excel")
        except FileNotFoundError:
            speak("Microsoft Excel is not installed on this computer")

    elif "open chrome" in query.lower():
        try:
            subprocess.Popen(["chrome.exe"])
            speak("Opening Google Chrome")
        except FileNotFoundError:
            speak("Google Chrome is not installed on this computer")

    elif "play music" in query.lower():
        speak("What song would you like me to play?")
        song_query = recognize_speech()
        if song_query:
            search_query = song_query.replace(" ", "+")
            # Search YouTube and get first video
            youtube_url = f"https://www.youtube.com/watch?v=" # Direct video URL format
            search_url = f"https://www.youtube.com/results?search_query={search_query}"
            import urllib.request
            import re
            html = urllib.request.urlopen(search_url)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            if video_ids:
                first_video = youtube_url + video_ids[0]
                webbrowser.open(first_video)
                speak(f"Playing {song_query} from YouTube")
            else:
                speak("Sorry, I couldn't find that song on YouTube")

    elif "search" in query.lower():
        search_query = query.lower().replace("search", "").strip()
        if search_query:
            search_url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(search_url)
            # Get ChatGPT response about the search query
            response = get_chatgpt_response(f"Give me a brief summary about {search_query}")
            print(f"Here's what I found about {search_query}: {response}")
            speak(f"Here's what I found about {search_query}: {response}")

    elif "wikipedia" in query.lower():
        speak("What would you like to know about?")
        question = recognize_speech()
        if question:
            try:
                search_term = question.replace("wikipedia", "").strip()
                response = wikipedia.summary(search_term, sentences=3)
                print(f"Wikipedia: {response}")
                speak(response)
                
                while True:
                    speak("Dose your doubt clear yes or no ")
                    clarity = recognize_speech()
                    
                    if clarity and "yes" in clarity.lower():
                        speak("Do you want to know more about this topic? yes or no")
                        more_info = recognize_speech()
                        if more_info and "yes" in more_info.lower():
                            wiki_page = wikipedia.page(search_term)
                            webbrowser.open(wiki_page.url)
                            speak("I have opened the wikipedia page for more detailed information")
                        break
                        
                    elif clarity and "no" in clarity.lower():
                        speak("let me try to explain it differently")
                        # Get a more detailed summary
                        detailed_response = wikipedia.summary(search_term, sentences=5)
                        print(f"Detailed explanation: {detailed_response}")
                        speak(detailed_response)
                    else:
                        break
                        
            except wikipedia.exceptions.DisambiguationError as e:
                speak("there are multiple matches for your query. please be more specific")
            except wikipedia.exceptions.PageError:
                speak("i couldn't find any information about that. let me search google for you")
                search_url = f"https://www.google.com/search?q={question}"
                webbrowser.open(search_url)
        else:
            speak("i didn't catch your question. please try again")

    elif "exit" in query.lower() or "stop" in query.lower():
        engine.say("goodbye!")
        engine.runAndWait()
        exit()

# Main loop  
while True:  
    query = recognize_speech()  
    perform_task(query)
