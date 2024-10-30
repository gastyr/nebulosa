import flet as ft
from stellar_sdk import Keypair, Server
from stellar_sdk.exceptions import NotFoundError
import time
from components import Header, BalanceCard, KeyCards

class WalletPage:
    def __init__(self, page, app):
        self.page = page
        self.app = app
        self.current_dialog = None
        self.is_private_key_visible = False
        self.setup_components()

    def setup_components(self):
        self.header = Header(self.page.window.width)
        self.balance_card = BalanceCard()
        self.key_cards = KeyCards(self)
        self.loading = ft.ProgressRing(visible=False, width=20, height=20)
        self.setup_buttons()

    def setup_buttons(self):
        self.create_wallet_btn = self.create_button(
            "Criar Nova Carteira",
            ft.icons.ADD,
            ft.colors.INDIGO_400,
            self.create_wallet
        )
        
        self.check_balance_btn = self.create_button(
            "Atualizar Saldo",
            ft.icons.REFRESH,
            ft.colors.INDIGO_700,
            self.check_balance,
            disabled=True
        )

    def create_button(self, text, icon, color, on_click, disabled=False):
        return ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(icon),
                    ft.Text(text),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=color,
                padding=20,
                animation_duration=500,
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            width=self.page.window.width - 40,
            on_click=on_click,
            disabled=disabled
        )
    
    def create_wallet(self, e):
        try:
            self.loading.visible = True
            e.page.update()
            
            time.sleep(1)
            
            self.current_keypair = Keypair.random()
            self.is_private_key_visible = False
            self.public_key_text.value = self.current_keypair.public_key
            self.update_private_key_display()
            self.update_visibility_icon()

            # Exibe os cartões das chaves e habilita o botão de verificação de saldo
            self.public_key_card.visible = True
            self.private_key_card.visible = True
            self.check_balance_btn.disabled = False
            self.loading.visible = False
            
            e.page.update()
            

            # Gera o mnemonic usando o método da chave
            mnemonic_phrase = self.current_keypair.generate_mnemonic_phrase()
            print(mnemonic_phrase)
            if mnemonic_phrase:
                # Exibir o mnemonic na interface
                mnemonic_display = self.display_mnemonic(mnemonic_phrase)
                e.page.add(mnemonic_display)
                e.page.open(
                    ft.SnackBar(
                        content=ft.Text("Anote seu mnemonic!", color="white"),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        action="OK"
                    )
                )

            else:
                e.page.open(
                    ft.SnackBar(
                        content=ft.Text("Falha ao gerar o mnemonic", color="white"),
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

    def update_visibility_icon(self):
        """Atualiza o ícone do botão de visibilidade com base no estado."""
        self.view_private_key_btn.icon = (
            ft.icons.VISIBILITY_OFF if self.is_private_key_visible else ft.icons.VISIBILITY
        )

    def display_mnemonic(self, mnemonic_phrase):
        words = mnemonic_phrase.split()
        num_words = len(words)
        rows = []
        
        # Cria uma linha para cada par de palavras
        for i in range(0, num_words, 2):
            row_controls = []
            # Processa até duas palavras por linha
            for j in range(2):
                if i + j < num_words:
                    # Cria um container para cada palavra
                    word_container = ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    f"#{i+j+1}",  # Número da palavra
                                    size=12,
                                    color=ft.colors.GREY_400,
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.Text(
                                    words[i+j],
                                    size=14,
                                    color=ft.colors.WHITE,
                                    weight=ft.FontWeight.W_500
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=4
                        ),
                        bgcolor=ft.colors.BLUE_GREY_900,
                        border_radius=8,
                        padding=ft.padding.all(12),
                        margin=ft.margin.all(4),
                        width=160,  # Largura fixa para todos os containers
                        height=70,  # Altura fixa para todos os containers
                        alignment=ft.alignment.center,
                    )
                    row_controls.append(word_container)
            
            # Adiciona a linha com os containers das palavras
            rows.append(
                ft.Row(
                    controls=row_controls,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )
        
        # Retorna o container principal com todas as linhas
        return ft.Container(
            content=ft.Column(
                controls=rows,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            padding=ft.padding.all(16),
            alignment=ft.alignment.center,
        )
    
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
            
            self.current_dialog = ft.AlertDialog(
                title=ft.Text("Conta não ativada"),
                content=ft.Text("Use o Friendbot para ativar sua conta na testnet."),
                actions=[
                    ft.TextButton("OK", on_click=self.close_dlg),
                ],
            )
            e.control.page.overlay.append(self.current_dialog)
            self.current_dialog.open = True
            e.control.page.update()
            
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