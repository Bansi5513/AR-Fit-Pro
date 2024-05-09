from flet import *
import flet as ft
import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017')

mydb = myclient["ExerciseTracking"]
mycol = mydb["User"]

class Workout_Screen1(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.build()

    def preference(self, e):
        self.option1.style.bgcolor = ft.colors.WHITE
        self.option2.style.bgcolor = ft.colors.WHITE
        self.option3.style.bgcolor = ft.colors.WHITE
        self.option4.style.bgcolor = ft.colors.WHITE
        
        # Change the clicked button's color to green
        e.control.style.bgcolor = ft.colors.BLUE_200

        # Update the UI to reflect the changes
        self.update() 

    def on_triangle_click(self):

        preference_choice = None
        if self.option1.style.bgcolor == ft.colors.BLUE_200:
            preference_choice = "Little or No Activity"
        elif self.option2.style.bgcolor == ft.colors.BLUE_200:
            preference_choice = "Lightly Active"
        elif self.option3.style.bgcolor == ft.colors.BLUE_200:
            preference_choice = "Moderately Active"
        elif self.option4.style.bgcolor == ft.colors.BLUE_200:
            preference_choice = "Very Active"

        data_1 = self.page.session.get("data_1")
        data_2 = self.page.session.get("data_2")
        data_3 = {
            "BMI Score": self.bmi,        
            "Classification": self.classification,               
            "Goal": self.weight_range, 
            "Active": preference_choice, 
        }

        self.page.session.set("data_3", data_3)

        # Merge data into a single dictionary
        merged_data = {}
        merged_data.update(data_1)
        merged_data.update(data_2)
        merged_data.update(data_3)

        # Insert merged data into MongoDB
        self.page.session.set("data", merged_data)
        
        mycol.insert_one(merged_data)

        self.page.go('/home')

        

    def build(self):
        # Define a function to handle tab clicks
        def on_tab_click(tab_name):
            print(f"{tab_name} clicked")
        
        # Create custom tabs
        tabs = ft.Container(
            content=Row([
                ft.Container(
                    content=ft.TextButton("", on_click=lambda e: on_tab_click("Tab 1")),
                    width=100, # Adjust the width as needed
                    height=2, # Adjust the height as needed
                    bgcolor="white", # Corrected property name
                    border_radius=ft.border_radius.all(5)
                ),
                ft.Container(
                    content=ft.TextButton("", on_click=lambda e: on_tab_click("Tab 2")),
                    width=100, # Adjust the width as needed
                    height=2, # Adjust the height as needed
                    bgcolor="blue", # Corrected property name
                    border_radius=ft.border_radius.all(5)                
                ),
                # ft.Container(
                #     content=ft.TextButton("", on_click=lambda e: on_tab_click("Tab 3")),
                #     width=100, # Adjust the width as needed
                #     height=2, # Adjust the height as needed
                #     bgcolor="white", # Corrected property name
                #     border_radius=ft.border_radius.all(5)                
                # )
            ],alignment="center"),
            margin=ft.margin.only(top=10),
        )
        
        user_data = self.page.session.get("user_data")

        if user_data:
            height = float(user_data.get("height", 0))  # Default to 0 if height is not available
            weight = float(user_data.get("weight", 0))  # Default to 0 if weight is not available
            height_unit = user_data.get("height_unit")
            weight_unit = user_data.get("weight_unit")

            # Convert height to centimeters if it's in feet and inches
            if height_unit == "ft/in":
                feet = int(height)
                inches = (height - feet) * 12  # Convert remaining decimal to inches
                height = (feet * 30.48) + (inches * 2.54)  # Convert feet to cm and inches to cm
            # Convert feet and inches to meters

            # Convert weight to kilograms if it's in pounds
            if weight_unit == "lbs":
                weight *= 0.453592  # Convert pounds to kilograms

            if height > 0 and weight > 0:
                self.bmi = round((weight / (height * height)) * 10000, 2)

                if self.bmi < 16:
                    self.classification = "Severe Thinness"
                elif 16 <= self.bmi < 17:
                    self.classification = "Moderate Thinness"
                elif 17 <= self.bmi < 18.5:
                    self.classification = "Mild Thinness"
                elif 18.5 <= self.bmi < 25:
                    self.classification = "Normal"
                elif 25 <= self.bmi < 30:
                    self.classification = "Overweight"
                elif 30 <= self.bmi < 35:
                    self.classification = "Obese Class I"
                elif 35 <= self.bmi < 40:
                    self.classification = "Obese Class II"
                else:
                    self.classification = "Obese Class III"

            else:
                # Handle case where height or weight is missing or invalid
                self.bmi = None
                self.classification = None
        else:
            # Handle case where user data is not available in the session
            self.bmi = None
            self.classification = None

        if self.bmi is not None:
            if self.bmi < 18.5:
                # Underweight
                self.weight_to_gain = (18.5 - self.bmi) * (height * height) / 10000
                self.weight_range = f"GOAL : Gain {self.weight_to_gain:.2f} kg"
            elif self.bmi >= 25:
                # Overweight or Obese
                self.weight_to_lose = (self.bmi - 24.9) * (height * height) / 10000
                self.weight_range = f"GOAL : Lose {self.weight_to_lose:.2f} kg"
            else:
                # Normal BMI
                self.weight_range = "Maintain current weight"
        else:
            # Handle case where BMI is not available
            self.weight_range = "BMI calculation not available"

        self.option1 = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(name=ft.icons.CHAIR, color="black"),
                ft.Text(value="Little or No Activity", size=18),
            ]),
            width=260,
            style=ft.ButtonStyle(
                color={ft.MaterialState.DEFAULT: ft.colors.BLACK},
                bgcolor={ft.MaterialState.DEFAULT: ft.colors.WHITE},
            ),
            on_click=lambda e: self.preference(e)
        )
        self.option2 = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(name=ft.icons.MAN_ROUNDED, color="black"),
                ft.Text(value="Lightly Active", size=18),
            ]),
            width=260,
            style=ft.ButtonStyle(
                color={ft.MaterialState.DEFAULT: ft.colors.BLACK},
                bgcolor={ft.MaterialState.DEFAULT: ft.colors.WHITE},
            ),
            on_click=lambda e: self.preference(e)
        )
        self.option3 = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(name=ft.icons.DIRECTIONS_WALK_ROUNDED, color="black"),
                ft.Text(value="Moderately Active", size=18),
            ]),
            width=260,
            style=ft.ButtonStyle(
                color={ft.MaterialState.DEFAULT: ft.colors.BLACK},
                bgcolor={ft.MaterialState.DEFAULT: ft.colors.WHITE},
            ),
            on_click=lambda e: self.preference(e)
        )
        self.option4 = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(name=ft.icons.SPORTS_HANDBALL_ROUNDED, color="black"),
                ft.Text(value="Very Active", size=18),
            ]),
            width=260,
            style=ft.ButtonStyle(
                color={ft.MaterialState.DEFAULT: ft.colors.BLACK},
                bgcolor={ft.MaterialState.DEFAULT: ft.colors.WHITE},
            ),
            on_click=lambda e: self.preference(e)
        )

        main_page = ft.Container(
            content=ft.Column([
                ft.Container(
                    ft.Text("Workout", size=26, weight=ft.FontWeight.BOLD),
                    margin=ft.margin.only(left=300,top=60,bottom=10),
                ),
                ft.Column([
                    ft.Row([
                        ft.Container(
                            ft.Card(
                                ft.Container(
                                    ft.Column([
                                        ft.Text("BMI Score", size=22, weight=ft.FontWeight.BOLD),
                                        ft.Text(self.bmi, size=18, weight=ft.FontWeight.BOLD),
                                        ft.Text(self.classification, size=12),
                                        ft.Text(self.weight_range, size=18),
                                    ]),
                                    margin = ft.margin.all(20),
                                    padding = ft.padding.all(20),
                                ),                 
                            ),
                            margin=ft.margin.only(left=300,top=40),
                            alignment=ft.alignment.center, 
                            # width=300,
                        ),
                        ft.Container(
                            ft.Column([
                                ft.Container(
                                    ft.Text("How Active Are You ?", size=22, weight=ft.FontWeight.BOLD),
                                    margin=ft.margin.only(bottom=30),
                                ),
                                ft.Container(
                                    self.option1,
                                    margin=ft.margin.only(bottom=10), 
                                ),
                                ft.Container(
                                    self.option2,
                                    margin=ft.margin.only(bottom=10),
                                ),
                                ft.Container(
                                    self.option3,
                                    margin=ft.margin.only(bottom=10),
                                ),
                                ft.Container(
                                    self.option4,
                                    margin=ft.margin.only(bottom=10),
                                ),
                            ]),
                            margin=ft.margin.only(left=170,top=50),
                        ),
                    ]),
                ]),

                ft.Container(
                    ft.ElevatedButton(
                        content=ft.Icon(name=ft.icons.ARROW_FORWARD_IOS, color="white"),
                        style=ft.ButtonStyle(
                            bgcolor={ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT},
                            shape={
                                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=50),
                            },
                        ),
                        # on_click=lambda _: self.page.go('/home'),
                        on_click=lambda _: self.on_triangle_click(),
                    ),
                    alignment = alignment.Alignment(0.8, 0.7)
                    
                ),
            ]),          
        )

        return ft.Container(
            content=ft.Column([
            tabs,
            main_page, 
            ], alignment="center")
        )