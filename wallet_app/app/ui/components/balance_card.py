import flet as ft
from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass
class BalanceInfo:
    asset_code: str
    balance: float
    asset_type: str
    asset_issuer: str = ''
    liquidity_pool_id: str = ''

class AssetTheme:
    COLORS: List[Tuple[str, str]] = [
        (ft.colors.BLUE, ft.colors.BLUE_700),
        (ft.colors.PURPLE, ft.colors.PURPLE_700),
        (ft.colors.TEAL, ft.colors.TEAL_700),
        (ft.colors.AMBER, ft.colors.AMBER_700),
        (ft.colors.PINK, ft.colors.PINK_700),
        (ft.colors.GREEN, ft.colors.GREEN_700),
        (ft.colors.ORANGE, ft.colors.ORANGE_700),
        (ft.colors.CYAN, ft.colors.CYAN_700),
    ]

    ICONS: Dict[str, str] = {
        'native': ft.icons.STARS,
        'liquidity_pool_shares': ft.icons.CURRENCY_EXCHANGE,
        'credit_alphanum4': ft.icons.ATTACH_MONEY,
        'credit_alphanum12': ft.icons.ATTACH_MONEY,
    }

    @classmethod
    def get_colors(cls, index: int) -> Tuple[str, str]:
        return cls.COLORS[index % len(cls.COLORS)]

    @classmethod
    def get_icon(cls, asset_type: str) -> str:
        return cls.ICONS.get(asset_type, ft.icons.QUESTION_MARK)

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
        primary_color, secondary_color = AssetTheme.get_colors(color_index)
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    BalanceCardBuilder._build_header(balance, primary_color),
                    BalanceCardBuilder._build_balance_text(balance.balance),
                    BalanceCardBuilder._build_additional_info(balance),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            margin=ft.margin.only(top=10),
            padding=20,
            border_radius=20,
            gradient=BalanceCardBuilder._create_gradient(secondary_color),
        )

    @staticmethod
    def _build_header(balance: BalanceInfo, primary_color: str) -> ft.Row:
        return ft.Row(
            controls=[
                ft.Icon(
                    AssetTheme.get_icon(balance.asset_type),
                    color=primary_color,
                    size=22,
                ),
                ft.Text(
                    balance.asset_code,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=primary_color,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    @staticmethod
    def _build_balance_text(balance: float) -> ft.Text:
        return ft.Text(
            f"{balance:.7f}",
            size=24,
            weight=ft.FontWeight.W_700,
            color=ft.colors.WHITE,
        )

    @staticmethod
    def _build_additional_info(balance: BalanceInfo) -> ft.Control:
        info = BalanceCardBuilder._get_additional_info_text(balance)
        if not info:
            return ft.Container()
            
        return ft.Text(
            info,
            size=12,
            color=ft.colors.GREY_400,
            text_align=ft.TextAlign.CENTER,
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

    @staticmethod
    def _create_gradient(secondary_color: str) -> ft.LinearGradient:
        return ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[
                ft.colors.with_opacity(0.3, secondary_color),
                ft.colors.with_opacity(0.1, ft.colors.SURFACE)
            ],
        )

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
                spacing=10,
            ),
        )