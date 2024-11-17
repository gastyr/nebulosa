import flet as ft
from app.ui.components import Header, BalanceDisplay
from stellar_sdk import Server, Keypair
from stellar_sdk.exceptions import NotFoundError, BadResponseError
import asyncio
from typing import Optional, cast
from enum import Enum
from dataclasses import dataclass

class KeyType(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    INVALID = "invalid"

@dataclass
class KeyValidationResult:
    type: KeyType
    public_key: str = ""
    error_message: str = ""

class BalancePage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.header = Header(page.window.width)
        self.server = Server("https://horizon.stellar.org")
        self.setup_components()
        
    def setup_components(self):
        self.key_field = self.create_key_field()
        self.verify_button = self.create_verify_button()
        self.loading = self.create_loading_container()
        self.error_container = self.create_error_container()
        self.balance_container = self.create_balance_container()
    
    def create_loading_container(self):
        return ft.Container(
            content=ft.ProgressRing(
                width=40,
                height=40,
                color=ft.colors.INDIGO_400,
            ),
            visible=False,
        )
    
    def create_error_container(self) -> ft.Container:
        return ft.Container(
            content=ft.Text(
                color=ft.colors.RED_400,
                size=12,
            ),
            visible=False,
        )

    def update_error_message(self,
                           message: Optional[str] = None,
                           show: Optional[bool] = None):
        text_control = cast(ft.Text, self.error_container.content)
        if message is not None:
            text_control.value = message
        if show is not None:
            self.error_container.visible = show

    def create_balance_container(self):
        return ft.Container(
            content=ft.Column(
                controls=[],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            visible=False,
        )
    
    def create_key_field(self):
        return ft.TextField(
            label="Chave Stellar",
            hint_text="Digite sua chave Stellar",
            prefix_icon=ft.icons.KEY,
            on_submit=self.load_balance,
            border_color=ft.colors.INDIGO_400,
            text_size=12,
        )
    
    def create_verify_button(self):
        return ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.ACCOUNT_BALANCE),
                    ft.Text("Verificar Saldo", size=15),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.INDIGO_400,
                padding=20,
                animation_duration=500,
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            on_click=self.load_balance,
            width=200,
        )

    def create_content_container(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.key_field,
                    self.verify_button,
                    self.loading,
                    self.error_container,
                    self.balance_container,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=20,
        )

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.header.build(),
                    self.create_content_container(),
                ],
                spacing=0,
            ),
            width=self.page.window.width,
        )

    def validate_key(self, key: str | None) -> KeyValidationResult:
        if not key:
            return KeyValidationResult(
                type=KeyType.INVALID,
                error_message="Por favor, insira uma chave Stellar"
            )

        try:
            if key.startswith('G'):
                Keypair.from_public_key(key)
                return KeyValidationResult(
                    type=KeyType.PUBLIC,
                    public_key=key
                )
            elif key.startswith('S'):
                keypair = Keypair.from_secret(key)
                return KeyValidationResult(
                    type=KeyType.PRIVATE,
                    public_key=keypair.public_key
                )
            else:
                return KeyValidationResult(
                    type=KeyType.INVALID,
                    error_message="Chave inválida"
                )
        except Exception as ex:
            return KeyValidationResult(
                type=KeyType.INVALID,
                error_message=f"Chave inválida: {str(ex)}"
            )

    def load_balance(self, e):
        key = self.key_field.value
        validation_result = self.validate_key(key)
        
        if validation_result.type == KeyType.INVALID:
            self.update_error_message(validation_result.error_message, True)
            self.balance_container.visible = False
            self.loading.visible = False
            self.page.update()
            return

        e.control.disabled = True
        self.update_error_message(show=False)
        self.balance_container.visible = False
        self.loading.visible = True
        self.page.update()
        
        asyncio.run(self.account_balance(e, validation_result.public_key))

    def process_balance_entry(self, balance):
        asset_type = balance.get('asset_type', 'native')
        processed_balance = {
            'balance': balance.get('balance', '0'),
            'asset_type': asset_type,
            'asset_code': '',
            'asset_issuer': '',
            'liquidity_pool_id': ''
        }

        if asset_type == 'native':
            processed_balance['asset_code'] = 'XLM'
        elif asset_type == 'liquidity_pool_shares':
            processed_balance['asset_code'] = 'Pool Shares'
            processed_balance['liquidity_pool_id'] = balance.get('liquidity_pool_id', '')
        else:
            processed_balance['asset_code'] = balance.get('asset_code', '')
            processed_balance['asset_issuer'] = balance.get('asset_issuer', '')

        return processed_balance

    def process_balances(self, balances):
        processed_balances = [self.process_balance_entry(balance) for balance in balances]
        type_order = {
            'native': 0,
            'credit_alphanum4': 1,
            'credit_alphanum12': 1,
            'liquidity_pool_shares': 2
        }
        processed_balances.sort(
            key=lambda x: (
                type_order.get(x['asset_type'], 3),
                x.get('asset_code', '')
            )
        )
        return processed_balances
        
    async def account_balance(self, e, public_key: str):
        try:
            account = await self._fetch_account_data(public_key)
            if not account.get("balances"):
                self.update_error_message("Nenhum saldo encontrado", True)
                return
            processed_balances = self.process_balances(account["balances"])
            balance_display = BalanceDisplay(processed_balances)
            self.balance_container.content = balance_display.build()
            self.balance_container.visible = True
            self.page.update()
            
        except Exception as ex:
            self.page.open(
                ft.SnackBar(
                    content=ft.Text(f"Erro ao consultar saldo: {str(ex)}", color="white"),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    action="OK"
                )
            )
        finally:
            e.control.disabled = False
            self.loading.visible = False
            self.page.update()

    async def _fetch_account_data(self, public_key):
        try:
            await asyncio.sleep(0.5)
            return self.server.accounts().account_id(public_key).call()
        except NotFoundError:
            raise ValueError("Conta não encontrada. Verifique a chave.")
        except BadResponseError:
            raise ValueError("Erro ao conectar com a rede Stellar. Tente novamente.")
        except Exception as e:
            raise ValueError(f"Erro inesperado: {str(e)}")