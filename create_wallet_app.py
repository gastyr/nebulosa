import flet as ft
from stellar_sdk import Keypair, Server, Network, TransactionBuilder, Asset
from stellar_sdk.exceptions import NotFoundError
import time

class StellarWalletApp:
    def __init__(self):
        self.current_keypair = None
        ft.app(target=self.main)  # Definindo vista em coluna

    def copy_to_clipboard(self, e, text):
        e.page.set_clipboard(text)
        e.page.open(
            ft.SnackBar(
                content=ft.Text("Copiado para a área de transferência!", color="white"),
                bgcolor=ft.colors.SURFACE_VARIANT,
                action="OK"
            )
        )

    def create_wallet(self, e):
        try:
            self.loading.visible = True
            e.page.update()
            
            time.sleep(1)
            
            self.current_keypair = Keypair.random()

            self.public_key_text.value = self.current_keypair.public_key
            # self.private_key_text.value = self.current_keypair.secret
            self.private_key_text.value = "•" * 56

            self.public_key_card.visible = True
            self.private_key_card.visible = True
            self.check_balance_btn.disabled = False
            self.loading.visible = False
            
            e.page.update()
            
            e.page.open(
                ft.SnackBar(
                    content=ft.Text("Carteira criada com sucesso!", color="white"),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    action="OK"
                )
            )
            
        except Exception as ex:
            self.loading.visible = False
            e.page.update()
            e.page.open(
                ft.SnackBar(
                    content=ft.Text(f"Erro ao criar carteira: {str(ex)}", color="white"),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    action="OK"
                )
            )

    def toggle_private_key_visibility(self, e):
    # Verifica se o keypair atual existe antes de acessar "secret"
        if self.current_keypair:
            # Alterna entre mostrar a chave privada e exibir 56 pontos
            if self.private_key_text.value == "•" * 56:
                # Se a chave está oculta, exibe o valor real
                self.private_key_text.value = self.current_keypair.secret
                self.view_private_key_btn.icon = ft.icons.VISIBILITY_OFF
            else:
                # Se a chave está visível, oculta com pontos
                self.private_key_text.value = "•" * 56
                self.view_private_key_btn.icon = ft.icons.VISIBILITY
        
        # Atualiza a interface
        e.page.update()

    def check_balance(self, e):
        if not self.current_keypair:
            e.page.open(
                ft.SnackBar(
                    content=ft.Text("Crie uma carteira primeiro!", color="white"),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    action="OK"
                )
            )
            return

        try:
            self.loading.visible = True
            e.page.update()
            
            server = Server("https://horizon-testnet.stellar.org")
            account = server.accounts().account_id(self.current_keypair.public_key).call()
            
            time.sleep(1)
            
            self.balance_card.visible = True
            balances = []
            for balance in account['balances']:
                if balance['asset_type'] == 'native':
                    self.balance_amount.value = f"{float(balance['balance']):.2f}"
                    balances.append(f"XLM: {balance['balance']}")
                else:
                    balances.append(f"{balance['asset_code']}: {balance['balance']}")
            
            self.other_assets.value = " | ".join(balances[1:]) if len(balances) > 1 else "Nenhum outro ativo"
            self.loading.visible = False
            e.page.update()
            
        except NotFoundError:
            self.loading.visible = False
            self.balance_card.visible = False
            e.page.update()
            
            dlg = ft.AlertDialog(
                title=ft.Text("Conta não ativada"),
                content=ft.Text("Use o Friendbot para ativar sua conta na testnet."),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: self.close_dlg(e)),
                ],
            )
            e.page.dialog = dlg
            dlg.open = True
            e.page.update()
            
        except Exception as ex:
            self.loading.visible = False
            e.page.update()
            e.page.open(
                ft.SnackBar(
                    content=ft.Text(f"Erro ao verificar saldo: {str(ex)}", color="white"),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    action="OK"
                )
            )

    def close_dlg(self, e):
        e.page.dialog.open = False
        e.page.update()

    def copy_private_key(self, e):
        # Verifica se "current_keypair" existe antes de copiar a chave privada
        if self.current_keypair and self.current_keypair.secret:
            self.copy_to_clipboard(e, self.current_keypair.secret)
        else:
            print("Erro: Nenhuma chave privada foi carregada para copiar.")

    def main(self, page: ft.Page):
        page.title = "Stellar Wallet"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 0
        page.window.width = 430  # Largura padrão para mobile
        page.window.height = 932  # Altura padrão para mobile
        # page.scroll = "auto"  # Habilitando scroll na página
        
        # Tema escuro moderno
        page.theme = ft.Theme(
            color_scheme_seed="indigo",
            color_scheme=ft.ColorScheme(
                primary=ft.colors.INDIGO_400,
                surface=ft.colors.GREY_900,
                surface_tint=ft.colors.INDIGO_200,
            )
        )

        # Header com gradiente
        header = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(ft.icons.ACCOUNT_BALANCE_WALLET_ROUNDED, size=50, color=ft.colors.INDIGO_200),
                    ft.Text("Stellar Wallet", size=28, weight=ft.FontWeight.BOLD),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.colors.INDIGO_900, ft.colors.SURFACE],
            ),
            padding=ft.padding.only(top=60, bottom=20),
            width=page.window.width,
        )

        # Loading indicator
        self.loading = ft.ProgressRing(visible=False, width=20, height=20)

        # Cartão de saldo principal
        self.balance_amount = ft.Text(
            "0.00",
            size=48,
            weight=ft.FontWeight.W_900,
            color=ft.colors.INDIGO_200,
        )
        
        self.other_assets = ft.Text(
            "Nenhum outro ativo",
            size=14,
            color=ft.colors.GREY_400,
        )
        
        self.balance_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Seu Saldo", size=16, color=ft.colors.GREY_400),
                    self.balance_amount,
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.icons.CURRENCY_EXCHANGE, color=ft.colors.GREY_400, size=16),
                                self.other_assets,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        margin=ft.margin.only(top=5),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            margin=ft.margin.only(top=20, bottom=20),
            padding=30,
            border_radius=20,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.colors.with_opacity(0.2, ft.colors.INDIGO_700), 
                       ft.colors.with_opacity(0.1, ft.colors.SURFACE)],
            ),
            visible=False,
        )

        # Cartões de chaves
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

        self.public_key_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.KEY_OUTLINED, color=ft.colors.GREY_400),
                            ft.Text("Chave Pública", color=ft.colors.GREY_400),
                            ft.IconButton(
                                icon=ft.icons.COPY,
                                icon_color=ft.colors.INDIGO_200,
                                on_click=lambda e: self.copy_to_clipboard(e, self.public_key_text.value),
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

        self.private_key_card = ft.Container(
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
                                        on_click=lambda e: self.copy_private_key(e),
                                    ),
                                ],
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




        # Botões principais
        create_wallet_btn = ft.ElevatedButton(
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
            width=page.window.width - 40,
            on_click=self.create_wallet,
        )

        self.check_balance_btn = ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.REFRESH),
                    ft.Text("Atualizar Saldo"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.INDIGO_700,
                padding=20,
                animation_duration=500,
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            width=page.window.width - 40,
            on_click=self.check_balance,
            disabled=True,
        )

        # Container principal com scroll
        main_content = ft.Container(
            content=ft.Column(
                controls=[
                    header,
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                self.balance_card,
                                create_wallet_btn,
                                self.public_key_card,
                                self.private_key_card,
                                self.check_balance_btn,
                                self.loading,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=15,
                        ),
                        padding=20,
                    ),
                ],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
            ),
        )

        page.add(main_content)
        page.update()

if __name__ == "__main__":
    StellarWalletApp()