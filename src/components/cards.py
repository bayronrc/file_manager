import flet as ft

def DashboardCards(documents):
    procesados = len([d for d in documents if d["estado"]=="Procesado"])
    pendientes = len([d for d in documents if d["estado"]=="Pendiente"])
    errores = len([d for d in documents if d["estado"]=="Error"])
    return ft.Row(
        [
            ft.Container(
                content=ft.Text(f"Procesados : {procesados}"),
                 bgcolor=ft.Colors.GREEN,
                 padding=15,
                 border_radius=10
            ),
            ft.Container(
                content=ft.Text(f"Pendientes: {pendientes}"),
                bgcolor=ft.Colors.ORANGE,
                padding=15,
                border_radius=10
            ),
            ft.Container(
                content=ft.Text(f"Errores: {errores}"),
                bgcolor=ft.Colors.RED,
                padding=15,
                border_radius=10
            ),
        ],
        spacing=10
    )
