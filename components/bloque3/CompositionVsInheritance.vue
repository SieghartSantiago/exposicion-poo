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

const badInheritanceLines = [
  "# ANTIPATRÓN: heredar solo para reutilizar list",
  "class PilaInsegura(list):",
  "    def apilar(self, x: int) -> None:",
  "        self.append(x)",
  "",
  "pila = PilaInsegura()",
  "pila.apilar(10)",
  "pila.apilar(20)",
  "",
  "# Hereda toda la interfaz pública de list!",
  "# Cualquiera rompe la invariante LIFO:",
  "pila.insert(0, 999)",
];

const goodCompositionLines = [
  "# SOLUCIÓN: Composición («tiene-un») + Delegación",
  "class PilaSegura:",
  "    def __init__(self) -> None:",
  "        self._datos: list[int] = []",
  "",
  "    def apilar(self, x: int) -> None:",
  "        self._datos.append(x)  # Delega adentro",
  "",
  "    def desapilar(self) -> int:",
  "        if not self._datos:",
  '            raise ValueError("Pila vacía")',
  "        return self._datos.pop()",
];
</script>

<template>
  <div class="ci-stage">
    <nav class="ci-nav" aria-label="Comparación entre herencia y composición">
      <button type="button" class="ci-btn" :class="{ 'is-active': step === 0 }" @click="setStep(0)">
        1. Patologías del abuso de herencia
      </button>
      <button type="button" class="ci-btn" :class="{ 'is-active': step === 1 }" @click="setStep(1)">
        2. Composición y delegación en Python
      </button>
      <button type="button" class="ci-btn" :class="{ 'is-active': step === 2 }" @click="setStep(2)">
        3. Matriz de decisión arquitectónica
      </button>
    </nav>

    <div class="ci-body">
      <Transition name="poo-fade" mode="out-in">
        <!-- PASO 0 -->
        <div v-if="step === 0" key="ci0" class="ci-split">
          <PythonCodePanel
            file-name="antipatron_pila_list.py"
            status-text="Invariante LIFO rota"
            accent="problem"
            :lines="badInheritanceLines"
            state-key="bad"
          />
          <article class="ci-card ci-card--problem">
            <span class="poo-kicker poo-kicker--problem">Cuándo falla la herencia</span>
            <h3>Tres patologías clásicas</h3>
            <ul class="ci-list">
              <li>
                <strong>Exposición de interfaz ajena:</strong> igual que el histórico <code>Stack extends Vector</code> en Java, heredar de <code>list</code> filtra <code>insert()</code> y <code>sort()</code>, violando LIFO.
              </li>
              <li>
                <strong>Clase Base Frágil:</strong> pequeños cambios internos en la superclase rompen subclases lejanas (reúso de «caja blanca»).
              </li>
              <li>
                <strong>Jerarquías forzadas:</strong> <code>Pinguino(Ave)</code> anulando <code>volar()</code> con excepciones rompe la sustitución polimórfica.
              </li>
            </ul>
          </article>
        </div>

        <!-- PASO 1 -->
        <div v-else-if="step === 1" key="ci1" class="ci-split">
          <PythonCodePanel
            file-name="composicion_delegacion.py"
            status-text="Caja negra segura"
            accent="valid"
            :lines="goodCompositionLines"
            state-key="good"
          />
          <article class="ci-card ci-card--valid">
            <span class="poo-kicker poo-kicker--valid">Máxima Moderna (GoF)</span>
            <h3>Favorecer composición sobre herencia</h3>
            <ul class="ci-list">
              <li>
                <strong>Composición («tiene-un»):</strong> <code>PilaSegura</code> contiene una lista interna privada <code>self._datos</code> sin heredar su interfaz pública.
              </li>
              <li>
                <strong>Delegación:</strong> cada operación pública redirige el trabajo al colaborador interno bajo reglas controladas.
              </li>
              <li>
                <strong>Flexibilidad dinámica:</strong> un colaborador compuesto puede cambiarse en tiempo de ejecución; una superclase queda fija al definir la clase.
              </li>
            </ul>
          </article>
        </div>

        <!-- PASO 2: MATRIZ COMPARATIVA -->
        <div v-else key="ci2" class="ci-matrix-wrap">
          <table class="ci-table">
            <thead>
              <tr>
                <th>Dimensión</th>
                <th>Herencia de Clases («es-un»)</th>
                <th>Composición + Delegación («tiene-un»)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Tiempo de ligadura</strong></td>
                <td>Estática (fijada en la definición de la clase)</td>
                <td>Dinámica (intercambiable en tiempo de ejecución)</td>
              </tr>
              <tr>
                <td><strong>Visibilidad del reúso</strong></td>
                <td>«Caja blanca»: subclase conoce detalles de la base</td>
                <td>«Caja negra»: interactúa solo con la interfaz pública</td>
              </tr>
              <tr>
                <td><strong>Acoplamiento</strong></td>
                <td>Alto (cambios en la base impactan en derivadas)</td>
                <td>Bajo (acoplado únicamente al contrato del colaborador)</td>
              </tr>
              <tr>
                <td><strong>Cuándo elegirla</strong></td>
                <td>Relación taxonómica genuina y subtipado completo</td>
                <td>Reutilizar estructuras o combinar comportamientos variables</td>
              </tr>
            </tbody>
          </table>
        </div>
      </Transition>
    </div>
  </div>
</template>

<style scoped>
.ci-stage {
  display: grid;
  grid-template-rows: 34px minmax(0, 1fr);
  row-gap: 0.7rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.ci-nav {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.6rem;
}

.ci-btn {
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

.ci-btn.is-active {
  background: var(--tint-interface);
  border-color: rgba(56, 189, 248, 0.55);
  color: #e0f2fe;
}

.ci-body {
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.ci-split {
  display: grid;
  grid-template-columns: minmax(0, 1.06fr) minmax(0, 0.94fr);
  gap: 1.15rem;
  height: 100%;
}

.ci-card {
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

.ci-card--problem {
  border-top: 3px solid var(--accent-problem);
}

.ci-card--valid {
  border-top: 3px solid var(--accent-valid);
}

.ci-card h3 {
  font-size: 1.03rem;
  line-height: 1.24;
  font-weight: 700;
}

.ci-list {
  margin: 0;
  padding-left: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.44rem;
  font-size: 0.77rem;
  line-height: 1.42;
  color: var(--text-secondary);
}

.ci-matrix-wrap {
  box-sizing: border-box;
  height: 100%;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-top: 3px solid var(--accent-interface);
  border-radius: var(--radius-md);
  padding: 0.85rem 1rem;
  display: flex;
  align-items: center;
}

.ci-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.79rem;
}

.ci-table th,
.ci-table td {
  padding: 0.62rem 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--border-subtle);
}

.ci-table th {
  font-size: 0.71rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #7dd3fc;
  background: #0b1120;
}

.ci-table tr:last-child td {
  border-bottom: none;
}
</style>
