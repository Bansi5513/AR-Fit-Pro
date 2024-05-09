from flet import *
import flet as ft
import pymongo
from datetime import datetime


current_date = datetime.now().strftime("%Y-%m-%d")
myclient = pymongo.MongoClient('mongodb://localhost:27017')

mydb = myclient["ExerciseTracking"]
mycol = mydb["Exercise"]

class Training(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def check_bicep(self, e):
        count = self.page.session.get("bicep_curl")

        email = self.page.session.get("email")

        query = {
            "Email": email,
            "Exercise_Name": "Bicep Curl",
            "Date": current_date
        }

        projection = {
            "_id": 0,  # Exclude the document ID from the result
            "Correct_Reps": 1  # Include only the Correct_Reps field
        }
        
        # Find documents matching the query with the specified projection
        result = mycol.find_one(query, projection)
        
        # Now 'result' contains the document with the Correct_Reps value for the Bicep Curl exercise for the user on the current date
        if result:
            correct_reps = result.get("Correct_Reps")
            if correct_reps == count:
                print("Disabled")
                # color change on click

            elif correct_reps < count:
                bicep_curl = count-correct_reps
                self.page.session.set("bicep_curl",bicep_curl)
                self.page.go('/bicep-curl/information')
        else:
            self.page.go('/bicep-curl/information')

        self.update()
    
    def check_squat(self, e):
        count = self.page.session.get("squat")

        email = self.page.session.get("email")

        query = {
            "Email": email,
            "Exercise_Name": "Squat",
            "Date": current_date
        }

        projection = {
            "_id": 0,  # Exclude the document ID from the result
            "Correct_Reps": 1  # Include only the Correct_Reps field
        }
        
        # Find documents matching the query with the specified projection
        result = mycol.find_one(query, projection)
        
        # Now 'result' contains the document with the Correct_Reps value for the Bicep Curl exercise for the user on the current date
        if result:
            correct_reps = result.get("Correct_Reps")
            if correct_reps == count:
                print("Disabled")
                # color change on click
                
            elif correct_reps < count:
                squat = count-correct_reps
                self.page.session.set("squat",squat)
                self.page.go('/squat/information')
        else:
            self.page.go('/squat/information')

        self.update()

    def build(self):
        self.page.scroll = "adaptive"

        # Navigation bar with icons and onclick actions
        navigation_bar = ft.Row(
            controls=[
                ft.Image(src="logo1.png", width=100, height=100, fit=ft.ImageFit.CONTAIN), # Logo on the top left
                ft.Container(width=940), # Container acting as a spacer to push the navigation items to the right
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.icons.HOME_ROUNDED, # Using built-in icon
                                icon_color="white",
                                on_click=lambda _: self.page.go('/home')
                            ),
                            padding=ft.padding.all(30) # Add padding around the icon button
                        ),
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.icons.DIRECTIONS_RUN_ROUNDED, # Replace with actual icon name for training
                                icon_color="white",
                                on_click=lambda _: self.page.go('/training')
                            ),
                            padding=ft.padding.all(30) # Add padding around the icon button
                        ),
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.icons.AUTO_GRAPH_ROUNDED, # Replace with actual icon name for progress
                                icon_color="white",
                                on_click=lambda _: self.page.go('/progress')
                            ),
                            padding=ft.padding.all(30) # Add padding around the icon button
                        ),
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.icons.ACCOUNT_CIRCLE_SHARP, # Replace with actual icon name for profile
                                icon_color="white",
                                on_click=lambda _: self.page.go('/profile')
                            ),
                            padding=ft.padding.all(30) # Add padding around the icon button
                        ),
                    ],
                    alignment=ft.alignment.center
                )
            ],
            alignment=ft.alignment.center
        )

        # Training Page Content
        exercises_heading = ft.Container(
            content=ft.Text("Exercise", size=24, weight=ft.FontWeight.BOLD),
            margin=ft.margin.only(top=20, bottom=20, left=15)
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
                        alignment=ft.alignment.center,
                        on_click=lambda e: self.check_bicep(e),
                        # on_click=lambda _: self.page.go('/bicep-curl/information'),
                        width=300,
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
                        alignment=ft.alignment.center,
                        on_click=lambda e: self.check_squat(e),
                        width=300,
                    ),
                    margin=ft.margin.all(10),
                    elevation=5
                )
                # Add more cards for other exercises as needed
            ]),
        ]

        # Add navigation bar, exercises heading, and cards to the page
        return ft.Container(
            margin=ft.margin.only(left=10, top=0),
            content=ft.Column([
                navigation_bar,
                exercises_heading,
                *exercise_cards, # Unpack list of exercise cards
            ], alignment="center")
        )
