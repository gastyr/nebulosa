import flet as ft

class Navigation:
    def __init__(self, page, wallet_page):
        self.page = page
        self.wallet_page = wallet_page
        self.current_index = 0
        self.setup_pages()

    def setup_pages(self):
        from app.ui.pages.wallet_page import WalletPage
        from app.ui.pages.balance_page import BalancePage
        from app.ui.pages.transfer_page import TransferPage
        
        self.pages = [
            WalletPage(self.page),
            BalancePage(self.page),
            TransferPage(self.page),
        ]

    def build(self):
        return ft.Column(
            controls=[
                self.create_navigation_bar(),
                self.pages[self.current_index].build(),
            ],
            spacing=0,
        )

    def create_navigation_bar(self):
        return ft.NavigationBar(
            bgcolor=ft.colors.SURFACE_VARIANT,
            selected_index=self.current_index,
            on_change=self.change_tab,
            destinations=[
                ft.NavigationDestination(
                    icon=ft.icons.ACCOUNT_BALANCE_WALLET_OUTLINED,
                    selected_icon=ft.icons.ACCOUNT_BALANCE_WALLET,
                    label="Criar Carteira",
                ),
                ft.NavigationDestination(
                    icon=ft.icons.BALANCE_OUTLINED,
                    selected_icon=ft.icons.BALANCE,
                    label="Saldo",
                ),
                ft.NavigationDestination(
                    icon=ft.icons.SEND_OUTLINED,
                    selected_icon=ft.icons.SEND,
                    label="Transferir",
                ),
            ],
        )

    def create_nav_destination(self, icon, selected_icon, label):
        return ft.NavigationBarDestination(
            icon=icon,
            selected_icon=selected_icon,
            label=label
        )

    def change_tab(self, e):
        self.current_index = e.control.selected_index
        self.page.controls[0].controls[1] = self.pages[self.current_index].build()
        self.page.update()