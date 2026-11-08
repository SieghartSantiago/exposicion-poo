<script setup lang="ts">
import { computed } from "vue";
import { useSlideContext } from "@slidev/client";
import PythonCodePanel from "../common/PythonCodePanel.vue";

const { $clicks } = useSlideContext();

type Step = 0 | 1;

const step = computed<Step>(() => {
  const n = Number($clicks?.value ?? 0);
  return n <= 0 ? 0 : 1;
});

function setStep(s: Step) {
  if ($clicks) $clicks.value = s;
}

const adapterLines = [
  "# Librería externa incompatible (cobra en centavos):",
  "class SDKPagosExterno:",
  "    def charge_cents(self, cents: int) -> str:",
  '        return f"OK:{cents}c"',
  "",
  "# ADAPTER: traduce al contrato esperado cobrar(pesos)",
  "class AdaptadorSDK:",
  "    def __init__(self, sdk: SDKPagosExterno) -> None:",
  "        self._sdk = sdk",
  "",
  "    def cobrar(self, pesos: float) -> str:",
  "        return self._sdk.charge_cents(int(pesos * 100))",
];

const decoratorLines = [
  "# DECORATOR: envuelve un Notificador con el mismo contrato",
  "class NotificadorEmail:",
  "    def enviar(self, msg: str) -> str:",
  '        return f"Email: {msg}"',
  "",
  "class ConPrefijoUrgente:",
  "    def __init__(self, base: NotificadorEmail) -> None:",
  "        self._base = base  # Mismo contrato que envuelve",
  "",
  "    def enviar(self, msg: str) -> str:",
  '        return self._base.enviar(f"[URGENTE] {msg}")',
  "",
  '# ConPrefijoUrgente(NotificadorEmail()).enviar("Caída")',
];
</script>

<template>
  <div class="ad-stage">
    <nav class="ad-nav" aria-label="Patrones estructurales">
      <button type="button" class="ad-btn" :class="{ 'is-active': step === 0 }" @click="setStep(0)">
        1. Patrón Adapter (traducir interfaces incompatibles)
      </button>
      <button type="button" class="ad-btn" :class="{ 'is-active': step === 1 }" @click="setStep(1)">
        2. Patrón Decorator (apilar responsabilidades sin subclases)
      </button>
    </nav>

    <div class="ad-body">
      <Transition name="poo-fade" mode="out-in">
        <!-- ADAPTER -->
        <div v-if="step === 0" key="ad0" class="ad-grid">
          <PythonCodePanel
            file-name="patron_adapter.py"
            status-text="Traductor de contrato"
            accent="interface"
            :lines="adapterLines"
            state-key="adapter"
          />

          <article class="ad-card ad-card--cyan">
            <span class="poo-kicker">Patrón Adapter (Adaptador)</span>
            <h3>Integrar terceros sin ensuciar el dominio</h3>
            <svg viewBox="0 0 360 94" class="ad-svg" role="img" aria-label="Diagrama Adapter">
              <rect x="8" y="22" width="92" height="50" rx="8" fill="#0b1120" stroke="#38bdf8" />
              <text x="54" y="45" text-anchor="middle" fill="#e0f2fe" style="font-size: 10px; font-weight: 700;">Cliente</text>
              <text x="54" y="60" text-anchor="middle" fill="#7dd3fc" style="font-family: var(--font-mono); font-size: 8.5px;">cobrar($)</text>

              <line x1="102" y1="47" x2="128" y2="47" stroke="#38bdf8" stroke-width="1.8" />
              <rect x="130" y="16" width="100" height="62" rx="8" fill="rgba(56,189,248,0.14)" stroke="#38bdf8" stroke-width="1.8" />
              <text x="180" y="42" text-anchor="middle" fill="#f8fafc" style="font-size: 10px; font-weight: 700;">Adapter</text>
              <text x="180" y="59" text-anchor="middle" fill="#bae6fd" style="font-size: 8.5px;">pesos × 100</text>

              <line x1="232" y1="47" x2="258" y2="47" stroke="#fbbf24" stroke-width="1.8" />
              <rect x="260" y="22" width="92" height="50" rx="8" fill="#0b1120" stroke="#fbbf24" />
              <text x="306" y="45" text-anchor="middle" fill="#fde68a" style="font-size: 10px; font-weight: 700;">SDK Externo</text>
              <text x="306" y="60" text-anchor="middle" fill="#cbd5e1" style="font-family: var(--font-mono); font-size: 8.5px;">charge_cents</text>
            </svg>
            <ul class="ad-list">
              <li><strong>Problema inicial:</strong> la librería externa usa otra firma y unidades, y no podemos editar su código.</li>
              <li><strong>Mejora:</strong> aísla la conversión en un único puente; si cambiamos de proveedor, solo cambia el adaptador.</li>
            </ul>
          </article>
        </div>

        <!-- DECORATOR -->
        <div v-else key="ad1" class="ad-grid">
          <PythonCodePanel
            file-name="patron_decorator.py"
            status-text="Envoltorio transparente"
            accent="valid"
            :lines="decoratorLines"
            state-key="decorator"
          />

          <article class="ad-card ad-card--emerald">
            <span class="poo-kicker poo-kicker--valid">Patrón Decorator (Decorador)</span>
            <h3>Sumar capas en ejecución sin explosión de clases</h3>
            <svg viewBox="0 0 360 94" class="ad-svg" role="img" aria-label="Diagrama Decorator">
              <rect x="16" y="10" width="328" height="74" rx="12" fill="rgba(52,211,153,0.1)" stroke="#34d399" stroke-width="1.6" />
              <text x="90" y="34" text-anchor="middle" fill="#6ee7b7" style="font-size: 9.5px; font-weight: 700;">ConAuditoria</text>
              <text x="90" y="52" text-anchor="middle" fill="#cbd5e1" style="font-family: var(--font-mono); font-size: 8.5px;">enviar(msg)</text>

              <rect x="160" y="18" width="174" height="58" rx="9" fill="#0b1120" stroke="#818cf8" stroke-width="1.5" />
              <text x="247" y="40" text-anchor="middle" fill="#a5b4fc" style="font-size: 9.5px; font-weight: 700;">NotificadorEmail</text>
              <text x="247" y="58" text-anchor="middle" fill="#f8fafc" style="font-family: var(--font-mono); font-size: 8.5px;">enviar(msg)</text>
            </svg>
            <ul class="ad-list">
              <li><strong>Problema inicial:</strong> crear subclases para cada combinación (<code>EmailUrgenteConLogYReintento</code>) es inmanejable.</li>
              <li><strong>Mejora:</strong> cada envoltorio implementa la misma interfaz y encadena capacidades dinámicamente como piezas enchufables.</li>
            </ul>
          </article>
        </div>
      </Transition>
    </div>
  </div>
</template>

<style scoped>
.ad-stage {
  display: grid;
  grid-template-rows: 34px minmax(0, 1fr);
  row-gap: 0.7rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.ad-nav {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.6rem;
}

.ad-btn {
  height: 34px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background: var(--bg-surface);
  color: var(--text-muted);
  font-size: 0.73rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
}

.ad-btn.is-active {
  background: var(--tint-interface);
  border-color: rgba(56, 189, 248, 0.55);
  color: #e0f2fe;
}

.ad-body {
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.ad-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.06fr) minmax(0, 0.94fr);
  gap: 1.15rem;
  height: 100%;
}

.ad-card {
  box-sizing: border-box;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.55rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 0.9rem 1.05rem;
}

.ad-card--cyan {
  border-top: 3px solid var(--accent-interface);
}

.ad-card--emerald {
  border-top: 3px solid var(--accent-valid);
}

.ad-card h3 {
  font-size: 1.01rem;
  line-height: 1.24;
  font-weight: 700;
}

.ad-svg {
  width: 100%;
  height: auto;
  max-height: 92px;
  display: block;
}

.ad-list {
  margin: 0;
  padding-left: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.38rem;
  font-size: 0.76rem;
  line-height: 1.4;
  color: var(--text-secondary);
}
</style>
