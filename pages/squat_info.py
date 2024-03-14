from flet import *
import flet as ft

class Squat_Info(UserControl):
  def __init__(self,page):
    super().__init__()
    self.page = page

  def build(self):
        self.page.scroll = "adaptive"
        return ft.Container(
            ft.Column([
                ft.Row([

                    ft.Column([
                        ft.Container(
                        content=ft.Text("Squat", size=26, weight=ft.FontWeight.BOLD),
                        margin=ft.margin.only(bottom=15, left=15, top = 15)
                        ),
                        ft.Container(
                            content=ft.Image(src="exercise2.jpg",width=450,height=500,fit=ft.ImageFit.CONTAIN),
                            margin=ft.margin.only(left=15)
                        ),
                    ]),
                    
                    ft.Container(
                        content=ft.Column([ 

                            ft.Container(
                                ft.Text("Steps : ", size=20, weight=ft.FontWeight.BOLD),
                                margin=ft.margin.only(bottom=10)
                            ),

                            ft.Container(
                                content=ft.Column([ 
                                    ft.Text("1. Camera Setup: Position the camera directly in front of you, ensuring it's at a fixed 90-degree angle relative to the ground.", size=16),
                                    ft.Text("2. Body Positioning and Angle Adjustment: Stand facing the camera with your feet slightly wider than hip-width apart, toes pointing forward. Tilt your body slightly sideways from the camera for accurate detection.", size=16),
                                    ft.Text("3. Start Squatting: Drive your hips back, bending at the knees and ankles, while pressing your knees slightly open.", size=16),
                                    ft.Text("4. Maintain Form: Sit into a squat position while ensuring your heels and toes remain on the ground, with your chest up and shoulders back.", size=16),
                                    ft.Text("5. Controlled Descent: Lower your body until your thighs are parallel to the ground or your knees form a 90-degree angle.", size=16),
                                    ft.Text("6. Push through Heels: Press into your heels and straighten your legs to return to a standing upright position.", size=16),
                                    ft.Text("7. Monitor Feedback: Pay attention to warnings for incorrect posture and adjust accordingly.", size=16),
                                    ft.Text("8. Track Reps: Keep an eye on the displayed reps, focusing on quality over quantity.", size=16),
                                    ft.Text("9. End Session: Click 'Stop Workout' to finish and store your exercise data.", size=16),
                                ])
                            ),

                            ft.Container(
                                ft.OutlinedButton(text="Start Workout",  on_click= lambda _: self.page.go('/squat/detection')),
                                margin=ft.margin.only(top=20)
                            )
                        ]),
                        margin=ft.margin.only(left=50, top=90),
                        width=950,
                    )
                ])
            ])
        )