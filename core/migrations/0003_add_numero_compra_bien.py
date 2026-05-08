from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_usuario_tema_oscuro"),
    ]

    operations = [
        migrations.AddField(
            model_name="bienpatrimonial",
            name="numero_compra",
            field=models.CharField(max_length=50, blank=True, default="", verbose_name="N° de Compra"),
            preserve_default=False,
        ),
    ]
