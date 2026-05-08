
import threading
from tracemalloc import start
import flet as ft

from components.file_picker_dialog import FolderPicker
from components.log_viewer import LogViewer
from services.document_processor import DocumentsProcesator
class ProcessorPage(ft.Column):
    def __init__(self, page: ft.Page ):
        super().__init__()
        self._page = page
        self.spacing = 20

        self.picker_source = FolderPicker(page, "📂Carpeta de Soportes")
        self.picker_dest = FolderPicker(page, "📤 Carpeta destino")

        self.log_viewer = LogViewer()
        self.progress_bar = ft.ProgressBar(width=400, visible=False)
        self.status_text = ft.Text("", weight=ft.FontWeight.BOLD)

        self.btn_procesar = ft.Button(
             "🚀 Procesar",
            icon=ft.Icons.PLAY_ARROW,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            on_click=self._start_processing
        )

        self.controls.extend([
             ft.Text("Procesador de Documentos", size=24, weight=ft.FontWeight.BOLD),
            self.picker_source.build(),
            self.picker_dest.build(),
            ft.Row([self.btn_procesar, self.status_text],
                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            self.progress_bar,
            ft.Text(" Logs:", weight=ft.FontWeight.BOLD),
            self.log_viewer,
        ])

    def _start_processing(self,e):
        """Valida y Lanza el procesamiento en segundo plano"""
        source = self.picker_source.path
        destination = self.picker_dest.path

        if not source or not destination:
            self._page.show_dialog(ft.SnackBar(ft.Text("⚠️ Selecciona ambas carpetas primero")))
            return

        self.btn_procesar.disabled = True
        self.progress_bar.visible =True
        self.log_viewer.clear()
        self._page.update()


        async def _update_status(msg: str):
            self.status_text.value = msg
            self._page.update()

        async def _update_log(msg: str):
            self.log_viewer.add_log(msg)
            self._page.update()


        def run_thread():
            try:
                self._page.run_task(_update_status, "⏳ Procesando...")
                processator = DocumentsProcesator(
                    source,
                    destination,
                    callback_log= self._add_log_async)

                result = processator.procesar()
                if result:
                    self._page.run_task(_update_status,"✅ Completado")
                    self._page.show_dialog(ft.SnackBar(
                        ft.Text(f"✅ Reporte: {result.name}"), open=True))
                else:
                    self.status_text.value = "❎ Error"

            except Exception as ex:
                self._page.show_dialog(ft.SnackBar(
                    ft.Text(f"💥 {str(ex)}"), open=True))
                self._page.update()
            finally:
                self._page.run_task(self._reset_ui)
        threading.Thread(target=run_thread,daemon=True).start()

    def _add_log_async(self,msg:str):
        self._page.run_task(self._update_log_ui,msg)

    async def _update_log_ui(self,msg:str):
        self.log_viewer.add_log(msg)
        self._page.update()

    async def _reset_ui(self):
        self.progress_bar.visible = False
        self.btn_procesar.disabled = False
        self._page.update()
