import flet as ft

from pages.signup import SignUp
from pages.login import Login
from pages.home import Home
from pages.bicep_curl_info import BicepCurl_Info
from pages.bicep_curl_detection import BicepCurl_Detection
from pages.squat_info import Squat_Info
from pages.squat_detection import Squat_Detection

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
  }