from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import RoundedRectangle
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from pathlib import Path
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import RenderContext
import datetime
import random
import bcrypt

import singlestoredb as s2

# Conectar à base de dados SingleStore
conn = s2.connect(host='svc-3482219c-a389-4079-b18b-d50662524e8a-shared-dml.aws-virginia-6.svc.singlestore.com', port='3333', user='shiftwallet', password='1SuhdjXZxoByHWLWsWQk7bXyXSgMO4xS', database='database_e8ebb')

DIRPATH = Path(__file__).parent
LOGO = DIRPATH.joinpath("logo.png")

DIRPATH_2 = Path(__file__).parent
WALLET = DIRPATH_2.joinpath("wallet.png")

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.bind(size=self.update_canvas)
        self.bind(pos=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.0, 0.0745, 0.1725, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[20,])

class User:
    def __init__(self,userID, username, password, email, phoneNumber, card):
        self.id = userID
        self.username = username
        self.password = password
        self.email = email
        self.phoneNumber = phoneNumber
        self.card = card

class Card:
    def __init__(self, ID,cardNum,userID,cvv,expirationDATE, balance):
        self.id = ID
        self.num = cardNum
        self.userID = userID
        self.cvv = cvv
        self.expirationDate = expirationDATE
        self.balance = balance

class LinkLabel(ButtonBehavior, Label):
    pass

class Aplicacao(App):
    def build(self):        
        Window.size = (350, 600)
        self.layout = FloatLayout(size=(350, 600))

        with self.layout.canvas.before:
            Color(0.2745, 0.5294, 0.5451, 1) # Cor de fundo #415F61
            self.rect = Rectangle(size=Window.size, pos=self.layout.pos)

        self.logo = Image(source=str(LOGO), size_hint=(None, None), size=(200, 200))
        self.logo.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.layout.add_widget(self.logo)

        Clock.schedule_once(self.initiate_fade_out, 2)
        return self.layout

    def initiate_fade_out(self, *args):
        animation = Animation(opacity=0, duration=2)
        animation.bind(on_complete=self.on_fade_out_complete)
        animation.start(self.logo)

    def on_fade_out_complete(self, animation, widget):
        self.layout.remove_widget(self.logo)
        self.show_login_screen()

    def show_login_screen(self):
        self.logo = Image(source=str(LOGO), size_hint=(None, None), size=(200, 200))
        self.logo.pos_hint = {'center_x': 0.5, 'center_y': 0.80}
        self.layout.add_widget(self.logo)

        self.username = TextInput(
            size_hint=(0.8, 0.08),
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            hint_text='Username',
            font_size = 40
        )
        self.layout.add_widget(self.username)

        self.password = TextInput(
            password=True,
            size_hint=(0.8, 0.08),
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
            hint_text='Password',
            font_size = 40
        )
        self.layout.add_widget(self.password)

        self.login_button = RoundedButton(
            text="Login",
            size_hint=(0.8, 0.08),
            pos_hint={'center_x': 0.5, 'center_y': 0.33}
        )
        self.create_account_button = RoundedButton(
            text="Create an acount",
            size_hint=(0.8, 0.08),
            pos_hint={'center_x': 0.5, 'center_y': 0.24}
        )
        self.login_button.bind(on_press=self.validate_user)
        self.layout.add_widget(self.login_button)

        self.create_account_button.bind(on_press=self.create_user)
        self.layout.add_widget(self.create_account_button)
        
        self.forgot_password_label = LinkLabel(
            text="I forgot my password",
            size_hint=(0.8, 0.05),
            pos_hint={'center_x': 0.5, 'center_y': 0.15},
            color=(1,1,1,1)
        )
        self.layout.add_widget(self.forgot_password_label)
        self.forgot_password_label.bind(on_release=self.on_forgot_password)

        self.error_label = Label(
            text="",
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.18},
            color=(1, 0, 0, 1)
        )
        self.layout.add_widget(self.error_label)

    def validate_user(self, instance):
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM Users')
            for row in cur.fetchall():
                if self.username.text == row[1] and bcrypt.checkpw(self.password.text.encode('utf-8'), row[3].encode('utf-8')):
                    self.error_label.text = "Login successful!"
                    card = self.getCard(row[0])
                    if not card:
                        self.error_label.text = "Error finding card."
                        return
                    self.user = User(row[0],self.username.text,self.password.text,row[2],row[4],card)
                    self.show_main_screen()
                    return
                
        self.error_label.text = "Invalid username or password."
        
    def getCard(self,userID):
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM Cards')
            for row in cur.fetchall():
                if userID == row[2]:
                    return Card(row[0],row[1],row[2],row[3],row[4],row[5])
        return None
        
    def create_user(self, instance):
        self.clear_widgets()
        self.logo = Image(source=str(LOGO), size_hint=(None, None), size=(200, 200))
        self.logo.pos_hint = {'center_x': 0.5, 'center_y': 0.85}
        self.layout.add_widget(self.logo)

        self.username = TextInput(size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.65}, hint_text='Username',font_size=40)
        self.layout.add_widget(self.username)

        self.email = TextInput(size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.55}, hint_text='Email',font_size=40)
        self.layout.add_widget(self.email)

        self.phonenumber = TextInput(size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.45}, hint_text='PhoneNumber',font_size=40)
        self.layout.add_widget(self.phonenumber)

        self.password = TextInput(password=True, size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.35}, hint_text='Password',font_size=40)
        self.layout.add_widget(self.password)
        
        self.repeat = TextInput(size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.25}, hint_text='Confirm Password',font_size=40)
        self.layout.add_widget(self.repeat)
        
        self.create_button = RoundedButton(text="Create", size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.15})
        self.create_button.bind(on_press=self.check_passwords)
        self.layout.add_widget(self.create_button)

        self.back_to_login_button = RoundedButton(text="Back to Login", size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.05})
        self.back_to_login_button.bind(on_press=self.clear_and_show_login)
        self.layout.add_widget(self.back_to_login_button)
        
    def check_passwords(self,repeat):
        pass
        
    def show_reset_password_screen(self):
        self.logo = Image(source=str(LOGO), size_hint=(None, None), size=(200, 200))
        self.logo.pos_hint = {'center_x': 0.5, 'center_y': 0.80}
        self.layout.add_widget(self.logo)
        self.email_input = TextInput(
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            hint_text='Email'
        )
        self.layout.add_widget(self.email_input)

        self.send_reset_button = RoundedButton(
            text="Send reset link",
            size_hint=(0.8, 0.08),
            pos_hint={'center_x': 0.5, 'center_y': 0.37}
        )
        self.layout.add_widget(self.send_reset_button)

        self.back_to_login_button = RoundedButton(
            text="Back to Login",
            size_hint=(0.8, 0.08),
            pos_hint={'center_x': 0.5, 'center_y': 0.27}
        )
        self.back_to_login_button.bind(on_press=self.clear_and_show_login)
        self.layout.add_widget(self.back_to_login_button)
        
    def show_main_screen(self):
        self.clear_widgets()  # Clear existing widgets from the layout
        
        name_label = Label(
            text=self.username.text,
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'center_x': 0.22, 'center_y': 0.97},
            color=(0, 0, 0, 1),
            font_size='20sp',
            bold=True,
            font_name='Roboto'
        )
        self.layout.add_widget(name_label)
        
        self.wallet = Image(source=str(WALLET), size_hint=(None, None), size=(200, 200))
        self.wallet.pos_hint = {'center_x': 0.5, 'center_y': 0.80}
        self.layout.add_widget(self.wallet)

        balance_label = Label(
            text=f"{self.user.card.balance}€",
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            color=(0, 0, 0, 1),
            font_size='80sp',
            bold=True,
            font_name='Roboto'
        )
        self.layout.add_widget(balance_label)

        # FEATURES
        # COFRE, LEVANTAR, DEPOSITAR, TRANSFERIR, INVESTIMENTOS
        
        self.transfer_button = RoundedButton(
            text="TRANSFER",
            size_hint=(0.7, 0.08),
            pos_hint={'center_x': 0.55, 'center_y': 0.50}
        )
        self.layout.add_widget(self.transfer_button)
        
        self.deposit_button = RoundedButton(
            text="DEPOSIT",
            size_hint=(0.7, 0.08),
            pos_hint={'center_x': 0.55, 'center_y': 0.40}
        )
        self.layout.add_widget(self.deposit_button)
        
        self.withdraw_button = RoundedButton(
            text="WITHDRAW",
            size_hint=(0.7, 0.08),
            pos_hint={'center_x': 0.55, 'center_y': 0.30}
        )
        self.layout.add_widget(self.withdraw_button)
        
        self.safe_button = RoundedButton(
            text="SAFE",
            size_hint=(0.7, 0.08),
            pos_hint={'center_x': 0.55, 'center_y': 0.20}
        )
        self.layout.add_widget(self.safe_button)

        # Add a button to log out and return to the login screen
        logout_button = RoundedButton(
            text="Log Out",
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.1}
        )
        logout_button.bind(on_press=self.clear_and_show_login)
        self.layout.add_widget(logout_button)

    def clear_and_show_login(self, instance):
        self.clear_widgets()
        self.show_login_screen()

    def on_forgot_password(self, instance):
        self.clear_widgets()
        self.show_reset_password_screen()

    def clear_widgets(self):
        self.layout.clear_widgets()

    # Você precisará implementar esta função para enviar o email
    # def send_reset_link(self, instance):
    #     email = self.email_input.text
    #     # Adicione a lógica para enviar o email de redefinição de senha
    
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
message.txt
13 KB