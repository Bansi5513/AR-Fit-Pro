import flet as ft

from pages.signup import SignUp
from pages.login import Login
from pages.home import Home
from pages.training import Training
from pages.progress_day import Progress_Day
from pages.progress_month import Progress_Month
from pages.progress_week import Progress_Week
from pages.profile import Profile
from pages.signup_screen1 import Screen1
from pages.signup_workout_screen1 import Workout_Screen1
from pages.signup_physio_screen1 import Physio_Screen1
from pages.bicep_curl_info import BicepCurl_Info
from pages.bicep_curl_detection import BicepCurl_Detection
from pages.squat_info import Squat_Info
from pages.squat_detection import Squat_Detection
from pages.congratulations import Congo 

def views_handler(page):
  return {
    '/':ft.View(
        route='/',
        controls=[
          SignUp(page)
        ]
      ),
    '/login':ft.View(
        route='/login',
        controls=[
          Login(page)
        ]
      ),
    '/home':ft.View(
        route='/home',
        controls=[
          Home(page)
        ]
      ),
    '/training':ft.View(
        route='/training',
        controls=[
          Training(page)
        ]
      ),
    '/progress_month':ft.View(
        route='/progress_month',
        controls=[
          Progress_Month(page)
        ]
      ),
    '/progress_week':ft.View(
        route='/progress_week',
        controls=[
          Progress_Week(page)
        ]
      ),
    '/progress':ft.View(
        route='/progress',
        controls=[
          Progress_Day(page)
        ]
      ),
    '/profile':ft.View(
        route='/profile',
        controls=[
          Profile(page)
        ]
      ),
    '/screen1':ft.View(
      route='/screen1',
      controls=[
        Screen1(page)
      ]
    ),
    '/workout-screen2':ft.View(
      route='/workout-screen2',
      controls=[
        Workout_Screen1(page)
      ]
    ),
    '/physiotherapy-screen2':ft.View(
      route='/physiotherapy-screen2',
      controls=[
        Physio_Screen1(page)
      ]
    ),
    '/bicep-curl/detection':ft.View(
        route='/bicep-curl/detection',
        controls=[
          BicepCurl_Detection(page)
        ]
      ),
    '/bicep-curl/information':ft.View(
        route='/bicep-curl/information',
        controls=[
          BicepCurl_Info(page)
        ]
      ),
    '/squat/detection':ft.View(
        route='/squat/detection',
        controls=[
          Squat_Detection(page)
        ]
      ),
    '/squat/information':ft.View(
        route='/squat/information',
        controls=[
          Squat_Info(page)
        ]
      ),
    '/congratulation':ft.View(
        route='/congratulation',
        controls=[
          Congo(page)
        ]
      ),
  }