import flet as ft
from app.ui.styles import ColorScheme  # Importe sua classe ColorScheme

class KeyCards:
    def __init__(self, wallet_page):
        self.wallet_page = wallet_page
        self.setup_components()

    def setup_components(self):
        self.public_key_text = ft.Text(
            value="",
            size=12,
            color=ColorScheme.STARDUST,
            text_align=ft.TextAlign.CENTER,
        )

        self.private_key_text = ft.TextField(
            value="",
            text_style=ft.TextStyle(
                size=12,
                color=ColorScheme.STARDUST
            ),
            color=ColorScheme.STARDUST,
            text_align=ft.TextAlign.CENTER,
            border=ft.InputBorder.NONE,
            read_only=True,
            multiline=True,
            password=True,
            can_reveal_password=True,
        )

        self.public_key_card = self.create_public_key_card()
        self.private_key_card = self.create_private_key_card()

    def create_public_key_card(self):
        inner_content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.KEY_OUTLINED, color=ColorScheme.STARDUST),
                            ft.Text("Chave Pública", color=ColorScheme.STARDUST, weight=ft.FontWeight.BOLD),
                            ft.IconButton(
                                icon=ft.icons.COPY,
                                icon_color=ColorScheme.NEBULA_GLOW,
                                on_click=lambda e: self.copy_to_clipboard(
                                    e, self.public_key_text.value),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    self.public_key_text,
                ],
            ),
            padding=10,
            border_radius=15,
            bgcolor=ft.colors.with_opacity(0.95, ColorScheme.GRAY),
        )
    
        return ft.Container(
            content=inner_content,
            gradient=ColorScheme.CARD_LIGHT,
            padding=ft.padding.only(top=1, left=1),
            border_radius=15,
        )

    def create_private_key_card(self):
        inner_content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.SECURITY, color=ColorScheme.STARDUST),
                            ft.Text("Chave Privada", color=ColorScheme.STARDUST, weight=ft.FontWeight.BOLD),
                            ft.IconButton(
                                icon=ft.icons.COPY,
                                icon_color=ColorScheme.NEBULA_GLOW,
                                on_click=lambda e: self.copy_to_clipboard(
                                    e, self.private_key_text.value),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    self.private_key_text,
                ],
            ),
            padding=10,
            bgcolor=ft.colors.with_opacity(0.95, ColorScheme.GRAY),
            border_radius=15,
            
            
        )

        return ft.Container(
            content=inner_content,
            gradient=ColorScheme.CARD_LIGHT,
            padding=ft.padding.only(top=1, left=1),
            border_radius=15,
        )

    def update_private_key(self, new_key):
        self.private_key_text.value = new_key
        self.private_key_text.update()

    def update_public_key(self, new_key):
        self.public_key_text.value = new_key
        self.public_key_text.update()
    
    def copy_to_clipboard(self, e, text):
        e.page.set_clipboard(text)
        e.page.open(
            ft.SnackBar(
                content=ft.Text(
                    "Copiado para a área de transferência!", 
                    color=ColorScheme.MILKY_WAY_WHITE
                ),
                bgcolor=ColorScheme.DARK_MATTER,
                action="OK"
            )
        )