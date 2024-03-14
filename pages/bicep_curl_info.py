from flet import *
import flet as ft

class BicepCurl_Info(UserControl):
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
                        content=ft.Text("Bicep Curl", size=26, weight=ft.FontWeight.BOLD),
                        margin=ft.margin.only(bottom=15, left=15, top = 15)
                        ),
                        ft.Container(
                            content=ft.Image(src="exercise1.jpg",width=450,height=500,fit=ft.ImageFit.CONTAIN),
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
                                    ft.Text("1. Prepare Equipment: You'll need a dumbbell or any suitable weight for resistance.", size=16),
                                    ft.Text("2. Camera Setup: Position the camera directly in front of you, ensuring it's at a fixed 90-degree angle relative to the ground.", size=16),
                                    ft.Text("3. Body Positioning: Stand facing the camera with your feet slightly wider than hip-width apart, toes pointing forward. Hold the dumbbell in one hand with an underhand grip (palms facing upward), allowing it to hang down by your side.", size=16),
                                    ft.Text("4. Angle Adjustment: Tilt your body slightly sideways from the camera for accurate detection.", size=16),
                                    ft.Text("5. Initiate Movement: Slowly lift the dumbbell upward by bending your elbow, exhaling as you contract your bicep muscles. Keep your upper arm still.", size=16),
                                    ft.Text("6. Complete Repetition: Lift the dumbbell until your forearm is fully contracted near your shoulder, then lower it back down in a controlled manner. Maintain muscle engagement..", size=16),
                                    ft.Text("7. Repeat with Proper Posture: Perform smooth, controlled repetitions while ensuring proper posture. Keep your back straight and core engaged to prevent swinging or using momentum.", size=16),
                                    ft.Text("8. Monitor Feedback: Pay attention to warnings for incorrect posture and adjust accordingly.", size=16),
                                    ft.Text("9. Track Reps: Keep an eye on the displayed reps, focusing on quality over quantity.", size=16),
                                    ft.Text("10. End Session: Click 'Stop Workout' to finish and store your exercise data.", size=16),
                                    
                                ])
                            ),

                            ft.Container(
                                ft.OutlinedButton(text="Start Workout",  on_click= lambda _: self.page.go('/bicep-curl/detection')),
                                margin=ft.margin.only(top=20)   
                            )
                        ]),
                        margin=ft.margin.only(left=50, top=90),
                        width=950,
                    )
                ])
            ])
        )