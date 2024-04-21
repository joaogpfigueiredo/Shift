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

conn = s2.connect(host='svc-3482219c-a389-4079-b18b-d50662524e8a-shared-dml.aws-virginia-6.svc.singlestore.com', port='3333', user='shiftwallet', password='1SuhdjXZxoByHWLWsWQk7bXyXSgMO4xS', database='database_e8ebb')

DIRPATH = Path(__file__).parent
LOGO = DIRPATH.joinpath("logo.png")

DIRPATH_2 = Path(__file__).parent
WALLET = DIRPATH_2.joinpath("wallet.png")

DIRPATH_3 = Path(__file__).parent
SAFE = DIRPATH_3.joinpath("safe.png")

class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source_normal = kwargs.get('source')
        self.source_down = kwargs.get('source_down', self.source_normal)

    def on_state(self, widget, value):
        if value == 'down':
            self.source = self.source_down
        else:
            self.source = self.source_normal

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
            Color(0.2745, 0.5294, 0.5451, 1)
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

        self.create_account_button.bind(on_press=self.create_user_screen)
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
        
    def create_user_screen(self, instance):
        self.clear_widgets()
        self.logo = Image(source=str(LOGO), size_hint=(None, None), size=(200, 200))
        self.logo.pos_hint = {'center_x': 0.5, 'center_y': 0.85}
        self.layout.add_widget(self.logo)

        self.username = TextInput(size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.65}, hint_text='Username',font_size=25)
        self.layout.add_widget(self.username)

        self.email = TextInput(size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.55}, hint_text='Email',font_size=25)
        self.layout.add_widget(self.email)

        self.phonenumber = TextInput(size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.45}, hint_text='PhoneNumber',font_size=25)
        self.layout.add_widget(self.phonenumber)

        self.password = TextInput(password=True, size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.35}, hint_text='Password',font_size=25)
        self.layout.add_widget(self.password)
        
        self.repeat = TextInput(password=True,size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.25}, hint_text='Confirm Password',font_size=25)
        self.layout.add_widget(self.repeat)
        
        self.error_label_create_user = Label(
            text="",
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.18},
            color=(1, 0, 0, 1)
        )
        self.layout.add_widget(self.error_label_create_user)
        
        self.create_button = RoundedButton(text="Create", size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.15})
        self.create_button.bind(on_press=self.create_user)
        self.layout.add_widget(self.create_button)

        self.back_to_login_button = RoundedButton(text="Back to Login", size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.05})
        self.back_to_login_button.bind(on_press=self.clear_and_show_login)
        self.layout.add_widget(self.back_to_login_button)
        
    def create_user(self):
        if not self.check_passwords():
            self.error_label_create_user = "Passwords don't match"
            return
        if not self.checkUsername():
            self.error_label_create_user = "Username already taken"
            return
        with conn.cursor() as cur:
            insert_sql = "INSERT INTO Users (name, email, password, phonenumber) VALUES (%s, %s, %s, %s)"
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cur.execute(insert_sql, (self.username.text, self.email.text, self.password.text, self.phonenumber.text))
            userID = self.getUserID(self.username.text)
            self.createCard(userID)
        self.validate_user()
        
    def getUserID(self,userName):
        with conn.cursor() as cur:
            cur.execute('SELECT id,name FROM Users')
            for row in cur.fetchall():
                if userName == row[1]:
                    return row[0]
        return None
        
    def createCard(self,UserID):

        ID = random.randint(1000000000000000, 9999999999999999)

        while not self.checkCardID(ID):
            ID = random.randint(1000000000000000, 9999999999999999)

        cvv = random.randint(100,999)

        current_datetime = datetime.datetime.now()

        new_year = current_datetime.year + 5

        formatted_datetime = "{}-{:02d}-{:02d}".format(new_year, current_datetime.month, current_datetime.day)
        try:
            with conn.cursor() as cur:
                insert_sql = "INSERT INTO Cards (card_number, user_id, cvv, expire_date) VALUES (%s, %s, %s, %s)"
                cur.execute(insert_sql, (ID, UserID, cvv, formatted_datetime))
                conn.commit() 
        except Exception as e:
            print(f"Failed to Commit: {e}")
            conn.rollback()
            
    def checkCardID(self,ID):
        with conn.cursor() as cur:
            cur.execute('SELECT card_number FROM Cards')
            for number in cur.fetchall():
                if number == ID:
                    return False
        return True
        
    def checkUsername(self):
        with conn.cursor() as cur:
            cur.execute('SELECT name FROM Users')
            for user in cur.fetchall():
                if user == self.username.text:
                    return False
        return True
        
    def check_passwords(self):
        if self.password.text == self.repeat.text:
            return True
        return False
        
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
        self.clear_widgets()
        
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
            text=f"{self.user.card.balance} €",
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            color=(0, 0, 0, 1),
            font_size='80sp',
            bold=True,
            font_name='Roboto'
        )
        self.layout.add_widget(balance_label)

        self.payment_button = RoundedButton(
            text="PAYMENT",
            size_hint=(0.7, 0.08),
            pos_hint={'center_x': 0.55, 'center_y': 0.50}
        )
        self.payment_button.bind(on_press=self.show_payment_screen)
        self.layout.add_widget(self.payment_button)
        
        self.transfer_button = RoundedButton(
            text="TRANSFER",
            size_hint=(0.7, 0.08),
            pos_hint={'center_x': 0.55, 'center_y': 0.40}
        )
        self.transfer_button.bind(on_press=self.show_transfer_screen)
        self.layout.add_widget(self.transfer_button)
        
        self.deposit_button = RoundedButton(
            text="DEPOSIT",
            size_hint=(0.7, 0.08),
            pos_hint={'center_x': 0.55, 'center_y': 0.30}
        )
        self.deposit_button.bind(on_press=self.show_deposit_screen)
        self.layout.add_widget(self.deposit_button)
        
        self.withdraw_button = RoundedButton(
            text="WITHDRAW",
            size_hint=(0.7, 0.08),
            pos_hint={'center_x': 0.55, 'center_y': 0.20}
        )
        self.withdraw_button.bind(on_press=self.show_withdraw_screen)
        self.layout.add_widget(self.withdraw_button)
        
        self.safe_button = ImageButton(
            source=str(SAFE),
            size_hint=(None, None),
            size=(140, 70),
            pos_hint={'center_x': 0.92, 'center_y': 0.95}
        )
        self.safe_button.bind(on_press=self.show_safe_screen)
        self.layout.add_widget(self.safe_button)

        logout_button = RoundedButton(
            text="Log Out",
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.1}
        )
        logout_button.bind(on_press=self.clear_and_show_login)
        self.layout.add_widget(logout_button)
        
    def show_payment_screen(self,intance):
        self.clear_widgets()
        
        back_button = RoundedButton(
            text="Back",
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        back_button.bind(on_press=self.clear_and_show_menu)
        self.layout.add_widget(back_button)
        
    def show_deposit_screen(self, instance):
        self.clear_widgets()

        self.amount_input =  TextInput(size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.65},
                                  hint_text='Amount', font_size=40)
        self.layout.add_widget(self.amount_input)
        deposit_button = RoundedButton(
            text="Deposit",
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        deposit_button.bind(on_press=self.deposit_and_back_menu)
        self.layout.add_widget(deposit_button)

        back_button = RoundedButton(
            text="Back",
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        back_button.bind(on_press=self.clear_and_show_menu)
        self.layout.add_widget(back_button)

    def deposit_and_back_menu(self, instance):
        self.clear_widgets()
        try:
            amount = float(self.amount_input.text.replace(",", "."))
        except ValueError:
            print("Por favor, insira um valor numÃ©rico.")
            return

        try:
            with conn.cursor() as cur:
                update_sql = "UPDATE Cards SET balance = balance + %s WHERE id = %s"
                cur.execute(update_sql, (amount, self.user.card.id))
                conn.commit()
                self.user.card.balance += amount
                self.amount_input.text = ''
                self.show_main_screen()
        except Exception as e:
            print(f"Erro ao atualizar o banco de dados: {e}")

    def show_withdraw_screen(self, instance):
        self.clear_widgets()

        self.amount_input =  TextInput(size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.65},
                                  hint_text='Amount', font_size=40)
        self.layout.add_widget(self.amount_input)

        withdraw_button = RoundedButton(
            text="Withdraw",
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        withdraw_button.bind(on_press=self.withdraw_and_back_menu)
        self.layout.add_widget(withdraw_button)

        back_button = RoundedButton(
            text="Back",
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        back_button.bind(on_press=self.clear_and_show_menu)
        self.layout.add_widget(back_button)

    def withdraw_and_back_menu(self, instance):
        self.clear_widgets()
        try:
            amount = float(self.amount_input.text.replace(",", "."))
            if amount > self.user.card.balance:
                print("Saldo insuficiente.")
                self.clear_widgets()
                self.show_withdraw_screen(instance)
        except ValueError:
            print("Por favor, insira um valor numÃ©rico.")
            self.clear_widgets()
            self.show_withdraw_screen(instance)

        try:
            with conn.cursor() as cur:
                update_sql = "UPDATE Cards SET balance = balance - %s WHERE id = %s"
                cur.execute(update_sql, (amount, self.user.card.id))
                conn.commit()
                self.user.card.balance -= amount  
                self.amount_input.text = ''
                self.show_main_screen()
        except Exception as e:
            print(f"Erro ao atualizar o banco de dados: {e}")
            
    def show_transfer_screen(self, instance):
        self.clear_widgets()

        self.amount_input =  TextInput(size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.65},
                                  hint_text='Amount', font_size=40)
        self.layout.add_widget(self.amount_input)
        self.send_transfer_button = RoundedButton(
            text="Send Transfer",
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        back_button = RoundedButton(
            text="Back",
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        back_button.bind(on_press=self.clear_and_show_menu)
        self.layout.add_widget(back_button)
        
    def show_safe_screen(self,instance):
        self.clear_widgets()
        
        back_button = RoundedButton(
            text="Back",
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        back_button.bind(on_press=self.clear_and_show_menu)
        self.layout.add_widget(back_button)

    def clear_and_show_login(self, instance):
        self.clear_widgets()
        self.show_login_screen()
        
    def clear_and_show_menu(self,instance):
        self.clear_widgets()
        self.show_main_screen()

    def on_forgot_password(self, instance):
        self.clear_widgets()
        self.show_reset_password_screen()

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