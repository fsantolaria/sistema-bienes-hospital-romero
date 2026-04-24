from io import BytesIO

import pandas as pd
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from core.models import ArchivoCargaMasiva, BienPatrimonial


User = get_user_model()


class CargaMasivaBienesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create_user(
            username="admincarga",
            password="1234",
            tipo_usuario="admin",
        )

    def setUp(self):
        self.client.force_login(self.usuario)

    def _crear_excel_simple(self, nombre="inventario.xlsx", hoja="Hoja1", descripcion="Monitor 24 pulgadas"):
        buffer = BytesIO()
        df = pd.DataFrame(
            [
                {
                    "n° id": "ID-100",
                    "descripcion": descripcion,
                    "cantidad": 1,
                    "n° serie": "SER-100",
                    "servicio": "CARDIOLOGIA",
                }
            ]
        )
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name=hoja)
        buffer.seek(0)
        return SimpleUploadedFile(
            nombre,
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    def _crear_excel_desde_filas(self, filas, nombre="inventario.xlsx", hoja="Hoja1"):
        buffer = BytesIO()
        df = pd.DataFrame(filas)
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name=hoja)
        buffer.seek(0)
        return SimpleUploadedFile(
            nombre,
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    def test_bloquea_excel_ya_cargado(self):
        url = reverse("carga_masiva")

        primer_archivo = self._crear_excel_simple("relevamiento.xlsx")
        respuesta_1 = self.client.post(url, {"archivo_excel": [primer_archivo]})

        self.assertEqual(respuesta_1.status_code, 302)
        self.assertEqual(BienPatrimonial.objects.count(), 1)
        self.assertEqual(ArchivoCargaMasiva.objects.count(), 1)

        segundo_archivo = self._crear_excel_simple("relevamiento-copia.xlsx")
        respuesta_2 = self.client.post(url, {"archivo_excel": [segundo_archivo]})

        mensajes = [m.message for m in get_messages(respuesta_2.wsgi_request)]

        self.assertEqual(respuesta_2.status_code, 302)
        self.assertEqual(BienPatrimonial.objects.count(), 1)
        self.assertEqual(ArchivoCargaMasiva.objects.count(), 1)
        self.assertTrue(any("Excel ya cargado" in mensaje for mensaje in mensajes))

    def test_actualiza_bien_si_el_excel_viene_con_cambios(self):
        url = reverse("carga_masiva")

        primer_archivo = self._crear_excel_simple("relevamiento.xlsx", descripcion="Monitor 24 pulgadas")
        respuesta_1 = self.client.post(url, {"archivo_excel": [primer_archivo]})

        self.assertEqual(respuesta_1.status_code, 302)
        self.assertEqual(BienPatrimonial.objects.count(), 1)

        segundo_archivo = self._crear_excel_simple("relevamiento-actualizado.xlsx", descripcion="Monitor 27 pulgadas")
        respuesta_2 = self.client.post(url, {"archivo_excel": [segundo_archivo]})
        mensajes = [m.message for m in get_messages(respuesta_2.wsgi_request)]

        self.assertEqual(respuesta_2.status_code, 302)
        self.assertEqual(BienPatrimonial.objects.count(), 1)
        self.assertEqual(BienPatrimonial.objects.get().descripcion, "Monitor 27 pulgadas")
        self.assertTrue(any("Actualizados: 1" in mensaje for mensaje in mensajes))

    def test_omite_filas_duplicadas_en_el_excel(self):
        url = reverse("carga_masiva")
        archivo = self._crear_excel_desde_filas(
            [
                {
                    "n° id": "ID-200",
                    "descripcion": "Electrocardiografo",
                    "cantidad": 1,
                    "n° serie": "SER-200",
                    "servicio": "CARDIOLOGIA",
                },
                {
                    "n° id": "ID-200",
                    "descripcion": "Electrocardiografo",
                    "cantidad": 1,
                    "n° serie": "SER-200",
                    "servicio": "CARDIOLOGIA",
                },
            ],
            nombre="duplicados.xlsx",
        )

        respuesta = self.client.post(url, {"archivo_excel": [archivo]})
        mensajes = [m.message for m in get_messages(respuesta.wsgi_request)]

        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(BienPatrimonial.objects.count(), 1)
        self.assertTrue(any("Duplicados omitidos: 1" in mensaje for mensaje in mensajes))

    def test_bloquea_excel_con_mismo_contenido_y_archivo_distinto(self):
        url = reverse("carga_masiva")

        primer_archivo = self._crear_excel_simple("relevamiento.xlsx", hoja="Original")
        respuesta_1 = self.client.post(url, {"archivo_excel": [primer_archivo]})

        self.assertEqual(respuesta_1.status_code, 302)
        self.assertEqual(BienPatrimonial.objects.count(), 1)
        self.assertEqual(ArchivoCargaMasiva.objects.count(), 1)

        segundo_archivo = self._crear_excel_simple("relevamiento-otro.xlsx", hoja="Copia")
        respuesta_2 = self.client.post(url, {"archivo_excel": [segundo_archivo]})
        mensajes = [m.message for m in get_messages(respuesta_2.wsgi_request)]

        self.assertEqual(respuesta_2.status_code, 302)
        self.assertEqual(BienPatrimonial.objects.count(), 1)
        self.assertEqual(ArchivoCargaMasiva.objects.count(), 1)
        self.assertTrue(any("Excel ya cargado" in mensaje for mensaje in mensajes))
