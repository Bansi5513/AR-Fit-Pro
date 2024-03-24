import flet as ft
from flet import *
from flet import TextField, OutlinedButton
import re
import pymongo
import hashlib

myclient = pymongo.MongoClient('mongodb://localhost:27017')
mydb = myclient["ExerciseTracking"]
mycol = mydb["User"]

class Login(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        
        self.text_email:  TextField = TextField(label="Email", text_align=ft.TextAlign.LEFT,width=300, keyboard_type=ft.KeyboardType.EMAIL,
            input_filter=ft.InputFilter(
                allow=True,
                regex_string=r'[A-Za-z0-9@.]',
                replacement_string="",
            ),
            on_change=self.validate)
        self.text_password: TextField = TextField(label="Password", text_align=ft.TextAlign.LEFT,width=300, password=True, can_reveal_password=True, on_change=self.validate)
        
        self.button: OutlinedButton = OutlinedButton(text="Login",width=150,disabled=True, on_click=self.submit)


    def validate(self, e):
        error = False
            
        # Validate email format
        if self.text_email.value and not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{1,7}\b', self.text_email.value):
            error = True
            self.button.disabled = True
            self.text_email.error_text = "Invalid email format"
        else:
            error = False
            self.text_email.error_text = ""


        # Enable submit button if all fields are valid
        if not all([self.text_email.value, self.text_password.value]):
            # print("Please fill in all fields")
           self.button.disabled = True
           error = True
        else:
            if error == False:
                self.button.disabled = False

        self.update()

    def submit(self,e):
        user_data = mycol.find_one({"Email": self.text_email.value})
        if user_data:
            user_password = user_data.get("Password")
            if user_password != hashlib.sha256(self.text_password.value.encode()).hexdigest():
                self.text_password.error_text = "Invalid password."
            else:
                print("Login successful")
                self.page.go('/home')
        else:
            self.text_email.error_text = "Invalid email."

        self.update()

    def build(self):

        login_content = ft.Container(
            ft.Card(
                ft.Row(
                controls=[
                    ft.Container(
                        ft.Column([
                            ft.Container(
                            ft.Text(value="LOGIN", size=26, weight=ft.FontWeight.BOLD,),
                            margin=ft.margin.only(bottom=25),
                            width=600,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            self.text_email,
                            margin=ft.margin.only(bottom=10),
                            width=600,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            self.text_password,
                            margin=ft.margin.only(bottom=15),
                            width=600,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            self.button,
                            margin=ft.margin.only(bottom=140),
                            width=600,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            ft.Row([
                                ft.Text(value="Create an account?", scale=0.9 ,width=160),
                                ft.TextButton(text="Sign Up", scale=0.9 ,width=100, on_click=lambda e: self.page.go('/')),
                            ],),
                            width=600,
                            margin=ft.margin.only(left=170),
                            # alignment=ft.alignment.center,
                        )
                        
                        ]),
                    margin=ft.margin.only(top=40),
                    alignment=ft.alignment.center,
                    ),
                ]),
                width = 600,
                height = 600,    
            ),
            alignment = ft.alignment.center,
            margin=ft.margin.only(top=90),
        )
           
    
        return login_content
