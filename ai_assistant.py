import os
import pyttsx3
import speech_recognition as sr
import pywhatkit
import wikipedia
import pytesseract
from PIL import Image
from googletrans import Translator
import openai
import requests

# Initialize components
engine = pyttsx3.init()
recognizer = sr.Recognizer()
translator = Translator()

# OpenAI API Key
openai.api_key = "xxiyxx"  # Replace with your OpenAI API key

# Weather API Key
weather_api_key = "xxiyxx"  # Replace with your OpenWeatherMap API key

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for voice input."""
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError as e:
            speak(f"There was an error with the speech recognition service: {e}")
            return ""

def chat_with_gpt(prompt):
    """Generate a response using OpenAI GPT."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't process that."

def get_weather(city):
    """Get the weather for a given city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            weather = data['weather'][0]['description']
            temp = round(data['main']['temp'] - 273.15, 2)
            return f"The weather in {city} is {weather} with a temperature of {temp} degrees Celsius."
        else:
            return "I couldn't fetch the weather information."
    except Exception as e:
        return f"Error: {e}"

def execute_command(command):
    """Execute a recognized command."""
    if "hello" in command:
        speak("Hello! How can I help you?")
    elif "weather" in command:
        city = command.replace("weather", "").strip()
        if city:
            weather_info = get_weather(city)
            speak(weather_info)
            print(weather_info)
        else:
            speak("Please tell me the city.")
    elif "wikipedia" in command:
        topic = command.replace("wikipedia", "").strip()
        try:
            summary = wikipedia.summary(topic, sentences=2)
            speak(summary)
            print(summary)
        except wikipedia.exceptions.DisambiguationError as e:
            speak(f"Which {e.options[0]} did you mean?")
            print(f"Which {e.options[0]} did you mean?")
        except Exception as e:
            speak("I couldn't fetch information from Wikipedia.")
            print(f"Error: {e}")
    elif "chat" in command:
        speak("What would you like to talk about?")
        user_input = listen()
        if user_input:
            response = chat_with_gpt(user_input)
            speak(response)
            print(response)
    elif "exit" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("I didn't understand that command. Can you please repeat it?")

if __name__ == "__main__":
    speak("Hello, I am your assistant. How can I help you today?")
    while True:
        user_command = listen()
        if user_command:
            execute_command(user_command)
