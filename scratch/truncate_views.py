with open('core/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Truncar después de la línea que termina agregar_servicio_ajax
# La línea es: return JsonResponse({"ok": True, "nombre": nombre, "mensaje": f"Servicio '{nombre}' agregado correctamente."})
# Que está en la línea 2321 (1-indexed)

new_lines = lines[:2321]

with open('core/views.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
