# squat - final

from flet import *
import flet as ft
import base64
import cv2
import numpy as np
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)


#counter variable
counter = 0
stage = 0
warning = False


def calculate_angle(a, b, c):
    a = np.array(a) 
    b = np.array(b) 
    c = np.array(c) 
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return round(angle, 2)

    #setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

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
                    angleL_knee = calculate_angle(hipL, kneeL, ankleL)
                    angleR_knee = calculate_angle(hipR, kneeR, ankleR)
                    
                    # Visualize angle
                    cv2.putText(image, str(angleL_knee), 
                                tuple(np.multiply(kneeL, [640, 480]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                        )

                    cv2.putText(image, str(angleR_knee), 
                                tuple(np.multiply(kneeR, [640, 480]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                        )
                    
                    # Get coordinates of shoulder, hip, and a point on the ground (e.g., between the feet)
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * image.shape[1],
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * image.shape[0]]
                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * image.shape[1],
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * image.shape[0]]
                    ground_point = [(landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x + landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x) / 2 * image.shape[1],
                                    (landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y + landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y) / 2 * image.shape[0]]

                    # Calculate angle between shoulder, hip, and the ground
                    angle_back = calculate_angle(shoulder, hip, ground_point)


                    state=0
                    
                    if(angleL_knee < 135 and angleR_knee < 135) and  stage==0:
                        stage = 1
                    elif (angleL_knee > 140 and angleR_knee > 140) and stage == 1:
                        stage = 0
                    
                    elif angle_back > 160 and stage == 1:
                        stage = 1
                        cv2.putText(image, "Bend Forwards", (50, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
                    elif angle_back < 135 and stage == 1:
                        stage = 1
                        cv2.putText(image, "Bend Backwards", (50, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
                    elif (angleL_knee > 110 and angleR_knee > 110) and stage == 1:
                        stage = 1
                        cv2.putText(image, "Squat too high", (50, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
                        warning = True
                    elif (angleL_knee == 90 and angleR_knee == 90) or (angleL_knee < 90 and angleR_knee < 90) and stage == 1 :
                        stage = 2
                    # elif (angleL_knee == 90 and angleR_knee == 90) or (angleL_knee < 90 and angleR_knee < 90) and stage == 1 and warning:
                    #     stage = 2
                    #     print("INcorrect")
                    elif (angleL_knee < 70 and angleR_knee < 70) and stage == 2 :
                        stage = 2
                        cv2.putText(image, "Squat too deep", (50, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
                        warning = True
                    elif angleL_knee > 90 and angleR_knee > 90 and stage == 2:
                        stage=1
                        counter+=1
                        print(counter)
                    # elif angleL_knee > 110 and angleR_knee > 110 and stage == 2 and warning:
                    #     stage=1
                    #     print("Incorrect")
                    




                    # # curl counter logic
                        
                    # if (angleL_knee == 90 and angleR_knee == 90) or (angleL_knee < 90 and angleR_knee < 90) and not warning:
                    #     stage = "down"
                    # elif angleL_knee > 90 and angleR_knee > 90 and stage =='down' and not warning:
                    #     stage="up"
                    #     counter+=1
                    #     print(counter)

                else:
                    # print("Body Points Not Detected")
                    cv2.putText(image, "Body Points Not Detected", (50, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
                    # self.warning_msg = "Body Points Not Detected"
                    # self.update_warning_text()
            except:
                pass


            #render squats counter
            
            cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)

            #rep data
            cv2.putText(image, 'SQUATS - REPS', (15,12),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, str(stage), (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            #render detection
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                     mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                     mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()