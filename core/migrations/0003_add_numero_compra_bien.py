from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_notificacion_eliminada_operador_dni_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="bienpatrimonial",
            name="numero_compra",
            field=models.CharField(max_length=50, blank=True, null=True, verbose_name="N° de Compra"),
        ),
    ]
