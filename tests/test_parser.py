"""
Tests para el parser de relevamientos Excel.

Cubre los 8 escenarios imprescindibles del spec:
1. Parser con Excel estilo Podología (headers en fila 3)
2. Parser con Excel estilo Neonatología (columnas distintas)
3. Parser con modelo limpio (headers en fila 1)
4. Parser con columna inventada ("CHAMUYO")
5. Parser con Excel vacío → EmptyWorkbookError
6. normalize_header con N° y newlines
7. Fila con "NO" → interpretado como vacío
8. Cantidad no numérica → default 1 + warning
"""
import os
import sys
from pathlib import Path

import pytest

# Agregar raíz al path para imports
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.parsers import (
    normalize_header,
    detect_data_sheet,
    detect_header_row,
    map_columns,
    parse_relevamiento,
    EmptyWorkbookError,
    HeaderNotFoundError,
)
from openpyxl import load_workbook

FIXTURES = Path(__file__).resolve().parent / "fixtures"


# ──────────────────────────────────────────────
# Test 6: normalize_header
# ──────────────────────────────────────────────

class TestNormalizeHeader:
    def test_degrees_newline_accents(self):
        result = normalize_header("N° DE EXPEDIENTE\nPOR DONACIÓN  ")
        assert result == "n de expediente por donacion"

    def test_ordinal(self):
        result = normalize_header("Nº DE SERIE")
        assert result == "n de serie"

    def test_empty(self):
        assert normalize_header("") == ""
        assert normalize_header(None) == ""

    def test_special_chars(self):
        result = normalize_header("ESTADO (ACTIVO/BAJA/DEFINITIVA /BAJA POR TRASLADO")
        assert result == "estado activo baja definitiva baja por traslado"


# ──────────────────────────────────────────────
# Test 1: Parser con Podología (headers en fila 3)
# ──────────────────────────────────────────────

class TestPodologia:
    def test_carga_correcta(self):
        path = str(FIXTURES / "relevamiento_podologia.xlsx")
        result = parse_relevamiento(path, default_year=2025)

        assert len(result.rows) == 4, f"Se esperaban 4 filas, se obtuvieron {len(result.rows)}"
        assert result.meta['header_row'] == 3

        # Primera fila
        row0 = result.rows[0]
        assert row0['numero_identificacion'] == 'POD-001'
        assert 'podológico' in row0['descripcion'].lower() or 'podologico' in row0['descripcion'].lower()
        assert row0['cantidad'] == 1
        assert row0['estado'] == 'ACTIVO'
        assert row0['numero_serie'] == 'SN-001'

        # Fila con estado MANTENIMIENTO
        row2 = result.rows[2]
        assert row2['estado'] == 'MANTENIMIENTO'

        # Fila con estado BAJA
        row3 = result.rows[3]
        assert row3['estado'] == 'BAJA'

    def test_columna_no_reconocida(self):
        path = str(FIXTURES / "relevamiento_podologia.xlsx")
        result = parse_relevamiento(path)
        # "N° ITEM" no debe matchear ningún sinónimo
        assert any("ITEM" in col.upper() for col in result.meta['columnas_no_reconocidas'])


# ──────────────────────────────────────────────
# Test 2: Parser con Neonatología (columnas distintas)
# ──────────────────────────────────────────────

class TestNeonatologia:
    def test_carga_correcta(self):
        path = str(FIXTURES / "relevamiento_neonatologia.xlsx")
        result = parse_relevamiento(path, default_year=2025)

        assert len(result.rows) == 3, f"Se esperaban 3 filas, se obtuvieron {len(result.rows)}"
        assert result.meta['header_row'] == 1

        row0 = result.rows[0]
        assert row0['numero_identificacion'] == 'NEO-001'
        assert 'monitor' in row0['descripcion'].lower()
        assert row0['cantidad'] == 2
        assert row0['estado'] == 'ACTIVO'

        # Fila con expediente por donación (no OC)
        row1 = result.rows[1]
        assert row1['_expediente_str'] == 'EX-DON-001'

        # Fila con serie "NO" → debe quedar vacío
        row2 = result.rows[2]
        assert row2['numero_serie'] == ''


# ──────────────────────────────────────────────
# Test 3: Parser con modelo limpio
# ──────────────────────────────────────────────

class TestModeloLimpio:
    def test_carga_correcta(self):
        path = str(FIXTURES / "modelo_limpio.xlsx")
        result = parse_relevamiento(path, default_year=2025)

        assert len(result.rows) == 2
        assert result.meta['header_row'] == 1

        row0 = result.rows[0]
        assert row0['numero_identificacion'] == 'LIM-001'
        assert row0['descripcion'] == 'Escritorio de oficina'
        assert row0['_expediente_str'] == 'EX-100'


# ──────────────────────────────────────────────
# Test 4: Columna inventada ("CHAMUYO")
# ──────────────────────────────────────────────

class TestColumnaInventada:
    def test_chamuyo_en_no_reconocidas(self):
        path = str(FIXTURES / "con_columna_inventada.xlsx")
        result = parse_relevamiento(path)

        assert 'CHAMUYO' in result.meta['columnas_no_reconocidas']
        # Pero los campos conocidos deben haberse cargado
        assert len(result.rows) == 1
        assert result.rows[0]['numero_identificacion'] == 'INV-001'


# ──────────────────────────────────────────────
# Test 5: Excel vacío → EmptyWorkbookError
# ──────────────────────────────────────────────

class TestVacio:
    def test_raises_empty_error(self):
        path = str(FIXTURES / "vacio.xlsx")
        with pytest.raises(EmptyWorkbookError):
            parse_relevamiento(path)


# ──────────────────────────────────────────────
# Test 7: Fila con "NO" como valor
# ──────────────────────────────────────────────

class TestValoresNO:
    def test_no_como_vacio(self):
        path = str(FIXTURES / "valores_no.xlsx")
        result = parse_relevamiento(path)

        assert len(result.rows) == 1
        row = result.rows[0]
        assert row['numero_serie'] == ''  # "NO" → vacío
        assert row['servicios'] == ''  # "NO" → vacío
        assert row['observaciones'] == ''  # "NO" → vacío


# ──────────────────────────────────────────────
# Test 8: Cantidad no numérica
# ──────────────────────────────────────────────

class TestCantidadNoNumerica:
    def test_default_1_con_warning(self):
        path = str(FIXTURES / "valores_no.xlsx")
        result = parse_relevamiento(path)

        row = result.rows[0]
        assert row['cantidad'] == 1  # "tres" → default 1
        assert any('cantidad' in w.lower() for w in result.warnings)
