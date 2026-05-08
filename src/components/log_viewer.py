from typing import Any

import flet as ft

class LogViewer(ft.Container):
    def __init__(self):
        super().__init__()
        self.logs = []
        self.text_log = ft.Text(value="", size=24)

        self.content = ft.Column(
            [self.text_log],
            scroll=ft.ScrollMode.AUTO,
            width=100000,
            height=150
        )
        self.padding = 15
        self.border = ft.Border.all(1,ft.Colors.OUTLINE)
        self.border_radius = 8
        self.bgcolor = ft.Colors.ON_SURFACE_VARIANT
        self.expand = True

    def add_log(self, mensaje:str):
        self.logs.append(mensaje)
        self.text_log.value = "\n".join(self.logs[-100:])
        self.update()

    def clear(self):
        self.logs.clear()
        self.text_log.value = ""
        self.update()
