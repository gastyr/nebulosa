import flet as ft

class BalanceCard:
    def __init__(self, asset_code: str, balance: str, asset_type: str, asset_issuer: str = ''):
        self.asset_code = asset_code
        self.balance = float(balance)
        self.asset_type = asset_type
        self.asset_issuer = asset_issuer

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(
                                ft.icons.CURRENCY_EXCHANGE if self.asset_type != 'native' else ft.icons.STARS,
                                color=ft.colors.INDIGO_200,
                                size=24,
                            ),
                            ft.Text(
                                self.asset_code,
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.INDIGO_200,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text(
                        f"{self.balance:.7f}",
                        size=32,
                        weight=ft.FontWeight.W_900,
                        color=ft.colors.WHITE,
                    ),
                    ft.Text(
                        self.get_asset_info(),
                        size=12,
                        color=ft.colors.GREY_400,
                        text_align=ft.TextAlign.CENTER,
                    ) if self.asset_type != 'native' else ft.Container(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            margin=ft.margin.only(top=10),
            padding=20,
            border_radius=20,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    ft.colors.with_opacity(0.3, ft.colors.INDIGO_700),
                    ft.colors.with_opacity(0.1, ft.colors.SURFACE)
                ],
            ),
        )

    def get_asset_info(self):
        if len(self.asset_issuer) > 8:
            return f"Issuer: {self.asset_issuer[:4]}...{self.asset_issuer[-4:]}"
        return "Native Asset"