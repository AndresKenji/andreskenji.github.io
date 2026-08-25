/* Editor del CV: formulario a la izquierda, preview real a la derecha.
   Sin build step ni dependencias: el formulario se genera desde la
   especificación SECTIONS de abajo, que refleja src/models.py. */

const state = {
  resume: null,
  schema: null,
  themes: [],
  theme: null,
  previewLang: 'en',
  dirty: false,
  errors: [],
  isExample: false,
};

/*——————————————————— Especificación del formulario ———————————————————*/

const DATE_HINT = 'YYYY-MM-DD';

const PROFILE_FIELDS = [
  { name: 'network', type: 'text', label: 'Red' },
  { name: 'username', type: 'text', label: 'Usuario' },
  { name: 'url', type: 'url', label: 'URL' },
];

const LOCATION_FIELDS = [
  { name: 'address', type: 'text', label: 'Dirección' },
  { name: 'postal_code', type: 'text', label: 'Código postal' },
  { name: 'city', type: 'text', label: 'Ciudad' },
  { name: 'region', type: 'text', label: 'Región' },
  { name: 'country_code', type: 'text', label: 'País (código)' },
];

const SECTIONS = [
  {
    key: 'basics', kind: 'object', label: 'Datos básicos',
    fields: [
      { name: 'name', type: 'text', label: 'Nombre completo' },
      { name: 'label', type: 'i18n', label: 'Título profesional' },
      { name: 'summary', type: 'i18n-area', label: 'Sobre mí' },
      { name: 'image', type: 'text', label: 'Foto', hint: 'Ruta relativa, p. ej. static/img/kenji.png' },
      { name: 'email', type: 'email', label: 'Email' },
      { name: 'phone', type: 'text', label: 'Teléfono' },
      { name: 'url', type: 'url', label: 'Sitio o LinkedIn' },
      { name: 'location', kind: 'object', label: 'Ubicación', fields: LOCATION_FIELDS },
      { name: 'profiles', kind: 'list', label: 'Perfiles', itemName: 'perfil', title: (i) => i.network, fields: PROFILE_FIELDS },
    ],
  },
  {
    key: 'work', kind: 'list', label: 'Experiencia laboral', itemName: 'experiencia',
    title: (i) => i.name,
    fields: [
      { name: 'name', type: 'text', label: 'Empresa' },
      { name: 'position', type: 'i18n', label: 'Cargo' },
      { name: 'url', type: 'url', label: 'Sitio de la empresa' },
      { name: 'start_date', type: 'date', label: 'Inicio' },
      { name: 'end_date', type: 'end-date', label: 'Fin' },
      { name: 'summary', type: 'i18n-area', label: 'Descripción' },
      { name: 'highlights', type: 'i18n-list', label: 'Logros', itemName: 'logro' },
    ],
  },
  {
    key: 'education', kind: 'list', label: 'Educación', itemName: 'estudio',
    title: (i) => i.institution,
    fields: [
      { name: 'institution', type: 'text', label: 'Institución' },
      { name: 'url', type: 'url', label: 'Sitio' },
      { name: 'area', type: 'i18n', label: 'Área' },
      { name: 'study_type', type: 'enum', label: 'Tipo', options: 'study_type' },
      { name: 'start_date', type: 'date', label: 'Inicio' },
      { name: 'end_date', type: 'end-date', label: 'Fin' },
      { name: 'score', type: 'text', label: 'Promedio' },
      { name: 'courses', type: 'i18n-list', label: 'Cursos', itemName: 'curso' },
    ],
  },
  {
    key: 'skills', kind: 'list', label: 'Aptitudes', itemName: 'aptitud',
    title: (i) => loc(i.name),
    fields: [
      { name: 'name', type: 'i18n', label: 'Nombre' },
      { name: 'level', type: 'enum', label: 'Nivel', options: 'skill_level' },
      { name: 'color', type: 'color', label: 'Color' },
      { name: 'keywords', type: 'i18n-list', label: 'Keywords', itemName: 'keyword' },
    ],
  },
  {
    key: 'languages', kind: 'list', label: 'Idiomas', itemName: 'idioma',
    title: (i) => loc(i.language),
    fields: [
      { name: 'language', type: 'i18n', label: 'Idioma' },
      { name: 'fluency', type: 'enum', label: 'Nivel', options: 'fluency' },
    ],
  },
  {
    key: 'interests', kind: 'list', label: 'Intereses', itemName: 'interés',
    title: (i) => loc(i.name),
    fields: [
      { name: 'name', type: 'i18n', label: 'Nombre' },
      { name: 'keywords', type: 'i18n-list', label: 'Keywords', itemName: 'keyword' },
    ],
  },
  {
    key: 'projects', kind: 'list', label: 'Proyectos', itemName: 'proyecto',
    title: (i) => i.name,
    fields: [
      { name: 'name', type: 'text', label: 'Nombre' },
      { name: 'url', type: 'url', label: 'URL' },
      { name: 'start_date', type: 'date', label: 'Inicio' },
      { name: 'end_date', type: 'end-date', label: 'Fin' },
      { name: 'description', type: 'i18n-area', label: 'Descripción' },
      { name: 'highlights', type: 'i18n-list', label: 'Logros', itemName: 'logro' },
    ],
  },
  {
    key: 'certificates', kind: 'list', label: 'Certificaciones', itemName: 'certificación',
    title: (i) => loc(i.name),
    fields: [
      { name: 'name', type: 'i18n', label: 'Nombre' },
      { name: 'issuer', type: 'text', label: 'Emisor' },
      { name: 'date', type: 'date', label: 'Fecha' },
      { name: 'url', type: 'url', label: 'URL' },
    ],
  },
  {
    key: 'volunteer', kind: 'list', label: 'Voluntariado', itemName: 'voluntariado',
    title: (i) => i.organization,
    fields: [
      { name: 'organization', type: 'text', label: 'Organización' },
      { name: 'position', type: 'i18n', label: 'Rol' },
      { name: 'url', type: 'url', label: 'Sitio' },
      { name: 'start_date', type: 'date', label: 'Inicio' },
      { name: 'end_date', type: 'end-date', label: 'Fin' },
      { name: 'summary', type: 'i18n-area', label: 'Descripción' },
      { name: 'highlights', type: 'i18n-list', label: 'Logros', itemName: 'logro' },
    ],
  },
  {
    key: 'awards', kind: 'list', label: 'Reconocimientos', itemName: 'reconocimiento',
    title: (i) => loc(i.title),
    fields: [
      { name: 'title', type: 'i18n', label: 'Título' },
      { name: 'awarder', type: 'text', label: 'Otorgado por' },
      { name: 'date', type: 'date', label: 'Fecha' },
      { name: 'summary', type: 'i18n-area', label: 'Descripción' },
    ],
  },
  {
    key: 'publications', kind: 'list', label: 'Publicaciones', itemName: 'publicación',
    title: (i) => i.name,
    fields: [
      { name: 'name', type: 'text', label: 'Nombre' },
      { name: 'publisher', type: 'text', label: 'Editor' },
      { name: 'release_date', type: 'date', label: 'Fecha' },
      { name: 'url', type: 'url', label: 'URL' },
      { name: 'summary', type: 'i18n-area', label: 'Descripción' },
    ],
  },
  {
    key: 'references', kind: 'list', label: 'Referencias', itemName: 'referencia',
    title: (i) => i.name,
    fields: [
      { name: 'name', type: 'text', label: 'Nombre' },
      { name: 'email', type: 'email', label: 'Email' },
      { name: 'phone', type: 'text', label: 'Teléfono' },
      { name: 'reference', type: 'i18n-area', label: 'Texto' },
    ],
  },
];

/*——————————————————— Utilidades ———————————————————*/

/** Un I18nStr puede venir como string plano (idiomas idénticos) o {en, es}. */
function loc(value, lang = 'en') {
  if (value == null) return '';
  return typeof value === 'string' ? value : (value[lang] ?? value.en ?? '');
}

function getAt(obj, path) {
  return path.reduce((acc, key) => (acc == null ? undefined : acc[key]), obj);
}

function setAt(obj, path, value) {
  const parent = path.slice(0, -1).reduce((acc, key) => acc[key], obj);
  parent[path.at(-1)] = value;
}

function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') node.className = v;
    else if (k === 'text') node.textContent = v;
    else if (k.startsWith('on')) node.addEventListener(k.slice(2).toLowerCase(), v);
    else if (v !== null && v !== undefined && v !== false) node.setAttribute(k, v);
  }
  for (const child of [].concat(children)) {
    if (child) node.appendChild(child);
  }
  return node;
}

function pathKey(path) {
  return path.join('.');
}

function errorsFor(path) {
  const key = pathKey(path);
  return state.errors.filter((e) => e.path.join('.') === key);
}

/** Estructura vacía para un elemento nuevo, deducida de la spec de campos. */
function blankItem(fields) {
  const item = {};
  for (const f of fields) {
    if (f.kind === 'list') item[f.name] = [];
    else if (f.kind === 'object') item[f.name] = blankItem(f.fields);
    else if (f.type === 'i18n-list') item[f.name] = [];
    else if (f.type === 'i18n' || f.type === 'i18n-area') item[f.name] = { en: '', es: '' };
    else if (f.type === 'enum') item[f.name] = state.schema[f.options][0];
    else if (f.type === 'end-date') item[f.name] = null;
    else if (f.type === 'color') item[f.name] = '#0070c0';
    else item[f.name] = '';
  }
  return item;
}

/*——————————————————— Renderizado de campos ———————————————————*/

function attachError(wrapper, path) {
  const errs = errorsFor(path);
  if (!errs.length) return;
  wrapper.classList.add('has-error');
  wrapper.appendChild(el('div', { class: 'field-error', text: errs.map((e) => e.message).join('. ') }));
}

function bindInput(node, path, { nullable = false } = {}) {
  node.addEventListener('input', () => {
    const value = node.value;
    setAt(state.resume, path, nullable && value === '' ? null : value);
    scheduleSync();
  });
  return node;
}

/** Dos campos lado a lado, uno por idioma. Es el punto del JSON unificado. */
function i18nControl(path, { area = false } = {}) {
  const current = getAt(state.resume, path);
  // Un string plano en el JSON significa "igual en ambos idiomas": se expande
  // al editarlo para poder darles valores distintos.
  const value = typeof current === 'string' ? { en: current, es: current } : (current || { en: '', es: '' });
  if (typeof current === 'string' || current == null) setAt(state.resume, path, value);

  const grid = el('div', { class: 'i18n' });
  for (const lang of ['en', 'es']) {
    const input = area
      ? el('textarea', { rows: 5 })
      : el('input', { type: 'text' });
    input.value = value[lang] ?? '';
    bindInput(input, [...path, lang]);
    const cell = el('div', { class: 'lang-cell' }, [input, el('span', { class: 'lang-tag', text: lang.toUpperCase() })]);
    attachError(cell, [...path, lang]);
    grid.appendChild(cell);
  }
  attachError(grid, path);
  return grid;
}

/** Lista de textos bilingües: keywords, cursos, logros. */
function i18nListControl(path, field) {
  const items = getAt(state.resume, path) || [];
  const box = el('div', { class: 'tag-rows' });

  items.forEach((_, index) => {
    const row = el('div', { class: 'inline-row' }, [
      i18nControl([...path, index]),
      el('button', {
        class: 'icon-btn danger', type: 'button', title: 'Eliminar',
        onclick: () => { items.splice(index, 1); rerenderAndSync(); },
      }, [document.createTextNode('✕')]),
    ]);
    box.appendChild(el('div', { class: 'list-item' }, [row]));
  });

  box.appendChild(el('button', {
    class: 'btn-add', type: 'button', text: `+ Agregar ${field.itemName || 'elemento'}`,
    onclick: () => { items.push({ en: '', es: '' }); rerenderAndSync(); },
  }));
  return box;
}

function endDateControl(path) {
  const value = getAt(state.resume, path);
  const isCurrent = value === null || value === undefined;

  const input = el('input', { type: 'text', placeholder: DATE_HINT });
  input.value = value || '';
  input.disabled = isCurrent;
  bindInput(input, path, { nullable: true });

  const check = el('input', { type: 'checkbox' });
  check.checked = isCurrent;
  check.addEventListener('change', () => {
    setAt(state.resume, path, check.checked ? null : (input.value || ''));
    rerenderAndSync();
  });

  return el('div', { class: 'date-row' }, [
    input,
    el('label', { class: 'check' }, [check, document.createTextNode('Actualmente')]),
  ]);
}

function enumControl(path, field) {
  const select = el('select', { class: 'enum' });
  for (const option of state.schema[field.options]) {
    select.appendChild(el('option', { value: option, text: option }));
  }
  select.value = getAt(state.resume, path) ?? state.schema[field.options][0];
  select.addEventListener('change', () => {
    setAt(state.resume, path, select.value);
    scheduleSync();
  });
  return select;
}

function renderField(field, basePath) {
  const path = [...basePath, field.name];

  if (field.kind === 'object') {
    return el('fieldset', { class: 'fieldset' }, [
      el('div', { class: 'field-label', text: field.label }),
      ...field.fields.map((f) => renderField(f, path)),
    ]);
  }

  if (field.kind === 'list') {
    return el('fieldset', { class: 'fieldset' }, [
      el('div', { class: 'field-label', text: field.label }),
      renderList(field, path),
    ]);
  }

  let control;
  if (field.type === 'i18n') control = i18nControl(path);
  else if (field.type === 'i18n-area') control = i18nControl(path, { area: true });
  else if (field.type === 'i18n-list') control = i18nListControl(path, field);
  else if (field.type === 'end-date') control = endDateControl(path);
  else if (field.type === 'enum') control = enumControl(path, field);
  else if (field.type === 'color') {
    control = el('input', { type: 'text', placeholder: '#0070c0' });
    control.value = getAt(state.resume, path) ?? '';
    bindInput(control, path);
  } else {
    const type = field.type === 'email' ? 'email' : field.type === 'url' ? 'url' : 'text';
    control = el('input', { type, placeholder: field.type === 'date' ? DATE_HINT : '' });
    control.value = getAt(state.resume, path) ?? '';
    bindInput(control, path, { nullable: field.type === 'email' || field.type === 'url' });
  }

  const wrapper = el('div', { class: 'field' }, [
    el('label', { class: 'field-label', text: field.label }),
    control,
    field.hint ? el('div', { class: 'hint', text: field.hint }) : null,
  ]);
  if (field.type !== 'i18n' && field.type !== 'i18n-area') attachError(wrapper, path);
  return wrapper;
}

/** Lista repetible con agregar / eliminar / reordenar. */
function renderList(section, path) {
  const items = getAt(state.resume, path) || [];
  const box = el('div', {});

  items.forEach((item, index) => {
    const move = (delta) => {
      const target = index + delta;
      if (target < 0 || target >= items.length) return;
      [items[index], items[target]] = [items[target], items[index]];
      rerenderAndSync();
    };

    const title = (section.title ? section.title(item) : '') || `${section.itemName} ${index + 1}`;
    const head = el('div', { class: 'item-head' }, [
      el('span', { class: 'item-title', text: title }),
      Object.assign(el('button', { class: 'icon-btn', type: 'button', title: 'Subir', text: '▲', onclick: () => move(-1) }), { disabled: index === 0 }),
      Object.assign(el('button', { class: 'icon-btn', type: 'button', title: 'Bajar', text: '▼', onclick: () => move(1) }), { disabled: index === items.length - 1 }),
      el('button', {
        class: 'icon-btn danger', type: 'button', title: 'Eliminar', text: '✕',
        onclick: () => {
          if (!confirm(`¿Eliminar "${title}"?`)) return;
          items.splice(index, 1);
          rerenderAndSync();
        },
      }),
    ]);

    box.appendChild(el('div', { class: 'list-item' }, [
      head,
      ...section.fields.map((f) => renderField(f, [...path, index])),
    ]));
  });

  box.appendChild(el('button', {
    class: 'btn-add', type: 'button', text: `+ Agregar ${section.itemName}`,
    onclick: () => {
      items.push(blankItem(section.fields));
      rerenderAndSync({ open: pathKey(path) });
    },
  }));
  return box;
}

/*——————————————————— Formulario completo ———————————————————*/

const openSections = new Set(['basics']);

function renderForm() {
  const form = document.getElementById('form');
  form.replaceChildren();
  renderExampleNotice();

  for (const section of SECTIONS) {
    const path = [section.key];
    const isOpen = openSections.has(section.key);
    const body = el('div', { class: 'section-body' });

    if (section.kind === 'object') {
      section.fields.forEach((f) => body.appendChild(renderField(f, path)));
    } else {
      body.appendChild(renderList(section, path));
    }

    const count = section.kind === 'list' ? (getAt(state.resume, path) || []).length : null;
    const summary = el('summary', {}, [
      el('span', { text: section.label }),
      count !== null ? el('span', { class: 'count', text: String(count) }) : null,
    ]);

    const details = el('details', { class: 'section' }, [summary, body]);
    details.open = isOpen;
    details.addEventListener('toggle', () => {
      details.open ? openSections.add(section.key) : openSections.delete(section.key);
    });
    form.appendChild(details);
  }

  renderErrorSummary();
}

function renderExampleNotice() {
  const box = document.getElementById('example-notice');
  if (!state.isExample) {
    box.hidden = true;
    return;
  }
  box.hidden = false;
  box.replaceChildren(
    el('strong', { text: 'Estás sobre el CV de ejemplo.' }),
    document.createTextNode(' Edítalo y guarda para hacerlo tuyo — el aviso desaparece cuando dejes de estar sobre los datos de ejemplo. También puedes empezar de cero con '),
    el('code', { text: 'python -m scripts.reset' }),
    document.createTextNode('.'),
  );
}

function renderErrorSummary() {
  const box = document.getElementById('error-summary');
  if (!state.errors.length) {
    box.hidden = true;
    return;
  }
  box.hidden = false;
  box.replaceChildren(
    el('strong', { text: `${state.errors.length} error(es) de validación — no se puede guardar:` }),
    el('ul', {}, state.errors.slice(0, 12).map((e) =>
      el('li', { text: `${e.path.join(' → ')}: ${e.message}` }))),
  );
}

/*——————————————————— Sincronización con el servidor ———————————————————*/

let syncTimer = null;

function scheduleSync() {
  setStatus('Sin guardar', 'dirty');
  state.dirty = true;
  document.getElementById('save-btn').disabled = false;
  clearTimeout(syncTimer);
  syncTimer = setTimeout(sync, 400);
}

function rerenderAndSync() {
  renderForm();
  scheduleSync();
}

async function sync() {
  const res = await fetch('/api/draft', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(state.resume),
  });

  if (res.status === 422) {
    state.errors = (await res.json()).errors;
    renderForm();
    setStatus(`${state.errors.length} error(es)`, 'err');
    document.getElementById('save-btn').disabled = true;
    return;
  }

  if (state.errors.length) {
    state.errors = [];
    renderForm();
  }
  setStatus('Sin guardar', 'dirty');
  document.getElementById('save-btn').disabled = false;
  reloadPreview();
}

function reloadPreview() {
  const frame = document.getElementById('preview');
  // El parámetro sirve para saltar la caché del iframe.
  frame.src = `/preview/${state.previewLang}/?theme=${state.theme}&v=${Date.now()}`;
}

function setStatus(text, kind = '') {
  const node = document.getElementById('status');
  node.textContent = text;
  node.className = `status ${kind}`;
}

async function save() {
  const btn = document.getElementById('save-btn');
  btn.disabled = true;
  setStatus('Guardando…');

  const res = await fetch('/api/save', { method: 'POST' });
  if (res.status === 422) {
    state.errors = (await res.json()).errors;
    renderForm();
    setStatus('No se pudo guardar: hay errores', 'err');
    return;
  }

  const data = await res.json();
  state.dirty = false;
  state.isExample = data.is_example;
  renderExampleNotice();
  setStatus(`Guardado · ${data.written.join(', ')}`, 'ok');
  reloadPreview();
}

/*——————————————————— Barra superior ———————————————————*/

function renderTopbar() {
  const select = document.getElementById('theme-select');
  select.replaceChildren(...state.themes.map((t) =>
    el('option', { value: t.id, text: t.name, title: t.description })));
  select.value = state.theme;
  select.addEventListener('change', async () => {
    state.theme = select.value;
    await fetch('/api/config', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ theme: state.theme }),
    });
    reloadPreview();
  });

  const toggle = document.getElementById('lang-toggle');
  toggle.replaceChildren(...state.schema.languages.map((lang) => {
    const btn = el('button', {
      type: 'button', text: lang.toUpperCase(),
      'aria-pressed': String(lang === state.previewLang),
      onclick: () => {
        state.previewLang = lang;
        renderTopbar();
        reloadPreview();
      },
    });
    return btn;
  }));

  document.getElementById('save-btn').onclick = save;
}

/*——————————————————— Arranque ———————————————————*/

(async function init() {
  const [resumeRes, schemaRes, themesRes] = await Promise.all([
    fetch('/api/resume').then((r) => r.json()),
    fetch('/api/schema').then((r) => r.json()),
    fetch('/api/themes').then((r) => r.json()),
  ]);

  state.resume = resumeRes.resume;
  state.isExample = resumeRes.is_example;
  state.schema = schemaRes;
  state.themes = themesRes.themes;
  state.theme = themesRes.active;

  renderTopbar();
  renderForm();
  reloadPreview();
  setStatus('Sin cambios');

  window.addEventListener('beforeunload', (e) => {
    if (state.dirty) e.preventDefault();
  });
})();
