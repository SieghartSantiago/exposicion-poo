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

const codeByStep: Record<Step, { file: string; status: string; accent: "problem" | "interface" | "valid"; lines: string[] }> = {
  0: {
    file: "01_sin_abstraccion.py",
    status: "Detalles expuestos",
    accent: "problem",
    lines: [
      "# El cliente manipula minutos crudos y reglas sueltas",
      "inicio_min = 9 * 60 + 30",
      "fin_min = 8 * 60 + 15      # Fin anterior al inicio!",
      "",
      "# Cada módulo debe recordar cómo calcular y validar:",
      "duracion = fin_min - inicio_min  # -75 min (inválido)",
      "",
      "# Si mañana pasamos a segundos, se rompen todos",
      "# los puntos que asumían minutos enteros.",
    ],
  },
  1: {
    file: "02_contrato_temperatura.py",
    status: "Interfaz + Invariante",
    accent: "interface",
    lines: [
      "class Temperatura:",
      '    """Invariante: _kelvin >= 0.0 (cero absoluto)"""',
      "    def __init__(self, celsius: float) -> None:",
      "        kelvin = celsius + 273.15",
      "        if kelvin < 0.0:",
      '            raise ValueError("Menor a 0 K físico")',
      "        self._kelvin: float = kelvin",
      "",
      "    @property",
      "    def celsius(self) -> float:",
      "        return round(self._kelvin - 273.15, 2)",
      "",
      "    @property",
      "    def kelvin(self) -> float:",
      "        return round(self._kelvin, 2)",
    ],
  },
  2: {
    file: "03_evolucion_interna.py",
    status: "Cliente desacoplado",
    accent: "valid",
    lines: [
      "# El código cliente solo conoce la INTERFAZ PÚBLICA:",
      "t = Temperatura(celsius=25.0)",
      "print(t.celsius)   # 25.0",
      "print(t.kelvin)    # 298.15",
      "",
      "# Intento de violar la invariante física (-300 °C):",
      "try:",
      "    Temperatura(celsius=-300.0)",
      "except ValueError as err:",
      '    print(err)     # "Menor a 0 K físico"',
    ],
  },
};

const cur = computed(() => codeByStep[step.value]);
</script>

<template>
  <div class="abs-stage">
    <nav class="abs-nav" aria-label="Pasos de abstracción e invariantes">
      <button type="button" class="abs-btn" :class="{ 'is-active': step === 0 }" @click="setStep(0)">
        1. Problema: detalles expuestos
      </button>
      <button type="button" class="abs-btn" :class="{ 'is-active': step === 1 }" @click="setStep(1)">
        2. Interfaz vs. Implementación
      </button>
      <button type="button" class="abs-btn" :class="{ 'is-active': step === 2 }" @click="setStep(2)">
        3. Garantía y límites
      </button>
    </nav>

    <div class="abs-grid">
      <PythonCodePanel
        :file-name="cur.file"
        :status-text="cur.status"
        :accent="cur.accent"
        :lines="cur.lines"
        :state-key="step"
      />

      <div class="abs-right">
        <Transition name="poo-fade" mode="out-in">
          <article v-if="step === 0" key="a0" class="abs-card abs-card--problem">
            <span class="poo-kicker poo-kicker--problem">El Problema</span>
            <h3>Complejidad accidental en el cliente</h3>
            <p class="abs-p">
              Cuando no existe una abstracción del dominio, cada parte del programa debe conocer fórmulas internas, unidades físicas y restricciones de validez.
            </p>
            <div class="abs-split-box">
              <div class="abs-mini">
                <strong>Riesgo 1</strong>
                <span>Estados imposibles en el mundo real (duraciones o Kelvin negativos).</span>
              </div>
              <div class="abs-mini">
                <strong>Riesgo 2</strong>
                <span>Alto esfuerzo cognitivo para entender qué representa cada número suelto.</span>
              </div>
            </div>
          </article>

          <article v-else-if="step === 1" key="a1" class="abs-card abs-card--interface">
            <span class="poo-kicker">El Principio</span>
            <h3>Separar el «Qué hace» del «Cómo lo hace»</h3>
            <div class="abs-layers">
              <div class="abs-layer abs-layer--pub">
                <strong>Interfaz Pública (¿Qué ofrece?)</strong>
                <span><code>Temperatura(c)</code> · <code>.celsius</code> · <code>.kelvin</code></span>
              </div>
              <div class="abs-layer abs-layer--inv">
                <strong>Invariante de Representación</strong>
                <span>Predicado verdadero tras <code>__init__</code> y en cada método: <code>_kelvin &gt;= 0</code></span>
              </div>
              <div class="abs-layer abs-layer--priv">
                <strong>Implementación (¿Cómo se guarda?)</strong>
                <span>Almacena solo <code>self._kelvin</code> y calcula Celsius al vuelo</span>
              </div>
            </div>
          </article>

          <article v-else key="a2" class="abs-card abs-card--valid">
            <span class="poo-kicker poo-kicker--valid">Ventajas y Limitaciones</span>
            <h3>Independencia de representación</h3>
            <ul class="abs-list">
              <li>
                <strong>Ventaja clave:</strong> podríamos guardar internamente Celsius o Kelvin sin tocar una sola línea del código cliente.
              </li>
              <li>
                <strong>Detección inmediata:</strong> <code>Temperatura(-300)</code> falla en el origen con un mensaje claro de dominio.
              </li>
              <li>
                <strong>Límite a cuidar:</strong> abstraer en exceso conceptos triviales agrega clases innecesarias; abstraé cuando exista una regla o variación real.
              </li>
            </ul>
          </article>
        </Transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
.abs-stage {
  display: grid;
  grid-template-rows: 34px minmax(0, 1fr);
  row-gap: 0.7rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.abs-nav {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.6rem;
}

.abs-btn {
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

.abs-btn.is-active {
  background: var(--tint-interface);
  border-color: rgba(56, 189, 248, 0.55);
  color: #e0f2fe;
}

.abs-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(0, 0.92fr);
  gap: 1.15rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.abs-right {
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.abs-card {
  box-sizing: border-box;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.65rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 0.95rem 1.05rem;
}

.abs-card--problem {
  border-top: 3px solid var(--accent-problem);
}

.abs-card--interface {
  border-top: 3px solid var(--accent-interface);
}

.abs-card--valid {
  border-top: 3px solid var(--accent-valid);
}

.abs-card h3 {
  font-size: 1.04rem;
  line-height: 1.24;
  font-weight: 700;
}

.abs-p {
  font-size: 0.8rem;
  line-height: 1.44;
  color: var(--text-secondary);
}

.abs-split-box {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.abs-mini {
  background: #0b1120;
  border: 1px solid rgba(251, 113, 133, 0.32);
  border-radius: 8px;
  padding: 0.52rem 0.7rem;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.abs-mini strong {
  font-size: 0.72rem;
  color: #fda4af;
}

.abs-mini span {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.abs-layers {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.abs-layer {
  border-radius: 8px;
  padding: 0.48rem 0.68rem;
  display: flex;
  flex-direction: column;
  gap: 0.16rem;
  font-size: 0.74rem;
}

.abs-layer--pub {
  background: rgba(56, 189, 248, 0.1);
  border: 1px solid rgba(56, 189, 248, 0.34);
}

.abs-layer--inv {
  background: rgba(52, 211, 153, 0.1);
  border: 1px solid rgba(52, 211, 153, 0.34);
}

.abs-layer--priv {
  background: rgba(129, 140, 248, 0.1);
  border: 1px solid rgba(129, 140, 248, 0.34);
}

.abs-layer strong {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-primary);
}

.abs-layer span {
  color: var(--text-secondary);
}

.abs-list {
  margin: 0;
  padding-left: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.42rem;
  font-size: 0.77rem;
  line-height: 1.42;
  color: var(--text-secondary);
}
</style>
