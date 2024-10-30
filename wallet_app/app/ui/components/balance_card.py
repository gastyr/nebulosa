import flet as ft

class BalanceCard:
    def __init__(self):
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
        self.container = self.build()

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Seu Saldo", size=16, color=ft.colors.GREY_400),
                    self.balance_amount,
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.icons.CURRENCY_EXCHANGE, 
                                       color=ft.colors.GREY_400, 
                                       size=16),
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
                colors=[
                    ft.colors.with_opacity(0.2, ft.colors.INDIGO_700),
                    ft.colors.with_opacity(0.1, ft.colors.SURFACE)
                ],
            ),
            visible=False,
        )