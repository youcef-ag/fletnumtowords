import flet as ft
from num2words import num2words
import json
import os

def main(page: ft.Page):
    page.title = "Converter"
    page.window.width = 370
    page.window.height = 700

    # Variables globales
    max_digits = 35
    current_theme = ft.ThemeMode.DARK

    # Fichier de configuration pour sauvegarder les préférences
    config_file = "app_config.json"

    # Fonction pour charger la configuration
    def load_or_create_config():
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                return json.load(f)
        else:
            default_config = {"language": "en", "theme": "dark"}
            with open(config_file, "w") as f:
                json.dump(default_config, f)
            return default_config

    # Fonction pour sauvegarder la configuration
    def save_config(config):
        with open(config_file, "w") as f:
            json.dump(config, f)

# Load or create configuration
    config = load_or_create_config()
    current_language = config.get("language", "en")
    current_theme = ft.ThemeMode.DARK if config.get("theme", "dark") == "dark" else ft.ThemeMode.LIGHT

    page.theme_mode = current_theme  # Définir le thème sur la page
    
    languages = {
        "fr": "Français",
        "en": "English",
        "es": "Español"
    }

    class AppColors:
        @staticmethod
        def get_colors(theme_mode):
            if theme_mode == ft.ThemeMode.DARK:
                return {
                    "BG": "#201E43",
                    "PRIMARY": "#134B70",
                    "SECONDARY": "#508C9B",
                    "ON_PRIMARY": "#EEEEEE",
                    "SURFACE": "#201E43",
                    "INPUT_TEXT": "#EEEEEE",
                    "OUTPUT_TEXT": "#EEEEEE"
                }
            else:
                return {
                    "BG": "#D1E9F6",
                    "PRIMARY": "#F6EACB",
                    "SECONDARY": "#241D1F",
                    "ON_PRIMARY": "#241D1F",
                    "SURFACE": "#ECE1C8",
                    "INPUT_TEXT": "#000000",
                    "OUTPUT_TEXT": "#000000"
                }


    def update_theme_colors():
        colors = AppColors.get_colors(current_theme)
        page.bgcolor = colors["BG"]
        page.update()

        if input_field.page:
            input_field.bgcolor = colors["SURFACE"]
            input_field.border_color = colors["SECONDARY"]
            input_field.focused_border_color = colors["PRIMARY"]
            input_field.color = colors["INPUT_TEXT"]
            input_field.update()

        if output.page:
            output.color = colors["OUTPUT_TEXT"]
            output.update()

        if langue_utilisee.page:
            langue_utilisee.color = colors["SECONDARY"]
            langue_utilisee.update()

        if top_bar.page:
            top_bar.bgcolor = colors["PRIMARY"]
            top_bar.update()
        
        if settings_view.page:
            settings_view.bgcolor = colors["BG"]
            settings_view.controls[0].bgcolor = colors["PRIMARY"]
            for control in settings_view.controls[1].controls:
                if isinstance(control, ft.ListTile):
                    control.title.color = colors["ON_PRIMARY"]
            settings_view.update()  

    def change_theme(e):
        nonlocal current_theme
        current_theme = ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT
        page.theme_mode = current_theme
        update_theme_colors()
        config["theme"] = "dark" if current_theme == ft.ThemeMode.DARK else "light"
        save_config(config)

    def change_language(lang):
        nonlocal current_language
        current_language = lang
        langue_utilisee.value = languages[lang]
        config["language"] = lang
        save_config(config)
        update_conversion()

    def update_conversion():
        if input_field.page and output.page:
            try:
                if input_field.value:
                    number = int(input_field.value)
                    result = num2words(number, lang=current_language)
                    output.value = result.capitalize()
                else:
                    output.value = ""
                output.update()
            except ValueError:
                output.value = "Error"
                output.update()

    def convert_number(e):
        input_field.value = ''.join(filter(str.isdigit, input_field.value))[:max_digits]
        update_conversion()

    def open_settings(e):
        page.go("/settings")

    input_field = ft.TextField(
        label="Enter a number",
        on_change=convert_number,
        text_style=ft.TextStyle(size=18),
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    
    langue_utilisee = ft.Text(
        languages[current_language],
        size=12,
        weight=ft.FontWeight.NORMAL,
        text_align=ft.TextAlign.RIGHT,
    )

    output = ft.Text(
        size=20,
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.NORMAL
    )

    top_bar = ft.AppBar(
        title=ft.Text("Numbers to Words"),
        center_title=True,
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
                    ft.Container(height=20),
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
                        padding=ft.padding.symmetric(horizontal=20, vertical=10),
                        alignment=ft.alignment.top_center,
                    ),
                    ft.Container(height=20),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                spacing=15
                ),
                expand=True
            )
        ]
    )

    settings_view = ft.View(
        "/settings",
        [
            ft.AppBar(
                leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: page.go("/")),
                title=ft.Text("Settings"),
                center_title=False,
                bgcolor=AppColors.get_colors(current_theme)["PRIMARY"]
            ),
            ft.Column([
                ft.ListTile(
                    title=ft.Text("Dark theme"),
                    trailing=ft.Switch(
                        value=current_theme == ft.ThemeMode.DARK,
                        on_change=change_theme
                    )
                ),
                ft.ListTile(
                    title=ft.Text("Language"),
                    trailing=ft.Dropdown(
                        width=100,
                        options=[ft.dropdown.Option(code, label) for code, label in languages.items()],
                        value=current_language,
                        on_change=lambda e: change_language(e.control.value)
                    )
                ),
            ])
        ]
    )

    # Mettre à jour les couleurs une fois que la configuration est chargée
    update_theme_colors()
    
    def route_change(route):
        page.views.clear()
        page.views.append(main_view if page.route == "/" else settings_view)
        page.update()
        update_theme_colors()
        if page.route == "/":
            update_conversion()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
