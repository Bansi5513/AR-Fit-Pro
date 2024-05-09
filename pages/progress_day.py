from flet import *
import flet as ft
import numpy as np
import pymongo
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd
import calendar

current_date = datetime.now().strftime("%Y-%m-%d")
# current_date = datetime.strptime("2024-03-10", "%Y-%m-%d")
myclient = pymongo.MongoClient('mongodb://localhost:27017')

mydb = myclient["ExerciseTracking"]
mycol = mydb["Exercise"]

class Progress_Day(UserControl):
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


        progress_bar = ft.Container(
            content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.TextButton(
                                text="Day",
                                on_click=lambda _: self.page.go('/progress')
                            ),
                            padding=ft.padding.all(30) # Add padding around the icon button
                        ),
                        ft.Container(
                            content=ft.TextButton(
                                text="Week",
                                on_click=lambda _: self.page.go('/progress_week')
                            ),
                            padding=ft.padding.all(30) # Add padding around the icon button
                        ),
                        ft.Container(
                            content=ft.TextButton(
                                text="Month",
                                on_click=lambda _: self.page.go('/progress_month')
                            ),
                            padding=ft.padding.all(30) # Add padding around the icon button
                        ),
                        
                    ],
                    alignment=ft.alignment.center,
                ),
            margin=ft.margin.only(top=5),
        )


        email = self.page.session.get("email")

        count1 = self.page.session.get("bicep_curl")
        count2 = self.page.session.get("squat")

        # print(count1,count2)

        if count1 is not None:

            query = {
                "Email": email,
                "Exercise_Name": "Bicep Curl",
                "Date": current_date
            }
            # Retrieve exercise data from MongoDB
            exercise_data = list(mycol.find(query))

            # Convert MongoDB data to a DataFrame for easy manipulation
            df = pd.DataFrame(exercise_data)

            # print(df)

            # Convert 'Start_Time' and 'End_Time' columns to datetime format
            df['Start_Time'] = pd.to_datetime(df['Start_Time'])
            df['End_Time'] = pd.to_datetime(df['End_Time'])

            # Extract hour component from 'Start_Time' and 'End_Time' columns
            df['Start_Hour'] = df['Start_Time'].dt.hour
            df['End_Hour'] = df['End_Time'].dt.hour

            # Initialize dictionary to store correct rep count for each hour
            correct_reps_by_hour = {hour: 0 for hour in range(1, 25)}  # Change range to start from 1

            # Update correct rep count for each hour where activity occurred
            for index, row in df.iterrows():
                for hour in range(row['Start_Hour'], row['End_Hour']):
                    correct_reps_by_hour[hour + 1] += row['Correct_Reps']  # Add 1 to each hour

            # Plot the bar graph
            plt.figure(figsize=(10, 6))
            plt.bar(correct_reps_by_hour.keys(), correct_reps_by_hour.values(), color='skyblue')
            plt.title('Bicep Curl Correct Reps by Hour of Day', fontsize=20)
            plt.xlabel('Hour of Day')
            plt.ylabel('Correct Reps')
            plt.xticks(range(1, 25))  # Change range to start from 1
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig('bicep_today.png')
            # plt.show()
            plt.close()

        if count2 is not None:

            query = {
                "Email": email,
                "Exercise_Name": "Squat",
                "Date": current_date
            }
            # Retrieve exercise data from MongoDB
            exercise_data = list(mycol.find(query))

            # Convert MongoDB data to a DataFrame for easy manipulation
            df = pd.DataFrame(exercise_data)

            # print(df)

            # Convert 'Start_Time' and 'End_Time' columns to datetime format
            df['Start_Time'] = pd.to_datetime(df['Start_Time'])
            df['End_Time'] = pd.to_datetime(df['End_Time'])

            # Extract hour component from 'Start_Time' and 'End_Time' columns
            df['Start_Hour'] = df['Start_Time'].dt.hour
            df['End_Hour'] = df['End_Time'].dt.hour

            # Initialize dictionary to store correct rep count for each hour
            correct_reps_by_hour = {hour: 0 for hour in range(1, 25)}  # Change range to start from 1

            # Update correct rep count for each hour where activity occurred
            for index, row in df.iterrows():
                for hour in range(row['Start_Hour'], row['End_Hour']):
                    correct_reps_by_hour[hour + 1] += row['Correct_Reps']  # Add 1 to each hour

            # Plot the bar graph
            plt.figure(figsize=(10, 6))
            plt.bar(correct_reps_by_hour.keys(), correct_reps_by_hour.values(), color='skyblue')
            plt.title('Squat Correct Reps by Hour of Day', fontsize=20)
            plt.xlabel('Hour of Day')
            plt.ylabel('Correct Reps')
            plt.xticks(range(1, 25))  # Change range to start from 1
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig('squat_today.png')
            # plt.show()
            plt.close()

        # Progress Page Content
        progress_title = ft.Container(
            content=ft.Text("Workout Progress", size=24, weight=ft.FontWeight.BOLD),
            margin=ft.margin.only(top=20, bottom=20)
        )
        graph_container = ft.Container(
            ft.Row([
                ft.Image(src="bicep_today.png", height=320, fit=ft.ImageFit.CONTAIN),
                ft.Image(src="squat_today.png", height=320, fit=ft.ImageFit.CONTAIN),
            ]),
            margin=ft.margin.only(top=10) # Add some margin to separate the title and the graph
        )

        # Add navigation bar, title, and graph container to the page
        return ft.Container(
            margin=ft.margin.only(left=10, top=0),
            content=ft.Column([
                navigation_bar,
                progress_title,
                progress_bar,
                graph_container,
            ], alignment="center")
        )
        