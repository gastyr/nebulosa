import flet as ft

class ColorScheme:
    PRIMARY = "#4169E1"
    SECONDARY = "#4B0082"
    ACCENT = "#FFD700"
    COSMIC_PURPLE = "#9B30FF"
    COSMIC_PINK = "#FF69B4"
    STARDUST = "#E6E6FA"
    DEEP_SPACE = "#191970"
    NEBULA_GLOW = "#00CED1"
    STARRY_NIGHT = "#0B3D91"
    INTERSTELLAR_VIOLET = "#4A148C"
    CRIMSON_NEBULA = "#880E4F"
    STELLAR_INDIGO = "#1A237E"
    AURORA_TEAL = "#20B2AA"
    COSMIC_NAVY = "#00008B"
    BLACK_HOLE = "#000000"
    METEOR_GRAY = "#202020"
    BLUE_GRAY = "#1b1b21"
    GRAY = "#252528"
    AURORA_BOREALIS = "#5CE1E6"
    CRIMSON_COMET = "#FF4500"
    ANDROMEDA_VIOLET = "#6A0DAD"
    MILKY_WAY_WHITE = "#F8F8FF"
    NEBULA_PINK = "#F47174"
    DARK_MATTER = "#2C2C2C"
    CELESTIAL_CYAN = "#00FFFF"
    ECLIPSE_SHADOW = "#161616"
    WARNING = "#F47174"

    CARD_GRADIENTS = [
        ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[
                ft.colors.with_opacity(0.8, INTERSTELLAR_VIOLET),
                ft.colors.with_opacity(0.6, CRIMSON_NEBULA),
                ft.colors.with_opacity(0.3, STELLAR_INDIGO),
            ],
            stops=[0.0, 0.5, 1.0],
        ),
        ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[
                ft.colors.with_opacity(0.7, COSMIC_PURPLE),
                ft.colors.with_opacity(0.6, PRIMARY),
                ft.colors.with_opacity(0.3, AURORA_TEAL),
                
            ],
            stops=[0.0, 0.5, 1.0],
        ),
        ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[
                ft.colors.with_opacity(0.7, CRIMSON_COMET),
                ft.colors.with_opacity(0.6, ACCENT),
                ft.colors.with_opacity(0.3, COSMIC_PINK),
            ],
            stops=[0.0, 0.5, 1.0],
        ),
        ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[
                ft.colors.with_opacity(0.4, COSMIC_PURPLE),
                ft.colors.with_opacity(0.6, COSMIC_PINK),
                ft.colors.with_opacity(0.4, NEBULA_GLOW),
            ],
            stops=[0.0, 0.5, 1.0],
        ),
        ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[
                ft.colors.with_opacity(0.8, PRIMARY),
                ft.colors.with_opacity(0.5, NEBULA_GLOW),
                ft.colors.with_opacity(0.3, COSMIC_NAVY),
            ],
            stops=[0.0, 0.5, 1.0],
        ),
]

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
        colors=[PRIMARY, SECONDARY],
    )

    CARD_LIGHT = ft.LinearGradient(
        rotation=0.95,
        colors=[NEBULA_GLOW, GRAY],
        stops=[0.0, 0.4]
    )

    WORD_LIGHT = ft.LinearGradient(
        rotation=0.95,
        colors=[
            COSMIC_PURPLE,
            "transparent"
        ],
        stops=[0.0, 0.6]
    )

    NAV_GRADIENT = ft.LinearGradient(
        begin=ft.alignment.top_center,
        end=ft.alignment.bottom_center,
        colors=[ft.colors.TRANSPARENT, SECONDARY],
    )

    @classmethod
    def get_card_gradient(cls, index: int) -> ft.LinearGradient:
        return cls.CARD_GRADIENTS[index % len(cls.CARD_GRADIENTS)]