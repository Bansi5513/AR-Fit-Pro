from flet import *
import flet as ft
import base64
import cv2
import numpy as np
import mediapipe as mp
import pymongo
from datetime import datetime

# Get current date
current_date = datetime.now().strftime("%Y-%m-%d")
current_time = datetime.now().strftime("%H:%M:%S")


myclient = pymongo.MongoClient('mongodb://localhost:27017')

mydb = myclient["ExerciseTracking"]
mycol = mydb["Exercise"]


# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

class BicepCurl_Detection(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.correct_count = 0
        self.incorrect_count = 0
        self.exercise_name = "Bicep Curl"
        self.exercise_data = []

    def build(self):
        self.page.scroll = "adaptive"
        cap = cv2.VideoCapture(0)

        class Camera(ft.UserControl):
            def __init__(self):
                super().__init__()
                self.correct_count = 0
                self.incorrect_count = 0
                self.stage = None
                self.reps_text = ft.Text(value="", size=18, weight=ft.FontWeight.BOLD)
                self.warning_msg = ""
                self.warning_text = ft.Text(value="", size=18, weight=ft.FontWeight.BOLD)

            def did_mount(self):
                self.update_timer()

            def update_timer(self):
                with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
                    while True:
                        ret, frame = cap.read()
                        if not ret:
                            break

                        # original (width =640, height = 480)
                        frame = cv2.resize(frame, (860, 645))
                        # Recolor image to RGB
                        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        image.flags.writeable = False
                        image = cv2.flip(image, 1)

                        # Make detection
                        results = pose.process(image)

                        # Recolor back to BGR
                        image.flags.writeable = True
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                        # Extract landmarks
                        try:
                            landmarks = results.pose_landmarks.landmark

                            frame_height, frame_width, _ = image.shape

                            # Check if all required landmarks are detected and visible on screen
                            if (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value] and landmarks[
                                mp_pose.PoseLandmark.LEFT_ELBOW.value] and
                                    landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value] and landmarks[
                                mp_pose.PoseLandmark.LEFT_HIP.value] and
                                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value] and landmarks[
                                mp_pose.PoseLandmark.RIGHT_ELBOW.value] and
                                    landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value] and landmarks[
                                mp_pose.PoseLandmark.RIGHT_HIP.value] and
                                    all(
                                        0 <= landmark.x * frame_width < frame_width and 0 <= landmark.y * frame_height < frame_height for
                                        landmark in
                                        [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                         landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                         landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value],
                                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]])):

                                # Get coordinates
                                shoulderL = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                                elbowL = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                                          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                                wristL = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                                shoulderR = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                             landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                                elbowR = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                                wristR = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                                          landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                                hipL = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                                hipR = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                                        landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

                                kneeL = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                                         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                                kneeR = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                                         landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

                                # Calculate angle
                                angleL_hand = self.calculate_angle(shoulderL, elbowL, wristL)
                                angleR_hand = self.calculate_angle(shoulderR, elbowR, wristR)

                                # Calculate angles with knees instead of the midpoint
                                angleL_back = self.calculate_angle(shoulderL, hipL, kneeL)
                                angleR_back = self.calculate_angle(shoulderR, hipR, kneeR)
    
                                # Visualize angle
                                cv2.putText(image, str(angleL_hand),
                                            tuple(np.multiply(elbowL, [640, 480]).astype(int)),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA
                                            )

                                cv2.putText(image, str(angleR_hand),
                                            tuple(np.multiply(elbowR, [640, 480]).astype(int)),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA
                                            )

                                # Check posture
                                warning = False
                                level = 0

                                if angleL_back < 170 or angleR_back < 170 or angleL_back > 190 or angleR_back > 190:
                                    warning = True
                                    self.warning_msg = "Back Not Straight"
                                    self.update_warning_text()

                                elif (angleL_hand < 20 or angleR_hand < 20) and level == 0:
                                    warning = True
                                    level = 1
                                    self.warning_msg = "Dumbbell is rising above your shoulder level"
                                    self.update_warning_text()

                                if (angleL_hand < 70 and angleR_hand < 70) and not warning:
                                    self.stage = "up"
                                    self.warning_msg = ""
                                    self.update_warning_text()

                                if angleL_hand > 170 and angleR_hand > 170 and self.stage == 'up' and not warning:
                                    self.stage = "down"
                                    self.correct_count += 1
                                    self.warning_msg = ""
                                    print("Correct Rep:", self.correct_count)
                                    self.update_reps_text()
                                    self.update_warning_text()

                                elif self.stage == 'up' and level == 1:
                                    warning = True
                                    level = 0
                                    self.stage = "down"
                                    self.incorrect_count += 1
                                    print("Incorrect Rep:", self.incorrect_count)
                                    self.update_reps_text()
                                    self.warning_msg = "Hand not lowering sufficiently"
                                    self.update_warning_text()
                            else:
                                self.warning_msg = "Body Points Not Detected"
                                self.update_warning_text()

                        except:
                            pass

                        # Render detections
                        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                                   mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2,
                                                                          circle_radius=2),
                                                   mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2,
                                                                          circle_radius=2))

                        # Encode frame to base64 for display
                        _, im_arr = cv2.imencode(".png", image)
                        im_b64 = base64.b64encode(im_arr)
                        self.img.src_base64 = im_b64.decode("utf-8")
                        self.update()

            def calculate_angle(self, a, b, c):
                a = np.array(a)
                b = np.array(b)
                c = np.array(c)
                radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
                angle = np.abs(radians * 180.0 / np.pi)
                if angle > 180.0:
                    angle = 360 - angle
                return round(angle, 2)
            
            def update_reps_text(self):
                self.reps_text.value = f"Correct Reps : {self.correct_count}, Incorrect Reps : {self.incorrect_count}"

            def update_warning_text(self):
                self.warning_text.value = f"Warning : {self.warning_msg}"

            def build(self):
                self.img = ft.Image(
                    border_radius=ft.border_radius.all(20)
                )

                return ft.Column([
                    self.img,
                    self.reps_text,
                    self.warning_text,
                ])

        camera = Camera()
        def stop_Workout(e):
            nonlocal camera

            correct_count = camera.correct_count
            incorrect_count = camera.incorrect_count

            end_time = datetime.now().strftime("%H:%M:%S")
            data = {
                "exercise_name": self.exercise_name,
                "correct_reps": correct_count,
                "incorrect_reps": incorrect_count,
                "date": current_date,
                "start_time": current_time,
                "end_time": end_time,
                # Add other data fields as needed
            }
            mycol.insert_one(data)
            print("Exercise data inserted into MongoDB.")
            self.page.go('/')

            # page.go error
            


        return ft.Container(
            # margin= ft.margin.all(10),
            content=ft.Column([
                ft.Container(
                    ft.Text("Bicep Curl", size=24, weight="bold", color="white"),
                    margin=ft.margin.only(top=10, bottom=5, left=10),
                ),
                ft.Row([
                    ft.Card(
                        elevation=10,
                        content=ft.Container(
                            height=685,
                            padding=20,
                            # border_radius= ft.border_radius.all(20),
                            content=camera
                        )),

                    ft.Container(
                        ft.Column([
                            camera.reps_text,
                            camera.warning_text,
                            ft.OutlinedButton(text="Stop Workout",  on_click= stop_Workout),
                        ]),
                        width = 600,
                        padding=ft.padding.only(left=100),
                        # margin=ft.margin.only(left=20),  # Adjusted margin for consistent spacing
                    ),
                ]),

            ])
        )