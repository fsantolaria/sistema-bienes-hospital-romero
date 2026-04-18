"""
Script para limpiar todos los marcadores de conflicto de Git en el proyecto.
Conserva el bloque THEIRS (el de upstream/tus compañeros) en cada conflicto.
Skippea archivos binarios, venv y staticfiles.
"""
import os
import re

SKIP_DIRS = {"venv", "staticfiles", ".git", "__pycache__", "node_modules"}
EXTENSIONS = {".py", ".html", ".css", ".js", ".json", ".txt", ".md"}

# Archivos que NO tocamos (configuración de producción que protegemos)
PROTECTED_FILES = {
    "sistema_bienes/settings/production.py",
    "sistema_bienes/settings/base.py",
    "sistema_bienes/settings.py",
    "sistema_bienes/wsgi.py",
    "requirements.txt",
    "vercel.json",
}

def clean_conflicts(text, keep="theirs"):
    """Elimina los marcadores de conflicto conservando el bloque elegido."""
    lines = text.splitlines(keepends=True)
    result = []
    in_ours = False
    in_theirs = False
    ours_lines = []
    theirs_lines = []

    for line in lines:
        if line.startswith("<<<<<<< "):
            in_ours = True
            in_theirs = False
            ours_lines = []
            theirs_lines = []
        elif line.startswith("=======") and in_ours:
            in_ours = False
            in_theirs = True
        elif line.startswith(">>>>>>> ") and in_theirs:
            in_theirs = False
            if keep == "theirs":
                result.extend(theirs_lines)
            else:
                result.extend(ours_lines)
        elif in_ours:
            ours_lines.append(line)
        elif in_theirs:
            theirs_lines.append(line)
        else:
            result.append(line)

    return "".join(result)

def has_conflicts(text):
    return "<<<<<<< " in text

def normalize_path(path, base):
    return os.path.relpath(path, base).replace("\\", "/")

base_dir = os.path.dirname(os.path.abspath(__file__))
fixed = []
skipped_protected = []
errors = []

for root, dirs, files in os.walk(base_dir):
    # Excluir directorios a no procesar
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

    for fname in files:
        ext = os.path.splitext(fname)[1].lower()
        if ext not in EXTENSIONS:
            continue

        fpath = os.path.join(root, fname)
        rel = normalize_path(fpath, base_dir)

        if rel in PROTECTED_FILES:
            skipped_protected.append(rel)
            continue

        try:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()
        except Exception as e:
            errors.append(f"  LEER: {rel}: {e}")
            continue

        if not has_conflicts(text):
            continue

        cleaned = clean_conflicts(text, keep="theirs")

        try:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(cleaned)
            fixed.append(rel)
        except Exception as e:
            errors.append(f"  ESCRIBIR: {rel}: {e}")

print(f"\n✅ Archivos limpiados ({len(fixed)}):")
for f in fixed:
    print(f"  {f}")

print(f"\n🔒 Archivos protegidos omitidos ({len(skipped_protected)}):")
for f in skipped_protected:
    print(f"  {f}")

if errors:
    print(f"\n❌ Errores ({len(errors)}):")
    for e in errors:
        print(e)
else:
    print("\n✅ Sin errores.")
