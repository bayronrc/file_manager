# src/services/document_processor.py
import logging
import re
from pathlib import Path
from typing import Any, Callable, Optional
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

patron_factura = re.compile(r"FESI\d+", re.IGNORECASE)
patron_tipo = re.compile(r"^([A-Z]{1,8})_", re.IGNORECASE)


class DocumentsProcesator:
    def __init__(self, ruta_carpeta_soportes: str, ruta_destino: str,
                 callback_log: Optional[Callable[[str], Any]] = None):
        self.ruta_soportes = Path(ruta_carpeta_soportes)
        self.ruta_destino = Path(ruta_destino)
        self.callback_log = callback_log
        self.carpetas_soportes_extraidos = 0

    def _log(self, mensaje: str, nivel: str = "info"):
        getattr(logger, nivel)(mensaje)
        if self.callback_log:
            self.callback_log(f"[{nivel.upper()}] {mensaje}")

    def validar_configuracion_inicial(self) -> bool:
        if not self.ruta_soportes.exists():
            self._log("❌ La ruta no existe", "error")
            return False
        return True

    def crear_directorio_destino(self) -> None:
        self.ruta_destino.mkdir(parents=True, exist_ok=True)
        self._log(f"📁 Directorio: {self.ruta_destino}")

    def _extraer_numero_factura(self, file_path: str) -> str:
        match = patron_factura.search(file_path)
        if match:
            return match.group(0).upper()
        for parte in reversed(Path(file_path).parts):
            match = patron_factura.search(parte)
            if match:
                return match.group(0).upper()
        return "Desconocido"

    def _extraer_tipo_documento(self, nombre_archivo: str) -> str:
        match = patron_tipo.match(nombre_archivo)
        return match.group(1).upper() if match else "Desconocido"

    def _escanear_archivos(self) -> dict:
        datos = {}
        archivos = list(self.ruta_soportes.rglob("*.*"))
        self._log(f"🔍 Archivos encontrados: {len(archivos)}")

        for i, archivo in enumerate(archivos, 1):
            factura = self._extraer_numero_factura(str(archivo))
            print(factura)
            tipo = self._extraer_tipo_documento(archivo.name)

            if tipo == "Desconocido":
                continue

            if factura not in datos:
                datos[factura] = set()
            datos[factura].add(tipo)

            if i % 10 == 0:
                self._log(f"📊 Progreso: {i}/{len(archivos)}")

        self.carpetas_soportes_extraidos = len(datos)
        return datos

    def procesar(self) -> Optional[Path]:
        if not self.validar_configuracion_inicial():
            return None

        self.crear_directorio_destino()
        datos = self._escanear_archivos()

        if not datos:
            self._log("❌ No hay datos", "error")
            return None

        # Generar Excel
        todos_los_tipos = sorted({t for tipos in datos.values() for t in tipos})
        filas = []
        for factura, tipos_presentes in sorted(datos.items()):
            fila = {"Factura": factura}
            for tipo in todos_los_tipos:
                fila[tipo] = "✅" if tipo in tipos_presentes else "❌"
            filas.append(fila)

        df = pd.DataFrame(filas)
        ruta_excel = self.ruta_destino / "reporte_soportes.xlsx"
        df.to_excel(ruta_excel, index=False, engine="openpyxl")

        self._log(f"✅ Reporte: {ruta_excel}")
        return ruta_excel
