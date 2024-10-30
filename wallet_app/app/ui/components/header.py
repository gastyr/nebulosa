import flet as ft

class Header:
    def __init__(self, page_width):
        self.page_width = page_width

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(ft.icons.ACCOUNT_BALANCE_WALLET_ROUNDED, 
                           size=50, 
                           color=ft.colors.INDIGO_200),
                    ft.Text("Stellar Wallet", 
                           size=28, 
                           weight=ft.FontWeight.BOLD),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.colors.INDIGO_900, ft.colors.SURFACE],
            ),
            padding=ft.padding.only(top=60, bottom=20),
            width=self.page_width,
        )