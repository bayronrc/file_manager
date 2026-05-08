from types import CoroutineType

import flet as ft

from components import CustomInput


class FolderPicker:
    """Componente reutilizable para seleccionar carpetas con la API actual"""
    def __init__(self,page: ft.Page, label: str = "Seleccionar Carpeta") -> None:

        self.page = page
        self.label = label
        self.text_field = CustomInput(label,read_only=True, expand=True)
        self.btn = ft.Button("Buscar", icon=ft.Icons.FOLDER_OPEN)
        self._selected_path: str | None = None
        self.btn.on_click = self._handle_pick

    @property
    def path(self):
        return self._selected_path

    async def _handle_pick(self, e):
        """Metodo async que llama a get_directory_path() y actualiza la UI"""
        try:
            result = await ft.FilePicker().get_directory_path(dialog_title="Selecciona una carpeta")

            if result:
                self._selected_path = result
                self.text_field.value = result
                self.page.update()
        except Exception as ex:
            self.page.show_dialog(
                ft.SnackBar(ft.Text(f"❌ Error: {str(ex)}"),open=True)
            )
    def build(self):
        return ft.Row([self.text_field, self.btn], spacing=10)
