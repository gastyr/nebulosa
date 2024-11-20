import flet as ft
from app.ui.components import Header, SuccessDialog, SuccessDialogData
from stellar_sdk import (
    Server, Keypair, TransactionBuilder, Network, Asset,
    Account, exceptions
)
import asyncio
from typing import Optional, cast
from decimal import Decimal
from enum import Enum
from dataclasses import dataclass

class OperationType(Enum):
    TRANSFER = "transfer"
    CREATE_ACCOUNT = "create_account"

@dataclass
class TransactionResult:
    success: bool
    message: str
    hash: Optional[str] = None

@dataclass
class TransactionData:
    source_secret: str
    destination_id: str
    amount: str
    operation_type: OperationType
    memo: Optional[str] = None
    asset_type: Optional[str] = None

class TransactionProcessor:
    def __init__(self, server: Server):
        self.server = server

    async def check_account_exists(self, public_key: str) -> bool:
        try:
            self.server.accounts().account_id(public_key).call()
            return True
        except exceptions.NotFoundError:
            return False
        except exceptions.BadResponseError:
            return False
        except Exception as ex:
            raise ValueError(f"Erro ao checar conta destino: {str(ex)}")

    async def build_transaction(
        self,
        source_account: Account,
        data: TransactionData
    ) -> TransactionBuilder:
        base_fee = self.server.fetch_base_fee()
        builder = TransactionBuilder(
            source_account=source_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        )

        if data.operation_type == OperationType.CREATE_ACCOUNT:
            builder.append_create_account_op(
                destination=data.destination_id,
                starting_balance=data.amount
            )
        else:
            asset = Asset.native() if data.asset_type == "XLM (Nativo)" else None
            if asset is None:
                raise ValueError("Ativo não suportado")
            builder.append_payment_op(
                destination=data.destination_id,
                asset=asset,
                amount=data.amount
            )

        if data.memo:
            builder.add_text_memo(data.memo)

        return builder

    async def process_transaction(self, data: TransactionData) -> TransactionResult:
        try:
            source_keypair = Keypair.from_secret(data.source_secret)
            destination_exists = await self.check_account_exists(data.destination_id)
            
            if data.operation_type == OperationType.TRANSFER and not destination_exists:
                return TransactionResult(False, "A conta de destino não existe")
            elif data.operation_type == OperationType.CREATE_ACCOUNT and destination_exists:
                return TransactionResult(False, "A conta de destino já existe")

            source_account = self.server.load_account(source_keypair.public_key)
            transaction = await self.build_transaction(source_account, data)
            
            transaction = transaction.set_timeout(30).build()
            transaction.sign(source_keypair)
            
            response = self.server.submit_transaction(transaction)
            
            return TransactionResult(
                success=True,
                message="A transação foi processada com sucesso na rede Stellar.",
                hash=response['hash']
            )
            
        except Exception as e:
            return TransactionResult(False, f"Erro na transação: {str(e)}")
        
class TransferPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.header = Header(page.window.width)
        self.server = Server("https://horizon-testnet.stellar.org")
        self.transaction_processor = TransactionProcessor(self.server)
        self.setup_components()
    
    def setup_components(self):
        self.recipient_field = self._create_text_field(
            "Endereço do Destinatário",
            "Digite a chave pública do destinatário",
            ft.icons.ACCOUNT_CIRCLE
        )
        self.amount_field = self._create_number_field()
        self.private_key_field = self._create_private_key_field()
        self.asset_dropdown = self._create_asset_dropdown()
        self.memo_field = self._create_text_field(
            "Memo (Opcional)",
            "Digite um memo para a transação",
            ft.icons.NOTE
        )
        self.operation_type = self._create_operation_type()
        self.transfer_button = self._create_transfer_button()
        self.loading = self._create_loading_indicator()
        self.error_container = self._create_error_container()
        self.success_dialog = SuccessDialog(
            page=self.page,

        )
        
    def _create_text_field(self, label: str, hint: str, icon: str) -> ft.TextField:
        return ft.TextField(
            label=label,
            hint_text=hint,
            prefix_icon=icon,
            border_color="#4169E1",
            label_style=ft.TextStyle(size=14),
            hint_style=ft.TextStyle(size=14),
        )
    
    def _create_number_field(self) -> ft.TextField:
        return ft.TextField(
            label="Quantidade",
            hint_text="Digite a quantidade a ser transferida",
            prefix_icon=ft.icons.ATTACH_MONEY,
            border_color="#4169E1",
            label_style=ft.TextStyle(size=14),
            hint_style=ft.TextStyle(size=14),
            keyboard_type=ft.KeyboardType.NUMBER,
        )
    
    def _create_private_key_field(self):
        return ft.TextField(
            label="Chave Privada",
            hint_text="Digite sua chave privada",
            prefix_icon=ft.icons.SECURITY,
            border_color="#4169E1",
            label_style=ft.TextStyle(size=14),
            hint_style=ft.TextStyle(size=14),
            password=True,
            can_reveal_password=True,
        )

    def _create_asset_dropdown(self):
        return ft.Dropdown(
            label="Ativo",
            hint_text="Selecione o ativo",
            options=[
                ft.dropdown.Option("XLM (Nativo)"),
            ],
            border_color="#4169E1",
            label_style=ft.TextStyle(size=14),
            hint_style=ft.TextStyle(size=14),
            value="XLM (Nativo)",
        )
    
    def _create_operation_type(self):
        return ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value=OperationType.TRANSFER.value, label="Transferência"),
                ft.Radio(value=OperationType.CREATE_ACCOUNT.value, label="Criar Conta"),
            ]),
            value=OperationType.TRANSFER.value,
            on_change=self._handle_operation_type_change
        )
    
    def _create_loading_indicator(self) -> ft.Container:
        return ft.Container(
            content=ft.ProgressRing(
                width=40,
                height=40,
                color="#4169E1",
            ),
            visible=False,
        )
    
    def _create_error_container(self) -> ft.Container:
        return ft.Container(
            content=ft.Text(
                color=ft.colors.RED_400,
                size=12,
            ),
            visible=False,
        )
    
    def _create_transfer_button(self) -> ft.Container:
        return ft.Container(
            ft.ElevatedButton(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.icons.SEND, color="#FFD700"),
                        ft.Text(
                            "Enviar",
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
                on_click=self._handle_transaction,
                width=200,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=["#4169E1", "#4B0082"],
            ),
            border_radius=12,
            padding=2,
        )

    def _handle_operation_type_change(self, e):
        is_create_account = e.control.value == OperationType.CREATE_ACCOUNT.value
        self.asset_dropdown.disabled = is_create_account
        self.asset_dropdown.value = "XLM (Nativo)" if is_create_account else self.asset_dropdown.value
        self.amount_field.label = "Quantidade Inicial (XLM)" if is_create_account else "Quantidade"
        self.page.update()

    def _validate_fields(self) -> Optional[str]:
        if not self.private_key_field.value:
            return "A chave privada é obrigatória"
        if not self.recipient_field.value:
            return "O endereço do destinatário é obrigatório"
        if not self.amount_field.value:
            return "A quantidade é obrigatória"
        
        try:
            amount = Decimal(self.amount_field.value)
            if amount <= 0:
                return "A quantidade deve ser maior que zero"
        except Exception:
            return "Quantidade inválida"
        
        try:
            Keypair.from_secret(self.private_key_field.value)
        except Exception:
            return "Chave privada inválida"
        
        try:
            Keypair.from_public_key(self.recipient_field.value)
        except Exception:
            return "Endereço do destinatário inválido"
        
        return None


    def _show_transaction_success(self, result: TransactionResult):
        if result.hash:
            dialog_data = SuccessDialogData(
                title="Transação realizada com sucesso!",
                message="A transação foi processada",
                hash=result.hash
            )
            self.success_dialog.update(dialog_data)
            self.success_dialog.show()

    def _update_error_message(self, message: Optional[str] = None, show: Optional[bool] = None):
        text_control = cast(ft.Text, self.error_container.content)
        if message is not None:
            text_control.value = message
        if show is not None:
            self.error_container.visible = show

    def _clear_fields(self):
        self.recipient_field.value = ""
        self.amount_field.value = ""
        self.memo_field.value = ""
        self.private_key_field.value = ""

    def _create_content_container(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.private_key_field,
                    self.recipient_field,
                    self.asset_dropdown,
                    self.amount_field,
                    self.memo_field,
                    self.operation_type,
                    self.transfer_button,
                    self.loading,
                    self.error_container,
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
    
    def _handle_transaction(self, e):
        e.control.disabled = True
        self.loading.visible = True
        self.error_container.visible = False
        self.page.update()
        asyncio.run(self._process_transaction(e))

    async def _process_transaction(self, e):
        try:
            error = self._validate_fields()
            if error:
                self._update_error_message(error, True)
                return

            transaction_data = TransactionData(
                source_secret=cast(str, self.private_key_field.value),
                destination_id=cast(str, self.recipient_field.value),
                amount=cast(str, self.amount_field.value),
                operation_type=OperationType(self.operation_type.value),
                memo=self.memo_field.value,
                asset_type=self.asset_dropdown.value
            )

            result = await self.transaction_processor.process_transaction(transaction_data)
            
            if result.success:
                self._show_transaction_success(result)
                self._clear_fields()
            else:
                self._update_error_message(result.message, True)
                
        except Exception as ex:
            self._update_error_message(f"Erro inesperado: {str(ex)}", True)
        
        finally:
            e.control.disabled = False
            self.loading.visible = False
            self.page.update()