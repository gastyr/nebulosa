import flet as ft
from typing import Callable

class StylizedButton:
    def __init__(self,
                 icon: str,
                 text: str,
                 on_click:Callable,
                 width: int | float
    ):
        self.icon = icon
        self.text = text
        self.on_click = on_click
        self.width = width

    def _create_content(self) -> ft.Row:
        return ft.Row(
            controls=[
                ft.Icon(self.icon, color="#FFD700"),
                ft.Text(
                    self.text,
                    color="#FFFFFF",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    
    def build(self) -> ft.Container:
        return ft.Container(
            ft.ElevatedButton(
                content=self._create_content(),
                style=ft.ButtonStyle(
                    padding=ft.padding.all(16),
                    shape=ft.RoundedRectangleBorder(radius=12),
                    elevation=5,
                ),
                on_click=self.on_click,
                width=self.width,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=["#4169E1", "#4B0082"],
            ),
            border_radius=12,
            padding=2,
        )