import flet as ft

class KeyCards:
    def __init__(self, wallet_page):
        self.wallet_page = wallet_page
        self.is_private_key_visible = False
        self.setup_components()

    def setup_components(self):
        self.public_key_text = ft.Text(
            value="",
            size=12,
            color=ft.colors.GREY_300,
            text_align=ft.TextAlign.CENTER,
        )

        self.private_key_text = ft.Text(
            value="•" * 56,
            size=12,
            color=ft.colors.GREY_300,
            text_align=ft.TextAlign.CENTER,
        )

        self.view_private_key_btn = ft.IconButton(
            icon=ft.icons.VISIBILITY,
            icon_color=ft.colors.INDIGO_200,
            on_click=self.toggle_private_key_visibility,
        )

        self.public_key_card = self.create_public_key_card()
        self.private_key_card = self.create_private_key_card()

    def create_public_key_card(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.KEY_OUTLINED, color=ft.colors.GREY_400),
                            ft.Text("Chave Pública", color=ft.colors.GREY_400),
                            ft.IconButton(
                                icon=ft.icons.COPY,
                                icon_color=ft.colors.INDIGO_200,
                                on_click=lambda e: self.wallet_page.copy_to_clipboard(
                                    e, self.public_key_text.value),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    self.public_key_text,
                ],
            ),
            padding=15,
            border_radius=15,
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.SURFACE_VARIANT),
            visible=False,
        )

    def create_private_key_card(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.SECURITY, color=ft.colors.GREY_400),
                            ft.Text("Chave Privada", color=ft.colors.GREY_400),
                            ft.Row(
                                controls=[
                                    self.view_private_key_btn,
                                    ft.IconButton(
                                        icon=ft.icons.COPY,
                                        icon_color=ft.colors.INDIGO_200,
                                        on_click=lambda e: self.wallet_page.copy_private_key(e),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    self.private_key_text,
                ],
            ),
            padding=15,
            border_radius=15,
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.SURFACE_VARIANT),
            visible=False,
        )
    
    def toggle_private_key_visibility(self, e):
        """Alterna o estado de visibilidade da chave privada."""
        if self.current_keypair:
            self.is_private_key_visible = not self.is_private_key_visible
            self.update_private_key_display()
            self.update_visibility_icon()
            e.page.update()
        
        # Atualiza a interface
        e.page.update()

    def update_private_key_display(self):
        """Atualiza o texto da chave privada com base no estado de visibilidade."""
        if self.current_keypair:  # Verifica se current_keypair não é None
            self.private_key_text.value = (
                self.current_keypair.secret if self.is_private_key_visible else self.get_hidden_private_key()
            )
        else:
            self.private_key_text.value = self.get_hidden_private_key()  # Ou você pode definir um valor padrão

    def get_hidden_private_key(self):
        """Retorna a chave privada oculta com 56 caracteres de '•'."""
        return "•" * 56