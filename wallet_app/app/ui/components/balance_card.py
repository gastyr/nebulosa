import flet as ft
from dataclasses import dataclass
from typing import List, Dict
from app.ui.styles import ColorScheme

@dataclass
class BalanceInfo:
    asset_code: str
    balance: float
    asset_type: str
    asset_issuer: str = ''
    liquidity_pool_id: str = ''

class AssetTheme:
    ICONS: Dict[str, str] = {
        'native': ft.icons.AUTO_AWESOME,
        'liquidity_pool_shares': ft.icons.CURRENCY_EXCHANGE,
        'credit_alphanum4': ft.icons.ATTACH_MONEY,
        'credit_alphanum12': ft.icons.ATTACH_MONEY,
    }

    @classmethod
    def get_icon(cls, asset_type: str) -> str:
        return cls.ICONS.get(asset_type, ft.icons.HELP_OUTLINE)

class BalanceProcessor:
    @staticmethod
    def process_balance(balance: Dict) -> BalanceInfo:
        asset_type = balance.get('asset_type', 'native')
        
        processors = {
            'liquidity_pool_shares': BalanceProcessor._process_pool_shares,
            'native': BalanceProcessor._process_native,
        }
        
        processor = processors.get(asset_type, BalanceProcessor._process_custom_asset)
        return processor(balance)

    @staticmethod
    def _process_pool_shares(balance: Dict) -> BalanceInfo:
        return BalanceInfo(
            asset_code='Pool Shares',
            balance=float(balance.get('balance', '0')),
            asset_type='liquidity_pool_shares',
            liquidity_pool_id=balance.get('liquidity_pool_id', '')
        )

    @staticmethod
    def _process_native(balance: Dict) -> BalanceInfo:
        return BalanceInfo(
            asset_code='XLM',
            balance=float(balance.get('balance', '0')),
            asset_type='native'
        )

    @staticmethod
    def _process_custom_asset(balance: Dict) -> BalanceInfo:
        return BalanceInfo(
            asset_code=balance.get('asset_code', 'Unknown'),
            balance=float(balance.get('balance', '0')),
            asset_type=balance.get('asset_type', 'unknown'),
            asset_issuer=balance.get('asset_issuer', '')
        )

class BalanceCardBuilder:
    @staticmethod
    def create_balance_card(balance: BalanceInfo, color_index: int) -> ft.Container:

        return ft.Container(
            content=ft.Row(
                controls=[
                    BalanceCardBuilder._build_icon(balance),
                    ft.Column(
                        controls=[
                            BalanceCardBuilder._build_asset_code(balance),
                            BalanceCardBuilder._build_balance_text(balance.balance),
                            BalanceCardBuilder._build_additional_info(balance),
                        ],
                        spacing=3,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                    ),
                ],
                spacing=10,
            ),
            margin=ft.margin.only(bottom=8),
            padding=ft.padding.only(left=15, right=15, top=10, bottom=10),
            border_radius=15,
            gradient=ColorScheme.get_card_gradient(color_index),
        )

    @staticmethod
    def _build_icon(balance: BalanceInfo) -> ft.Container:
        return ft.Container(
            content=ft.Icon(
                AssetTheme.get_icon(balance.asset_type),
                color=ColorScheme.STARDUST,
                size=20,
            ),
            padding=8,
        )

    @staticmethod
    def _build_asset_code(balance: BalanceInfo) -> ft.Text:
        return ft.Text(
            balance.asset_code,
            size=16,
            weight=ft.FontWeight.BOLD,
            color=ColorScheme.STARDUST,
        )

    @staticmethod
    def _build_balance_text(balance: float) -> ft.Text:
        return ft.Text(
            f"{balance:.7f}",
            size=14,
            weight=ft.FontWeight.BOLD,
            color=ColorScheme.MILKY_WAY_WHITE,
        )

    @staticmethod
    def _build_additional_info(balance: BalanceInfo) -> ft.Control:
        info = BalanceCardBuilder._get_additional_info_text(balance)
        if not info:
            return ft.Container()
            
        return ft.Text(
            info,
            size=12,
            color=ColorScheme.STARDUST,
        )

    @staticmethod
    def _get_additional_info_text(balance: BalanceInfo) -> str:
        if balance.asset_type == 'native':
            return "Native Asset"
        elif balance.asset_type == 'liquidity_pool_shares':
            return f"Pool ID: {balance.liquidity_pool_id[:4]}...{balance.liquidity_pool_id[-4:]}"
        elif balance.asset_issuer:
            return f"Issuer: {balance.asset_issuer[:4]}...{balance.asset_issuer[-4:]}"
        return ""

class BalanceDisplay:
    def __init__(self, balances: List[Dict]):
        self.balances = [BalanceProcessor.process_balance(balance) for balance in balances]

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    BalanceCardBuilder.create_balance_card(balance, idx)
                    for idx, balance in enumerate(self.balances)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            padding=ft.padding.only(left=20, right=20),
        )