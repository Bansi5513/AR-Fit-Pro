from flet import *
import flet as ft
import datetime

class Screen1(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.build()

    def update_button_text(self, event):
        dob = self.date_picker.value
        formatted_dob = dob.strftime("%d/%m/%Y")
        print(formatted_dob)
        self.text_widget.value = formatted_dob

        today = datetime.datetime.now()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        print(f"Age: {age}")
        self.age.value = str(age)

        self.update()

    def validate_and_update_height(self, value):
        unit = self.height_units.value
        max_height_cm = 250
        max_height_ft = 8.3

        if unit == "cm":
            self.height_units.error_text = ""
            if self.height_input.value.isdigit():
                if 55 <= int(self.height_input.value) <= max_height_cm:
                    print(self.height_input.value, unit)
                    self.height_input.error_text = ""
                else:
                    self.height_input.error_text = "Invalid height"
            else:
                self.height_input.error_text = "Please enter a number."
        elif unit == "ft/in":
            self.height_units.error_text = ""
            if self.height_input.value:
                if 1.10 <= float(self.height_input.value) <= max_height_ft:
                    print(self.height_input.value, unit)
                    self.height_input.error_text = ""
                else:
                    self.height_input.error_text = "Invalid height"
            else:
                self.height_input.error_text = "Please enter a number."
        else:
            self.height_units.error_text = "*"

        self.update()
            
    def validate_and_update_weight(self, value):
        unit = self.weight_units.value
        max_weight_kg = 500
        max_weight_lbs = 1100

        if unit == "kg":
            self.weight_units.error_text = ""
            if self.weight_input.value.isdigit():
                if 15 <= int(self.weight_input.value) <= max_weight_kg:
                    print(self.weight_input.value, unit)
                    self.weight_input.error_text = ""
                else:
                    self.weight_input.error_text = "Invalid height"
            else:
                self.weight_input.error_text = "Please enter a number."
        elif unit == "lbs":
            self.weight_units.error_text = ""
            if self.weight_input.value:
                if 33 <= float(self.weight_input.value) <= max_weight_lbs:
                    print(self.weight_input.value, unit)
                    self.weight_input.error_text = ""
                else:
                    self.weight_input.error_text = "Invalid height"
            else:
                self.weight_input.error_text = "Please enter a number."
        else:
            self.weight_units.error_text = "*"

        self.update()

    def preference(self, e):
        self.workout_option.style.bgcolor = ft.colors.WHITE
        self.physio_option.style.bgcolor = ft.colors.WHITE

        # Change the clicked button's color to green
        e.control.style.bgcolor = ft.colors.BLUE_200

        # Update the UI to reflect the changes
        self.update() 

    def on_triangle_click(self):
        session_data = {
            "height": self.height_input.value,
            "weight": self.weight_input.value,
            "height_unit": self.height_units.value,
            "weight_unit": self.weight_units.value
        }
        self.page.session.set("user_data", session_data)

        preference_choice = None
        if self.workout_option.style.bgcolor == ft.colors.BLUE_200:
            preference_choice = "Workout"
        elif self.physio_option.style.bgcolor == ft.colors.BLUE_200:
            preference_choice = "Physiotherapy"

        data_2 = {
            # DOB, Age, Gender, Height, Weight, Preference
            "Date Of Birth": self.text_widget.value,        
            "Age": self.age.value,               
            "Gender": self.gender_group.value,
            "Height": self.height_input.value,
            "Height_unit": self.height_units.value,
            "Weight": self.weight_input.value,
            "Weight_unit": self.weight_units.value, 
            "Preference": preference_choice, 
        }
        self.page.session.set("data_2", data_2)
        
        if preference_choice:
            # Redirect to a page based on preference choice
            if preference_choice == "Workout":
                print("Workout")
                self.page.go('/workout-screen2')
            elif preference_choice == "Physiotherapy":
                print("Physiotherapy")
                self.page.go('/physiotherapy-screen2')
        else:
            # No preference choice selected, handle accordingly
            print("Error")

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
                    bgcolor="blue", # Corrected property name
                    border_radius=ft.border_radius.all(5)
                ),
                ft.Container(
                    content=ft.TextButton("", on_click=lambda e: on_tab_click("Tab 2")),
                    width=100, # Adjust the width as needed
                    height=2, # Adjust the height as needed
                    bgcolor="white", # Corrected property name
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
        self.date_picker = ft.DatePicker(
            first_date=datetime.datetime(1900, 1, 1),
            last_date=datetime.datetime.now(), # Set the last date to the current date
            current_date=datetime.datetime.now(), 
            on_change=self.update_button_text,
        )

        self.text_widget = ft.Text(value="Select", size=18, color="white")

        self.date_button = ft.TextButton(
            content=self.text_widget,
            on_click=lambda _: self.date_picker.pick_date(),
        )

        self.age = ft.Text("--",size=18)

        self.gender_group = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="Male", label="Male"),
                ft.Radio(value="Female", label="Female"),
                ft.Radio(value="Other", label="Other"),
            ]),
            on_change=lambda e: print(f"Selected Gender: {e.control.value}"),
        )

        self.height_input = ft.TextField(
            width=200,
            label="Enter Height",
            text_size=18,
            on_change=lambda e: self.validate_and_update_height(e.control.value),
        )

        self.height_units = ft.Dropdown(
            label="Height Unit",
            width=100,
            text_size=16,
            options=[
                ft.dropdown.Option("cm"),
                ft.dropdown.Option("ft/in"),
            ],
            on_change=lambda e: self.validate_and_update_height(self.height_input.value),
        )


        # Weight input field
        self.weight_input = ft.TextField(
            width=200,
            label="Enter Weight",
            text_size=18,
            on_change=lambda e: self.validate_and_update_weight(e.control.value),
        )
        # Weight unit dropdown
        self.weight_units = ft.Dropdown(
            label="Weight Unit",
            width=100,
            text_size=16,
            options=[
                ft.dropdown.Option("kg"),
                ft.dropdown.Option("lbs"),
            ],
            on_change=lambda e: self.validate_and_update_weight(self.weight_input.value),
        )

        self.workout_option = ft.ElevatedButton(
            content=ft.Text(value="Workout", size=18),
            style=ft.ButtonStyle(
                color={ft.MaterialState.DEFAULT: ft.colors.BLACK},
                bgcolor={ft.MaterialState.DEFAULT: ft.colors.WHITE},
            ),
            on_click=lambda e: self.preference(e)
        )
        self.physio_option = ft.ElevatedButton(
            content=ft.Text(value="Physiotherapy", size=18),
            style=ft.ButtonStyle(
                color={ft.MaterialState.DEFAULT: ft.colors.BLACK},
                bgcolor={ft.MaterialState.DEFAULT: ft.colors.WHITE},
            ),
            on_click=lambda e: self.preference(e)
        )

        main_page = ft.Container(
            content=ft.Column([
                ft.Container(
                    ft.Text("Personal Information", size=26, weight=ft.FontWeight.BOLD),
                    margin=ft.margin.only(left=300,top=60,bottom=10),
                ),
                ft.Column([
                    ft.Row([
                        ft.Container(
                            ft.Text("Date Of Birth", size=20, weight=ft.FontWeight.BOLD),
                            margin=ft.margin.only(left=300,top=40),
                            width=200
                        ),
                        ft.Container(
                            ft.Text("Height", size=20, weight=ft.FontWeight.BOLD),
                            margin=ft.margin.only(left=250,top=40)
                        ),
                    ]),
                ]),
                ft.Column([
                    ft.Row([
                        ft.Container(
                            content=self.date_button,
                            margin=ft.margin.only(left=300,top=10),
                            width=200,
                        ),
                        ft.Container(
                            content=ft.Row([
                                self.height_input,
                                self.height_units,
                            ]),
                            margin=ft.margin.only(left=250,top=10)
                        ),
                        ft.Container(  # Add the DatePicker control here
                            content=self.date_picker,
                        ),
                    ]),
                ]),
                ft.Column([
                    ft.Row([
                        ft.Container(
                            ft.Text("Age", size=20, weight=ft.FontWeight.BOLD),
                            margin=ft.margin.only(left=300,top=20),
                            width=200,
                        ),
                        ft.Container(
                            ft.Text("Weight", size=20, weight=ft.FontWeight.BOLD),
                            margin=ft.margin.only(left=250,top=20)
                        ),
                    ]),
                ]),
                ft.Column([
                    ft.Row([
                        ft.Container(
                            content=self.age,
                            margin=ft.margin.only(left=300,top=10),
                            width=200,
                        ),
                        ft.Container(
                            content=ft.Row([
                                self.weight_input,
                                self.weight_units,
                            ]),
                            margin=ft.margin.only(left=250,top=10)
                        ),
                    ]),
                ]),
                ft.Column([
                    ft.Row([
                        ft.Container(
                            ft.Text("Gender", size=20, weight=ft.FontWeight.BOLD),
                            margin=ft.margin.only(left=300,top=20),
                            width=200,
                        ),
                        ft.Container(
                            ft.Text("Preference", size=20, weight=ft.FontWeight.BOLD),
                            margin=ft.margin.only(left=250,top=20)
                        ),
                    ]),
                ]),
                ft.Column([
                    ft.Row([
                        ft.Container(
                            content=self.gender_group,
                            margin=ft.margin.only(left=300,top=10),
                            width=200,
                        ),
                        ft.Container(
                            ft.Row([
                                self.workout_option,
                                self.physio_option,
                            ]),
                            margin=ft.margin.only(left=250,top=10)
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