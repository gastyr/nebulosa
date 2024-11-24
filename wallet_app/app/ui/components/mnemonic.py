import flet as ft
from typing import List

class MnemonicDisplay:
    def __init__(self, mnemonic_phrase: str):
        self.words = mnemonic_phrase.split()

    def _create_word_container(self, index: int, word: str) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(f"#{index + 1}", size=12, color=ft.colors.GREY_400, weight=ft.FontWeight.BOLD),
                    ft.Text(word, size=14, color=ft.colors.WHITE, weight=ft.FontWeight.W_500)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4
            ),
            bgcolor=ft.colors.BLUE_GREY_900,
            border_radius=8,
            padding=ft.padding.all(12),
            margin=ft.margin.all(4),
            width=160,
            height=70,
            alignment=ft.alignment.center,
        )

    def _create_word_columns(self) -> List[ft.Column]:
        word_containers = [
            self._create_word_container(i, word)
            for i, word in enumerate(self.words)
        ]
        
        return [
            ft.Column(
                controls=word_containers[:len(self.words)//2],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Column(
                controls=word_containers[len(self.words)//2:],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ]

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                controls=self._create_word_columns(),
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=ft.padding.all(16),
            alignment=ft.alignment.center,
        )