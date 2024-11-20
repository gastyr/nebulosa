from dataclasses import dataclass
import flet as ft


class NebulosaPalette:
    PRIMARY = "#4169E1"      
    SECONDARY = "#4B0082"    
    ACCENT = "#FFD700"       
    COSMIC_PURPLE = "#9B30FF"  
    COSMIC_PINK = "#FF69B4"   
    STARDUST = "#E6E6FA"    
    DEEP_SPACE = "#191970"    
    NEBULA_GLOW = "#00CED1" 

    BORDER_GRADIENT = ft.LinearGradient(
        begin=ft.alignment.top_left,
        end=ft.alignment.bottom_right,
        colors=[
            COSMIC_PINK,
            COSMIC_PURPLE,
            NEBULA_GLOW,
        ],
    )

    BUTTON_GRADIENT = ft.LinearGradient(
        begin=ft.alignment.center_left,
        end=ft.alignment.center_right,
        colors=[
            PRIMARY,
            SECONDARY
        ],
    )


@dataclass
class SuccessDialogData:
    title: str
    message: str
    hash: str = ""


class SuccessDialog:
    def __init__(self, page: ft.Page) -> None:
        self.page: ft.Page = page
        self._message_text = self._create_message_text()
        self._hash_text = self._create_hash_text()
        self._explorer_button = self._create_explorer_button()
        self._dialog: ft.AlertDialog = self._create_dialog()
        self.page.overlay.append(self._dialog)

    def _create_message_text(self):
        return ft.Text(
            "",
            size=16,
            color=NebulosaPalette.STARDUST,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.W_500,
        )
    
    def _create_hash_text(self):
        return ft.Text(
            "",
            size=14,
            color=NebulosaPalette.STARDUST,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.W_400,
        )
    
    def _create_explorer_button(self):
        return ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.OPEN_IN_NEW, color=NebulosaPalette.STARDUST),
                    ft.Text(
                        "Stellar Expert",
                        color=NebulosaPalette.STARDUST,
                        size=14,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                tight=True
            ),
            url="",
            style=ft.ButtonStyle(
                padding=ft.padding.all(15),
                bgcolor=ft.colors.TRANSPARENT,
                elevation={"pressed": 0, "": 0},
            ),
        )

    def _create_status_icon(self) -> ft.Container:
        return ft.Container(
            content=ft.Icon(
                name=ft.icons.CHECK_CIRCLE_ROUNDED,
                color=ft.colors.GREEN_600,
                size=64,
            ),
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=8,
                blur_radius=20,
                color=ft.colors.with_opacity(0.3, ft.colors.GREEN_600),
            ),
            margin=ft.margin.only(bottom=15)
        )


    def _create_message_section(self) -> ft.Container:
        return ft.Container(
            content=self._message_text,
            margin=ft.margin.only(bottom=15),
            padding=ft.padding.symmetric(horizontal=20)
        )

    def _create_hash_section(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Hash da Transação",
                        size=16,
                        color=NebulosaPalette.COSMIC_PURPLE,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(
                        content=ft.SelectionArea(
                            content=self._hash_text
                        ),

                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            margin=ft.margin.only(bottom=15, top=5)
        )


    def _create_stellar_button(self, label: str) -> ft.Container:
        return ft.Container(
            content=self._explorer_button,
            margin=ft.margin.only(bottom=20, top=20),
            gradient=NebulosaPalette.BUTTON_GRADIENT,
            border_radius=30,
        )
    
    def _create_content(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    self._create_status_icon(),
                    self._create_message_section(),
                    self._create_hash_section(),
                    self._create_stellar_button("Stelar Expert"),
                    self._create_action_buttons(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                tight=True,
            ),
            padding=ft.padding.all(15),
            bgcolor="#121212",
            border_radius=12,
        )

    def _create_action_buttons(self) -> ft.Row:
        return ft.Row(
            controls=[
                ft.TextButton(
                    "Copiar Hash",
                    on_click=lambda _: self._handle_copy(),
                    style=ft.ButtonStyle(
                        color={"": NebulosaPalette.STARDUST}
                    ),
                ),
                ft.TextButton(
                    "Fechar",
                    on_click=lambda _: self.hide(),
                    style=ft.ButtonStyle(
                        color={"": NebulosaPalette.STARDUST}
                    ),
                ),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.END,
        )

    def _create_dialog(self) -> ft.AlertDialog:
        inner_content = self._create_content()
        outer_content = ft.Container(
            content=inner_content,
            gradient=NebulosaPalette.BORDER_GRADIENT,
            padding=ft.padding.all(2),
            border_radius=12,
        )

        return ft.AlertDialog(
            modal=True,
            content=outer_content,
            bgcolor=ft.colors.TRANSPARENT,
        )

    def _handle_copy(self) -> None:
        if self._hash_text.value:
            self._copy_transaction_hash(self._hash_text.value)

    def _copy_transaction_hash(self, hash_text: str) -> None:
        self.page.set_clipboard(hash_text)
        self.hide()

    def _get_stellar_expert_url(self, hash: str) -> str:
        return f"https://stellar.expert/explorer/testnet/tx/{hash}"
    
    def _get_stellar_explorer_url(self, hash: str) -> str:
        return f"https://testnet.stellarchain.io/transactions/{hash}"

    def update(self, data: SuccessDialogData) -> None:
        self._message_text.value = data.message
        self._hash_text.value = data.hash
        self._explorer_button.url = self._get_stellar_expert_url(data.hash)
        self.show()

    def show(self) -> None:
        self._dialog.open = True
        self.page.update()

    def hide(self) -> None:
        self._dialog.open = False
        self.page.update()