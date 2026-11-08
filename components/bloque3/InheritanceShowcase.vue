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
    tab: "1. Problema: duplicación",
    file: "01_clases_duplicadas.py",
    status: "Código repetido",
    accent: "problem" as const,
    lines: [
      "class EnvioEstandar:",
      "    def __init__(self, codigo: str, peso: float) -> None:",
      "        if peso <= 0:",
      '            raise ValueError("Peso inválido")',
      "        self.codigo = codigo",
      "        self.peso = peso",
      "",
      "class EnvioExpres:",
      "    def __init__(self, codigo: str, peso: float) -> None:",
      "        if peso <= 0:  # Validación copiada y pegada!",
      '            raise ValueError("Peso inválido")',
      "        self.codigo = codigo",
      "        self.peso = peso",
    ],
  },
  1: {
    tab: "2. Jerarquía con <code>ABC</code> y <code>super()</code>",
    file: "02_jerarquia_envio.py",
    status: "Relación «es-un»",
    accent: "class" as const,
    lines: [
      "from abc import ABC, abstractmethod",
      "",
      "class Envio(ABC):",
      "    def __init__(self, codigo: str, peso: float) -> None:",
      "        if peso <= 0:",
      '            raise ValueError("Peso <= 0")',
      "        self.codigo, self.peso = codigo, peso",
      "",
      "    @abstractmethod",
      "    def calcular_costo(self) -> float: ...",
      "",
      "class EnvioExpres(Envio):",
      "    def calcular_costo(self) -> float:",
      "        return (3800.0 + self.peso * 550.0) * 1.20",
    ],
  },
  2: {
    tab: "3. Subclase vs. Subtipo y <code>MRO</code>",
    file: "03_subtipo_y_mro.py",
    status: "Precisión académica",
    accent: "valid" as const,
    lines: [
      "class EnvioRefrigerado(Envio):",
      "    def __init__(self, codigo: str, peso: float, c: float):",
      "        super().__init__(codigo, peso)  # Reúsa invariante",
      "        self.temp_c = c",
      "",
      "    def calcular_costo(self) -> float:",
      "        return 4600.0 + self.peso * 600.0",
      "",
      "# Orden de Resolución de Métodos (algoritmo C3):",
      "# [cls.__name__ for cls in EnvioRefrigerado.mro()]",
      '# -> ["EnvioRefrigerado", "Envio", "ABC", "object"]',
    ],
  },
};

const cur = computed(() => steps[step.value]);
</script>

<template>
  <div class="inh-stage">
    <nav class="inh-nav" aria-label="Etapas de herencia">
      <button
        v-for="idx in ([0, 1, 2] as Step[])"
        :key="idx"
        type="button"
        class="inh-btn"
        :class="{ 'is-active': step === idx }"
        @click="setStep(idx)"
        v-html="steps[idx].tab"
      />
    </nav>

    <div class="inh-grid">
      <PythonCodePanel
        :file-name="cur.file"
        :status-text="cur.status"
        :accent="cur.accent"
        :lines="cur.lines"
        :state-key="step"
      />

      <div class="inh-right">
        <Transition name="poo-fade" mode="out-in">
          <!-- PASO 0 -->
          <article v-if="step === 0" key="i0" class="inh-card inh-card--problem">
            <span class="poo-kicker poo-kicker--problem">El Problema</span>
            <h3>Clases paralelas sin factor común</h3>
            <p class="inh-p">
              Repetir atributos e invariantes entre variantes de una misma familia multiplica el mantenimiento y carece de un tipo común para procesarlas juntas.
            </p>
            <div class="inh-callout">
              <strong>Síntoma clásico:</strong> corregir una validación en <code>EnvioEstandar</code> y olvidar actualizarla en <code>EnvioExpres</code>.
            </div>
          </article>

          <!-- PASO 1: ÁRBOL DE HERENCIA ANIMADO -->
          <article v-else-if="step === 1" key="i1" class="inh-card inh-card--class">
            <span class="poo-kicker poo-kicker--class">Árbol de Especialización</span>
            <h3>Clase abstracta común + especializaciones</h3>
            <svg viewBox="0 0 360 150" class="inh-svg" role="img" aria-label="Árbol de herencia de Envio">
              <rect x="105" y="8" width="150" height="46" rx="9" fill="rgba(129,140,248,0.16)" stroke="#818cf8" stroke-width="1.8" />
              <text x="180" y="28" text-anchor="middle" fill="#e0e7ff" style="font-family: var(--font-mono); font-size: 11px; font-weight: 700;">Envio (ABC)</text>
              <text x="180" y="44" text-anchor="middle" fill="#94a3b8" style="font-size: 9.5px;">calcular_costo()</text>

              <line x1="150" y1="54" x2="82" y2="96" stroke="#818cf8" stroke-width="1.8" />
              <line x1="210" y1="54" x2="278" y2="96" stroke="#818cf8" stroke-width="1.8" />

              <rect x="12" y="96" width="140" height="44" rx="8" fill="#0b1120" stroke="#38bdf8" />
              <text x="82" y="122" text-anchor="middle" fill="#7dd3fc" style="font-family: var(--font-mono); font-size: 10.5px;">EnvioEstandar</text>

              <rect x="208" y="96" width="140" height="44" rx="8" fill="#0b1120" stroke="#34d399" />
              <text x="278" y="122" text-anchor="middle" fill="#6ee7b7" style="font-family: var(--font-mono); font-size: 10.5px;">EnvioExpres</text>
            </svg>
            <p class="inh-p">
              <code>@abstractmethod</code> impide instanciar un <code>Envio</code> incompleto y exige implementar la tarifa en cada subclase concreta.
            </p>
          </article>

          <!-- PASO 2: DISTINCIÓN SUBCLASE VS SUBTIPO -->
          <article v-else key="i2" class="inh-card inh-card--valid">
            <span class="poo-kicker poo-kicker--valid">Distinción Conceptual Clave</span>
            <h3>Herencia (Subclase) ≠ Subtipado</h3>
            <ul class="inh-list">
              <li>
                <strong>Herencia (reúso de código):</strong> mecanismo sintáctico para compartir atributos y métodos mediante <code>super()</code>.
              </li>
              <li>
                <strong>Subtipado (contrato conductual):</strong> la subclase solo es un <em>subtipo legítimo</em> si puede sustituir a <code>Envio</code> en cualquier contexto sin romper sus garantías.
              </li>
              <li>
                <strong>Herencia múltiple en Python:</strong> se linealiza de forma determinista con el algoritmo <code>C3 MRO</code>.
              </li>
            </ul>
          </article>
        </Transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
.inh-stage {
  display: grid;
  grid-template-rows: 34px minmax(0, 1fr);
  row-gap: 0.7rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.inh-nav {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.6rem;
}

.inh-btn {
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

.inh-btn.is-active {
  background: var(--tint-class);
  border-color: rgba(129, 140, 248, 0.55);
  color: #e0e7ff;
}

.inh-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(0, 0.92fr);
  gap: 1.15rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.inh-right {
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.inh-card {
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

.inh-card--problem {
  border-top: 3px solid var(--accent-problem);
}

.inh-card--class {
  border-top: 3px solid var(--accent-class);
}

.inh-card--valid {
  border-top: 3px solid var(--accent-valid);
}

.inh-card h3 {
  font-size: 1.04rem;
  line-height: 1.24;
  font-weight: 700;
}

.inh-p {
  font-size: 0.79rem;
  line-height: 1.44;
  color: var(--text-secondary);
}

.inh-svg {
  width: 100%;
  height: auto;
  max-height: 138px;
  display: block;
}

.inh-callout {
  background: rgba(251, 113, 133, 0.1);
  border: 1px solid rgba(251, 113, 133, 0.35);
  border-radius: 8px;
  padding: 0.6rem 0.78rem;
  font-size: 0.77rem;
  line-height: 1.4;
  color: #fecdd3;
}

.inh-list {
  margin: 0;
  padding-left: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  font-size: 0.76rem;
  line-height: 1.4;
  color: var(--text-secondary);
}
</style>
