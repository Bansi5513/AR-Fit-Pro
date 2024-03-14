from flet import *
import flet as ft

class Home(UserControl):
  def __init__(self,page):
    super().__init__()
    self.page = page

  def build(self):
    self.page.scroll = "adaptive"

    # heading for the exercises
    exercises_heading = ft.Container(
        content=ft.Text("Exercise", size=24, weight=ft.FontWeight.BOLD),
        margin=ft.margin.only(bottom=20,left=15)
    )

    # Create cards for each exercise
    exercise_cards = [

        ft.Row([
            # exercise 1 - Standing Bicep Curl
            ft.Card(
                ft.Container(
                    content=ft.Column([
                        ft.Image(
                            src="exercise1.jpg",
                            width=250,
                            height=250,
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        ft.Container(
                            content=ft.Text("Standing Bicep Curl", size=16, weight=ft.FontWeight.BOLD),
                            alignment=ft.alignment.center,
                        )
                    ]),
                    padding=ft.padding.all(25),
                    alignment = ft.alignment.center,
                    on_click= lambda _: self.page.go('/bicep-curl/information'),
                    width = 300,
                ), 
                margin=ft.margin.all(10),
                elevation=5
            ),
            
            # exercise 2 - Air Squat
            ft.Card(
                ft.Container(
                    content=ft.Column([
                        ft.Image(
                            src="exercise2.jpg",
                            width=250,
                            height=250,
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        ft.Container(
                            content=ft.Text("Air Squat", size=16, weight=ft.FontWeight.BOLD),
                            alignment=ft.alignment.center,
                        )
                    ]),
                    padding=ft.padding.all(25),
                    alignment = ft.alignment.center,
                    on_click= lambda _: self.page.go('/squat/information'),
                    width = 300,
                ),
                margin=ft.margin.all(10),
                elevation=5
            )
            # Add more cards for other exercises as needed
        ]),
            
    ]

    # Add exercises heading and cards to the page
    return ft.Container(
        margin=ft.margin.only(top=10),
        content=ft.Column([
            exercises_heading,
            *exercise_cards,  # Unpack list of exercise cards
        ], alignment="center")
    )