from flet import *
import flet as ft
import threading

class Congo(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def transition_to_next_page(self):
        self.page.go('/home')

    def build(self):
        self.page.scroll = "adaptive"

        page_content = ft.Container(
            ft.Column([
                ft.Container(
                    ft.Image(src="badge.png",height=300, fit=ft.ImageFit.CONTAIN),
                    alignment = ft.alignment.center,
                ),
                ft.Container(
                    ft.Text("Congratulations, you have completed your Goal for today!", size=20, weight=ft.FontWeight.BOLD),
                    alignment = ft.alignment.center,
                    margin=ft.margin.only(top=10),
                ),
                ft.Audio(
                    src="audio.mp3", autoplay=True
                ),
            ]),
            alignment = ft.alignment.center,
            margin=ft.margin.only(top=150),
        )
        

        delay_seconds = 3
        threading.Timer(delay_seconds, self.transition_to_next_page).start()

        # Add navigation bar, and other page content here
        return ft.Container(
            content=ft.Column([
            page_content,
            ], alignment="center")
        )
        