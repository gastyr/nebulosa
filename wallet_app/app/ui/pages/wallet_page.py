import flet as ft
from app.core.services import generate_wallet
from app.ui.components import Header, KeyCards, MnemonicDisplay, StylizedButton
import asyncio
from typing import Dict
from app.ui.styles import ColorScheme


class WalletPage:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.header = Header(page.window.width)
        self.key_cards = KeyCards(self)
        self.setup_components()

    def setup_components(self) -> None:
        self.loading = self._create_loading_indicator()
        self.mnemonic_container = self.create_mnemonic_container()

    def _create_loading_indicator(self) -> ft.Container:
        return ft.Container(
            content=ft.ProgressRing(
                width=40,
                height=40,
                color=ColorScheme.AURORA_BOREALIS,
            ),
            visible=False,
        )
    
    def create_mnemonic_container(self) -> ft.Container:
        return ft.Container(
            visible=False,
            alignment=ft.alignment.center,
            padding=ft.padding.only(bottom=20)
        )

    def create_content_container(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.create_wallet_button(),
                    self.key_cards.public_key_card,
                    self.key_cards.private_key_card,
                    self.loading,
                    self.mnemonic_container
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            padding=20,
        )

    def create_wallet_button(self) -> ft.Container:
        button = StylizedButton(ft.icons.ADD,
                                "Criar Nova Carteira",
                                self.create_wallet,
                                240)
        return button.build()
        
    def build(self) -> ft.Container:
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
    
    def _update_wallet_ui(self, wallet_data: Dict[str, str]) -> None:
        self.key_cards.update_public_key(wallet_data["public_key"])
        self.key_cards.update_private_key(wallet_data["private_key"])
        mnemonic_display = MnemonicDisplay(wallet_data["mnemonic"])
        self.mnemonic_container.content = mnemonic_display.build()
        self.page.update()

    async def _async_wallet_creation(self, e: ft.ControlEvent) -> None:
        try:
            wallet_data = await generate_wallet()
            self._update_wallet_ui(wallet_data)
            self.page.open(
                ft.SnackBar(
                    content=ft.Text("Carteira criada com sucesso!", color=ColorScheme.STARDUST),
                    bgcolor=ColorScheme.DARK_MATTER,
                    action="OK"
                )
            )

        except Exception as ex:
            self.page.open(
                ft.SnackBar(
                    content=ft.Text(f"Erro ao criar carteira: {str(ex)}", color=ColorScheme.STARDUST),
                    bgcolor=ColorScheme.DARK_MATTER,
                    action="OK"
                )
            )
        finally:
            e.control.disabled = False
            self.loading.visible = False
            self.mnemonic_container.visible = True
            self.page.update()
    
    def create_wallet(self, e) -> None:
        e.control.disabled = True
        self.loading.visible = True
        self.page.update()
        asyncio.run(self._async_wallet_creation(e))