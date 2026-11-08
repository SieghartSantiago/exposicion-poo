<script setup lang="ts">
import { computed } from "vue";
import { useSlideContext } from "@slidev/client";

const { $clicks } = useSlideContext();

type Step = 0 | 1 | 2 | 3;

const step = computed<Step>(() => {
  const n = Number($clicks?.value ?? 0);
  if (n <= 0) return 0;
  if (n === 1) return 1;
  if (n === 2) return 2;
  return 3;
});

function setStep(s: Step) {
  if ($clicks) $clicks.value = s;
}

const captions: Record<Step, { badge: string; text: string }> = {
  0: {
    badge: "Paso 1 · Definición estática",
    text: "La clase <code>CuentaBancaria</code> existe como descriptor de código, pero todavía no se reservó estado para ninguna cuenta.",
  },
  1: {
    badge: "Paso 2 · Instanciación independiente",
    text: "<code>ana</code> y <code>bruno</code> referencian dos instancias distintas: comparten los métodos de la clase, pero cada una aloja su propio <code>_saldo</code>.",
  },
  2: {
    badge: "Paso 3 · Paso de mensajes",
    text: "<code>ana.transferir_a(bruno, 8_000)</code> ejecuta <code>ana.extraer(8_000)</code> y luego envía el mensaje <code>bruno.depositar(8_000)</code>.",
  },
  3: {
    badge: "Paso 4 · Aliasing de referencias",
    text: "<code>alias = ana</code> NO clona el objeto: copia la referencia (<code>alias is ana</code> es <code>True</code>). Nota: CPython gestiona objetos dinámicamente; C++ o C# admiten también instancias por valor en pila.",
  },
};
</script>

<template>
  <div class="mem-stage">
    <nav class="mem-nav" aria-label="Estados de instanciación y referencias">
      <button type="button" class="mem-btn" :class="{ 'is-active': step === 0 }" @click="setStep(0)">
        1. Molde de clase
      </button>
      <button type="button" class="mem-btn" :class="{ 'is-active': step === 1 }" @click="setStep(1)">
        2. Dos instancias
      </button>
      <button type="button" class="mem-btn" :class="{ 'is-active': step === 2 }" @click="setStep(2)">
        3. Paso de mensaje
      </button>
      <button type="button" class="mem-btn" :class="{ 'is-active': step === 3 }" @click="setStep(3)">
        4. Referencia compartida
      </button>
    </nav>

    <div class="mem-canvas">
      <svg viewBox="0 0 820 235" class="mem-svg" role="img" aria-label="Diagrama de clase, referencias e instancias">
        <!-- COLUMNA 1: CLASE -->
        <rect x="14" y="20" width="196" height="194" rx="12" fill="#111827" stroke="#818cf8" stroke-width="1.8" />
        <text x="112" y="46" text-anchor="middle" fill="#a5b4fc" style="font-size: 11px; font-weight: 700;">CLASE (MOLDE)</text>
        <text x="112" y="68" text-anchor="middle" fill="#f8fafc" style="font-family: var(--font-mono); font-size: 12.5px; font-weight: 700;">CuentaBancaria</text>
        <line x1="30" y1="80" x2="194" y2="80" stroke="rgba(148,163,184,0.25)" />
        <text x="34" y="104" fill="#94a3b8" style="font-size: 10.5px;">Atributos definidos:</text>
        <text x="42" y="123" fill="#cbd5e1" style="font-family: var(--font-mono); font-size: 10.5px;">_titular, _saldo</text>
        <text x="34" y="150" fill="#94a3b8" style="font-size: 10.5px;">Métodos compartidos:</text>
        <text x="42" y="169" fill="#7dd3fc" style="font-family: var(--font-mono); font-size: 10.5px;">extraer() · depositar()</text>
        <text x="42" y="188" fill="#7dd3fc" style="font-family: var(--font-mono); font-size: 10.5px;">transferir_a()</text>

        <!-- COLUMNA 2: NOMBRES / REFERENCIAS -->
        <rect x="248" y="20" width="176" height="194" rx="12" fill="#0d1424" stroke="rgba(148,163,184,0.3)" />
        <text x="336" y="44" text-anchor="middle" fill="#94a3b8" style="font-size: 10.5px; font-weight: 700;">VARIABLES (NOMBRES)</text>

        <g v-if="step >= 1">
          <rect x="270" y="62" width="132" height="36" rx="8" fill="#1e293b" stroke="#38bdf8" />
          <text x="336" y="84" text-anchor="middle" fill="#f8fafc" style="font-family: var(--font-mono); font-size: 11.5px;">ana</text>

          <rect x="270" y="152" width="132" height="36" rx="8" fill="#1e293b" stroke="#34d399" />
          <text x="336" y="174" text-anchor="middle" fill="#f8fafc" style="font-family: var(--font-mono); font-size: 11.5px;">bruno</text>
        </g>

        <g v-if="step === 3">
          <rect x="270" y="107" width="132" height="36" rx="8" fill="rgba(251,191,36,0.14)" stroke="#fbbf24" />
          <text x="336" y="129" text-anchor="middle" fill="#fde68a" style="font-family: var(--font-mono); font-size: 11px;">alias = ana</text>
        </g>

        <!-- COLUMNA 3: INSTANCIAS EN MEMORIA -->
        <rect x="468" y="20" width="338" height="194" rx="12" fill="#0d1424" stroke="rgba(148,163,184,0.3)" />
        <text x="637" y="44" text-anchor="middle" fill="#94a3b8" style="font-size: 10.5px; font-weight: 700;">INSTANCIAS CON ESTADO PROPIO</text>

        <g v-if="step === 0">
          <text x="637" y="124" text-anchor="middle" fill="#64748b" style="font-size: 12px;">
            (0 instancias creadas todavía — presioná → para instanciar)
          </text>
        </g>

        <g v-if="step >= 1">
          <!-- Instancia 1 -->
          <rect x="492" y="56" width="292" height="64" rx="10" fill="#111827" stroke="#38bdf8" stroke-width="1.7" />
          <text x="508" y="78" fill="#7dd3fc" style="font-family: var(--font-mono); font-size: 10.5px; font-weight: 700;">Instancia #1 (id 0xA1)</text>
          <text x="508" y="102" fill="#f8fafc" style="font-family: var(--font-mono); font-size: 11px;">
            _titular: "Ana" · _saldo: {{ step >= 2 ? "22_000.0" : "30_000.0" }}
          </text>

          <!-- Instancia 2 -->
          <rect x="492" y="138" width="292" height="64" rx="10" fill="#111827" stroke="#34d399" stroke-width="1.7" />
          <text x="508" y="160" fill="#6ee7b7" style="font-family: var(--font-mono); font-size: 10.5px; font-weight: 700;">Instancia #2 (id 0xB2)</text>
          <text x="508" y="184" fill="#f8fafc" style="font-family: var(--font-mono); font-size: 11px;">
            _titular: "Bruno" · _saldo: {{ step >= 2 ? "18_000.0" : "10_000.0" }}
          </text>

          <!-- Flechas de referencia -->
          <line x1="402" y1="80" x2="488" y2="80" stroke="#38bdf8" stroke-width="2" />
          <polygon points="492,80 484,75 484,85" fill="#38bdf8" />

          <line x1="402" y1="170" x2="488" y2="170" stroke="#34d399" stroke-width="2" />
          <polygon points="492,170 484,165 484,175" fill="#34d399" />
        </g>

        <!-- Flecha de mensaje transferir_a en paso 2 -->
        <g v-if="step === 2">
          <path d="M 754 96 C 792 112, 792 146, 754 162" fill="none" stroke="#fbbf24" stroke-width="2.2" />
          <polygon points="750,164 759,165 756,156" fill="#fbbf24" />
          <rect x="615" y="117" width="166" height="20" rx="5" fill="#1e293b" stroke="#fbbf24" />
          <text x="698" y="131" text-anchor="middle" fill="#fde68a" style="font-family: var(--font-mono); font-size: 9.5px;">depositar(8_000)</text>
        </g>

        <!-- Flecha de alias en paso 3 -->
        <g v-if="step === 3">
          <line x1="402" y1="125" x2="488" y2="92" stroke="#fbbf24" stroke-width="2" stroke-dasharray="5 3" />
          <polygon points="492,90 483,89 486,98" fill="#fbbf24" />
        </g>
      </svg>
    </div>

    <div class="mem-caption">
      <span class="poo-kicker" v-html="captions[step].badge" />
      <p v-html="captions[step].text" />
    </div>
  </div>
</template>

<style scoped>
.mem-stage {
  display: grid;
  grid-template-rows: 34px minmax(0, 1fr) auto;
  row-gap: 0.65rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.mem-nav {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.55rem;
}

.mem-btn {
  height: 34px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background: var(--bg-surface);
  color: var(--text-muted);
  font-size: 0.72rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
}

.mem-btn.is-active {
  background: var(--tint-interface);
  border-color: rgba(56, 189, 248, 0.55);
  color: #e0f2fe;
}

.mem-canvas {
  background: #090d16;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 0.4rem 0.65rem;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 0;
  min-height: 0;
}

.mem-svg {
  width: 100%;
  height: auto;
  max-height: 222px;
  display: block;
}

.mem-caption {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0.8rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
}

.mem-caption p {
  font-size: 0.77rem;
  line-height: 1.38;
  color: var(--text-secondary);
}
</style>
