from flet import *
import flet as ft
import base64
import cv2
import numpy as np
import mediapipe as mp
import pymongo
from datetime import datetime
import time

# Get current date
current_date = datetime.now().strftime("%Y-%m-%d")
current_time = datetime.now().strftime("%H:%M:%S")


myclient = pymongo.MongoClient('mongodb://localhost:27017')

mydb = myclient["ExerciseTracking"]
mycol = mydb["Exercise"]


# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

class Squat_Detection(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.correct_count = 0
        self.incorrect_count = 0
        self.exercise_name = "Squat"
        self.exercise_data = []

    def build(self):
        self.page.scroll = "adaptive"
        cap = cv2.VideoCapture(0)

        class Camera(ft.UserControl):
            def __init__(self):
                super().__init__()
                self.correct_count = 0
                self.incorrect_count = 0
                self.stage = 0
                self.reps_text = ft.Text(value="", size=18, weight=ft.FontWeight.BOLD)
                self.warning_msg = ""
                self.warning_text = ft.Text(value="", size=18, weight=ft.FontWeight.BOLD)
                self.knee_angles = []
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
                            if (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value] and landmarks[
                            mp_pose.PoseLandmark.LEFT_KNEE.value] and
                                landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value] and landmarks[
                            mp_pose.PoseLandmark.LEFT_SHOULDER.value] and
                                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value] and landmarks[
                            mp_pose.PoseLandmark.RIGHT_ANKLE.value] and
                                landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value] and landmarks[
                            mp_pose.PoseLandmark.RIGHT_HIP.value] and
                                all(
                                    0 <= landmark.x * frame_width < frame_width and 0 <= landmark.y * frame_height < frame_height for
                                    landmark in
                                    [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                        landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                        landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value],
                                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]])):
                                # Get coordinates
                                hipL = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                                kneeL = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                                ankleL = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                                hipR = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                                kneeR = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                                ankleR = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                        
                                # Calculate angle
                                angleL_knee = self.calculate_angle(hipL, kneeL, ankleL)
                                angleR_knee = self.calculate_angle(hipR, kneeR, ankleR)
    
                                # Visualize angle
                                cv2.putText(image, str(angleL_knee),
                                            tuple(np.multiply(kneeL, [860, 645]).astype(int)),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA
                                            )

                                cv2.putText(image, str(angleR_knee),
                                            tuple(np.multiply(kneeR, [860, 645]).astype(int)),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA
                                            )

                                # Get coordinates of shoulder, hip, and a point on the ground (e.g., between the feet)
                                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * image.shape[1],
                                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * image.shape[0]]
                                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * image.shape[1],
                                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * image.shape[0]]
                                ground_point = [(landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x + landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x) / 2 * image.shape[1],
                                                (landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y + landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y) / 2 * image.shape[0]]

                                # Calculate angle between shoulder, hip, and the ground
                                angle_back = self.calculate_angle(shoulder, hip, ground_point)

                                # Check posture
                                warning = False

                                self.state=0
                    
                                if(angleL_knee < 135 and angleR_knee < 135) and  self.stage==0:
                                    self.stage = 1
                                    self.warning_msg = ""
                                    self.update_warning_text()

                                elif (angleL_knee > 140 and angleR_knee > 140) and self.stage == 1:
                                    self.stage = 0
                                    self.warning_msg = ""
                                    self.update_warning_text()
                                
                                elif angle_back > 160 and self.stage == 1:
                                    self.stage = 1
                                    # cv2.putText(image, "Bend Forwards", (50, 60),cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
                                    self.warning_msg = "Bend Forwards"
                                    self.update_warning_text()

                                elif angle_back < 135 and self.stage == 1:
                                    self.stage = 1
                                    # cv2.putText(image, "Bend Backwards", (50, 60),cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
                                    self.warning_msg = "Bend Backwards"
                                    self.update_warning_text()

                                elif (angleL_knee > 110 and angleR_knee > 110) and self.stage == 1:
                                    self.stage = 1
                                    # cv2.putText(image, "Squat too high", (50, 60),cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
                                    warning = True
                                    self.warning_msg = "Squat too high"
                                    self.update_warning_text()

                                elif (angleL_knee == 90 and angleR_knee == 90) or (angleL_knee < 90 and angleR_knee < 90) and self.stage == 1 :
                                    self.stage = 2
                                    self.warning_msg = ""
                                    self.update_warning_text()

                                # elif (angleL_knee == 90 and angleR_knee == 90) or (angleL_knee < 90 and angleR_knee < 90) and stage == 1 and warning:
                                #     stage = 2
                                #     print("Incorrect")
                                    
                                elif (angleL_knee < 70 and angleR_knee < 70) and self.stage == 2 :
                                    self.stage = 2
                                    # cv2.putText(image, "Squat too deep", (50, 60),cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
                                    warning = True
                                    self.warning_msg = "Squat too deep"
                                    self.update_warning_text()

                                elif angleL_knee > 90 and angleR_knee > 90 and self.stage == 2:
                                    self.warning_msg = ""

                                    if len(self.knee_angles) == self.correct_count:
                                        self.page.session.set("knee_angle", [angleL_knee, angleR_knee])
                                        angle = self.page.session.get("knee_angle")
                                        self.knee_angles.append(angle)

                                    self.stage=1
                                    self.correct_count += 1
                                    print("Correct Rep:", self.correct_count)
                                    self.update_reps_text()
                                    self.update_warning_text()
                                    

                                # elif angleL_knee > 110 and angleR_knee > 110 and stage == 2 and warning:
                                #     stage=1
                                #     print("Incorrect")
                                    
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
                self.reps_text.value = f"Correct Squats : {self.correct_count}, Incorrect Squats : {self.incorrect_count}"

                count = self.page.session.get("squat")
                print(count)
                if self.correct_count == count:
                    time.sleep(1)
                    complete_Workout(None)


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
            email = self.page.session.get("email")
            end_time = datetime.now().strftime("%H:%M:%S")

            angle_squat = camera.knee_angles
            print("Squat Knee Angles : " ,camera.knee_angles)

            query = {
                "Email": email,
                "Exercise_Name": "Squat",
                "Date": current_date
            }

            existing_data = mycol.find_one(query)

            if existing_data:
                # Update existing document with incremented counts
                new_correct_count = existing_data["Correct_Reps"] + correct_count
                new_incorrect_count = existing_data["Incorrect_Reps"] + incorrect_count

                # Update angles
                existing_data["Angles"]["Squat_Knee"].extend(camera.knee_angles)

                # Update other fields
                existing_data["Correct_Reps"] = new_correct_count
                existing_data["Incorrect_Reps"] = new_incorrect_count
                existing_data["End_Time"] = end_time

                mycol.update_one(query, {"$set": existing_data})
                print("Exercise data updated in MongoDB.")
            else:
                data = {
                    "Email": email,
                    "Exercise_Name": self.exercise_name,
                    "Correct_Reps": correct_count,
                    "Incorrect_Reps": incorrect_count,
                    "Angles" : {"Squat_Knee" : angle_squat},
                    "Date": current_date,
                    "Start_Time": current_time,
                    "End_Time": end_time,
                }

                
                mycol.insert_one(data)
                print("Exercise data inserted into MongoDB.")

            cap.release()
            cv2.destroyAllWindows()
            self.page.go('/home')

            # page.go error
            
        def complete_Workout(e):
            nonlocal camera

            correct_count = camera.correct_count
            incorrect_count = camera.incorrect_count
            email = self.page.session.get("email")
            end_time = datetime.now().strftime("%H:%M:%S")

            angle_squat = camera.knee_angles
            print("Squat Knee Angles : " ,camera.knee_angles)

            query = {
                "Email": email,
                "Exercise_Name": "Squat",
                "Date": current_date
            }

            existing_data = mycol.find_one(query)

            if existing_data:
                # Update existing document with incremented counts
                new_correct_count = existing_data["Correct_Reps"] + correct_count
                new_incorrect_count = existing_data["Incorrect_Reps"] + incorrect_count

                # Update angles
                existing_data["Angles"]["Squat_Knee"].extend(camera.knee_angles)

                # Update other fields
                existing_data["Correct_Reps"] = new_correct_count
                existing_data["Incorrect_Reps"] = new_incorrect_count
                existing_data["End_Time"] = end_time

                mycol.update_one(query, {"$set": existing_data})
                print("Exercise data updated in MongoDB.")
            else:
                print("ERROR")
            
            cap.release()
            cv2.destroyAllWindows() 
            self.page.go('/congratulation')
            

        return ft.Container(
            # margin= ft.margin.all(10),
            content=ft.Column([
                ft.Container(
                    ft.Text("Squat", size=24, weight="bold", color="white"),
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