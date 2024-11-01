import flet as ft
from stellar_sdk import Keypair
from app.ui.components import Header, KeyCards, MnemonicDisplay
import asyncio

class WalletPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.header = Header(page.window.width)
        self.key_cards = KeyCards(self)
        self.loading = self.create_loading_ring()
        self.current_keypair = None
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
        """Cria um container invisível para exibir o mnemonic."""
        return ft.Container(
            visible=False,  # Inicialmente invisível
            alignment=ft.alignment.center,
            # padding=ft.padding.all(16)
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
            ),
            padding=20,
        )

    def create_wallet_button(self):
        return ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.icons.ADD),
                            ft.Text("Criar Nova Carteira"),
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
                    width=self.page.window.width - 40 if self.page.window.width else self.page.width,
                    on_click=self.create_wallet
                )
        
    def build(self):
        """Constrói a página completa"""
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
        """Função assíncrona para criar a carteira"""
        await asyncio.sleep(1)
        return Keypair.random()

    async def _async_wallet_creation(self, e):
        """Função assíncrona real para criar a carteira e atualizar a interface"""
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
        """Handler para criação da carteira"""
        e.control.disabled = True
        self.loading.visible = True
        self.page.update()
        asyncio.run(self._async_wallet_creation(e))