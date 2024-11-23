import flet as ft
from stellar_sdk import Keypair
from app.ui.components import Header, KeyCards, MnemonicDisplay
import asyncio

class WalletPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.header = Header(page.window.width)
        self.key_cards = KeyCards(self)
        self.current_keypair = None
        self.setup_components()

    def setup_components(self):
        self.loading = self.create_loading_ring()
        self.mnemonic_container = self.create_mnemonic_container()

    def create_loading_ring(self):
        return ft.Container(
            content=ft.ProgressRing(
            width=40,
            height=40
            ),
            visible=False,
        )
    
    def create_mnemonic_container(self):
        return ft.Container(
            visible=False,
            alignment=ft.alignment.center,
        )

    def create_content_container(self):
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

    def create_wallet_button(self):
        return ft.Container(
            content=ft.ElevatedButton(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.icons.ADD, color="#FFD700"),
                        ft.Text(
                            "Criar Nova Carteira",
                            color="#FFFFFF",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                style=ft.ButtonStyle(
                    padding=ft.padding.all(16),
                    shape=ft.RoundedRectangleBorder(radius=12),
                    elevation=5,
                ),
                on_click=self.create_wallet,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=["#4169E1", "#4B0082"],
            ),
            border_radius=12,
            padding=2,
            width=self.page.window.width or 0 - 40,
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
    
    async def create_wallet_async(self):
        await asyncio.sleep(1)
        return Keypair.random()

    async def _async_wallet_creation(self, e):
        try:
            self.current_keypair = await self.create_wallet_async()
            self.key_cards.update_public_key(self.current_keypair.public_key)
            self.key_cards.update_private_key(self.current_keypair.secret)
            mnemonic_phrase = self.current_keypair.generate_mnemonic_phrase()
            mnemonic_display = MnemonicDisplay(mnemonic_phrase)
            self.mnemonic_container.content = mnemonic_display.build()
            self.page.update()
            self.page.open(
                ft.SnackBar(
                    content=ft.Text("Carteira criada com sucesso!", color="white"),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    action="OK"
                )
            )

        except Exception as ex:
            self.page.open(
                ft.SnackBar(
                    content=ft.Text(f"Erro ao criar carteira: {str(ex)}", color="white"),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    action="OK"
                )
            )
        finally:
            e.control.disabled = False
            self.loading.visible = False
            self.mnemonic_container.visible = True
            self.page.update()
    
    def create_wallet(self, e):
        e.control.disabled = True
        self.loading.visible = True
        self.page.update()
        asyncio.run(self._async_wallet_creation(e))