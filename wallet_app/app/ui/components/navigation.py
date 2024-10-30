import flet as ft

class Navigation:
    def __init__(self, page, wallet_page):
        self.page = page
        self.wallet_page = wallet_page
        self.current_index = 0

    def build(self):
        return ft.Pagelet(
            navigation_bar=self.create_navigation_bar(),
            content=self.wallet_page.create_wallet_content(),
            expand=True,
        )

    def create_navigation_bar(self):
        return ft.CupertinoNavigationBar(
            bgcolor=ft.colors.BLUE_GREY_900,
            inactive_color=ft.colors.BLUE_GREY_300,
            active_color=ft.colors.BLUE_500,
            on_change=self.change_tab,
            destinations=[
                self.create_nav_destination(
                    ft.icons.ACCOUNT_BALANCE_WALLET_OUTLINED,
                    ft.icons.ACCOUNT_BALANCE_WALLET,
                    "Criar Carteira"
                ),
                self.create_nav_destination(
                    ft.icons.BALANCE_OUTLINED,
                    ft.icons.BALANCE,
                    "Saldo"
                ),
                self.create_nav_destination(
                    ft.icons.SEND_OUTLINED,
                    ft.icons.SEND,
                    "Transferir"
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
        contents = [
            self.wallet_page.create_wallet_content(),
            self.wallet_page.balance_content(),
            self.wallet_page.transfer_content()
        ]
        e.control.parent.content = contents[self.current_index]
        self.page.update()