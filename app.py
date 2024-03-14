import flet as ft
from views import views_handler

def main(page: ft.Page):
    page.title = "AR FIT PRO"
    page.scroll = "adaptive"

    def route_change(route):
        print(page.route)
        page.views.clear()
        page.title = "AR FIT PRO"
        page.scroll = "adaptive"
        page.views.append(
        views_handler(page)[page.route])


    page.on_route_change = route_change
    page.go('/')
ft.app(target=main)
# ft.app(target=main,view=ft.WEB_BROWSER)