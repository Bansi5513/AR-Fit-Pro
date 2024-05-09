import flet as ft
from flet import *
from flet import TextField, OutlinedButton
import re
import hashlib
from datetime import datetime


current_date = datetime.now().strftime("%d-%m-%Y")

class SignUp(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        
        self.text_username: TextField = TextField(label="Name", text_align=ft.TextAlign.LEFT,width=300, on_change=self.validate)
        self.text_email:  TextField = TextField(label="Email", text_align=ft.TextAlign.LEFT,width=300, keyboard_type=ft.KeyboardType.EMAIL,
            input_filter=ft.InputFilter(
                allow=True,
                regex_string=r'[A-Za-z0-9@.]',
                replacement_string="",
            ),
            on_change=self.validate)
        self.text_password: TextField = TextField(label="Password", text_align=ft.TextAlign.LEFT,width=300, password=True, can_reveal_password=True, on_change=self.validate)
        self.text_confirm_password: TextField = TextField(label="Confirm Password", text_align=ft.TextAlign.LEFT,width=300, password=True, can_reveal_password=True, on_change=self.validate)

        self.submit_button: OutlinedButton = OutlinedButton(text="Sign Up",width=150,disabled=True,on_click= self.submit )

        

    def validate(self, e):
        error = False

        # Validate name is not empty
        if not self.text_username.value:
            error = True
            self.submit_button.disabled = True
            self.text_username.error_text = "Name cannot be empty"
        else:
            error = False
            self.text_username.error_text = ""
            
        # Validate email format
        if self.text_email.value and not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{1,7}\b', self.text_email.value):
            error = True
            self.submit_button.disabled = True
            self.text_email.error_text = "Invalid email format"
        else:
            error = False
            self.text_email.error_text = ""
            

        # Validate password format
        if self.text_password.value and len(self.text_password.value) < 6:
            error = True
            self.submit_button.disabled = True
            self.text_password.error_text = "Password must be at least 6 characters"
        else:
            error = False
            self.text_password.error_text = ""
        
        # Validate confirm password format
        if self.text_confirm_password.value and len(self.text_confirm_password.value) < 6:
            error = True
            self.submit_button.disabled = True
            self.text_confirm_password.error_text = "Password must be at least 6 characters"
        elif self.text_confirm_password.value and self.text_confirm_password.value != self.text_password.value:
            error = True
            self.submit_button.disabled = True
            self.text_confirm_password.error_text = "Passwords do not match"
        else:
            error = False
            self.text_confirm_password.error_text = ""


        # Enable submit button if all fields are valid
        if not all([self.text_username.value, self.text_email.value, self.text_password.value, self.text_confirm_password.value]):
            # print("Please fill in all fields")
           self.submit_button.disabled = True
           error = True
        else:
            if error == False:
                self.submit_button.disabled = False

        self.update()


    def submit(self,e):
        hashed_password = hashlib.sha256(self.text_password.value.encode()).hexdigest()

        print("Name:", self.text_username.value)
        print("Email:", self.text_email.value)

        # message passing
        self.page.session.set("key", self.text_email.value)

        value = self.page.session.get("key")
        print(value)
        print("Hashed Password:", hashed_password)
        data_1 = {
                "Name": self.text_username.value,
                "Email": self.text_email.value,
                "Password": hashed_password,
                "Date": current_date,
                # Add other data fields as needed
        }

        self.page.session.set("data_1", data_1)
        # mycol.insert_one(data)
        self.page.go('/screen1')

    def build(self):

        signup_content = ft.Container(
            ft.Card(
                ft.Row(
                controls=[
                    ft.Container(
                        ft.Column([
                            ft.Container(
                                ft.Text(value="SIGN UP", size=26, weight=ft.FontWeight.BOLD,),
                                margin=ft.margin.only(bottom=25),
                                width=600,
                                alignment=ft.alignment.center,
                            ),
                            ft.Container(
                                self.text_username,
                                margin=ft.margin.only(bottom=10),
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
                                margin=ft.margin.only(bottom=10),
                                width=600,
                                alignment=ft.alignment.center,
                            ),
                            ft.Container(
                                self.text_confirm_password,
                                margin=ft.margin.only(bottom=15),
                                width=600,
                                alignment=ft.alignment.center,
                            ),
                            ft.Container(
                                self.submit_button,
                                margin=ft.margin.only(bottom=30),
                                width=600,
                                alignment=ft.alignment.center,
                            ),
                            ft.Container(
                                ft.Row([
                                    ft.Text(value="Already have an account?", scale=0.9 ,width=200),
                                    ft.TextButton(text="Login", scale=0.9 ,width=100, on_click=lambda e: self.page.go('/login')),
                                ],),
                                width=600,
                                margin=ft.margin.only(left=150),
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
    
        return signup_content
