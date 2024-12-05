from stellar_sdk import (Server, Keypair, TransactionBuilder, Network, Asset, Account, exceptions)
from app.core.models import TransactionData, TransactionResult, OperationType, KeyType, KeyValidationResult
import asyncio
from typing import Dict, Any, List

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
            network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
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
                message="A transação foi processada com sucesso na rede Stellar",
                operation_type=data.operation_type,
                hash=response['hash']
            )
            
        except Exception as ex:
            return TransactionResult(False, f"Erro na transação: {str(ex)}")
        
    
class BalanceProcessor:
    def __init__(self, server: Server):
        self.server = server

    def validate_key(self, key: str | None) -> KeyValidationResult:
        if not key:
            return KeyValidationResult(
                type=KeyType.INVALID,
                error_message="Por favor, insira uma chave Stellar"
            )
        if len(key) != 56:
            return KeyValidationResult(
                type=KeyType.INVALID,
                error_message="Chave Stellar deve ter exatamente 56 caracteres"
            )

        try:
            if key.startswith('G'):
                Keypair.from_public_key(key)
                return KeyValidationResult(
                    type=KeyType.PUBLIC,
                    public_key=key
                )
            elif key.startswith('S'):
                keypair = Keypair.from_secret(key)
                return KeyValidationResult(
                    type=KeyType.PRIVATE,
                    public_key=keypair.public_key
                )
            else:
                return KeyValidationResult(
                    type=KeyType.INVALID,
                    error_message="Chave inválida"
                )
        except Exception as ex:
            return KeyValidationResult(
                type=KeyType.INVALID,
                error_message=f"Chave inválida: {str(ex)}"
            )
        
    async def fetch_account_data(self, public_key: str) -> Dict[str, Any]:
        try:
            await asyncio.sleep(0.2)
            return self.server.accounts().account_id(public_key).call()
        except exceptions.NotFoundError:
            raise ValueError("Conta não encontrada. Verifique a chave.")
        except exceptions.BadResponseError:
            raise ValueError("Erro ao conectar com a rede Stellar. Tente novamente.")
        except Exception as ex:
            raise ValueError(f"Erro inesperado: {str(ex)}")
        
    def process_balance_entry(self, balance: Dict[str, Any]) -> Dict[str, Any]:
        asset_type = balance.get('asset_type', 'native')
        processed_balance = {
            'balance': balance.get('balance', '0'),
            'asset_type': asset_type,
            'asset_code': '',
            'asset_issuer': '',
            'liquidity_pool_id': ''
        }

        if asset_type == 'native':
            processed_balance['asset_code'] = 'XLM'
        elif asset_type == 'liquidity_pool_shares':
            processed_balance['asset_code'] = 'Pool Shares'
            processed_balance['liquidity_pool_id'] = balance.get('liquidity_pool_id', '')
        else:
            processed_balance['asset_code'] = balance.get('asset_code', '')
            processed_balance['asset_issuer'] = balance.get('asset_issuer', '')

        return processed_balance

    def process_balances(self, balances: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        processed_balances = [self.process_balance_entry(balance) for balance in balances]
        type_order = {
            'native': 0,
            'credit_alphanum4': 1,
            'credit_alphanum12': 1,
            'liquidity_pool_shares': 2
        }
        processed_balances.sort(
            key=lambda x: (
                type_order.get(x['asset_type'], 3),
                x.get('asset_code', '')
            )
        )
        return processed_balances
    
async def generate_wallet() -> Dict[str, str]:
    await asyncio.sleep(1)
    keypair = Keypair.random()
    mnemonic_phrase = keypair.generate_mnemonic_phrase()
    return {
        "public_key": keypair.public_key,
        "private_key": keypair.secret,
        "mnemonic": mnemonic_phrase
    }