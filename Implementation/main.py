from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from pathlib import Path
from kivy.core.window import Window
from kivy.clock import Clock

DIRPATH = Path(__file__).parent
LOGO = DIRPATH.joinpath("logo.png")


class User:
    def __init__(self, username, password, email, phoneNumber, cards):
        self.username = username
        self.password = password
        self.email = email
        self.phoneNumber = phoneNumber
        self.cards = cards
        self.transactionsFile = username + ".txt"


class Card:
    def __init__(self, ID, balance, currencyCode):
        self.id = ID
        self.balance = balance
        self.currencyCode = currencyCode


class LinkLabel(ButtonBehavior, Label):
    pass


class Aplicacao(App):
    def build(self):
        self.fname = "users.txt"
        self.db = []
        self.readUserDatabase()

        Window.size = (350, 600)
        self.layout = FloatLayout(size=(350, 600))

        with self.layout.canvas.before:
            Color(0.2745, 0.5294, 0.5451, 1)  # Cor de fundo #415F61
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
        self.logo.pos_hint = {'center_x': 0.5, 'center_y': 0.80}
        self.layout.add_widget(self.logo)

        self.username = TextInput(
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            hint_text='Username'
        )
        self.layout.add_widget(self.username)

        # Cria o campo de senha
        self.password = TextInput(
            password=True,
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
            hint_text='Password'
        )
        self.layout.add_widget(self.password)

        # Cria um botão de login
        self.login_button = Button(
            text="Login",
            size_hint=(0.8, 0.08),
            pos_hint={'center_x': 0.5, 'center_y': 0.33}
        )
        self.create_account_button = Button(
            text="Create an acount",
            size_hint=(0.8, 0.08),
            pos_hint={'center_x': 0.5, 'center_y': 0.25}
        )
        self.login_button.bind(on_press=self.validate_user)
        self.layout.add_widget(self.login_button)

        self.create_account_button.bind(on_press=self.validate_user)
        self.layout.add_widget(self.create_account_button)
        self.error_label = Label(
            text="",
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            color=(1, 0, 0, 1)  # Vermelho
        )
        self.layout.add_widget(self.error_label)

        self.forgot_password_label = LinkLabel(
            text="I forgot my password",
            size_hint=(0.8, 0.05),
            pos_hint={'center_x': 0.5, 'center_y': 0.15},
            color=(1, 1, 1, 1)
        )
        self.layout.add_widget(self.forgot_password_label)
        self.forgot_password_label.bind(on_release=self.on_forgot_password)

        self.error_label = Label(
            text="",
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            color=(1, 0, 0, 1)  
        )
        self.layout.add_widget(self.error_label)

    def validate_user(self, instance):
        for user in self.db:
            if self.username.text == user.username and self.password.text == user.password:
                self.show_main_application()
                return
        self.error_label.text = "Invalid username or password."

    def show_main_application(self):
        self.layout.clear_widgets()

        label = Label(text="Welcome to the main application!", size_hint=(None, None),
                      pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.layout.add_widget(label)

    def on_forgot_password(self, instance):
        self.clear_widgets()
        self.show_reset_password_screen()

    def show_reset_password_screen(self):
        self.email_input = TextInput(
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            hint_text='Email'
        )
        self.layout.add_widget(self.email_input)

        self.send_reset_button = Button(
            text="Send reset link",
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )
        self.layout.add_widget(self.send_reset_button)

        self.back_to_login_button = Button(
            text="Back to Login",
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.3}
        )
        self.back_to_login_button.bind(on_press=self.clear_and_show_login)
        self.layout.add_widget(self.back_to_login_button)

    def clear_and_show_login(self, instance):
        self.clear_widgets()
        self.show_login_screen()

    def clear_widgets(self):
        self.layout.clear_widgets()
    def readUserDatabase(self):
        with open(self.fname, 'r') as f:
            for line in f:
                username, password, email, phoneNumber, cardsF = line.rstrip().split('/')
                cardsF = cardsF.split(';')
                cards = list()
                for i in cardsF:
                    ID, balance, currencyCode = i.split(':')
                    cards.append(Card(ID, balance, currencyCode))
                self.db.append(User(username, password, email, phoneNumber, cards))


if __name__ == '__main__':
    Aplicacao().run()
