# core/tests/test_models.py
from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from core.models import BienPatrimonial, Expediente
from core.constants import ORIGEN_COMPRA, ESTADO_ACTIVO


class ExpedienteModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.exp1 = Expediente.objects.create(
            numero_expediente="EXP-001",
            organismo_origen="Hospital Central",
            numero_compra="COMP-001",
            proveedor="Proveedor SA",
        )

    def test_creacion_ok(self):
        self.assertEqual(self.exp1.numero_expediente, "EXP-001")
        self.assertEqual(str(self.exp1), "EXP-001")

    def test_unicidad_numero_expediente(self):
        dup = Expediente(
            numero_expediente="EXP-001",  # repetido
            organismo_origen="Otro",
        )
        # Validamos a nivel modelo (sin golpear DB con IntegrityError)
        with self.assertRaises(ValidationError):
            dup.full_clean()

    def test_ordering_por_numero(self):
        Expediente.objects.create(numero_expediente="EXP-002")
        Expediente.objects.create(numero_expediente="EXP-000")
        nums = list(Expediente.objects.values_list("numero_expediente", flat=True))
        self.assertEqual(nums, sorted(nums))


class BienPatrimonialModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.exp = Expediente.objects.create(
            numero_expediente="EXP-100",
            organismo_origen="Hospital Central",
        )

    def test_creacion_minima_ok(self):
        bien = BienPatrimonial.objects.create(
            nombre="PC Escritorio",
            descripcion="Equipo de oficina",
            cantidad=1,
            expediente=self.exp,
            origen=ORIGEN_COMPRA,
            estado=ESTADO_ACTIVO,
            numero_identificacion="ID-001",
            valor_adquisicion=123.45,
        )
        # clean() se llama en el admin, acá validamos explícito
        bien.full_clean()
        self.assertEqual(bien.estado, ESTADO_ACTIVO)
        self.assertEqual(bien.expediente, self.exp)
        self.assertIn("PC Escritorio", str(bien))

    def test_valor_negativo_da_error(self):
        bien = BienPatrimonial(
            nombre="Silla",
            descripcion="Silla ergonómica",
            cantidad=1,
            origen=ORIGEN_COMPRA,
            numero_identificacion="ID-NEG",
            valor_adquisicion=-1,
        )
        with self.assertRaises(ValidationError):
            bien.full_clean()

    def test_fecha_adquisicion_futura_da_error(self):
        bien = BienPatrimonial(
            nombre="Impresora",
            descripcion="Laser",
            cantidad=1,
            origen=ORIGEN_COMPRA,
            numero_identificacion="ID-FUT",
            fecha_adquisicion=date.today() + timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            bien.full_clean()

    def test_origen_no_compra_borra_precio_en_clean(self):
        # Simulamos: setear un precio pero origen != COMPRA
        bien = BienPatrimonial(
            nombre="Donación de libros",
            descripcion="Lote de libros",
            cantidad=10,
            origen="DONACION",     # distinto a ORIGEN_COMPRA
            numero_identificacion="ID-DON",
            valor_adquisicion=500, # debería anularse
        )
        # clean() debería poner valor_adquisicion en None
        bien.clean()
        self.assertIsNone(bien.valor_adquisicion)

    def test_numero_identificacion_unico(self):
        BienPatrimonial.objects.create(
            nombre="Monitor",
            descripcion="24 pulgadas",
            cantidad=1,
            origen=ORIGEN_COMPRA,
            numero_identificacion="UNICO-1",
        )
        
        dup = BienPatrimonial(
            nombre="Monitor 2",
            descripcion="27 pulgadas",
            cantidad=1,
            origen=ORIGEN_COMPRA,
            numero_identificacion="UNICO-1",  # repetido
        )
        with self.assertRaises(ValidationError):
            dup.full_clean()
