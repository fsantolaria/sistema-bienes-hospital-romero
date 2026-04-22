document.addEventListener("DOMContentLoaded", () => {
  /* ================== Helpers genéricos ================== */
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const on = (el, ev, cb) => el && el.addEventListener(ev, cb);

  // Fecha de hoy en formato YYYY-MM-DD (para inputs type="date")
  const hoyISO = () => {
    const d = new Date();
    const m = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    return `${d.getFullYear()}-${m}-${day}`;
  };

  // Toggle clase oculto en un modal
  const abrir = (sel) => $(sel)?.classList.remove("oculto");
  const cerrar = (sel) => $(sel)?.classList.add("oculto");

  // Toggle ocultar una columna en toda la tabla
  function toggleColumn(tableSelector, colIndex, hide) {
    $$(tableSelector + " thead tr").forEach(tr => {
      const th = tr.children[colIndex];
      if (th) th.classList.toggle("col-hidden", hide);
    });
    $$(tableSelector + " tbody tr").forEach(tr => {
      const cell = tr.children[colIndex];
      if (cell) cell.classList.toggle("col-hidden", hide);
    });
  }
  // lo dejo global por si lo usás en consola
  window.toggleColumn = toggleColumn;

  /* ================== Modales (alta y carga masiva) ================== */
  // Abrir con data-open="#id"; Cerrar con data-close="#id"
  $$('[data-open]').forEach(btn => {
    on(btn, 'click', () => abrir(btn.getAttribute('data-open')));
  });
  document.addEventListener('click', (e) => {
    const closeBtn = e.target.closest('[data-close]');
    if (closeBtn) cerrar(closeBtn.getAttribute('data-close'));
  });
  // Cerrar por clic fuera del contenido
  $$('.custom-modal').forEach(modal => {
    on(modal, 'click', (e) => { if (e.target === modal) modal.classList.add('oculto'); });
  });

  // Botón cancelar del modal de ALTA (por id)
  on($('#cancelar-modal'), 'click', () => cerrar('#modal-bien'));

  /* ================== Alta: armar descripción y validar ================== */
  const formAlta = $('#form-alta-bien'); // viene del include model_bienes.html
  on(formAlta, 'submit', (e) => {
    // Combina nombre + descripcion1 + descripcion2
    const nombre = $('#nombre')?.value || "";
    const d1     = $('#descripcion1')?.value || "";
    const d2     = $('#descripcion2')?.value || "";
    const desc   = (nombre + ' ' + d1 + ' ' + d2).replace(/\s+/g, ' ').trim();
    const hidden = $('#descripcion-hidden');

    if (hidden) hidden.value = desc;

    // Validación mínima
    const cantidad = $('#cantidad')?.value || "";
    if (!desc || !cantidad) {
      e.preventDefault();
      alert("Completá al menos la Descripción y la Cantidad.");
      return false;
    }
    // Cierra el modal (el redirect del POST recargará la página)
    cerrar('#modal-bien');
  });

  /* ================== Precio según Origen (fila inline + modal) ================== */
  // Fila de alta inline (en la tabla)
  const selOrigenInline   = $('#id_origen');
  const celdaPrecioInline = $('#celda-precio');
  const inputPrecioInline = $('#id_valor_adquisicion');

  function togglePrecioInline() {
    if (!selOrigenInline || !celdaPrecioInline || !inputPrecioInline) return;
    const v = (selOrigenInline.value || '').toUpperCase();
    if (v === 'COMPRA') {
      celdaPrecioInline.style.display = '';
      inputPrecioInline.disabled = false;
    } else {
      celdaPrecioInline.style.display = 'none';
      inputPrecioInline.value = '';
      inputPrecioInline.disabled = true;
    }
  }
  togglePrecioInline();
  on(selOrigenInline, 'change', togglePrecioInline);

  // Modal de alta
  const selOrigenModal   = $('#origen');
  const inputPrecioModal = $('#valor_adquisicion');

  function togglePrecioModal() {
    if (!selOrigenModal || !inputPrecioModal) return;
    const v = (selOrigenModal.value || '').toUpperCase();
    inputPrecioModal.disabled = (v !== 'COMPRA');
    if (v !== 'COMPRA') inputPrecioModal.value = '';
  }
  togglePrecioModal();
  on(selOrigenModal, 'change', togglePrecioModal);

  /* ================== NUEVO: Fecha de Baja visible si estado = BAJA ================== */
  // Requiere que en el template exista:
  //   - un contenedor con id="grupo-fecha-baja" (con class "d-none" por defecto)
  //   - el input de fecha con id="id_fecha_baja"
  const selEstado       = $('#id_estado');
  const grupoFechaBaja  = $('#grupo-fecha-baja');
  const inputFechaBaja  = $('#id_fecha_baja');

  function toggleFechaBaja() {
    if (!selEstado || !grupoFechaBaja) return;
    const v = (selEstado.value || '').toUpperCase();
    if (v === 'BAJA') {
      grupoFechaBaja.classList.remove('d-none');
      if (inputFechaBaja && !inputFechaBaja.value) inputFechaBaja.value = hoyISO();
    } else {
      grupoFechaBaja.classList.add('d-none');
      if (inputFechaBaja) inputFechaBaja.value = '';
    }
  }
  toggleFechaBaja();
  on(selEstado, 'change', toggleFechaBaja);

  /* ================== Truncado expandible en celdas ================== */
  document.addEventListener('click', (e) => {
    const el = e.target.closest('.cell-clip, .text-clip, .text-truncate');
    if (el) el.classList.toggle('expanded');
  });

  /* ================== Menú Columnas con persistencia ================== */
  const COLS_KEY = 'bienes_hidden_cols';
  const tableSelector = '.tabla-operadores';
  const checks = $$('.columns-menu .col-toggle');
  const btnShowAll = $('#cols-show-all');
  const btnHideAll = $('#cols-hide-all');

  function loadHidden() {
    try { return JSON.parse(localStorage.getItem(COLS_KEY) || '[]'); }
    catch { return []; }
  }
  function saveHidden(arr) {
    localStorage.setItem(COLS_KEY, JSON.stringify(arr));
  }
  function applyHidden(hidden) {
    checks.forEach(cb => {
      const idx = Number(cb.dataset.col);
      const isHidden = hidden.includes(idx);
      cb.checked = !isHidden;
      toggleColumn(tableSelector, idx, isHidden);
    });
  }

  let hiddenCols = loadHidden();
  applyHidden(hiddenCols);

  checks.forEach(cb => {
    on(cb, 'change', () => {
      const idx = Number(cb.dataset.col);
      const hide = !cb.checked;
      toggleColumn(tableSelector, idx, hide);
      hiddenCols = loadHidden();
      const pos = hiddenCols.indexOf(idx);
      if (hide && pos === -1) hiddenCols.push(idx);
      if (!hide && pos > -1) hiddenCols.splice(pos, 1);
      saveHidden(hiddenCols);
    });
  });

  on(btnShowAll, 'click', () => {
    hiddenCols = [];
    saveHidden(hiddenCols);
    applyHidden(hiddenCols);
  });

  on(btnHideAll, 'click', () => {
    hiddenCols = checks.map(cb => Number(cb.dataset.col)); // oculta todas las listadas
    saveHidden(hiddenCols);
    applyHidden(hiddenCols);
  });

});

// ===== Dar de baja: botón que abre modal y setea acción =====
document.addEventListener('click', (e) => {
  const btn = e.target.closest('.btn-dar-baja');
  if (!btn) return;

  e.preventDefault();

  const pk = btn.getAttribute('data-pk');
  const desc = btn.getAttribute('data-descripcion') || '';

  // Setear acción del form a /bienes/<pk>/dar-baja/
  const form = document.getElementById('form-dar-baja');
  if (form) form.action = `/bienes/${pk}/dar-baja/`;  // si usás i18n_prefix o base, usa {% url %} data-... desde server

  // Texto informativo
  const info = document.getElementById('dar-baja-desc');
  if (info) info.textContent = desc ? `Bien: ${desc}` : '';

  // Reset campos
  const hoy = new Date().toISOString().slice(0,10);
  const f = document.getElementById('fecha_baja');
  if (f) f.value = hoy;
  const exp = document.getElementById('expediente_baja');
  if (exp) exp.value = '';
  const d = document.getElementById('descripcion_baja');
  if (d) d.value = '';

  // Abrir modal
  const modal = document.getElementById('modal-dar-baja');
  if (modal) modal.classList.remove('oculto');
});
