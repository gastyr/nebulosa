import flet as ft
from app.ui.components import Header, BalanceCard
from stellar_sdk import Server, Asset
from stellar_sdk.exceptions import NotFoundError, BadResponseError
import asyncio

class BalancePage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.header = Header(page.window.width)
        self.setup_components()
        self.server = Server("https://horizon-testnet.stellar.org")
        
    def setup_components(self):
        # Input field para a chave pública
        self.public_key_field = ft.TextField(
            label="Chave Pública",
            hint_text="Digite sua chave pública Stellar",
            prefix_icon=ft.icons.KEY,
            on_submit=self.load_balance,
            border_color=ft.colors.INDIGO_400,
            text_size=14,
        )
        
        # Botão de verificação com estado de loading
        self.verify_button = ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.ACCOUNT_BALANCE),
                    ft.Text("Verificar Saldo", size=14),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.INDIGO_400,
            ),
            on_click=self.load_balance,
            width=200,
        )
        
        # Progress bar para feedback visual
        self.progress_bar = ft.ProgressBar(
            color=ft.colors.INDIGO_400,
            bgcolor=ft.colors.INDIGO_100,
            visible=False,
        )
        
        # Mensagem de erro
        self.error_text = ft.Text(
            color=ft.colors.RED_400,
            size=14,
            visible=False,
        )
        
        # Cards de saldo
        self.balance_cards = []
        self.no_balance_text = ft.Text(
            "Nenhum saldo encontrado",
            color=ft.colors.GREY_400,
            size=14,
            visible=False,
        )

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.header.build(),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                self.public_key_field,
                                self.verify_button,
                                self.progress_bar,
                                self.error_text,
                                self.no_balance_text,
                                ft.Column(controls=self.balance_cards),
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

    async def fetch_account_data(self, public_key):
        try:
            account = await self.server.accounts().account_id(public_key).call()
            return account['balances']
        except NotFoundError:
            raise ValueError("Conta não encontrada. Verifique a chave pública.")
        except BadResponseError:
            raise ValueError("Erro ao conectar com a rede Stellar. Tente novamente.")
        except Exception as e:
            raise ValueError(f"Erro inesperado: {str(e)}")

    def create_balance_card(self, balance_data):
        asset_code = balance_data.get('asset_code', 'XLM')
        balance = balance_data.get('balance', '0')
        
        return BalanceCard(
            asset_code=asset_code,
            balance=balance,
            asset_type=balance_data.get('asset_type', 'native'),
            asset_issuer=balance_data.get('asset_issuer', '')
        ).build()

    async def load_balance(self, e):
        # Reset UI state
        self.error_text.visible = False
        self.progress_bar.visible = True
        self.no_balance_text.visible = False
        self.balance_cards.clear()
        self.page.update()

        try:
            public_key = self.public_key_field.value
            if not public_key:
                raise ValueError("Por favor, insira uma chave pública.")

            balances = await self.fetch_account_data(public_key)
            
            if not balances:
                self.no_balance_text.visible = True
            else:
                for balance in balances:
                    self.balance_cards.append(self.create_balance_card(balance))

        except ValueError as ve:
            self.error_text.value = str(ve)
            self.error_text.visible = True
        except Exception as e:
            self.error_text.value = "Erro inesperado ao carregar saldo."
            self.error_text.visible = True
        finally:
            self.progress_bar.visible = False
            self.page.update()