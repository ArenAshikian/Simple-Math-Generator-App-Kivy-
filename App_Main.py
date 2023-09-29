import kivy
import random
import time
import sys
import pygame
from pygame import mixer
from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

score=0
timer_switch=True
counter=0

Builder.load_file('App_Main.kv')

class MyGrid(GridLayout):
    pygame.init()
    #mixer.music.load('background.wav')
    #mixer.music.play(-1)

    def addition(self):
        answer=0
        question=""
        number_One=0
        number_Two=0
        
        number_One = random.randint(0,20)
        number_Two = random.randint(0,20)
        self.question="What is " + str(number_One) + " + " +str(number_Two)
        self.answer= (number_One + number_Two)
        return question, answer

    def __init__ (self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols=1
        self.inside = GridLayout()
        self.current_health=200
        self.maximum_health=1000
        self.health_bar_length=400
        self.health_ratio=self.maximum_health/self.health_bar_length
   
        #self.basic_health()
        self.addition()
        self.inside.cols=1
        self.inside.add_widget(Label(text=self.question)) 
        self.name=TextInput(multiline=False)
        self.inside.add_widget(self.name)
        self.add_widget(self.inside)
        self.submit = Button(text="Submit", font_size=40)
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)
        


        

        


    def pressed_answer(self, instance):
        Builder.unload_file('App_Main.kv')
        self.remove_widget(self.answer)
        self.__init__()
        

    def pressed_restart(self, instance):
        global score
        self.remove_widget(self.restart)
        self.remove_widget(self.ending)
        current= self.ids.my_progress_bar.value
        current=100
        
        self.ids.my_progress_bar.value=current
        score=0
        self.__init__()
        
    

    def pressed(self, instance):
        global score
        global counter

        
        if str(self.answer)==self.name.text:
            
            score+=1
            self.remove_widget(self.inside)
            self.remove_widget(self.submit)
            current= self.ids.my_progress_bar.value
            current+=10
            if current>100:
                current=100
            self.ids.my_progress_bar.value=current
            self.answer = Button(text="Great Job!", font_size=40)
            self.answer.bind(on_press=self.pressed_answer)
            self.add_widget(self.answer)


            
        else: 
            current= self.ids.my_progress_bar.value
            current-=10
            self.ids.my_progress_bar.value=current
            if current<=0:
                
                Builder.unload_file('App_Main.kv')
                Builder.unload_file('App_Main.kv')
                self.ids.my_progress_bar.value=1
                self.remove_widget(self.inside)
                self.remove_widget(self.submit)
                self.ending=GridLayout()
                self.ending.cols=1
                self.ending.add_widget(Label(text="You Lose", font_size=40))
                self.restart = Button(text="          Press to Try Again!\n You had " + str(score)+ " Questions Correct!", font_size=40)
                self.restart.bind(on_press=self.pressed_restart)
                self.add_widget(self.restart)

        self.name.text=""      
        
class MyApp(App):
    def build(self):
        return MyGrid()

if __name__ == "__main__":
    MyApp().run()