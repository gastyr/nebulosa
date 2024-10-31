import flet as ft
from app.ui.components.header import Header
from app.ui.components.balance_card import BalanceCard

class BalancePage:
    def __init__(self, page: ft.Page):
        self.page = page
        # self.wallet_app = wallet_app
        self.header = Header(page.window.width)
        self.balance_card = BalanceCard()
        
    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.header.build(),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.TextField(
                                    label="Chave Pública",
                                    hint_text="Digite sua chave pública Stellar",
                                    prefix_icon=ft.icons.KEY,
                                    on_submit=self.load_balance,
                                ),
                                ft.ElevatedButton(
                                    "Verificar Saldo",
                                    style=ft.ButtonStyle(
                                        color=ft.colors.WHITE,
                                        bgcolor=ft.colors.INDIGO_400,
                                    ),
                                    on_click=self.load_balance,
                                ),
                                self.balance_card.container,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=20,
                    ),
                ],
                spacing=0,
            ),
            width=self.page.window.width,
        )
    
    def load_balance(self, e):
        # Aqui você implementaria a lógica para carregar o saldo da carteira
        # Usando stellar_sdk para consultar a rede
        self.balance_card.container.visible = True
        self.balance_card.balance_amount.value = "1000.00"  # Exemplo
        self.page.update()