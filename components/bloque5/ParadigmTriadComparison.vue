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

const paradigms = {
  0: {
    tab: "1. Imperativo (Flujo explícito)",
    file: "ventas_imperativo.py",
    status: "O(n) · Estado mutable local",
    accent: "state" as const,
    lines: [
      "# Problema común: sumar ventas activas >= $3.000 + IVA 21%",
      "def liquidar_imperativo(filas: list[dict]) -> float:",
      "    total = 0.0",
      "    for f in filas:",
      '        if not f["activa"] or f["monto"] < 3000.0:',
      "            continue",
      '        total += f["monto"] * 1.21',
      "    return round(total, 2)",
      "",
      '# Salida sobre lote ejemplo -> $18,150.00',
    ],
    kicker: "Enfoque Imperativo / Procedural",
    title: "Control paso a paso con acumuladores",
    pros: "Directo, conciso y con mínima sobrecarga estructural cuando la regla es fija.",
    cons: "Si aparecen múltiples políticas fiscales o validaciones de entidad, el bucle crece con condicionales acoplados.",
  },
  1: {
    tab: "2. Orientado a Objetos (Contratos)",
    file: "ventas_poo.py",
    status: "O(n) · Entidad con invariante",
    accent: "class" as const,
    lines: [
      "class Venta:",
      "    def __init__(self, monto: float, activa: bool) -> None:",
      "        if monto <= 0: raise ValueError()",
      "        self._monto, self.activa = monto, activa",
      "",
      "    def con_iva(self, alicuota: float = 0.21) -> float:",
      "        return self._monto * (1.0 + alicuota)",
      "",
      "def liquidar_poo(ventas: list[Venta]) -> float:",
      "    return round(sum(",
      "        v.con_iva() for v in ventas",
      "        if v.activa and v.con_iva(0.0) >= 3000.0",
      "    ), 2)",
    ],
    kicker: "Enfoque Orientado a Objetos",
    title: "Reglas encapsuladas en entidades del dominio",
    pros: "Garantiza instancias válidas desde su creación y permite enchufar estrategias impositivas polimórficas.",
    cons: "Introduce más definiciones e instancias; excesivo si solo se suma una columna descartable una única vez.",
  },
  2: {
    tab: "3. Funcional (Sin mutación)",
    file: "ventas_funcional.py",
    status: "O(n) · Funciones puras",
    accent: "interface" as const,
    lines: [
      "from typing import Iterable",
      "",
      "def es_liquidable(f: dict) -> bool:",
      '    return bool(f["activa"]) and f["monto"] >= 3000.0',
      "",
      "def aplicar_iva(f: dict) -> float:",
      '    return float(f["monto"]) * 1.21',
      "",
      "def liquidar_funcional(filas: Iterable[dict]) -> float:",
      "    validas = filter(es_liquidable, filas)",
      "    return round(sum(map(aplicar_iva, validas)), 2)",
      "",
      "# Los 3 paradigmas recorren n filas -> O(n) lineal",
    ],
    kicker: "Enfoque Funcional + Síntesis",
    title: "Transformación declarativa sin efectos secundarios",
    pros: "Cada función pura se prueba trivialmente y no altera datos compartidos; ideal en pipelines y concurrencia.",
    cons: "Ningún paradigma es universalmente superior: la ingeniería moderna combina arquitectura de objetos con métodos internamente funcionales.",
  },
};

const cur = computed(() => paradigms[step.value]);
</script>

<template>
  <div class="tri-stage">
    <nav class="tri-nav" aria-label="Comparación entre tres paradigmas">
      <button
        v-for="idx in ([0, 1, 2] as Step[])"
        :key="idx"
        type="button"
        class="tri-btn"
        :class="{ 'is-active': step === idx }"
        @click="setStep(idx)"
        v-html="paradigms[idx].tab"
      />
    </nav>

    <div class="tri-grid">
      <PythonCodePanel
        :file-name="cur.file"
        :status-text="cur.status"
        :accent="cur.accent"
        :lines="cur.lines"
        :state-key="step"
      />

      <div class="tri-right">
        <Transition name="poo-fade" mode="out-in">
          <article :key="step" class="tri-card">
            <div class="tri-head">
              <span class="poo-kicker" v-html="cur.kicker" />
              <h3 v-html="cur.title" />
            </div>

            <div class="tri-box tri-box--pro">
              <strong>Dónde brilla</strong>
              <p v-html="cur.pros" />
            </div>

            <div class="tri-box tri-box--con">
              <strong>Compromiso / Criterio</strong>
              <p v-html="cur.cons" />
            </div>
          </article>
        </Transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tri-stage {
  display: grid;
  grid-template-rows: 34px minmax(0, 1fr);
  row-gap: 0.7rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.tri-nav {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.6rem;
}

.tri-btn {
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

.tri-btn.is-active {
  background: var(--tint-interface);
  border-color: rgba(56, 189, 248, 0.55);
  color: #e0f2fe;
}

.tri-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(0, 0.92fr);
  gap: 1.15rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.tri-right {
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.tri-card {
  box-sizing: border-box;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.6rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-top: 3px solid var(--accent-interface);
  border-radius: var(--radius-md);
  padding: 0.95rem 1.05rem;
}

.tri-head {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.4rem;
}

.tri-head h3 {
  font-size: 1.02rem;
  line-height: 1.24;
  font-weight: 700;
}

.tri-box {
  border-radius: 8px;
  padding: 0.55rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.tri-box strong {
  font-size: 0.69rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.tri-box p {
  font-size: 0.76rem;
  line-height: 1.42;
}

.tri-box--pro {
  background: rgba(52, 211, 153, 0.09);
  border: 1px solid rgba(52, 211, 153, 0.34);
}

.tri-box--pro strong {
  color: #6ee7b7;
}

.tri-box--con {
  background: rgba(251, 191, 36, 0.09);
  border: 1px solid rgba(251, 191, 36, 0.34);
}

.tri-box--con strong {
  color: #fde68a;
}
</style>
