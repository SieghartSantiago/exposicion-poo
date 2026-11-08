# Exposición Interactiva: Programación Orientada a Objetos (POO)

Aplicación educativa web interactiva desarrollada para **Programación I (Ingeniería en Informática — Unidad VI, 2026)**.

Integra una presentación proyectable **16:9 de 23 diapositivas animadas** construida con **Slidev (Vue 3 + TypeScript)**, **4 laboratorios de Python real ejecutables en el navegador** mediante **marimo + Pyodide (WebAssembly)** y una **Guía de Lectura Móvil** adaptable a celulares y tablets accesible por **código QR**. Todo el proyecto se compila a archivos **100 % estáticos**, sin servidor backend ni claves privadas expuestas.

---

## Estructura Temática de la Exposición (23 Diapositivas)

| Bloque | Diapositivas | Contenidos Principales |
| :--- | :---: | :--- |
| **Portada** | `1` | Identidad visual *Obsidian Tech Conference*, acceso por código QR y selector de movimiento reducido. |
| **Bloque 1 · Introducción** | `2 – 4` | Qué es un paradigma, comparación conceptual con programación procedural, problemas de ingeniería de software y línea de tiempo histórica animada (`Simula 67` → presente). |
| **Bloque 2 · Fundamentos** | `5 – 7` | Anatomía de clase en Python (`__init__`, atributos, `@property`, métodos), diagrama animado de instanciación e independencia de estado, referencias/aliasing, identidad (`is`) vs. igualdad (`==`) y paso de mensajes. |
| **Bloque 3 · Cuatro Pilares** | `8 – 14` | Abstracción e invariantes (`Temperatura`), Encapsulamiento y visibilidad en Python (`_saldo` vs. *name mangling* `__saldo`), **Lab 01**, Herencia (`ABC`, `super()`, C3 MRO), Composición y Delegación vs. Herencia, Polimorfismo y Despacho Dinámico (`Protocol`, `vtable`/`vptr` vs. Python MRO) y **Lab 02**. |
| **Bloque 4 · SOLID y Patrones** | `15 – 18` | Principios `S · O · L · I · D` centrados en cohesión y acoplamiento, Patrón **Strategy** con intercambio en tiempo de ejecución, patrones estructurales **Adapter** y **Decorator**, y **Lab 03**. |
| **Bloque 5 · Trade-offs y Paradigmas** | `19 – 21` | Compromisos de ingeniería, análisis riguroso de memoria/caché/indirección, cuándo **no** conviene usar POO, comparación equivalente `O(n)` entre **Imperativo, POO y Funcional** en Python, y **Lab 04**. |
| **Bloque 6 · Cierre** | `22 – 23` | Tres preguntas metodológicas de selección, síntesis multiparadigma, bibliografía académica y acceso directo a los 4 laboratorios. |

---

## Los 4 Laboratorios Interactivos Python + WebAssembly

Cada notebook en `labs/` se exporta automáticamente en dos modalidades independientes con recursos WASM deduplicados en `public/labs/shared/`:
- **Modo Simulador (`run`):** controles táctiles guiados (deslizadores, selectores e interruptores) ideales para demostración en clase y uso desde celulares.
- **Modo Sandbox Editable (`edit`):** celdas de código Python abiertas en el navegador para modificar clases, agregar subclases o estrategias y reejecutar al instante.

| Laboratorio | Fuente Python | Ruta Simulador (`run`) | Ruta Sandbox (`edit`) |
| :--- | :--- | :--- | :--- |
| **01 · Encapsulamiento e Invariantes** | `labs/lab_01_encapsulamiento.py` | `/labs/01-encapsulamiento/run/index.html` | `/labs/01-encapsulamiento/edit/index.html` |
| **02 · Herencia y Polimorfismo** | `labs/lab_02_herencia_polimorfismo.py` | `/labs/02-herencia-polimorfismo/run/index.html` | `/labs/02-herencia-polimorfismo/edit/index.html` |
| **03 · Patrón Strategy en Vivo** | `labs/lab_03_patron_strategy.py` | `/labs/03-patron-strategy/run/index.html` | `/labs/03-patron-strategy/edit/index.html` |
| **04 · Comparación de 3 Paradigmas** | `labs/lab_04_comparacion_paradigmas.py` | `/labs/04-comparacion-paradigmas/run/index.html` | `/labs/04-comparacion-paradigmas/edit/index.html` |

---

## Organización del Código Fuente

```text
├── slides.md                        # Definición de las 23 diapositivas y notas de orador
├── layouts/                         # 7 layouts reutilizables 16:9 (cover-poo, concept, code-explain, comparison, diagram, lab-entry, conclusions)
├── components/
│   ├── common/PythonCodePanel.vue   # Visor de código Python con dimensiones estables y resaltado léxico
│   ├── layout/SlideHeader.vue       # Encabezado consistente con kicker, título y badge
│   ├── bloque1/ ... bloque6/        # Componentes interactivos y diagramas SVG por bloque temático
│   ├── EncapsulationShowcase.vue    # Demostración paso a paso de encapsulamiento
│   ├── LabLaunchpad.vue             # Tarjetas de lanzamiento hacia Simulador y Sandbox
│   └── QrAccessModal.vue            # Generador QR dinámico + control de movimiento reducido
├── utils/pythonHighlighter.ts       # Tokenizador léxico en una pasada para Python tipado
├── styles/                          # Tokens de diseño (design-tokens.css) y tema global (slides-theme.css)
├── labs/                            # 4 laboratorios marimo Python + tema compartido lab_theme.css
├── public/guia/index.html           # Guía de lectura vertical responsive para celulares y tablets
├── scripts/                         # Pipeline de exportación WASM (build-labs.mjs) y postbuild estático
└── tests/                           # Pruebas unitarias Python (unittest) y auditoría Playwright (visual-audit.mjs)
```

---

## Requisitos e Instalación Local

- **Node.js** `>= 20` y `npm`
- **Python** `>= 3.11` *(únicamente requerido en la máquina del desarrollador al compilar los laboratorios; los usuarios finales ejecutan todo en el navegador sin instalar Python).*

```powershell
# 1. Instalar dependencias de Node.js
npm install

# 2. Crear entorno virtual Python e instalar marimo + uv
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install marimo uv
```

---

## Ejecución en Desarrollo y Pruebas de Calidad

### 1. Servidor de desarrollo local
```powershell
npm run dev
```
- **Presentación (16:9):** `http://localhost:3030/`
- **Vista de presentador (con notas):** `http://localhost:3030/presenter/`
- **Guía de lectura móvil:** `http://localhost:3030/guia/index.html`
- **Laboratorios WASM (`01` a `04`):** `http://localhost:3030/labs/01-encapsulamiento/run/index.html` *(y análogos)*

### 2. Verificación unitaria y auditoría visual automatizada
```powershell
# Ejecutar suite de pruebas unitarias de los 4 laboratorios Python
.\.venv\Scripts\python.exe -m unittest discover -s tests -v

# Compilar sitio estático completo y ejecutar auditoría Playwright (186 estados desktop + móvil + Pyodide WASM)
npm run build
npm run test:visual
```

---

## Compilación Estática y Despliegue en Cloudflare Pages

El comando de compilación genera la carpeta autocontenida `dist/` lista para alojamiento estático:

```powershell
npm run build
npm run preview
```

### Opción A — Despliegue directo con Wrangler CLI (Cloudflare Pages)
```powershell
npx wrangler pages deploy dist --project-name expo-poo-programacion1
```

### Opción B — Integración continua desde GitHub en Cloudflare Pages
1. Subir este repositorio a GitHub.
2. En el panel de **Cloudflare Dashboard → Workers & Pages → Create → Pages → Connect to Git**, seleccionar el repositorio.
3. Configurar los parámetros de compilación:
   - **Build command:** `pip install marimo uv && npm ci && npm run build`
   - **Build output directory:** `dist`
   - **Variables de entorno (opcional):** `NODE_VERSION = 20`, `PYTHON_VERSION = 3.11`.
4. El archivo `dist/_headers` generado por `scripts/postbuild.mjs` configura automáticamente `Content-Type: application/wasm` y caché inmutable para los binarios de Pyodide.

### Opción C — Publicación en GitHub Pages (subruta `/nombre-repo/`)
```powershell
npm run build:labs
npx slidev build --base /nombre-repo/
node scripts/postbuild.mjs
```
*(El script `postbuild.mjs` incluye `.nojekyll` y `404.html` para soportar rutas directas de diapositivas).*
