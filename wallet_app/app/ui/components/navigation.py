import flet as ft

class Navigation:
    def __init__(self, page):
        self.page = page
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
            expand=True,
            spacing=0,
            controls=[
                ft.Container(
                    content=self.create_navigation_bar(),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    padding=0,
                    height=65,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[self.pages[self.current_index].build()],
                        scroll=ft.ScrollMode.HIDDEN,
                        expand=True,
                        spacing=0,
                    ),
                    expand=True,
                    padding=0,
                ),
            ],
        )

    def create_navigation_bar(self):
        return ft.NavigationBar(
            bgcolor=ft.colors.SURFACE_VARIANT,
            selected_index=self.current_index,
            on_change=self.change_tab,
            height=65,
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.icons.WALLET_OUTLINED,
                    selected_icon=ft.icons.WALLET,
                    label="Criar Carteira",
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.ACCOUNT_BALANCE_OUTLINED,
                    selected_icon=ft.icons.ACCOUNT_BALANCE,
                    label="Saldo",
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.SEND_OUTLINED,
                    selected_icon=ft.icons.SEND,
                    label="Transferir",
                ),
            ],
        )

    def change_tab(self, e):
        self.current_index = e.control.selected_index
        page_content = self.page.controls[0].controls[1].content
        page_content.controls = [self.pages[self.current_index].build()]
        self.page.update()
