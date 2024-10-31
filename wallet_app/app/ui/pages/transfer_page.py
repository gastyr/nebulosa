import flet as ft
from app.ui.components.header import Header

class TransferPage:
    def __init__(self, page: ft.Page):
        self.page = page
        # self.wallet_app = wallet_app
        self.header = Header(page.window.width)
        
    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.header.build(),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.TextField(
                                    label="Destinatário",
                                    hint_text="Chave pública do destinatário",
                                    prefix_icon=ft.icons.PERSON,
                                ),
                                ft.TextField(
                                    label="Quantidade",
                                    hint_text="Quantidade de XLM",
                                    prefix_icon=ft.icons.ATTACH_MONEY,
                                    keyboard_type=ft.KeyboardType.NUMBER,
                                ),
                                ft.ElevatedButton(
                                    "Enviar",
                                    style=ft.ButtonStyle(
                                        color=ft.colors.WHITE,
                                        bgcolor=ft.colors.INDIGO_400,
                                    ),
                                    on_click=self.send_transaction,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                        ),
                        padding=20,
                    ),
                ],
                spacing=0,
            ),
            width=self.page.window.width,
        )
    
    def send_transaction(self, e):
        # Aqui você implementaria a lógica para enviar a transação
        # Usando stellar_sdk para criar e submeter a transação
        pass