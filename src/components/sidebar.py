
import flet as ft

def Sidebar(func,nav_items):
    return ft.NavigationRail(
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
        on_change=func
    )
