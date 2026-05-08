from pdb import run
from anyio import Path
import flet as ft
from routes import routes



async def main(page: ft.Page):

    # =========================
    # CONFIGURACIÓN GENERAL
    # =========================
    font_dir = await Path(__file__).resolve()
    page.title = "Dashboard de Documentos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.icon = str(font_dir.parent/"assets"/"icon.png")
    page.padding = 0
    page.spacing = 0
    page.fonts = {
        "Geist Mono Regular": str(font_dir.parent/ "assets" / "fonts"/"GeistMono-Regular.ttf"),
        "Geist Mono Bold":    str(font_dir.parent/ "assets" / "fonts"/"GeistMono-Bold.ttf"),
        "Geist Mono Black":   str(font_dir.parent/ "assets" / "fonts"/"GeistMono-Black.ttf"),
    }
    page.theme = ft.Theme(
          font_family="Geist Mono Regular"
    )
    # =========================
    # NAVIGATION
    # =========================
    nav_items = routes.get_nav_items(page)
    content_area = ft.Container(expand=True,padding=20)
    def on_nav_change(e):
        idx = e.control.selected_index
        if 0 <= len(nav_items):
            view_class = nav_items[idx]['view']
            content_area.content = view_class(page)
            page.update()

    sidebar = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=110,
        min_extended_width=180,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=item["icon"],
                label=item["label"],
                padding=10
            ) for item in nav_items
        ],
        on_change=on_nav_change
    )

    content_area.content = nav_items[0]["view"](page)


    page.add(
        ft.Row(
            [
                sidebar,
                ft.VerticalDivider(width=1),
                content_area
            ],
            expand=True
        )
    )

ft.run(main,view=ft.AppView.FLET_APP,assets_dir="assets" )
