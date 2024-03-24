from flet import *
import flet as ft
from flet import TextField, ElevatedButton
import re
import pymongo
import hashlib


class SignUp(UserControl):
  def __init__(self,page):
    super().__init__()
    self.page = page
    self.text_username: TextField = TextField(label="Full Name", text_align=ft.TextAlign.LEFT,width=300, on_change=self.validate)
    self.text_email: TextField = TextField(label="Email", text_align=ft.TextAlign.LEFT,width=300, on_change=self.validate)
    self.text_password: TextField = TextField(label="Password", text_align=ft.TextAlign.LEFT,width=300, password=True, can_reveal_password=True, on_change=self.validate)
    self.text_confirm_password: TextField = TextField(label="Confirm Password", text_align=ft.TextAlign.LEFT,width=300, password=True, can_reveal_password=True, on_change=self.validate)

    self.button: ElevatedButton = ElevatedButton(text="Sign Up",width=150,disabled=False,on_click= lambda _: self.page.go('/home'))
    self.warning = ""
    self.warning_text = ft.Text(value="", size=18, weight=ft.FontWeight.BOLD)
  
  def validate(self,e):
    print("Changed")
    if self.text_email.value and not re.match(r"[^@]+@[^@]+\.[^@]+", self.text_email.value):
        self.warning = "Invalid email format"
        self.update_warning_text()
    elif self.text_password.value and len(self.text_password.value) < 6:
        self.warning = "Password must be at least 6 characters"
        self.update_warning_text()
    elif self.text_confirm_password.value and len(self.text_confirm_password.value) < 6:
        self.warning = "Confirm Password must be at least 6 characters"
        self.update_warning_text()
    elif self.text_password.value and self.text_confirm_password.value and self.text_password.value != self.text_confirm_password.value:
        self.warning = "Passwords do not match"
        self.update_warning_text()
    else:
        if all([self.text_username.value, self.text_email.value, self.text_password.value, self.text_confirm_password.value]):
            self.warning = ""
            self.update_warning_text()
        else:
            self.warning = "Please fill in all fields"
            self.update_warning_text()
    
    self.page.update()
    
  def update_warning_text(self):
    self.warning_text.value = f"Warning: {self.warning}"
    self.page.update() 

  def build(self):
    self.page.scroll = "adaptive"


    signup_content = ft.Container(
        ft.Card(
            ft.Row(
            controls=[
                ft.Container(
                    ft.Column([
                        ft.Container(
                            ft.Text(value="SIGN UP", size=26, weight=ft.FontWeight.BOLD,),
                            margin=ft.margin.only(bottom=30),
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
                            width=600,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            self.warning_text,
                            ft.Text(value=self.warning),
                            margin=ft.margin.only(bottom=10, left=150),
                            width=600,
                            # alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            self.button,
                            margin=ft.margin.only(bottom=15),
                            width=600,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            ft.Row([
                                ft.Text(value="Already have an account?", scale=0.9 ,width=200),
                                ft.TextButton(text="Login", scale=0.9 ,width=100, on_click=lambda e: print("Login")),
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
          