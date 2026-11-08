<script setup lang="ts">
import { computed } from "vue";
import { useSlideContext } from "@slidev/client";
import PythonCodePanel from "../common/PythonCodePanel.vue";

const { $clicks } = useSlideContext();

type Step = 0 | 1 | 2;

const step = computed<Step>(() => {
  const n = Number($clicks?.value ?? 0);
  if (n <= 0) return 0;
  if (n === 1) return 1;
  return 2;
});

function setStep(s: Step) {
  if ($clicks) $clicks.value = s;
}

const steps = {
  0: {
    tab: "1. Problema: condicionales rígidos",
    file: "01_pedido_acoplado.py",
    status: "Difícil de extender",
    accent: "problem" as const,
    lines: [
      "class PedidoAcoplado:",
      "    def total(self, bruto: float, promo: str) -> float:",
      '        if promo == "regular":',
      "            return bruto",
      '        elif promo == "estudiante":',
      "            return bruto * 0.85",
      '        elif promo == "mayorista":',
      "            return bruto * 0.80",
      '        raise ValueError("Regla desconocida")',
      "",
      "# Mezcla estado del pedido con todas las promociones!",
    ],
  },
  1: {
    tab: "2. Solución: Contrato + Contexto",
    file: "02_patron_strategy.py",
    status: "Composición limpia",
    accent: "interface" as const,
    lines: [
      "class Estrategia(Protocol):",
      "    def descontar(self, bruto: float) -> float: ...",
      "",
      "class PromoEstudiante:",
      "    def descontar(self, bruto: float) -> float:",
      "        return bruto * 0.15",
      "",
      "class Pedido:",
      "    def __init__(self, bruto: float, est: Estrategia):",
      "        self._bruto = bruto",
      "        self.est = est  # Referencia intercambiable",
      "",
      "    def total(self) -> float:",
      "        return self._bruto - self.est.descontar(self._bruto)",
    ],
  },
  2: {
    tab: "3. Intercambio en tiempo real",
    file: "03_cambio_dinamico.py",
    status: "Sustitución en caliente",
    accent: "valid" as const,
    lines: [
      "class PromoMayorista:",
      "    def descontar(self, bruto: float) -> float:",
      "        return bruto * 0.20",
      "",
      "# Misma instancia de Pedido cambia de algoritmo en vivo:",
      "pedido = Pedido(100_000.0, PromoEstudiante())",
      "print(pedido.total())      # -> 85000.0",
      "",
      "pedido.est = PromoMayorista()",
      "print(pedido.total())      # -> 80000.0",
    ],
  },
};

const cur = computed(() => steps[step.value]);
</script>

<template>
  <div class="str-stage">
    <nav class="str-nav" aria-label="Etapas del patrón Strategy">
      <button
        v-for="idx in ([0, 1, 2] as Step[])"
        :key="idx"
        type="button"
        class="str-btn"
        :class="{ 'is-active': step === idx }"
        @click="setStep(idx)"
        v-html="steps[idx].tab"
      />
    </nav>

    <div class="str-grid">
      <PythonCodePanel
        :file-name="cur.file"
        :status-text="cur.status"
        :accent="cur.accent"
        :lines="cur.lines"
        :state-key="step"
      />

      <div class="str-right">
        <Transition name="poo-fade" mode="out-in">
          <article v-if="step === 0" key="s0" class="str-card str-card--problem">
            <span class="poo-kicker poo-kicker--problem">El Problema</span>
            <h3>Algoritmos soldados dentro del contexto</h3>
            <p class="str-p">
              Cuando las políticas variables viven dentro de <code>Pedido</code>, no pueden probarse aisladas ni reutilizarse en otro módulo (como un presupuestador), y violan el principio Abierto/Cerrado.
            </p>
          </article>

          <article v-else-if="step === 1" key="s1" class="str-card str-card--interface">
            <span class="poo-kicker">Estructura del Patrón Strategy</span>
            <h3>Contexto que delega en una interfaz</h3>
            <svg viewBox="0 0 360 140" class="str-svg" role="img" aria-label="Diagrama Strategy">
              <rect x="10" y="38" width="114" height="64" rx="9" fill="#0b1120" stroke="#38bdf8" stroke-width="1.6" />
              <text x="67" y="64" text-anchor="middle" fill="#7dd3fc" style="font-family: var(--font-mono); font-size: 11px; font-weight: 700;">Pedido</text>
              <text x="67" y="84" text-anchor="middle" fill="#cbd5e1" style="font-size: 9.5px;">delega total()</text>

              <line x1="126" y1="70" x2="182" y2="70" stroke="#38bdf8" stroke-width="2" />
              <polygon points="186,70 178,65 178,75" fill="#38bdf8" />

              <rect x="188" y="12" width="162" height="48" rx="8" fill="rgba(129,140,248,0.14)" stroke="#818cf8" />
              <text x="269" y="33" text-anchor="middle" fill="#e0e7ff" style="font-size: 10px; font-weight: 700;">«Protocol» Estrategia</text>
              <text x="269" y="49" text-anchor="middle" fill="#cbd5e1" style="font-family: var(--font-mono); font-size: 9.5px;">descontar(bruto)</text>

              <rect x="188" y="80" width="76" height="46" rx="7" fill="#0b1120" stroke="#34d399" />
              <text x="226" y="107" text-anchor="middle" fill="#6ee7b7" style="font-size: 9.5px;">Estudiante</text>

              <rect x="274" y="80" width="76" height="46" rx="7" fill="#0b1120" stroke="#34d399" />
              <text x="312" y="107" text-anchor="middle" fill="#6ee7b7" style="font-size: 9.5px;">Mayorista</text>
            </svg>
            <p class="str-p">
              Reemplaza una explosión de subclases (<code>PedidoEstudiante</code>, <code>PedidoMayorista</code>) por objetos ligeros intercambiables.
            </p>
          </article>

          <article v-else key="s2" class="str-card str-card--valid">
            <span class="poo-kicker poo-kicker--valid">Mejora Obtenida</span>
            <h3>Sustitución dinámica en tiempo de ejecución</h3>
            <div class="str-swap">
              <div class="str-row">
                <code>PromoEstudiante (15 %)</code>
                <strong>$100.000 → $85.000</strong>
              </div>
              <div class="str-row str-row--active">
                <code>PromoMayorista (20 %)</code>
                <strong>$100.000 → $80.000</strong>
              </div>
            </div>
            <p class="str-p">
              El objeto <code>pedido</code> conserva su identidad y sus ítems mientras cambia instantáneamente su regla de liquidación.
            </p>
          </article>
        </Transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
.str-stage {
  display: grid;
  grid-template-rows: 34px minmax(0, 1fr);
  row-gap: 0.7rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.str-nav {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.6rem;
}

.str-btn {
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

.str-btn.is-active {
  background: var(--tint-valid);
  border-color: rgba(52, 211, 153, 0.55);
  color: #d1fae5;
}

.str-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(0, 0.92fr);
  gap: 1.15rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.str-right {
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.str-card {
  box-sizing: border-box;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.6rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 0.95rem 1.05rem;
}

.str-card--problem {
  border-top: 3px solid var(--accent-problem);
}

.str-card--interface {
  border-top: 3px solid var(--accent-interface);
}

.str-card--valid {
  border-top: 3px solid var(--accent-valid);
}

.str-card h3 {
  font-size: 1.04rem;
  line-height: 1.24;
  font-weight: 700;
}

.str-p {
  font-size: 0.79rem;
  line-height: 1.44;
  color: var(--text-secondary);
}

.str-svg {
  width: 100%;
  height: auto;
  max-height: 132px;
  display: block;
}

.str-swap {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.str-row {
  background: #0b1120;
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 0.52rem 0.7rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.76rem;
}

.str-row--active {
  border-color: rgba(52, 211, 153, 0.5);
  background: rgba(52, 211, 153, 0.1);
}
</style>
