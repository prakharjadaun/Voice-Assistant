import threading
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import NumericProperty, ColorProperty
from kivy.uix.widget import Widget
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivymd.utils.fitimage import FitImage
#from kivy.uix.image import Image

# from kivymd.uix.screen import MDScreen
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import time
#import smtplib
# import keyboard
import pyautogui
import random
# from kivy.uix.label import Label
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices)
# print(voices[0])
engine.setProperty('voice', voices[0].id)



from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFloatingActionButton
from kivy.clock import Clock
KV='''
<MicAnimation>
    canvas:
        Color:
            rgba: root.set_color
        Ellipse:
            size: dp(self.rad),dp(self.rad)
            pos:(-dp(self.rad)/2+self.widget_pos/2,-dp(self.rad)/2+self.widget_pos/2)
<FloatingButton>:
    id: microphone
    icon: 'microphone'
    pos_hint:{'center_x':0.5}
    user_font_size:40
    md_bg_color: [0.5,0.5,0.5,1]
    on_release:
        app.listen() if not app.listening else ''
    RelativeLayout:
        MicAnimation:
            id: ellipse
            opacity: 0
            set_color: app.theme_cls.primary_color
            rad: 80
            widget_pos: self.parent.size[0]
            halign:'left'
'''

class FloatingButton(MDFloatingActionButton):
    Builder.load_string(KV)

class MicAnimation(Widget):
    set_color = ColorProperty([0, 0, 0, 1])
    rad = NumericProperty(80)
    widget_pos = NumericProperty(0)


class VoiceAssistant(MDApp):
    listening=False
    def build(self):
        self.count=0
        self.screen=MDScreen()
        self.label=MDLabel(text='Hello User...!', font_style='H3', halign='center',font_name="Bulgatti-xgMV")
        self.screen.add_widget(FitImage(source='new.jpg'))
        self.screen.add_widget(self.label)
        self.floating_button= FloatingButton()
        Clock.schedule_once(self.greet, 2.5)
        self.screen.add_widget(self.floating_button)
        return self.screen

    def animate_it(self, widget, *args) :
        widget.opacity = 0.15
        self.widget = widget
        self.rad = widget.rad
        self.animate = Animation(rad=self.rad * 1.8, duration=0.2)
        for i in range(15):
            self.animate += Animation(rad=self.rad * (1 + .6 * random.random()), duration=0.3)
        self.animate.start(self.widget)
        self.animate.repeat = True

    def listen(self,*args):
        self.listening=True
        self.animate_it(self.floating_button.ids.ellipse)
        self.floating_button.md_bg_color=self.theme_cls.primary_color
        def takeCommand():
            '''it takes microphone input from the user and returns string output '''
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold = 1
                audio = r.listen(source)

            try:
                print("Recognizing...")
                self.query = r.recognize_google(audio, language='en-in')
                print(f'User said : {self.query}')
                self.change_label()
            except Exception as e:
                print(e)
                print("Say that again please")

        self.label.text='Listening'
        threading.Thread(target=takeCommand, daemon=True).start()


    def change_label(self,*args):
        self.listening=False
        self.floating_button.md_bg_color=[0.5,0.5,0.5,1]
        self.animate.stop(self.widget)
        self.widget.opacity=0
        self.label.text=self.query.lower()
        self.query = self.query.lower()

        if 'wikipedia' in self.query:
            self.speak('Searching wikipedia...')
            self.query = self.query.replace("wikipedia", "")
            results = wikipedia.summary(self.query, sentences=2)
            print(results)
            self.speak("according to Wikipedia")
            self.speak(results)
        elif 'stop' in self.query:
            pyautogui.hotkey('ctrl', 'shift', 'u')
        elif (('news' or 'new') in self.query):
            webbrowser.open("https://www.indiatoday.in/india")
            time.sleep(5)
            pyautogui.hotkey('ctrl', 'shift', 'u')
            # keyboard.press_and_release("ctrl+shift+u")
        elif (('whatsapp') in self.query):
            webbrowser.open("http://web.whatsapp.com/")
            time.sleep(7)
            self.speak("Search the name of the person through the search bar in the upper left corner of the screen")
            self.speak("if you wish to place a video call then click on the video call option in the bar")
            self.speak(
                "if you wish to send a audio message then press and hold the audio button which is at bottom right corner of the type bar")
        elif ('youtube' in self.query):
            webbrowser.open("youtube.com")
            self.speak("Search your interest videos on the search bar in the center of the screen")
        elif (('netflix' or 'net flix') in self.query):
            webbrowser.open("https://www.netflix.com/in/")
            time.sleep(3)
            self.speak("Enter your email address and get started with your popcorns")
        elif ('facebook' in self.query):
            webbrowser.open("https://www.facebook.com/")
            time.sleep(3)
            self.speak("Enter your email or phone number and then enter your password")
            self.speak("You are good to go!")
        elif 'instagram' in self.query:
            webbrowser.open("https://www.instagram.com/")
            time.sleep(4)
            pyautogui.hotkey('tab')
            pyautogui.typewrite("#######")   #enter yur username 
            pyautogui.hotkey('tab')
            pyautogui.typewrite('#######')       #enter your password
            pyautogui.hotkey('enter')
        elif 'google' in self.query:
            webbrowser.open("google.com")
        elif 'play music' in self.query:
            #Enter the path to your music directory
            music_dir = "C:\\Users\\Prakhar Jadaun\\Desktop\\Media\\Music"  
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[random.randint(0, len(songs) - 1)]))
            # temp = webbrowser
        elif 'the time' in self.query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            self.speak(f"Sir, the time is {strTime}")
    
    def speak(self,audio):
        engine.say(audio)
        engine.runAndWait()

    def greet(self,*args):
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            self.speak("good morning ")
        elif hour >= 12 and hour < 18:
            self.speak("Good afternoon")
        else:
            self.speak("good evening")

        self.speak("I am Jarvis")
        self.speak("how can i help you sir")

VoiceAssistant().run()
