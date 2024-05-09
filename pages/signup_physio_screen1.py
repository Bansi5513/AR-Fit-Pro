from flet import *
import flet as ft
import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017')

mydb = myclient["ExerciseTracking"]
mycol = mydb["User"]

class Physio_Screen1(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.selected_medical_conditions = []
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
    
    def selected(self, e):
        
        checkbox_label = e.control.label
        if e.control.value:
            # If checkbox is checked, add it to the selected medical conditions list
            self.selected_medical_conditions.append(checkbox_label)
        else:
            # If checkbox is unchecked, remove it from the selected medical conditions list
            self.selected_medical_conditions.remove(checkbox_label)

        self.update()

    def on_triangle_click(self):

        preference_choice = None
        if self.option1.style.bgcolor == ft.colors.BLUE_200:
            preference_choice = "Back & Neck Pain"
        elif self.option2.style.bgcolor == ft.colors.BLUE_200:
            preference_choice = "Ankle Sprains"
        elif self.option3.style.bgcolor == ft.colors.BLUE_200:
            preference_choice = "Knee Ligament Injury"
        elif self.option4.style.bgcolor == ft.colors.BLUE_200:
            preference_choice = "Shoulder Impingement"

        data_1 = self.page.session.get("data_1")
        data_2 = self.page.session.get("data_2")
        data_3 = {
            "Medical Conditions": self.selected_medical_conditions,        
            "Physiotherapy Concerns": preference_choice,                
        }

        self.page.session.set("data_3", data_3)

        # Merge data into a single dictionary
        merged_data = {}
        merged_data.update(data_1)
        merged_data.update(data_2)
        merged_data.update(data_3)

        self.page.session.set("data", merged_data)
        
        # Insert merged data into MongoDB
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
        
        self.medical_conditions = ft.Container(
            content=ft.Column([
                ft.Checkbox(value=False, label="None"),
                ft.Row([
                    ft.Column([
                        ft.Checkbox(value=False, label="Diabetes", on_change=lambda e: self.selected(e)),
                        ft.Checkbox(value=False, label="Depression", on_change=lambda e: self.selected(e)),
                        ft.Checkbox(value=False, label="Hypertension", on_change=lambda e: self.selected(e)),
                    ]),
                    ft.Column([
                        ft.Checkbox(value=False, label="Thyroid", on_change=lambda e: self.selected(e)),
                        ft.Checkbox(value=False, label="Sleep Issues", on_change=lambda e: self.selected(e)),
                        ft.Checkbox(value=False, label="PCOS", on_change=lambda e: self.selected(e)),
                    ]),    
                ]),
                ft.Checkbox(value=False, label="Cholesterol", on_change=lambda e: self.selected(e)),
                ft.Checkbox(value=False, label="Excessive Stress / Anxiety", on_change=lambda e: self.selected(e)),
                
            ]),
        )

        self.option1 = ft.ElevatedButton(
            content=ft.Text(value="Back & Neck Pain", size=18),
            width=260,
            style=ft.ButtonStyle(
                color={ft.MaterialState.DEFAULT: ft.colors.BLACK},
                bgcolor={ft.MaterialState.DEFAULT: ft.colors.WHITE},
            ),
            on_click=lambda e: self.preference(e)
        )
        self.option2 = ft.ElevatedButton(
            content=ft.Text(value="Ankle Sprains", size=18),
            width=260,
            style=ft.ButtonStyle(
                color={ft.MaterialState.DEFAULT: ft.colors.BLACK},
                bgcolor={ft.MaterialState.DEFAULT: ft.colors.WHITE},
            ),
            on_click=lambda e: self.preference(e)
        )
        self.option3 = ft.ElevatedButton(
            content=ft.Text(value="Knee Ligament Injury", size=18),
            width=260,
            style=ft.ButtonStyle(
                color={ft.MaterialState.DEFAULT: ft.colors.BLACK},
                bgcolor={ft.MaterialState.DEFAULT: ft.colors.WHITE},
            ),
            on_click=lambda e: self.preference(e)
        )
        self.option4 = ft.ElevatedButton(
            content=ft.Text(value="Shoulder Impingement", size=18),
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
                    ft.Text("Physiotherapy", size=26, weight=ft.FontWeight.BOLD),
                    margin=ft.margin.only(left=300,top=60,bottom=50),
                ),
                ft.Column([
                    ft.Row([
                        ft.Container(
                            ft.Column([
                                ft.Container(
                                    ft.Text("Any Medical Conditions ?", size=20, weight=ft.FontWeight.BOLD),
                                    margin=ft.margin.only(bottom=30),
                                ),
                                ft.Container(
                                    content=self.medical_conditions,
                                    margin=ft.margin.only(bottom=10),
                                ),
                                
                            ]),
                            margin=ft.margin.only(left=300),
                        ),

                        ft.Container(
                            ft.Column([
                                ft.Container(
                                    ft.Text("Physiotherapy Concerns", size=20, weight=ft.FontWeight.BOLD),
                                    margin=ft.margin.only(bottom=30),
                                ),
                                ft.Container(
                                    self.option1,
                                    margin=ft.margin.only(bottom=15), 
                                ),
                                ft.Container(
                                    self.option2,
                                    margin=ft.margin.only(bottom=15),
                                ),
                                ft.Container(
                                    self.option3,
                                    margin=ft.margin.only(bottom=15),
                                ),
                                ft.Container(
                                    self.option4,
                                    margin=ft.margin.only(bottom=15),
                                ),
                            ]),
                            margin=ft.margin.only(left=200),
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