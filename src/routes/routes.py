import flet as ft

from pages.processor_page import ProcessorPage




def get_nav_items(page: ft.Page):
    return [
        {
            "label": "Reporte de Soportes",
            "icon": ft.Icons.DOCUMENT_SCANNER,   # ✅ lowercase (Flet ≥0.24)
            "view": ProcessorPage               # ✅ Referencia a clase, NO instanciada
        },
    ]

def setup_routes(page: ft.Page):
    nav_items = get_nav_items(page)

    # ✅ Contenedor explícito para vistas dinámicas
    content = ft.Container(expand=True)

    def navigation(e):
        index = e.control.selected_index
        if 0 <= index < len(nav_items):
            # ✅ Instanciar pasando `page` si tus vistas lo requieren
            content.content = nav_items[index]["view"](page)
            page.update()

    # ✅ Sidebar nativo de Flet (reemplaza tu componente custom si lo deseas)
    sidebar = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        on_change=navigation,
        destinations=[
            ft.NavigationRailDestination(
                icon=item["icon"],
                label=item["label"]
            ) for item in nav_items
        ]
    )

    #  Cargar vista inicial
    content.content = nav_items[0]["view"](page)

    page.add(
        ft.Row(
            [sidebar, ft.VerticalDivider(width=1), content],
            expand=True
        )
    )
