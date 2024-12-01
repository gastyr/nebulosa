import flet as ft
from typing import List
from app.ui.styles import ColorScheme

class MnemonicDisplay:
    def __init__(self, mnemonic_phrase: str):
        self.words = mnemonic_phrase.split()

    def _create_word_container(self, index: int, word: str) -> ft.Container:
        inner_content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(f"#{index + 1}", size=12, color=ColorScheme.CRIMSON_COMET, weight=ft.FontWeight.BOLD),
                    ft.Text(word, size=14, color=ColorScheme.STARDUST, weight=ft.FontWeight.W_500)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4
            ),
            bgcolor=ft.colors.with_opacity(0.4, ColorScheme.STELLAR_INDIGO),
            border_radius=8,
            padding=ft.padding.all(10),
            height=65,
            alignment=ft.alignment.center,
        )

        return ft.Container(
            content=inner_content,
            gradient=ColorScheme.WORD_LIGHT,
            border_radius=8,
        )

    def _create_word_columns(self) -> List[ft.Column]:
        column_count = 3
        columns = [[] for _ in range(column_count)]

        for index, word in enumerate(self.words):
            column_index = index % column_count
            columns[column_index].append(self._create_word_container(index, word))

        return [
            ft.Column(
                controls=column,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15,
                expand=True
            )
            for column in columns
        ]

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                controls=self._create_word_columns(),
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15,
                expand=True
            ),
            alignment=ft.alignment.center,
        )