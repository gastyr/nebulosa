import flet as ft
from app.ui.components import Header, SuccessDialog, SuccessDialogData, StylizedButton
from app.ui.styles import ColorScheme
from stellar_sdk import Server, Keypair
import asyncio
from typing import Optional, cast
from decimal import Decimal
from app.core.models import OperationType, TransactionData, TransactionResult
from app.core.services import TransactionProcessor


class TransferPage:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.header = Header(page.window.width)
        self.server = Server("https://horizon.stellar.org")
        self.transaction_processor = TransactionProcessor(self.server)
        self.setup_components()

    def setup_components(self) -> None:
        self.recipient_field = self._create_text_field(
            "Endereço do Destinatário",
            "Digite a chave pública do destinatário",
            ft.icons.ACCOUNT_CIRCLE,
        )
        self.amount_field = self._create_number_field()
        self.private_key_field = self._create_private_key_field()
        self.asset_dropdown = self._create_asset_dropdown()
        self.memo_field = self._create_text_field(
            "Memo (Opcional)", "Digite um memo para a transação", ft.icons.NOTE
        )
        self.operation_type = self._create_operation_type()
        self.transfer_button = self._create_transfer_button()
        self.loading = self._create_loading_indicator()
        self.error_container = self._create_error_container()
        self.success_dialog = SuccessDialog(page=self.page)

    def _create_text_field(self, label: str, hint: str, icon: str) -> ft.TextField:
        return ft.TextField(
            label=label,
            hint_text=hint,
            prefix_icon=icon,
            border_color=ColorScheme.PRIMARY,
            color=ColorScheme.STARDUST,
            label_style=ft.TextStyle(size=14, color=ColorScheme.STARDUST),
            hint_style=ft.TextStyle(size=14, color=ColorScheme.STARDUST),
        )

    def _create_number_field(self) -> ft.TextField:
        return ft.TextField(
            label="Quantidade",
            hint_text="Digite a quantidade a ser transferida",
            prefix_icon=ft.icons.ATTACH_MONEY,
            border_color=ColorScheme.PRIMARY,
            color=ColorScheme.STARDUST,
            label_style=ft.TextStyle(size=14, color=ColorScheme.STARDUST),
            hint_style=ft.TextStyle(size=14, color=ColorScheme.STARDUST),
            keyboard_type=ft.KeyboardType.NUMBER,
        )

    def _create_private_key_field(self) -> ft.TextField:
        return ft.TextField(
            label="Chave Privada",
            hint_text="Digite sua chave privada",
            prefix_icon=ft.icons.SECURITY,
            border_color=ColorScheme.PRIMARY,
            color=ColorScheme.STARDUST,
            label_style=ft.TextStyle(size=14, color=ColorScheme.STARDUST),
            hint_style=ft.TextStyle(size=14, color=ColorScheme.STARDUST),
            password=True,
            can_reveal_password=True,
        )

    def _create_asset_dropdown(self) -> ft.Dropdown:
        return ft.Dropdown(
            label="Ativo",
            hint_text="Selecione o ativo",
            options=[
                ft.dropdown.Option("XLM (Nativo)"),
            ],
            border_color=ColorScheme.PRIMARY,
            color=ColorScheme.STARDUST,
            label_style=ft.TextStyle(size=14, color=ColorScheme.STARDUST),
            hint_style=ft.TextStyle(size=14, color=ColorScheme.STARDUST),
            value="XLM (Nativo)",
        )

    def _create_operation_type(self) -> ft.RadioGroup:
        return ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(value=OperationType.TRANSFER.value, label="Transferência"),
                    ft.Radio(
                        value=OperationType.CREATE_ACCOUNT.value, label="Criar Conta"
                    ),
                ]
            ),
            value=OperationType.TRANSFER.value,
            on_change=self._handle_operation_type_change,
        )

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

    def _create_transfer_button(self) -> ft.Container:
        button = StylizedButton(ft.icons.SEND, "Enviar", self._handle_transaction, 200)
        return button.build()

    def _handle_operation_type_change(self, e) -> None:
        is_create_account = e.control.value == OperationType.CREATE_ACCOUNT.value
        self.asset_dropdown.disabled = is_create_account
        self.asset_dropdown.value = (
            "XLM (Nativo)" if is_create_account else self.asset_dropdown.value
        )
        self.amount_field.label = (
            "Quantidade Inicial (XLM)" if is_create_account else "Quantidade"
        )
        self.page.update()

    def _validate_fields(self) -> Optional[str]:
        validations = [
            (lambda: not self.private_key_field.value, "A chave privada é obrigatória"),
            (lambda: not self.recipient_field.value, "O endereço do destinatário é obrigatório"),
            (lambda: not self.amount_field.value, "A quantidade é obrigatória"),
            (self._validate_amount, "Quantidade inválida"),
            (self._validate_private_key, "Chave privada inválida"),
            (self._validate_recipient, "Endereço do destinatário inválido"),
        ]

        for error_condition, error_message in validations:
            if error_condition():
                return error_message

        return None

    def _validate_amount(self) -> bool:
        amount_str = str(self.amount_field.value).strip()
        try:
            amount = Decimal(amount_str)
            return amount <= 0
        except Exception:
            return True

    def _validate_private_key(self) -> bool:
        private_key = str(self.private_key_field.value).strip()
        try:
            Keypair.from_secret(private_key)
            return False
        except Exception:
            return True

    def _validate_recipient(self) -> bool:
        recipient = str(self.recipient_field.value).strip()
        try:
            Keypair.from_public_key(recipient)
            return False
        except Exception:
            return True

    def _show_transaction_success(self, result: TransactionResult) -> None:
        operation_messages = {
            OperationType.TRANSFER: "A transação foi processada",
            OperationType.CREATE_ACCOUNT: "Conta criada",
        }

        if result.operation_type in operation_messages:
            dialog_data = SuccessDialogData(
                message=operation_messages[result.operation_type],
                hash=cast(str, result.hash),
            )
            self.success_dialog.update(dialog_data)
            self.success_dialog.show()

    def update_error_message(
        self, message: Optional[str] = None, show: Optional[bool] = None
    ) -> None:
        text_control = cast(ft.Text, self.error_container.content)
        if message is not None:
            text_control.value = message
        if show is not None:
            self.error_container.visible = show

    def _clear_fields(self) -> None:
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

    def _handle_transaction(self, e) -> None:
        e.control.disabled = True
        self.loading.visible = True
        self.error_container.visible = False
        self.page.update()
        asyncio.run(self._process_transaction(e))

    async def _process_transaction(self, e) -> None:
        try:
            error = self._validate_fields()
            if error:
                self.update_error_message(error, True)
                return

            transaction_data = TransactionData(
                source_secret=cast(str, self.private_key_field.value),
                destination_id=cast(str, self.recipient_field.value),
                amount=cast(str, self.amount_field.value),
                operation_type=OperationType(self.operation_type.value),
                memo=self.memo_field.value,
                asset_type=self.asset_dropdown.value,
            )

            result = await self.transaction_processor.process_transaction(
                transaction_data
            )

            if result.success:
                self._show_transaction_success(result)
                self._clear_fields()
            else:
                self.update_error_message(result.message, True)

        except Exception as ex:
            self.update_error_message(f"Erro inesperado: {str(ex)}", True)

        finally:
            e.control.disabled = False
            self.loading.visible = False
            self.page.update()
