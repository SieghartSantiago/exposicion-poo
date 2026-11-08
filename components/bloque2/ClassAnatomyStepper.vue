<script setup lang="ts">
import { computed } from "vue";
import { useSlideContext } from "@slidev/client";
import PythonCodePanel from "../common/PythonCodePanel.vue";

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

const fullClassLines = [
  "class TermostatoAula:",
  "    def __init__(self, aula: str, meta: float = 22.0) -> None:",
  "        if not (16.0 <= meta <= 28.0):",
  '            raise ValueError("Meta fuera de rango")',
  "        self._aula: str = aula",
  "        self._meta_c: float = meta",
  "        self._encendido: bool = False",
  "",
  "    @property",
  "    def estado(self) -> str:",
  '        modo = "ACTIVO" if self._encendido else "REPOSO"',
  '        return f"{self._aula}: {self._meta_c}°C ({modo})"',
  "",
  "    def evaluar(self, temp_actual: float) -> None:",
  "        self._encendido = temp_actual < self._meta_c",
];

const stepConfigs: Record<
  Step,
  {
    short: string;
    accent: "class" | "state" | "interface" | "valid";
    status: string;
    highlights: number[];
    kicker: string;
    title: string;
    desc: string;
    points: { label: string; detail: string }[];
  }
> = {
  0: {
    short: "1. Clase y <code>__init__</code>",
    accent: "class",
    status: "Plantilla + Constructor",
    highlights: [0, 1, 2, 3],
    kicker: "Molde e Inicialización",
    title: "<code>class</code> y el constructor <code>__init__</code>",
    desc: "La clase es un plano estático: define qué datos tendrá cada objeto y cómo validarlos al nacer.",
    points: [
      {
        label: "Parámetro self",
        detail: "Referencia explícita en Python a la instancia concreta que se está construyendo o usando.",
      },
      {
        label: "Validación temprana",
        detail: "Si <code>meta</code> está fuera de 16-28 °C, el objeto ni siquiera llega a crearse.",
      },
    ],
  },
  1: {
    short: "2. Atributos (Estado)",
    accent: "state",
    status: "Estado por Instancia",
    highlights: [4, 5, 6],
    kicker: "Datos Propios",
    title: "Atributos = Estado del objeto",
    desc: "Cada atributo ligado a <code>self</code> almacena la situación actual de esa instancia particular en ejecución.",
    points: [
      {
        label: "self._aula / self._meta_c",
        detail: "Dos aulas distintas tendrán sus propios valores sin interferirse mutuamente.",
      },
      {
        label: "Tipado explícito",
        detail: "Anotar <code>str</code>, <code>float</code> y <code>bool</code> documenta el contrato para humanos y analizadores.",
      },
    ],
  },
  2: {
    short: "3. Métodos (Conducta)",
    accent: "interface",
    status: "Interfaz Pública",
    highlights: [8, 9, 10, 11, 13, 14],
    kicker: "Operaciones y Mensajes",
    title: "Métodos = Comportamiento cohesivo",
    desc: "Los métodos definen qué mensajes comprende el objeto y cómo evoluciona su estado de forma controlada.",
    points: [
      {
        label: "@property estado",
        detail: "Calcula una vista legible de solo lectura sin exponer las banderas internas.",
      },
      {
        label: "evaluar(temp_actual)",
        detail: "Actualiza <code>self._encendido</code> aplicando la regla propia del termostato.",
      },
    ],
  },
  3: {
    short: "4. Instancia viva",
    accent: "valid",
    status: "Ejecución Real",
    highlights: [1, 9, 13],
    kicker: "Resultado en Ejecución",
    title: "De la definición al objeto vivo",
    desc: "Al invocar <code>TermostatoAula('Lab 3', 23.0)</code>, Python reserva la instancia, ejecuta <code>__init__</code> y devuelve su referencia.",
    points: [
      {
        label: "t = TermostatoAula('Lab 3', 23.0)",
        detail: '<code>t.estado</code> → <code>"Lab 3: 23.0°C (REPOSO)"</code>',
      },
      {
        label: "t.evaluar(19.5)",
        detail: 'Cambia estado interno → <code>"Lab 3: 23.0°C (ACTIVO)"</code>',
      },
    ],
  },
};

const cfg = computed(() => stepConfigs[step.value]);
</script>

<template>
  <div class="anat-stage">
    <nav class="anat-nav" aria-label="Construcción gradual de una clase">
      <button
        v-for="idx in ([0, 1, 2, 3] as Step[])"
        :key="idx"
        type="button"
        class="anat-btn"
        :class="{ 'is-active': step === idx }"
        @click="setStep(idx)"
        v-html="stepConfigs[idx].short"
      />
    </nav>

    <div class="anat-grid">
      <PythonCodePanel
        file-name="termostato_aula.py"
        :status-text="cfg.status"
        :accent="cfg.accent"
        :lines="fullClassLines"
        :state-key="step"
        :highlight-indices="cfg.highlights"
      />

      <div class="anat-explain">
        <Transition name="poo-fade" mode="out-in">
          <article :key="step" class="anat-card" :data-accent="cfg.accent">
            <div class="anat-head">
              <span class="poo-kicker" v-html="cfg.kicker" />
              <h3 v-html="cfg.title" />
              <p v-html="cfg.desc" />
            </div>

            <div class="anat-points">
              <div v-for="pt in cfg.points" :key="pt.label" class="anat-point">
                <strong v-html="pt.label" />
                <span v-html="pt.detail" />
              </div>
            </div>
          </article>
        </Transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
.anat-stage {
  display: grid;
  grid-template-rows: 34px minmax(0, 1fr);
  row-gap: 0.7rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.anat-nav {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.55rem;
}

.anat-btn {
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

.anat-btn.is-active {
  background: var(--tint-class);
  border-color: rgba(129, 140, 248, 0.55);
  color: #e0e7ff;
}

.anat-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.12fr) minmax(0, 0.88fr);
  gap: 1.15rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.anat-explain {
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.anat-card {
  box-sizing: border-box;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.75rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-top: 3px solid var(--accent-class);
  border-radius: var(--radius-md);
  padding: 0.95rem 1.05rem;
}

.anat-card[data-accent="state"] {
  border-top-color: var(--accent-state);
}

.anat-card[data-accent="interface"] {
  border-top-color: var(--accent-interface);
}

.anat-card[data-accent="valid"] {
  border-top-color: var(--accent-valid);
}

.anat-head {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.42rem;
}

.anat-head h3 {
  font-size: 1.05rem;
  line-height: 1.24;
  font-weight: 700;
}

.anat-head p {
  font-size: 0.8rem;
  line-height: 1.44;
  color: var(--text-secondary);
}

.anat-points {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.anat-point {
  background: #0b1120;
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 0.55rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.anat-point strong {
  font-family: var(--font-mono);
  font-size: 0.74rem;
  color: #7dd3fc;
}

.anat-point span {
  font-size: 0.76rem;
  line-height: 1.38;
  color: var(--text-secondary);
}
</style>
