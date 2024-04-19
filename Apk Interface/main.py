from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from pathlib import Path
from kivy.core.window import Window
from kivy.clock import Clock

DIRPATH = Path(__file__).parent
LOGO = DIRPATH.joinpath("logo.png")

class Aplicacao(App):
    def build(self):
        Window.size = (300, 500)
        self.layout = FloatLayout(size=(300, 500))

        with self.layout.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.rect = Rectangle(size=Window.size, pos=self.layout.pos)

        self.logo = Image(source=str(LOGO), size_hint=(None, None), size=(200, 200))
        self.logo.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.layout.add_widget(self.logo)

        Clock.schedule_once(self.initiate_fade_out, 3)
        return self.layout

    def initiate_fade_out(self, *args):
        animation = Animation(opacity=0, duration=2)
        animation.bind(on_complete=self.on_fade_out_complete)
        animation.start(self.logo)

    def on_fade_out_complete(self, animation, widget):
        self.layout.remove_widget(self.logo)
        self.show_login_screen()

    def show_login_screen(self):
        # Cria o campo de usuário
        self.logo = Image(source=str(LOGO), size_hint=(None, None), size=(200, 200))
        self.logo.pos_hint = {'center_x': 0.5, 'center_y': 0.7}
        self.layout.add_widget(self.logo)

        self.username = TextInput(
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
            hint_text='Username'
        )
        self.layout.add_widget(self.username)

        # Cria o campo de senha
        self.password = TextInput(
            password=True,
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35},
            hint_text='Password'
        )
        self.layout.add_widget(self.password)

        # Cria um botão de login
        self.login_button = Button(
            text="Login",
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.login_button.bind(on_press=self.validate_user)
        self.layout.add_widget(self.login_button)

        # Mensagem de erro (oculta inicialmente)
        self.error_label = Label(
            text="",
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            color=(1, 0, 0, 1)  # Vermelho
        )
        self.layout.add_widget(self.error_label)

    def validate_user(self, instance):
        # Valida o usuário e a senha (aqui é só um placeholder)
        if self.username.text == "user" and self.password.text == "pass":
            self.error_label.text = "Login successful!"
        else:
            self.error_label.text = "Invalid username or password."

if __name__ == '__main__':
    Aplicacao().run()