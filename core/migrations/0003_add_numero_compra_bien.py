# Generated manually to restore missing migration 0003
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = False

    dependencies = [
        ('core', '0002_notificacion_eliminada_operador_dni_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bienpatrimonial',
            name='numero_compra',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='N° de Compra'),
        ),
    ]
