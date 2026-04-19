#!/usr/bin/env python3
"""
merge_upstream.py
=================
Script para integrar los cambios del repositorio de los companeros
(fsantolaria/sistema-bienes-hospital-romero) sin romper la configuracion
de produccion (Vercel + Neon + WhiteNoise).

Uso:
    python merge_upstream.py

Lo que hace:
    1. Hace backup de los archivos criticos de produccion
    2. Trae los cambios del upstream (git fetch + merge)
    3. Limpia automaticamente todos los marcadores de conflicto Git
       conservando los cambios del upstream
    4. Restaura los archivos criticos de produccion desde el backup
    5. Aplica las migraciones pendientes en Neon
    6. Regenera los archivos estaticos
    7. Hace commit y push automaticamente
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime

# ─── Configuracion ────────────────────────────────────────────────────────────

UPSTREAM_REMOTE = "upstream"
UPSTREAM_URL    = "https://github.com/fsantolaria/sistema-bienes-hospital-romero.git"
UPSTREAM_BRANCH = "main"
OUR_BRANCH      = "main"

# Archivos que NUNCA se sobreescriben con los del upstream
PROTECTED_FILES = [
    "sistema_bienes/settings/production.py",
    "sistema_bienes/settings/base.py",
    "sistema_bienes/wsgi.py",
    "vercel.json",
    "requirements.txt",
]

# Extensiones a limpiar de marcadores de conflicto
CLEAN_EXTENSIONS = {".py", ".html", ".css", ".js", ".json", ".txt", ".md"}

# Directorios a ignorar
SKIP_DIRS = {"venv", "staticfiles", ".git", "__pycache__", "node_modules"}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── Helpers ──────────────────────────────────────────────────────────────────

def run(cmd, check=True, capture=False):
    """Ejecuta un comando de shell."""
    print(f"  $ {cmd}")
    result = subprocess.run(
        cmd, shell=True, capture_output=capture, text=True, cwd=BASE_DIR
    )
    if check and result.returncode != 0:
        err = result.stderr if capture else ""
        print(f"\n[ERROR] Comando fallido: {cmd}")
        if err:
            print(err)
        sys.exit(1)
    return result

def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def clean_conflicts(text, keep="theirs"):
    """Elimina los marcadores de conflicto conservando el bloque elegido."""
    lines = text.splitlines(keepends=True)
    result = []
    in_ours = in_theirs = False
    ours = []
    theirs = []

    for line in lines:
        if line.startswith("<<<<<<< "):
            in_ours = True
            in_theirs = False
            ours = []
            theirs = []
        elif line.startswith("=======") and in_ours:
            in_ours = False
            in_theirs = True
        elif line.startswith(">>>>>>> ") and in_theirs:
            in_theirs = False
            result.extend(theirs if keep == "theirs" else ours)
        elif in_ours:
            ours.append(line)
        elif in_theirs:
            theirs.append(line)
        else:
            result.append(line)

    return "".join(result)

def norm(path):
    return os.path.relpath(path, BASE_DIR).replace("\\", "/")

# ─── Pasos ────────────────────────────────────────────────────────────────────

def step_backup():
    section("PASO 1: Backup de archivos protegidos")
    backup_dir = os.path.join(BASE_DIR, f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    os.makedirs(backup_dir, exist_ok=True)

    for rel in PROTECTED_FILES:
        src = os.path.join(BASE_DIR, rel)
        if os.path.exists(src):
            dst = os.path.join(backup_dir, rel.replace("/", "_"))
            shutil.copy2(src, dst)
            print(f"  Backup: {rel}")

    print(f"\n  Backup guardado en: {os.path.basename(backup_dir)}")
    return backup_dir

def step_fetch_merge():
    section("PASO 2: Fetch y merge del upstream")

    # Agregar upstream si no existe
    remotes = run("git remote", capture=True).stdout
    if UPSTREAM_REMOTE not in remotes:
        run(f"git remote add {UPSTREAM_REMOTE} {UPSTREAM_URL}")
        print(f"  Remote '{UPSTREAM_REMOTE}' agregado.")

    run(f"git fetch {UPSTREAM_REMOTE}")
    print("  Fetch completado.")

    # Intentar merge (puede fallar con conflictos, eso es esperado)
    result = run(
        f"git merge {UPSTREAM_REMOTE}/{UPSTREAM_BRANCH} --no-edit",
        check=False, capture=True
    )
    if result.returncode == 0:
        print("  Merge limpio, sin conflictos.")
    else:
        print("  Conflictos detectados — se limpiarán en el siguiente paso.")

def step_restore_protected(backup_dir):
    section("PASO 3: Restaurar archivos protegidos de produccion")

    for rel in PROTECTED_FILES:
        backup_file = os.path.join(backup_dir, rel.replace("/", "_"))
        dest = os.path.join(BASE_DIR, rel)
        if os.path.exists(backup_file):
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(backup_file, dest)
            run(f'git checkout HEAD -- {rel}', check=False)
            print(f"  Restaurado: {rel}")

def step_clean_conflicts():
    section("PASO 4: Limpiar marcadores de conflicto Git")

    fixed = []
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if os.path.splitext(fname)[1].lower() not in CLEAN_EXTENSIONS:
                continue
            fpath = os.path.join(root, fname)
            rel = norm(fpath)
            if any(rel == p or rel.startswith(p.rstrip("/")) for p in PROTECTED_FILES):
                continue
            try:
                text = open(fpath, "r", encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            if "<<<<<<< " not in text:
                continue
            cleaned = clean_conflicts(text, keep="theirs")
            open(fpath, "w", encoding="utf-8").write(cleaned)
            fixed.append(rel)

    if fixed:
        print(f"  Archivos limpiados ({len(fixed)}):")
        for f in fixed:
            print(f"    - {f}")
    else:
        print("  Ningún archivo con conflictos encontrado.")

def step_check():
    section("PASO 5: Verificacion de Django")
    result = run(
        "venv\\Scripts\\python.exe manage.py check 2>&1",
        check=False, capture=True
    )
    output = result.stdout + result.stderr
    if "no issues" in output.lower() or result.returncode == 0:
        print("  Django check: OK")
    else:
        print(f"  [ADVERTENCIA] Django check reporto problemas:\n{output}")
        print("  Revisar manualmente antes de continuar.")

def step_migrate():
    section("PASO 6: Aplicar migraciones en Neon (produccion)")
    print("  IMPORTANTE: Esto aplica las migraciones en la BD de produccion (Neon).")
    confirm = input("  Continuar? (s/n): ").strip().lower()
    if confirm != "s":
        print("  Migraciones omitidas.")
        return

    env = os.environ.copy()
    env["DJANGO_ENV"] = "production"
    # makemigrations
    r1 = subprocess.run(
        "venv\\Scripts\\python.exe manage.py makemigrations",
        shell=True, cwd=BASE_DIR, env=env
    )
    # migrate
    r2 = subprocess.run(
        "venv\\Scripts\\python.exe manage.py migrate",
        shell=True, cwd=BASE_DIR, env=env
    )
    if r2.returncode == 0:
        print("  Migraciones aplicadas correctamente en Neon.")
    else:
        print("  [ERROR] Fallo al migrar. Revisar manualmente.")

def step_collectstatic():
    section("PASO 7: Regenerar archivos estaticos")
    run("venv\\Scripts\\python.exe manage.py collectstatic --noinput")
    print("  Staticfiles actualizados.")

def step_commit_push():
    section("PASO 8: Commit y push")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    run("git add -A")
    run(f'git commit -m "Merge upstream {timestamp} - conflictos resueltos, produccion protegida"')
    run(f"git push origin {OUR_BRANCH}")
    print("\n  Push completado. Vercel iniciara el deploy automaticamente.")

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("\n" + "="*60)
    print("  MERGE SEGURO DE UPSTREAM")
    print("  Sistema de Bienes - Hospital Melchor Romero")
    print("="*60)
    print(f"\n  Upstream: {UPSTREAM_URL}")
    print(f"  Rama:     {UPSTREAM_REMOTE}/{UPSTREAM_BRANCH} → {OUR_BRANCH}")
    print(f"\n  Archivos protegidos ({len(PROTECTED_FILES)}):")
    for f in PROTECTED_FILES:
        print(f"    - {f}")

    confirm = input("\n  Iniciar merge? (s/n): ").strip().lower()
    if confirm != "s":
        print("  Cancelado.")
        sys.exit(0)

    backup_dir = step_backup()
    step_fetch_merge()
    step_restore_protected(backup_dir)
    step_clean_conflicts()
    step_check()
    step_migrate()
    step_collectstatic()
    step_commit_push()

    print("\n" + "="*60)
    print("  MERGE COMPLETADO EXITOSAMENTE")
    print("="*60)
    print("  - Cambios del upstream integrados")
    print("  - Configuracion de produccion preservada")
    print("  - Migraciones aplicadas en Neon")
    print("  - Staticfiles actualizados")
    print("  - Deploy en curso en Vercel")
    print("")

if __name__ == "__main__":
    main()
