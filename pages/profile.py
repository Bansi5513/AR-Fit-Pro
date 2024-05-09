from flet import *
import flet as ft
import datetime
import pymongo

class Profile(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.myclient = pymongo.MongoClient('mongodb://localhost:27017')
        self.mydb = self.myclient["ExerciseTracking"]
        self.mycol = self.mydb["User"]

    def build(self):
        self.page.scroll = "adaptive"

        # Retrieve email from session
        email = self.page.session.get("email")

        # Retrieve user data from MongoDB using the email
        user_data = self.mycol.find_one({"Email": email})

        # Extract user information
        if user_data:
            name = user_data.get('Name', "")
            email = user_data.get('Email', "")
            birthdate = user_data.get('Date Of Birth', "")
            gender = user_data.get('Gender', "")
            height = user_data.get('Height', "")
            weight = user_data.get('Weight', "")
            preference = user_data.get('Preference', "")
            bmi_score = user_data.get('BMI Score', "")
            classification = user_data.get('Classification', "")
            goal = user_data.get('Goal', "")
            active = user_data.get('Active', "")

            # Calculate age from birthdate
            if birthdate:
                birthdate_obj = datetime.datetime.strptime(birthdate, '%d/%m/%Y')  # Adjust format string
                age = (datetime.datetime.now() - birthdate_obj).days // 365

            # Create text elements for user information
            name_text = ft.Text(name, size=80)
            email_text = ft.Text(email, size=15)
            birthdate_text = ft.Text(f"Birthdate: {birthdate}", size=25)
            age_text = ft.Text(f"Age: {age}", size=25)
            gender_text = ft.Text(f"Gender: {gender}", size=25)
            height_text = ft.Text(f"Height: {height} cm", size=25)
            weight_text = ft.Text(f"Weight: {weight} kg", size=25)
            preference_text = ft.Text(f"Preference: {preference}", size=25)
            bmi_score_text = ft.Text(f"BMI Score: {bmi_score}", size=25)
            classification_text = ft.Text(f"Classification: {classification}", size=25)
            goal_text = ft.Text(f"Goal: {goal}", size=25)
            active_text = ft.Text(f"Active: {active}", size=25)

            # Create columns for left and right information
            # middle_part = ft.Column([
            #     name_text,
            #     email_text
            # ], alignment="center")

            # left_column = ft.Column([
            #     birthdate_text,
            #     age_text,
            #     gender_text,
            #     height_text,
            #     weight_text
            # ], alignment="start")

            # right_column = ft.Column([
            #     preference_text,
            #     bmi_score_text,
            #     classification_text,
            #     goal_text,
            #     active_text
            # ], alignment="end")

            profile_content = ft.Container(
            ft.Card(
                ft.Container(
                    content=ft.Column([
                        # ft.Text(value="Workout Routine", size=20, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=ft.Column([
                                name_text,
                                email_text
                            ], alignment=ft.alignment.center),
                            alignment=ft.alignment.center
                        ),

                        ft.Container(
                            content=ft.Row([
                                ft.Column([
                                    birthdate_text,
                                    age_text,
                                    gender_text,
                                    height_text,
                                    weight_text
                                ], 
                                alignment="start", spacing=30),
                                ft.Column([
                                    preference_text,
                                    bmi_score_text,
                                    classification_text,
                                    goal_text,
                                    active_text
                                ], alignment="end",  spacing=30)
                                ], alignment=ft.alignment.center, spacing=400),
                            alignment=ft.alignment.center
                        )


                    ],spacing=50, alignment=ft.alignment.center),


                    padding=ft.padding.all(20),
                    alignment=ft.alignment.center,
                    width=1000,
                    margin = ft.margin.all(15),
                )
            ),
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=30, bottom=30)
        )

            # Navigation bar
            navigation_bar = ft.Row(
                controls=[
                    ft.Image(src="logo1.png", width=100, height=100, fit=ft.ImageFit.CONTAIN),  # Logo on the top left
                    ft.Container(width=940),  # Container acting as a spacer to push the navigation items to the right
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.icons.HOME_ROUNDED,  # Using built-in icon
                                    icon_color="white",
                                    on_click=lambda _: self.page.go('/home')
                                ),
                                padding=ft.padding.all(30)  # Add padding around the icon button
                            ),
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.icons.DIRECTIONS_RUN_ROUNDED,  # Replace with actual icon name for training
                                    icon_color="white",
                                    on_click=lambda _: self.page.go('/training')
                                ),
                                padding=ft.padding.all(30)  # Add padding around the icon button
                            ),
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.icons.AUTO_GRAPH_ROUNDED,  # Replace with actual icon name for progress
                                    icon_color="white",
                                    on_click=lambda _: self.page.go('/progress')
                                ),
                                padding=ft.padding.all(30)  # Add padding around the icon button
                            ),
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.icons.ACCOUNT_CIRCLE_SHARP,  # Replace with actual icon name for profile
                                    icon_color="white",
                                    on_click=lambda _: self.page.go('/profile')
                                ),
                                padding=ft.padding.all(30)  # Add padding around the icon button
                            ),
                        ],
                        alignment=ft.alignment.center
                    )
                ],
                alignment=ft.alignment.center
            )

            # Combine the navigation bar and user info containers
            return ft.Container(
                margin=ft.margin.only(left=10, top=0),
                content=ft.Column([
                    navigation_bar,
                    profile_content
                ], alignment="center"))
        

            # return ft.Container(
            #     margin=ft.margin.only(left=10, top=0),
            #     content=ft.Column([
            #         navigation_bar,
            #         middle_part,
            #         ft.Row([
            #             left_column,
            #             right_column
            #         ], alignment="center")
            #     ], alignment="center"))
