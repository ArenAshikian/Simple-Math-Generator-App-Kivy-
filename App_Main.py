import kivy
import random
import pygame
from pygame import mixer
from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.boxlayout import BoxLayout

score = 0

# Load Kivy file
Builder.load_file('App_Main.kv')

class MyGrid(BoxLayout):
    pygame.init()
    mixer.init()
    # Uncomment the lines below if you have a background music file
    # mixer.music.load('background.wav')
    # mixer.music.play(-1)

    def addition(self):
        number_One = random.randint(0, 20)
        number_Two = random.randint(0, 20)
        question = f"What is {number_One} + {number_Two}?"
        answer = number_One + number_Two
        return question, answer

    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        self.current_health = 100
        self.maximum_health = 100

        self.progress_bar = self.ids.my_progress_bar

        self.inside = self.ids.inside_grid
        self.submit_button = self.ids.submit_button
        self.submit_button.bind(on_press=self.pressed)

        self.load_question()

    def load_question(self):
        self.inside.clear_widgets()
        self.question, self.answer = self.addition()
        self.inside.add_widget(Label(text=self.question))
        
        self.name_input = TextInput(multiline=False)
        self.inside.add_widget(self.name_input)
        
    def pressed_answer(self, instance):
        self.load_question()

    def pressed_restart(self, instance):
        global score
        score = 0
        self.current_health = 100
        self.progress_bar.value = self.current_health
        self.load_question()

    def pressed(self, instance):
        global score
        
        if str(self.answer) == self.name_input.text:
            score += 1
            self.current_health += 10
            if self.current_health > self.maximum_health:
                self.current_health = self.maximum_health

            self.inside.clear_widgets()
            self.inside.add_widget(Label(text="Great Job!", font_size=40))
            next_question_button = Button(text="Next Question", font_size=40)
            next_question_button.bind(on_press=self.pressed_answer)
            self.inside.add_widget(next_question_button)
        else:
            self.current_health -= 10
            if self.current_health <= 0:
                self.current_health = 0
                self.inside.clear_widgets()
                self.inside.add_widget(Label(text="You Lose", font_size=40))
                restart_button = Button(text=f"Press to Try Again! You had {score} Questions Correct!", font_size=40)
                restart_button.bind(on_press=self.pressed_restart)
                self.inside.add_widget(restart_button)
            else:
                self.load_question()
        
        self.progress_bar.value = self.current_health
        self.name_input.text = ""

class MyApp(App):
    def build(self):
        return MyGrid()

if __name__ == "__main__":
    MyApp().run()
