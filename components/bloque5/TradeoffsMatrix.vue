<script setup lang="ts">
import { computed } from "vue";
import { useSlideContext } from "@slidev/client";

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
</script>

<template>
  <div class="to-stage">
    <nav class="to-nav" aria-label="Análisis de trade-offs de POO">
      <button type="button" class="to-btn" :class="{ 'is-active': step === 0 }" @click="setStep(0)">
        1. Ventajas vs. Costos de diseño
      </button>
      <button type="button" class="to-btn" :class="{ 'is-active': step === 1 }" @click="setStep(1)">
        2. Rendimiento y memoria con rigor
      </button>
      <button type="button" class="to-btn" :class="{ 'is-active': step === 2 }" @click="setStep(2)">
        3. ¿Cuándo NO conviene usar POO?
      </button>
    </nav>

    <div class="to-body">
      <Transition name="poo-fade" mode="out-in">
        <!-- PASO 0 -->
        <div v-if="step === 0" key="t0" class="to-grid-2">
          <article class="to-card to-card--good">
            <span class="poo-kicker poo-kicker--valid">Fortalezas Reales</span>
            <h3>Alta cohesión y bajo acoplamiento</h3>
            <ul class="to-list">
              <li>
                <strong>Invariantes localizadas:</strong> las reglas de validez viven junto al estado que protegen, no dispersas en decenas de scripts.
              </li>
              <li>
                <strong>Extensibilidad modular:</strong> interfaces y delegación permiten incorporar comportamientos nuevos con impacto mínimo en el resto del sistema.
              </li>
              <li>
                <strong>Escalabilidad en equipo:</strong> contratos claros facilitan dividir módulos entre desarrolladores sin pisarse.
              </li>
            </ul>
          </article>

          <article class="to-card to-card--bad">
            <span class="poo-kicker poo-kicker--problem">Limitaciones y Riesgos</span>
            <h3>Sobreingeniería e indirección</h3>
            <ul class="to-list">
              <li>
                <strong>Complejidad accidental:</strong> abusar de jerarquías, fábricas e interfaces para problemas simples oscurece el flujo real del programa.
              </li>
              <li>
                <strong>Estado mutable distribuido:</strong> grafos grandes de objetos que se mutan entre sí pueden complicar la depuración y la concurrencia.
              </li>
              <li>
                <strong>Costo inicial de modelado:</strong> diseñar buenos límites entre clases exige comprender bien el dominio antes de abstraer.
              </li>
            </ul>
          </article>
        </div>

        <!-- PASO 1 -->
        <div v-else-if="step === 1" key="t1" class="to-grid-2">
          <article class="to-card to-card--cyan">
            <span class="poo-kicker">Memoria y Caché</span>
            <h3>Sin mitos ni generalizaciones</h3>
            <ul class="to-list">
              <li>
                <strong>Depende del lenguaje y diseño:</strong> en Python o Java abundan objetos dinámicos referenciados por punteros (menor localidad en caché frente a arreglos contiguos).
              </li>
              <li>
                <strong>No es intrínseco al paradigma:</strong> C++ y C# (<code>struct</code>) permiten componer objetos contiguos por valor sin indirección extra.
              </li>
            </ul>
          </article>

          <article class="to-card to-card--indigo">
            <span class="poo-kicker poo-kicker--class">Despacho y Optimización</span>
            <h3>Medir antes de optimizar</h3>
            <ul class="to-list">
              <li>
                <strong>Costo del enlace dinámico:</strong> una llamada polimórfica implica una indirección, aunque compiladores modernos aplican <em>desvirtualización</em> cuando infieren el tipo concreto.
              </li>
              <li>
                <strong>Regla de ingeniería:</strong> en apps limitadas por red, disco o base de datos ese costo es despreciable; en lazos numéricos intensivos se verifica con <em>profiling</em>.
              </li>
            </ul>
          </article>
        </div>

        <!-- PASO 2 -->
        <div v-else key="t2" class="to-grid-3">
          <article class="to-card to-card--amber">
            <span class="poo-kicker poo-kicker--problem">Caso 01</span>
            <h3>Scripts breves y automatización</h3>
            <p class="to-p">
              Para renombrar archivos, migrar un CSV único o ejecutar tareas lineales de 40 líneas, funciones claras y directas son más legibles que crear múltiples clases.
            </p>
          </article>

          <article class="to-card to-card--amber">
            <span class="poo-kicker poo-kicker--problem">Caso 02</span>
            <h3>Pipelines puros de datos</h3>
            <p class="to-p">
              Transformaciones analíticas o ETL (filtrar, agrupar, proyectar lotes inmutables) se expresan de forma más limpia y segura con un enfoque funcional o vectorial.
            </p>
          </article>

          <article class="to-card to-card--amber">
            <span class="poo-kicker poo-kicker--problem">Caso 03</span>
            <h3>Cómputo numérico masivo</h3>
            <p class="to-p">
              Álgebra lineal, física de partículas o procesamiento de señales sobre millones de escalares requieren matrices contiguas (<code>NumPy</code> / diseño orientado a datos), no un objeto Python por número.
            </p>
          </article>
        </div>
      </Transition>
    </div>
  </div>
</template>

<style scoped>
.to-stage {
  display: grid;
  grid-template-rows: 34px minmax(0, 1fr);
  row-gap: 0.7rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.to-nav {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.6rem;
}

.to-btn {
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

.to-btn.is-active {
  background: var(--tint-interface);
  border-color: rgba(56, 189, 248, 0.55);
  color: #e0f2fe;
}

.to-body {
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.to-grid-2 {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.1rem;
  height: 100%;
}

.to-grid-3 {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  height: 100%;
}

.to-card {
  box-sizing: border-box;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.55rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 0.95rem 1.05rem;
}

.to-card--good {
  border-top: 3px solid var(--accent-valid);
}

.to-card--bad {
  border-top: 3px solid var(--accent-problem);
}

.to-card--cyan {
  border-top: 3px solid var(--accent-interface);
}

.to-card--indigo {
  border-top: 3px solid var(--accent-class);
}

.to-card--amber {
  border-top: 3px solid var(--accent-state);
}

.to-card h3 {
  font-size: 1.02rem;
  line-height: 1.24;
  font-weight: 700;
}

.to-list {
  margin: 0;
  padding-left: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.42rem;
  font-size: 0.77rem;
  line-height: 1.42;
  color: var(--text-secondary);
}

.to-p {
  font-size: 0.8rem;
  line-height: 1.46;
  color: var(--text-secondary);
}
</style>
