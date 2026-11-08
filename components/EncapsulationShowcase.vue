<script setup lang="ts">
import { computed } from "vue";
import { useSlideContext } from "@slidev/client";

const { $clicks } = useSlideContext();

type StepIndex = 0 | 1 | 2;

const activeStep = computed<StepIndex>(() => {
  const raw = Number($clicks?.value ?? 0);
  if (raw <= 0) return 0;
  if (raw === 1) return 1;
  return 2;
});

function setStep(step: StepIndex) {
  if ($clicks) {
    $clicks.value = step;
  }
}

interface StepMeta {
  index: StepIndex;
  shortTitle: string;
  fileName: string;
  statusText: string;
  accent: "problem" | "class" | "valid";
  codeLines: string[];
}

const steps: StepMeta[] = [
  {
    index: 0,
    shortTitle: "1. Problema: mutación libre",
    fileName: "01_estado_expuesto.py",
    statusText: "Sin validación",
    accent: "problem",
    codeLines: [
      "# Estado expuesto sin reglas de validación",
      "cuenta = {",
      '    "titular": "Ana",',
      '    "saldo": 30_000.0,',
      "}",
      "",
      "# Cualquier función resta directamente",
      'cuenta["saldo"] -= 45_000.0',
      "",
      "# El programa sigue con estado inválido:",
      'print(cuenta["saldo"])  # -15000.0',
    ],
  },
  {
    index: 1,
    shortTitle: "2. Clase e invariante",
    fileName: "02_cuenta_bancaria.py",
    statusText: "Contrato activo",
    accent: "class",
    codeLines: [
      "class CuentaBancaria:",
      '    """Invariante: self._saldo >= 0.0"""',
      "    def __init__(self, saldo: float) -> None:",
      "        if saldo < 0.0:",
      '            raise ValueError("Saldo < 0")',
      "        self._saldo = saldo",
      "",
      "    @property",
      "    def saldo(self) -> float:",
      "        return self._saldo",
      "",
      "    def extraer(self, monto: float) -> None:",
      "        if monto <= 0.0 or monto > self._saldo:",
      '            raise ValueError("Sin fondos")',
      "        self._saldo -= monto",
    ],
  },
  {
    index: 2,
    shortTitle: "3. Operación inválida",
    fileName: "03_ejecucion_segura.py",
    statusText: "Estado preservado",
    accent: "valid",
    codeLines: [
      "cuenta = CuentaBancaria(saldo=30_000.0)",
      "",
      "# 1. Operación válida: respeta _saldo >= 0",
      "cuenta.extraer(10_000.0)  # -> 20000.0",
      "",
      "# 2. Operación inválida: sobregiro",
      "try:",
      "    cuenta.extraer(45_000.0)",
      "except ValueError as err:",
      '    print(err)            # "Sin fondos"',
      "",
      "# El estado interno permanece intacto:",
      "assert cuenta.saldo == 20_000.0",
    ],
  },
];

const currentMeta = computed(() => steps[activeStep.value]);

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

const PY_TOKEN_RE =
  /("""[^"]*"""|"[^"]*"|#.*$|@\w+|\b(?:class|def|if|or|return|raise|try|except|as|assert|None)\b|\b(?:CuentaBancaria|ValueError|float|print|self)\b|\b\d[\d_.]*\b)/g;

const KEYWORDS = new Set([
  "class",
  "def",
  "if",
  "or",
  "return",
  "raise",
  "try",
  "except",
  "as",
  "assert",
  "None",
]);

const TYPES = new Set(["CuentaBancaria", "ValueError", "float", "print", "self"]);

function highlightPythonLine(line: string): string {
  if (!line) return "&nbsp;";

  let result = "";
  let lastIndex = 0;

  for (const match of line.matchAll(PY_TOKEN_RE)) {
    const idx = match.index ?? 0;
    if (idx > lastIndex) {
      result += escapeHtml(line.slice(lastIndex, idx));
    }

    const token = match[0];
    const escaped = escapeHtml(token);

    if (token.startsWith("#")) {
      result += `<span class="tok-com">${escaped}</span>`;
    } else if (token.startsWith('"')) {
      result += `<span class="tok-str">${escaped}</span>`;
    } else if (token.startsWith("@")) {
      result += `<span class="tok-dec">${escaped}</span>`;
    } else if (KEYWORDS.has(token)) {
      result += `<span class="tok-kw">${escaped}</span>`;
    } else if (TYPES.has(token)) {
      result += `<span class="tok-type">${escaped}</span>`;
    } else {
      result += `<span class="tok-num">${escaped}</span>`;
    }

    lastIndex = idx + token.length;
  }

  if (lastIndex < line.length) {
    result += escapeHtml(line.slice(lastIndex));
  }

  return result;
}

const highlightedLines = computed(() =>
  currentMeta.value.codeLines.map((line) => highlightPythonLine(line))
);
</script>

<template>
  <div class="encap-stage">
    <!-- Barra de progreso de los 3 estados de animación -->
    <nav class="encap-stepper" aria-label="Pasos de la demostración">
      <button
        v-for="item in steps"
        :key="item.index"
        type="button"
        class="encap-step-btn"
        :class="[
          `encap-step-btn--${item.accent}`,
          { 'is-active': activeStep === item.index },
        ]"
        :aria-current="activeStep === item.index ? 'step' : undefined"
        @click="setStep(item.index)"
        v-html="item.shortTitle"
      />
    </nav>

    <!-- Grilla principal de altura fija en todos los estados -->
    <div class="encap-grid">
      <!-- PANEL IZQUIERDO: CÓDIGO PYTHON CON ESPACIO RESERVADO FIJO -->
      <section class="encap-code-panel" :data-accent="currentMeta.accent">
        <header class="encap-code-bar">
          <span class="encap-filename">{{ currentMeta.fileName }}</span>
          <span class="encap-status" :data-accent="currentMeta.accent">
            {{ currentMeta.statusText }}
          </span>
        </header>

        <div class="encap-code-body">
          <Transition name="poo-fade" mode="out-in">
            <pre :key="activeStep" class="encap-pre"><code
              ><span
                v-for="(lineHtml, idx) in highlightedLines"
                :key="idx"
                class="encap-line"
                v-html="lineHtml"
              /></code></pre>
          </Transition>
        </div>
      </section>

      <!-- PANEL DERECHO: EXPLICACIÓN Y ESTADO DEL OBJETO -->
      <section class="encap-explain-panel">
        <Transition name="poo-fade" mode="out-in">
          <!-- ESTADO 0: EL PROBLEMA -->
          <div v-if="activeStep === 0" key="exp-0" class="encap-card encap-card--problem">
            <div class="encap-card__top">
              <span class="poo-kicker poo-kicker--problem">El Problema</span>
              <h2 class="encap-card__title">Modificación directa sin invariante</h2>
            </div>

            <div class="state-flow">
              <div class="state-node">
                <span class="state-node__label">Estado inicial</span>
                <strong class="state-node__val">$30.000</strong>
              </div>
              <span class="state-arrow">→</span>
              <div class="state-node state-node--danger">
                <span class="state-node__label">Tras restar $45.000</span>
                <strong class="state-node__val state-node__val--danger">-$15.000</strong>
              </div>
            </div>

            <ul class="encap-list">
              <li>
                <strong>Regla rota:</strong> una cuenta sin descubierto nunca debe tener saldo menor a cero, pero ningún contrato intercepta la escritura.
              </li>
              <li>
                <strong>Acoplamiento a los datos:</strong> aunque en diseño procedural se podría encapsular con módulos o tipos abstractos, exponer el diccionario obliga a repetir validaciones en todo el programa.
              </li>
            </ul>
          </div>

          <!-- ESTADO 1: LA CLASE QUE PROTEGE SUS INVARIANTES -->
          <div v-else-if="activeStep === 1" key="exp-1" class="encap-card encap-card--class">
            <div class="encap-card__top">
              <span class="poo-kicker poo-kicker--class">La Solución POO</span>
              <h2 class="encap-card__title">Frontera pública e invariante de clase</h2>
            </div>

            <div class="architecture-box">
              <div class="arch-row arch-row--public">
                <span class="arch-tag">Interfaz pública</span>
                <code>__init__() · saldo · extraer()</code>
              </div>
              <div class="arch-row arch-row--guard">
                <span class="arch-tag">Invariante</span>
                <code>self._saldo &gt;= 0.0</code>
              </div>
              <div class="arch-row arch-row--internal">
                <span class="arch-tag">Estado interno</span>
                <code>self._saldo</code>
              </div>
            </div>

            <ul class="encap-list">
              <li>
                <strong>Lectura controlada:</strong> <code>@property</code> expone <code>cuenta.saldo</code> sin habilitar asignaciones directas desde afuera.
              </li>
              <li>
                <strong>Convención en Python:</strong> <code>_saldo</code> señala uso interno (PEP 8). El doble guion <code>__saldo</code> solo aplica <em>name mangling</em> (<code>_CuentaBancaria__saldo</code>), no privacidad estricta.
              </li>
            </ul>
          </div>

          <!-- ESTADO 2: RESULTADO ANTE OPERACIÓN INVÁLIDA -->
          <div v-else key="exp-2" class="encap-card encap-card--valid">
            <div class="encap-card__top">
              <span class="poo-kicker poo-kicker--valid">Resultado de Ejecución</span>
              <h2 class="encap-card__title">Rechazo atómico ante operación inválida</h2>
            </div>

            <div class="trace-list">
              <div class="trace-row trace-row--ok">
                <code>extraer(10_000)</code>
                <span>Válido → <strong>$20.000</strong></span>
              </div>
              <div class="trace-row trace-row--rejected">
                <code>extraer(45_000)</code>
                <span>Lanza <code>ValueError</code></span>
              </div>
            </div>

            <div class="preserved-banner">
              <span>Estado final verificado:</span>
              <code>cuenta.saldo == $20.000</code>
            </div>

            <p class="encap-summary">
              La validación falla <strong>antes</strong> de ejecutar <code>self._saldo -= monto</code>. El objeto jamás queda a mitad de camino ni en un estado inválido.
            </p>
          </div>
        </Transition>
      </section>
    </div>
  </div>
</template>

<style scoped>
.encap-stage {
  display: grid;
  grid-template-rows: 36px minmax(0, 1fr);
  row-gap: 0.7rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.encap-stepper {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.65rem;
}

.encap-step-btn {
  box-sizing: border-box;
  height: 36px;
  padding: 0 0.75rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background: var(--bg-surface);
  color: var(--text-muted);
  font-family: var(--font-sans);
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
  cursor: pointer;
  transition:
    background-color var(--duration-fast) var(--ease-standard),
    border-color var(--duration-fast) var(--ease-standard),
    color var(--duration-fast) var(--ease-standard);
}

.encap-step-btn:hover {
  color: var(--text-primary);
  border-color: var(--border-strong);
}

.encap-step-btn:focus-visible {
  outline: 2px solid var(--accent-interface);
  outline-offset: 2px;
}

.encap-step-btn--problem.is-active {
  background: var(--tint-problem);
  border-color: rgba(251, 113, 133, 0.55);
  color: #ffe4e6;
}

.encap-step-btn--class.is-active {
  background: var(--tint-class);
  border-color: rgba(129, 140, 248, 0.55);
  color: #e0e7ff;
}

.encap-step-btn--valid.is-active {
  background: var(--tint-valid);
  border-color: rgba(52, 211, 153, 0.55);
  color: #d1fae5;
}

.encap-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(0, 0.92fr);
  column-gap: 1.25rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

/* Panel de código de dimensiones invariables */
.encap-code-panel {
  box-sizing: border-box;
  display: grid;
  grid-template-rows: 34px minmax(0, 1fr);
  height: 100%;
  min-width: 0;
  min-height: 0;
  background: #0b1120;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
}

.encap-code-panel[data-accent="problem"] {
  border-color: rgba(251, 113, 133, 0.36);
}

.encap-code-panel[data-accent="class"] {
  border-color: rgba(129, 140, 248, 0.4);
}

.encap-code-panel[data-accent="valid"] {
  border-color: rgba(52, 211, 153, 0.4);
}

.encap-code-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 0.9rem;
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(17, 24, 39, 0.85);
  border-radius: var(--radius-md) var(--radius-md) 0 0;
}

.encap-filename {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--text-secondary);
}

.encap-status {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.encap-status[data-accent="problem"] {
  color: #fda4af;
}

.encap-status[data-accent="class"] {
  color: #a5b4fc;
}

.encap-status[data-accent="valid"] {
  color: #6ee7b7;
}

.encap-code-body {
  padding: 0.7rem 0.95rem;
  display: flex;
  align-items: flex-start;
  min-width: 0;
  min-height: 0;
}

.encap-pre {
  margin: 0;
  width: 100%;
  font-family: var(--font-mono);
  font-size: 0.77rem;
  line-height: 1.42;
  color: #f8fafc;
  background: transparent;
}

.encap-line {
  display: block;
  white-space: pre;
}

:deep(.tok-kw) {
  color: #c084fc;
  font-weight: 600;
}

:deep(.tok-type) {
  color: #38bdf8;
}

:deep(.tok-str) {
  color: #6ee7b7;
}

:deep(.tok-num) {
  color: #fbbf24;
}

:deep(.tok-dec) {
  color: #f472b6;
}

:deep(.tok-com) {
  color: #94a3b8;
  font-style: italic;
}

/* Panel derecho explicativo de altura fija */
.encap-explain-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.encap-card {
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.7rem;
  height: 100%;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 0.95rem 1.05rem;
}

.encap-card--problem {
  border-top: 3px solid var(--accent-problem);
}

.encap-card--class {
  border-top: 3px solid var(--accent-class);
}

.encap-card--valid {
  border-top: 3px solid var(--accent-valid);
}

.encap-card__top {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.4rem;
}

.encap-card__title {
  font-size: 1.05rem;
  line-height: 1.25;
  font-weight: 700;
  color: var(--text-primary);
}

.state-flow {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
  align-items: center;
  gap: 0.5rem;
}

.state-node {
  background: #0b1120;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 0.5rem 0.65rem;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.state-node--danger {
  border-color: rgba(251, 113, 133, 0.55);
  background: rgba(251, 113, 133, 0.08);
}

.state-node__label {
  font-size: 0.68rem;
  color: var(--text-muted);
}

.state-node__val {
  font-family: var(--font-mono);
  font-size: 0.98rem;
  color: var(--text-primary);
}

.state-node__val--danger {
  color: #fb7185;
}

.state-arrow {
  color: var(--text-muted);
  font-weight: 700;
}

.architecture-box {
  display: flex;
  flex-direction: column;
  gap: 0.38rem;
}

.arch-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  padding: 0.38rem 0.65rem;
  border-radius: 7px;
  font-size: 0.75rem;
}

.arch-row--public {
  background: rgba(56, 189, 248, 0.1);
  border: 1px solid rgba(56, 189, 248, 0.3);
}

.arch-row--guard {
  background: rgba(52, 211, 153, 0.1);
  border: 1px solid rgba(52, 211, 153, 0.32);
}

.arch-row--internal {
  background: rgba(129, 140, 248, 0.1);
  border: 1px solid rgba(129, 140, 248, 0.3);
}

.arch-tag {
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
  white-space: nowrap;
}

.encap-list {
  margin: 0;
  padding-left: 1.05rem;
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  font-size: 0.78rem;
  line-height: 1.42;
  color: var(--text-secondary);
}

.trace-list {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.trace-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  padding: 0.45rem 0.7rem;
  border-radius: 8px;
  font-size: 0.78rem;
  background: #0b1120;
}

.trace-row--ok {
  border-left: 3px solid var(--accent-valid);
}

.trace-row--rejected {
  border-left: 3px solid var(--accent-problem);
}

.preserved-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  background: rgba(52, 211, 153, 0.11);
  border: 1px solid rgba(52, 211, 153, 0.4);
  font-size: 0.78rem;
  color: #d1fae5;
}

.encap-summary {
  font-size: 0.79rem;
  line-height: 1.44;
  color: var(--text-secondary);
}
</style>
