from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="bienpatrimonial",
            name="numero_compra",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="N° de Compra"
            ),
        ),
        migrations.AddField(
            model_name="bienpatrimonial",
            name="siem",
            field=models.DateField(blank=True, null=True, verbose_name="SIEM"),
        ),
    ]

