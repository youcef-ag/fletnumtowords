import flet as ft
from num2words import num2words

def main(page: ft.Page):
    page.title = "Convertisseur"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 400
    page.window.height = 600

    # Variables globales
    max_digits = 25
    current_language = 'fr'
    current_theme = ft.ThemeMode.DARK

    languages = {
        "fr": "Français",
        "en": "English",
        "es": "Español"
    }

    # Définition des couleurs du thème
    class AppColors:
        DARK_BG = "#121212"
        LIGHT_BG = "#F5F5F5"
        PRIMARY = "#6200EE"
        SECONDARY = "#03DAC6"
        ON_PRIMARY = "#FFFFFF"
        ON_SECONDARY = "#000000"
        SURFACE_DARK = "#1E1E1E"
        SURFACE_LIGHT = "#FFFFFF"

    def update_theme_colors():
        if current_theme == ft.ThemeMode.DARK:
            page.bgcolor = AppColors.DARK_BG
            input_field.bgcolor = AppColors.SURFACE_DARK
            input_field.border_color = AppColors.SECONDARY
            input_field.focused_border_color = AppColors.PRIMARY
            output.color = AppColors.SECONDARY
        else:
            page.bgcolor = AppColors.LIGHT_BG
            input_field.bgcolor = AppColors.SURFACE_LIGHT
            input_field.border_color = AppColors.PRIMARY
            input_field.focused_border_color = AppColors.SECONDARY
            output.color = AppColors.PRIMARY
        page.update()

    def change_theme(theme):
        nonlocal current_theme
        current_theme = theme
        page.theme_mode = theme
        update_theme_colors()

    def change_language(lang):
        nonlocal current_language
        current_language = lang
        langue_utilisee.value = languages[lang]  # Mise à jour du texte
        convert_number(None)
        langue_utilisee.update()  # Mise à jour uniquement de l'élément modifié        

    def convert_number(e):
        input_field.value = ''.join(filter(str.isdigit, input_field.value))[:max_digits]
        try:
            if input_field.value:
                number = int(input_field.value)
                result = num2words(number, lang=current_language)
                output.value = result.capitalize()
            else:
                output.value = ""
            output.update()
        except ValueError:
            output.value = "Erreur"
            output.update()

    def open_settings(e):
        page.go("/settings")

    input_field = ft.TextField(
        label="Entrez un nombre",
        on_change=convert_number,
        text_style=ft.TextStyle(color=AppColors.ON_PRIMARY, size=18),
        border_color=AppColors.SECONDARY,
        focused_border_color=AppColors.PRIMARY,
        cursor_color=AppColors.PRIMARY,
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    langue_utilisee = ft.Text(
        "Français",
        size=10,
        color=AppColors.SECONDARY,
        weight=ft.FontWeight.NORMAL,
        text_align=ft.TextAlign.RIGHT,
    )

    output = ft.Text(
        size=20,
        color=AppColors.SECONDARY,
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.BOLD
    )

    top_bar = ft.AppBar(
        title=ft.Text("Chiffres en Lettres"),
        center_title=False,
        bgcolor=AppColors.PRIMARY,
        actions=[
            ft.IconButton(icon=ft.icons.SETTINGS, on_click=open_settings)
        ]
    )

    main_view = ft.View(
        "/",
        [
            top_bar,
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=input_field,
                        padding=ft.padding.symmetric(horizontal=20),
                    ),
                    ft.Container(
                        content=langue_utilisee,
                        padding=ft.padding.symmetric(horizontal=20),
                        alignment=ft.alignment.top_right,
                    ),
                    ft.Container(
                        content=output,
                        padding=ft.padding.symmetric(horizontal=20),
                        alignment=ft.alignment.top_center,
                    ),
                    ft.Container(height=20),  # Espace supplémentaire en bas si nécessaire
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                spacing=10
                ),
                expand=True
            )
        ]
    )

    settings_view = ft.View(
        "/settings",
        [
            ft.AppBar(title=ft.Text("Paramètres"), bgcolor=AppColors.PRIMARY),
            ft.Column([
                ft.ListTile(
                    title=ft.Text("Thème sombre"),
                    trailing=ft.Switch(
                        value=current_theme == ft.ThemeMode.DARK,
                        on_change=lambda e: change_theme(ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT)
                    )
                ),
                ft.ListTile(
                    title=ft.Text("Langue"),
                    trailing=ft.Dropdown(
                        width=100,
                        options=[ft.dropdown.Option(label, code) for label, code in languages.items()],
                        value=current_language,
                        on_change=lambda e: change_language(e.control.value)
                    )
                ),
                ft.ElevatedButton("Retour", on_click=lambda _: page.go("/"))
            ])
        ]
    )

    def route_change(route):
        page.views.clear()
        page.views.append(main_view if page.route == "/" else settings_view)
        update_theme_colors()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
