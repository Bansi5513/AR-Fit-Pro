from flet import *
import flet as ft
import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017')

mydb = myclient["ExerciseTracking"]
mycol = mydb["Doctor"]

class Home(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

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

        # Home Page Content
        data = self.page.session.get("data")
        # print(data)

        preference = data.get("Preference")
        bmi = data.get("BMI Score")
        physiotherapy_concerns = data.get("Physiotherapy Concerns")

        # Matching with Database Ranges
        matching_doctors = []
        for doctor in mycol.find({"Preference": preference}):
            doctor_bmi_range = doctor.get("BMI")
            doctor_physiotherapy_concern = doctor.get("Physiotherapy_Concerns")
            if doctor_bmi_range:
                lower_bound, upper_bound = map(float, doctor_bmi_range.split('-'))
                if bmi and lower_bound <= bmi <= upper_bound:
                    matching_doctors.append(doctor)
            elif physiotherapy_concerns and physiotherapy_concerns == doctor_physiotherapy_concern:
                matching_doctors.append(doctor)
        
        squat_text = ft.Text(value="", size=18, weight=ft.FontWeight.BOLD)
        squat_count = ft.Text(value="", size=18)
        bicep_text = ft.Text(value="", size=18, weight=ft.FontWeight.BOLD)
        bicep_count = ft.Text(value="", size=18)

        for doctor in matching_doctors:
            if doctor.get("squat") :
                squat = doctor.get("squat")
                squat_text.value = "Squat : "
                squat_count.value = squat
                print("Squat:", squat)
                self.page.session.set("squat",squat)
            if doctor.get("bicep_curl"):
                bicep_curl = doctor.get("bicep_curl")
                bicep_text.value = "Bicep Curls : "     
                bicep_count.value = bicep_curl
                print("Bicep Curl:", bicep_curl)
                self.page.session.set("bicep_curl",bicep_curl)
            
        
       

        home_content = ft.Container(
            ft.Card(
                ft.Container(
                    content=ft.Column([
                        ft.Text(value="Workout Routine", size=20, weight=ft.FontWeight.BOLD),
                        ft.Row([
                            squat_text,
                            squat_count,
                        ]),
                        ft.Row([
                            bicep_text,
                            bicep_count
                        ]),
                    ]),
                    padding=ft.padding.all(20),
                    alignment=ft.alignment.center,
                    width=300,
                    margin = ft.margin.all(15),
                )
            ),
            margin=ft.margin.only(top=30, bottom=30)
        )

        # Achievements Section
        # achievements_title = ft.Text(value="Achievements", size=34, weight=ft.FontWeight.BOLD)

        achievements_title = ft.Container(
            content=ft.Row([
                ft.Text(value="Achievements", size=34, weight=ft.FontWeight.BOLD)
            ]),
            padding=ft.padding.all(10)
        )

        achievements_images_and_titles = [
            ft.Container(
                content=ft.Column([
                    ft.Image(src="awards/Ghost Runner.jpeg", width=200, height=200),
                    ft.Text(value="        Initiate Ignition", size=16, weight=ft.FontWeight.NORMAL)
                ], spacing=5),
                padding=ft.padding.all(5),
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=ft.Column([
                    ft.Image(src="awards/3 week run streak.jpeg", width=200, height=200),
                    ft.Text(value="         3 Weeks Streak", size=16, weight=ft.FontWeight.NORMAL)
                ], spacing=5),
                padding=ft.padding.all(5),
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=ft.Column([
                    ft.Image(src="awards/5 week run streak.jpeg", width=200, height=200),
                    ft.Text(value="         5 Weeks Streak", size=16, weight=ft.FontWeight.NORMAL)
                ], spacing=5),
                padding=ft.padding.all(5),
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=ft.Column([
                    ft.Image(src="awards/7 runs in a week.jpeg", width=200, height=200),
                    ft.Text(value="         7 Weeks Streak", size=16, weight=ft.FontWeight.NORMAL)
                ], spacing=5),
                padding=ft.padding.all(5),
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=ft.Column([
                    ft.Image(src="awards/Break Through.jpeg", width=200, height=200),
                    ft.Text(value="           Stage on Fire", size=16, weight=ft.FontWeight.NORMAL)
                ], spacing=5),
                padding=ft.padding.all(5),
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=ft.Column([
                    ft.Image(src="awards/Gold Miles Completed.jpeg", width=200, height=200),
                    ft.Text(value="    Gold Miles Completed", size=16, weight=ft.FontWeight.NORMAL)
                ], spacing=5),
                padding=ft.padding.all(5),
                alignment=ft.alignment.center
            )
            # Add more achievements as needed
        ]

        achievements_section = ft.Container(
            content=ft.Row([
                # achievements_title,
                *achievements_images_and_titles  # Spread operator to add all images and titles
            ], spacing=20),  # Adjust spacing between title and images/titles
            padding=ft.padding.all(0),
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=30, bottom=30)
        )

        # Add achievements section to the main content
        return ft.Container(
            margin=ft.margin.only(left=10, top=0),
            content=ft.Column([
                navigation_bar,
                home_content,
                achievements_title,
                achievements_section  # Add achievements section here
            ], alignment="center")
        )
        

# 681x681