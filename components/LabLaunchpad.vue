<script setup lang="ts">
import { computed } from "vue";
import QrAccessModal from "./QrAccessModal.vue";

const props = withDefaults(
  defineProps<{
    slug: string;
    summary: string;
    runTitle?: string;
    runDesc?: string;
    editTitle?: string;
    editDesc?: string;
    hints?: string[];
  }>(),
  {
    runTitle: "Simulador Interactivo",
    runDesc:
      "Modificá parámetros de entrada con controles táctiles y observá en vivo cómo responden las invariantes y los contratos.",
    editTitle: "Laboratorio de Código Python",
    editDesc:
      "Inspeccioná y editá las celdas de Python en el navegador para extender clases o reglas y ejecutarlas al instante.",
    hints: () => [
      "1. Sobregiro (&gt; $30.000)",
      "2. Reasignación de <code>cuenta.saldo</code>",
      "3. Colaboración entre dos instancias",
    ],
  }
);

const basePath = computed(() => {
  const raw = import.meta.env.BASE_URL || "/";
  return raw.endsWith("/") ? raw : `${raw}/`;
});

const runUrl = computed(() => `${basePath.value}labs/${props.slug}/run/index.html`);
const editUrl = computed(() => `${basePath.value}labs/${props.slug}/edit/index.html`);
</script>

<template>
  <div class="launchpad">
    <!-- TARJETA PROTAGONISTA: ACCESO A VISTA DEDICADA A PANTALLA COMPLETA -->
    <section class="launchpad__main">
      <div class="launchpad__intro">
        <p class="launchpad__summary" v-html="props.summary" />
      </div>

      <div class="launchpad__modes">
        <!-- Modo 1: Controles interactivos -->
        <article class="mode-card mode-card--run">
          <div class="mode-card__head">
            <span class="poo-kicker">Modo Guiado · Controles Táctiles</span>
            <h2 class="mode-card__title" v-html="props.runTitle" />
          </div>
          <p class="mode-card__desc" v-html="props.runDesc" />
          <a :href="runUrl" target="_blank" rel="noopener" class="poo-btn poo-btn--primary mode-card__cta">
            🎛️ Abrir Simulador a Pantalla Completa ↗
          </a>
        </article>

        <!-- Modo 2: Edición de código en vivo -->
        <article class="mode-card mode-card--edit">
          <div class="mode-card__head">
            <span class="poo-kicker poo-kicker--valid">Modo Sandbox · Código Editable</span>
            <h2 class="mode-card__title" v-html="props.editTitle" />
          </div>
          <p class="mode-card__desc" v-html="props.editDesc" />
          <a :href="editUrl" target="_blank" rel="noopener" class="poo-btn poo-btn--emerald mode-card__cta">
            ✏️ Abrir Editor de Código Completo ↗
          </a>
        </article>
      </div>
    </section>

    <!-- BARRA INFERIOR COMPACTA: PRUEBAS SUGERIDAS Y ACCESO MÓVIL -->
    <footer class="launchpad__footer">
      <div class="launchpad__hints">
        <strong>Qué probar:</strong>
        <template v-for="(hint, idx) in props.hints" :key="idx">
          <span v-html="hint" />
          <span v-if="idx < props.hints.length - 1">·</span>
        </template>
      </div>
      <QrAccessModal :show-motion-toggle="false" />
    </footer>
  </div>
</template>

<style scoped>
.launchpad {
  display: grid;
  grid-template-rows: minmax(0, 1fr) auto;
  row-gap: 0.9rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.launchpad__main {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.9rem;
  min-width: 0;
  min-height: 0;
}

.launchpad__summary {
  font-size: 0.94rem;
  line-height: 1.45;
  color: var(--text-secondary);
  max-width: 78ch;
}

.launchpad__modes {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  column-gap: 1.25rem;
  flex: 1;
  min-width: 0;
  min-height: 0;
}

.mode-card {
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.8rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 1.2rem 1.35rem;
  min-width: 0;
}

.mode-card--run {
  border-top: 3px solid var(--accent-interface);
}

.mode-card--edit {
  border-top: 3px solid var(--accent-valid);
}

.mode-card__head {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
}

.mode-card__title {
  font-size: 1.22rem;
  line-height: 1.22;
  font-weight: 800;
  color: var(--text-primary);
}

.mode-card__desc {
  font-size: 0.85rem;
  line-height: 1.48;
  color: var(--text-secondary);
}

.mode-card__cta {
  width: 100%;
  min-height: 44px;
  font-size: 0.84rem;
}

.launchpad__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.65rem 0.95rem;
  background: rgba(17, 24, 39, 0.72);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
}

.launchpad__hints {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.78rem;
  color: var(--text-secondary);
}

.launchpad__hints strong {
  color: var(--text-primary);
}
</style>
