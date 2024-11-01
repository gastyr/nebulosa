import flet as ft
from app.ui.components import Navigation

class StellarWalletApp:
    def __init__(self):
        ft.app(target=self.main)

    def main(self, page: ft.Page):
        self.setup_page_config(page)
        navigation = Navigation(page)
        page.add(navigation.build())
        page.update()

    def setup_page_config(self, page: ft.Page):
        page.title = "Stellar Wallet"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 0
        page.window.width = 430
        page.window.height = 732
        page.window.resizable = False
        page.theme = self.create_theme()

    def create_theme(self):
        return ft.Theme(
            color_scheme_seed="indigo",
            color_scheme=ft.ColorScheme(
                primary=ft.colors.INDIGO_400,
                surface=ft.colors.GREY_900,
                surface_tint=ft.colors.INDIGO_200,
            )
        )
