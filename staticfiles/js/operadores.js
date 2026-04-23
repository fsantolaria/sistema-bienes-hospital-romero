// operadores.js (versión backend-friendly)
document.addEventListener('DOMContentLoaded', function() {
  const tablaOperadoresBody = document.querySelector('.tabla-operadores tbody');
  if (!tablaOperadoresBody) return;

  // Helper para crear un modal simple
  function crearModal(html) {
    const modal = document.createElement('div');
    modal.className = 'modal-operadores';
    modal.innerHTML = `
      <div class="modal-contenido">
        <div class="modal-header">
          <h3>Detalles del Operador</h3>
          <button class="btn-cerrar-modal" aria-label="Cerrar">&times;</button>
        </div>
        <div class="modal-body">${html}</div>
        <div class="modal-actions">
          <button class="btn-cerrar">Cerrar</button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);

    const cerrar = () => document.body.removeChild(modal);
    modal.addEventListener('click', (e) => { if (e.target === modal) cerrar(); });
    modal.querySelector('.btn-cerrar-modal')?.addEventListener('click', cerrar);
    modal.querySelector('.btn-cerrar')?.addEventListener('click', cerrar);

    // Estilos mínimos (por si no tenés CSS para esto)
    if (!document.getElementById('modal-operadores-style')) {
      const estilo = document.createElement('style');
      estilo.id = 'modal-operadores-style';
      estilo.textContent = `
        .modal-operadores{position:fixed;inset:0;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;z-index:1000}
        .modal-contenido{background:#fff;border-radius:8px;max-width:520px;width:92%;max-height:90vh;overflow:auto;box-shadow:0 10px 30px rgba(0,0,0,.2)}
        .modal-header{display:flex;align-items:center;justify-content:space-between;padding:14px 18px;border-bottom:1px solid #eee}
        .modal-body{padding:18px}
        .modal-actions{display:flex;justify-content:flex-end;gap:10px;padding:12px 18px;border-top:1px solid #eee}
        .btn-cerrar-modal{background:none;border:none;font-size:22px;cursor:pointer}
        .btn-cerrar{background:#6c757d;color:#fff;border:none;border-radius:6px;padding:8px 14px;cursor:pointer}
      `;
      document.head.appendChild(estilo);
    }
  }

  // Delegación de eventos para "ver más" (icono ✅)
  document.addEventListener('click', function(e) {
    const verMas = e.target.closest('.icono-ver-mas');
    if (!verMas) return;

    const fila = verMas.closest('tr');
    if (!fila) return;

    // Lee datos desde las columnas existentes (ajusta índices si cambias el orden):
    // En tu template: [0]=OPERADOR (username) | [1]=NOMBRES Y APELLIDOS | [2]=EDITAR | [3]=ESTADO
    const celdas = fila.querySelectorAll('td');
    const usuario = (celdas[0]?.textContent || '').trim();
    const nombre  = (celdas[1]?.textContent || '').trim();
    const estado  = (celdas[3]?.textContent || '').trim();

    // Si querés más info (email, doc, etc.), podés agregar data-attributes en el template:
    // <tr data-email="{{ op.email }}" data-doc="{{ op.numero_doc }}"> ... </tr>
    const email = fila.dataset.email || '';
    const numeroDoc = fila.dataset.doc || '';

    const html = `
      <div class="detalles-operador">
        <p><strong>Usuario:</strong> ${usuario || '—'}</p>
        <p><strong>Nombre y apellido:</strong> ${nombre || '—'}</p>
        <p><strong>Estado:</strong> ${estado || '—'}</p>
        ${email ? `<p><strong>Email:</strong> ${email}</p>` : ''}
        ${numeroDoc ? `<p><strong>N° Documento:</strong> ${numeroDoc}</p>` : ''}
      </div>
    `;
    crearModal(html);
  });

  // Importante: NO agregamos ningún handler al botón "agregar".
  // En tu template es un <a href="{% url 'alta_operadores' %}">, debe navegar al formulario.
});
