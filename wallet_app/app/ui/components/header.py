import flet as ft

class Header:
    def __init__(self, page_width):
        self.page_width = page_width

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(ft.icons.WALLET, 
                           size=50, 
                           color="#FFD700"),
                    ft.Text("Nebulosa", 
                           size=28, 
                           weight=ft.FontWeight.BOLD,
                           color="#FFFFFF"),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ "#4B0082", "transparent"],
            ),
            padding=ft.padding.only(top=20, bottom=20),
            width=self.page_width,
        )