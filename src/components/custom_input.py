import flet as ft

def CustomInput(label, icon = None, password = False, read_only:bool =False ,expand = False):
    return ft.TextField(
        label,
        prefix_icon=icon,
        password=password,
        can_reveal_password=password,
        border_radius=12,
        filled=True,
        expand=expand,
        read_only=read_only
    )
