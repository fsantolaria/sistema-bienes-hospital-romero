from django.db import migrations, models


def rellenar_numero_doc(apps, schema_editor):
    """Asigna un numero_doc temporal a usuarios que no tienen uno."""
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM core_usuario WHERE numero_doc IS NULL ORDER BY id")
        rows = cursor.fetchall()
        for i, (uid,) in enumerate(rows, start=1):
            cursor.execute(
                "UPDATE core_usuario SET numero_doc = %s WHERE id = %s",
                [f'TEMP{i:06d}', uid],
            )


def rebuild_all(apps, schema_editor):
    """
    Reconstruye todas las tablas que tienen FK a core_usuario para que
    apunten a numero_doc (varchar) en lugar de id (integer).
    Orden: primero las tablas hija, luego core_usuario.
    """
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA foreign_keys = OFF")
        try:
            # ── core_usuario_groups ──────────────────────────────────────────
            cursor.execute("""
                CREATE TABLE "core_usuario_groups_new" (
                    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                    "usuario_id" varchar(50) NOT NULL REFERENCES "core_usuario" ("numero_doc") DEFERRABLE INITIALLY DEFERRED,
                    "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED
                )
            """)
            cursor.execute("""
                INSERT INTO "core_usuario_groups_new" (id, usuario_id, group_id)
                SELECT g.id, u.numero_doc, g.group_id
                FROM "core_usuario_groups" g
                JOIN "core_usuario" u ON u.id = g.usuario_id
            """)
            cursor.execute('DROP TABLE "core_usuario_groups"')
            cursor.execute('ALTER TABLE "core_usuario_groups_new" RENAME TO "core_usuario_groups"')
            cursor.execute('CREATE UNIQUE INDEX "core_usuario_groups_usuario_id_group_id_bde3c750_uniq" ON "core_usuario_groups" ("usuario_id", "group_id")')
            cursor.execute('CREATE INDEX "core_usuario_groups_usuario_id_97385234" ON "core_usuario_groups" ("usuario_id")')
            cursor.execute('CREATE INDEX "core_usuario_groups_group_id_55312a9a" ON "core_usuario_groups" ("group_id")')

            # ── core_usuario_user_permissions ────────────────────────────────
            cursor.execute("""
                CREATE TABLE "core_usuario_user_permissions_new" (
                    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                    "usuario_id" varchar(50) NOT NULL REFERENCES "core_usuario" ("numero_doc") DEFERRABLE INITIALLY DEFERRED,
                    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED
                )
            """)
            cursor.execute("""
                INSERT INTO "core_usuario_user_permissions_new" (id, usuario_id, permission_id)
                SELECT p.id, u.numero_doc, p.permission_id
                FROM "core_usuario_user_permissions" p
                JOIN "core_usuario" u ON u.id = p.usuario_id
            """)
            cursor.execute('DROP TABLE "core_usuario_user_permissions"')
            cursor.execute('ALTER TABLE "core_usuario_user_permissions_new" RENAME TO "core_usuario_user_permissions"')
            cursor.execute('CREATE UNIQUE INDEX "core_usuario_user_permissions_usuario_id_permission_id_7a048d24_uniq" ON "core_usuario_user_permissions" ("usuario_id", "permission_id")')
            cursor.execute('CREATE INDEX "core_usuario_user_permissions_usuario_id_ce4108a7" ON "core_usuario_user_permissions" ("usuario_id")')
            cursor.execute('CREATE INDEX "core_usuario_user_permissions_permission_id_7f881653" ON "core_usuario_user_permissions" ("permission_id")')

            # ── django_admin_log ─────────────────────────────────────────────
            cursor.execute("""
                CREATE TABLE "django_admin_log_new" (
                    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                    "object_id" text NULL,
                    "object_repr" varchar(200) NOT NULL,
                    "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0),
                    "change_message" text NOT NULL,
                    "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
                    "user_id" varchar(50) NOT NULL REFERENCES "core_usuario" ("numero_doc") DEFERRABLE INITIALLY DEFERRED,
                    "action_time" datetime NOT NULL
                )
            """)
            cursor.execute("""
                INSERT INTO "django_admin_log_new" (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time)
                SELECT l.id, l.object_id, l.object_repr, l.action_flag, l.change_message, l.content_type_id, u.numero_doc, l.action_time
                FROM "django_admin_log" l
                JOIN "core_usuario" u ON u.id = l.user_id
            """)
            cursor.execute('DROP TABLE "django_admin_log"')
            cursor.execute('ALTER TABLE "django_admin_log_new" RENAME TO "django_admin_log"')
            cursor.execute('CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id")')
            cursor.execute('CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id")')

            # ── core_notificacion ─────────────────────────────────────────────
            cursor.execute("""
                CREATE TABLE "core_notificacion_new" (
                    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                    "mensaje" varchar(255) NOT NULL,
                    "leida" bool NOT NULL,
                    "fecha" datetime NOT NULL,
                    "usuario_id" varchar(50) NOT NULL REFERENCES "core_usuario" ("numero_doc") DEFERRABLE INITIALLY DEFERRED,
                    "eliminada" bool NOT NULL
                )
            """)
            cursor.execute("""
                INSERT INTO "core_notificacion_new" (id, mensaje, leida, fecha, usuario_id, eliminada)
                SELECT n.id, n.mensaje, n.leida, n.fecha, u.numero_doc, n.eliminada
                FROM "core_notificacion" n
                JOIN "core_usuario" u ON u.id = n.usuario_id
            """)
            cursor.execute('DROP TABLE "core_notificacion"')
            cursor.execute('ALTER TABLE "core_notificacion_new" RENAME TO "core_notificacion"')
            cursor.execute('CREATE INDEX "core_notificacion_usuario_id_f14c4107" ON "core_notificacion" ("usuario_id")')

            # ── core_operador ─────────────────────────────────────────────────
            cursor.execute("""
                CREATE TABLE "core_operador_new" (
                    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                    "nombre_completo" varchar(200) NOT NULL,
                    "telefono" varchar(20) NOT NULL,
                    "direccion" varchar(300) NOT NULL,
                    "fecha_creacion" datetime NOT NULL,
                    "fecha_actualizacion" datetime NOT NULL,
                    "usuario_id" varchar(50) NOT NULL UNIQUE REFERENCES "core_usuario" ("numero_doc") DEFERRABLE INITIALLY DEFERRED,
                    "dni" varchar(20) NULL UNIQUE
                )
            """)
            cursor.execute("""
                INSERT INTO "core_operador_new" (id, nombre_completo, telefono, direccion, fecha_creacion, fecha_actualizacion, usuario_id, dni)
                SELECT o.id, o.nombre_completo, o.telefono, o.direccion, o.fecha_creacion, o.fecha_actualizacion, u.numero_doc, o.dni
                FROM "core_operador" o
                JOIN "core_usuario" u ON u.id = o.usuario_id
            """)
            cursor.execute('DROP TABLE "core_operador"')
            cursor.execute('ALTER TABLE "core_operador_new" RENAME TO "core_operador"')

            # ── core_archivocargamasiva ───────────────────────────────────────
            cursor.execute("""
                CREATE TABLE "core_archivocargamasiva_new" (
                    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                    "nombre_archivo" varchar(255) NOT NULL,
                    "hash_archivo" varchar(64) NOT NULL UNIQUE,
                    "fecha_carga" datetime NOT NULL,
                    "usuario_id" varchar(50) NULL REFERENCES "core_usuario" ("numero_doc") DEFERRABLE INITIALLY DEFERRED,
                    "hash_contenido" varchar(64) NULL
                )
            """)
            cursor.execute("""
                INSERT INTO "core_archivocargamasiva_new" (id, nombre_archivo, hash_archivo, fecha_carga, usuario_id, hash_contenido)
                SELECT a.id, a.nombre_archivo, a.hash_archivo, a.fecha_carga, u.numero_doc, a.hash_contenido
                FROM "core_archivocargamasiva" a
                LEFT JOIN "core_usuario" u ON u.id = a.usuario_id
            """)
            cursor.execute('DROP TABLE "core_archivocargamasiva"')
            cursor.execute('ALTER TABLE "core_archivocargamasiva_new" RENAME TO "core_archivocargamasiva"')
            cursor.execute('CREATE INDEX "core_archiv_hash_ar_a2d9ef_idx" ON "core_archivocargamasiva" ("hash_archivo")')
            cursor.execute('CREATE INDEX "core_archivocargamasiva_usuario_id_4c40c52b" ON "core_archivocargamasiva" ("usuario_id")')
            cursor.execute('CREATE INDEX "core_archivocargamasiva_hash_contenido_45911657" ON "core_archivocargamasiva" ("hash_contenido")')

            # ── core_password_reset_token ─────────────────────────────────────
            cursor.execute("""
                CREATE TABLE "core_password_reset_token_new" (
                    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                    "token" varchar(255) NOT NULL UNIQUE,
                    "created_at" datetime NOT NULL,
                    "is_used" bool NOT NULL,
                    "user_id" varchar(50) NOT NULL REFERENCES "core_usuario" ("numero_doc") DEFERRABLE INITIALLY DEFERRED
                )
            """)
            cursor.execute("""
                INSERT INTO "core_password_reset_token_new" (id, token, created_at, is_used, user_id)
                SELECT t.id, t.token, t.created_at, t.is_used, u.numero_doc
                FROM "core_password_reset_token" t
                JOIN "core_usuario" u ON u.id = t.user_id
            """)
            cursor.execute('DROP TABLE "core_password_reset_token"')
            cursor.execute('ALTER TABLE "core_password_reset_token_new" RENAME TO "core_password_reset_token"')
            cursor.execute('CREATE INDEX "core_password_reset_token_user_id_720ba657" ON "core_password_reset_token" ("user_id")')

            # ── core_empleadohospital ─────────────────────────────────────────
            cursor.execute("""
                CREATE TABLE "core_empleadohospital_new" (
                    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                    "dni" varchar(20) NOT NULL UNIQUE,
                    "legajo" varchar(20) NOT NULL UNIQUE,
                    "nombre" varchar(100) NOT NULL,
                    "apellido" varchar(100) NOT NULL,
                    "email" varchar(254) NULL UNIQUE,
                    "telefono" varchar(30) NOT NULL,
                    "cargo" varchar(20) NOT NULL,
                    "sector" varchar(120) NOT NULL,
                    "fecha_ingreso" date NULL,
                    "estado" varchar(10) NOT NULL,
                    "fecha_creacion" datetime NOT NULL,
                    "fecha_actualizacion" datetime NOT NULL,
                    "usuario_creacion_id" varchar(50) NULL REFERENCES "core_usuario" ("numero_doc") DEFERRABLE INITIALLY DEFERRED
                )
            """)
            cursor.execute("""
                INSERT INTO "core_empleadohospital_new" (id, dni, legajo, nombre, apellido, email, telefono, cargo, sector, fecha_ingreso, estado, fecha_creacion, fecha_actualizacion, usuario_creacion_id)
                SELECT e.id, e.dni, e.legajo, e.nombre, e.apellido, e.email, e.telefono, e.cargo, e.sector, e.fecha_ingreso, e.estado, e.fecha_creacion, e.fecha_actualizacion, u.numero_doc
                FROM "core_empleadohospital" e
                LEFT JOIN "core_usuario" u ON u.id = e.usuario_creacion_id
            """)
            cursor.execute('DROP TABLE "core_empleadohospital"')
            cursor.execute('ALTER TABLE "core_empleadohospital_new" RENAME TO "core_empleadohospital"')
            cursor.execute('CREATE INDEX "core_empleadohospital_usuario_creacion_id_94655709" ON "core_empleadohospital" ("usuario_creacion_id")')
            cursor.execute('CREATE INDEX "core_emplea_dni_d5fdcb_idx" ON "core_empleadohospital" ("dni")')
            cursor.execute('CREATE INDEX "core_emplea_legajo_397a46_idx" ON "core_empleadohospital" ("legajo")')
            cursor.execute('CREATE INDEX "core_emplea_estado_21c99c_idx" ON "core_empleadohospital" ("estado")')
            cursor.execute('CREATE INDEX "core_emplea_cargo_8cd1de_idx" ON "core_empleadohospital" ("cargo")')

            # ── core_usuario (último: reconstruir con numero_doc como PK) ─────
            cursor.execute("""
                CREATE TABLE "core_usuario_new" (
                    "numero_doc" varchar(50) NOT NULL PRIMARY KEY,
                    "password" varchar(128) NOT NULL,
                    "last_login" datetime NULL,
                    "is_superuser" bool NOT NULL,
                    "username" varchar(150) NOT NULL UNIQUE,
                    "first_name" varchar(150) NOT NULL,
                    "last_name" varchar(150) NOT NULL,
                    "email" varchar(254) NOT NULL,
                    "is_staff" bool NOT NULL,
                    "is_active" bool NOT NULL,
                    "date_joined" datetime NOT NULL,
                    "tipo_usuario" varchar(10) NOT NULL,
                    "tema_oscuro" INTEGER NOT NULL DEFAULT 0
                )
            """)
            cursor.execute("""
                INSERT INTO "core_usuario_new" (numero_doc, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, tipo_usuario, tema_oscuro)
                SELECT numero_doc, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, tipo_usuario, tema_oscuro
                FROM "core_usuario"
            """)
            cursor.execute('DROP TABLE "core_usuario"')
            cursor.execute('ALTER TABLE "core_usuario_new" RENAME TO "core_usuario"')

        finally:
            cursor.execute("PRAGMA foreign_keys = ON")


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_siem_nullable'),
    ]

    operations = [
        migrations.RunPython(rellenar_numero_doc, migrations.RunPython.noop),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='usuario',
                    name='numero_doc',
                    field=models.CharField(
                        max_length=50,
                        primary_key=True,
                        serialize=False,
                        verbose_name='Número de Documento',
                    ),
                ),
            ],
            database_operations=[
                migrations.RunPython(rebuild_all, migrations.RunPython.noop),
            ],
        ),
    ]
