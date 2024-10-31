import flet as ft
from stellar_sdk import Keypair, Server
from stellar_sdk.exceptions import NotFoundError
import time
from app.ui.components import Header, KeyCards

class WalletPage:
    def __init__(self, page: ft.Page):
        self.page = page
        # self.wallet_app = wallet_app
        self.header = Header(page.window.width)
        self.key_cards = KeyCards(self)
        
    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.header.build(),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.ElevatedButton(
                                    "Gerar Nova Carteira",
                                    style=ft.ButtonStyle(
                                        color=ft.colors.WHITE,
                                        bgcolor=ft.colors.INDIGO_400,
                                    ),
                                    on_click=self.generate_wallet,
                                ),
                                self.key_cards.public_key_card,
                                self.key_cards.private_key_card,
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
    
    def generate_wallet(self, e):
        # Aqui você implementaria a lógica de geração da carteira Stellar
        # Por exemplo, usando stellar_sdk
        self.key_cards.public_key_card.visible = True
        self.key_cards.private_key_card.visible = True
        self.page.update()