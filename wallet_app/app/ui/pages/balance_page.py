import flet as ft
from app.ui.components import Header, BalanceDisplay, StylizedButton
from app.ui.styles import ColorScheme
from stellar_sdk import Server
import asyncio
from typing import Optional, cast
from app.core.models import KeyType
from app.core.services import BalanceProcessor


class BalancePage:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.header = Header(page.window.width)
        self.server = Server("https://horizon.stellar.org")
        self.balance_processor = BalanceProcessor(self.server)
        self.setup_components()
        
    def setup_components(self) -> None:
        self.key_field = self._create_key_field()
        self.verify_button = self._create_verify_button()
        self.loading = self._create_loading_indicator()
        self.error_container = self._create_error_container()
        self.balance_container = self._create_balance_container()
    
    def _create_loading_indicator(self) -> ft.Container:
        return ft.Container(
            content=ft.ProgressRing(
                width=40,
                height=40,
                color=ColorScheme.AURORA_BOREALIS,
            ),
            visible=False,
        )
    
    def _create_error_container(self) -> ft.Container:
        return ft.Container(
            content=ft.Text(
                color=ColorScheme.WARNING,
                size=12,
            ),
            visible=False,
        )

    def update_error_message(
            self,
            message: Optional[str] = None,
            show: Optional[bool] = None
    ) -> None:
        text_control = cast(ft.Text, self.error_container.content)
        if message is not None:
            text_control.value = message
        if show is not None:
            self.error_container.visible = show

    def _create_balance_container(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            visible=False,
        )
    
    def _create_key_field(self) -> ft.TextField:
        return ft.TextField(
            label="Chave Stellar",
            hint_text="Digite sua chave Stellar",
            prefix_icon=ft.icons.KEY,
            on_submit=self._load_balance,
            border_color=ColorScheme.PRIMARY,
            color=ColorScheme.STARDUST,
            label_style=ft.TextStyle(size=14, color=ColorScheme.STARDUST),
            hint_style=ft.TextStyle(size=14, color=ColorScheme.STARDUST),
        )
    
    def _create_verify_button(self) -> ft.Container:
        button = StylizedButton(ft.icons.ACCOUNT_BALANCE,
                                "Verificar Saldo",
                                self._load_balance,
                                200)
        return button.build()
    
    def _create_content_container(self) -> ft.Container:
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

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.header.build(),
                    self._create_content_container(),
                ],
                spacing=0,
            ),
            width=self.page.window.width,
        )

    def _load_balance(self, e) -> None:
        key = self.key_field.value
        validation_result = self.balance_processor.validate_key(key)
        
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
        
        asyncio.run(self._account_balance(e, validation_result.public_key))
        
    async def _account_balance(self, e, public_key: str) -> None:
        try:
            account = await self.balance_processor.fetch_account_data(public_key)
            if not account.get("balances"):
                self.update_error_message("Nenhum saldo encontrado", True)
                return
            processed_balances = self.balance_processor.process_balances(account["balances"])
            balance_display = BalanceDisplay(processed_balances)
            self.balance_container.content = balance_display.build()
            self.balance_container.visible = True
            self.page.update()
            
        except Exception as ex:
            self.page.open(
                ft.SnackBar(
                    content=ft.Text(f"Erro ao consultar saldo: {str(ex)}", color="white"),
                    bgcolor=ColorScheme.DARK_MATTER,
                    action="OK"
                )
            )
        finally:
            e.control.disabled = False
            self.loading.visible = False
            self.page.update()