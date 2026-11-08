<script setup lang="ts">
withDefaults(
  defineProps<{
    kicker?: string;
    badge?: string;
    footerLeft?: string;
    footerRight?: string;
  }>(),
  {
    kicker: "Programación I · Ingeniería en Informática",
    badge: "Unidad VI · 2026",
    footerLeft: "Navegación: → o Espacio para avanzar",
    footerRight: "Presentación Interactiva + Python WebAssembly",
  }
);
</script>

<template>
  <div class="slidev-layout poo-layout poo-cover">
    <header class="poo-cover__topbar">
      <span class="poo-kicker">{{ kicker }}</span>
      <span class="poo-cover__badge">{{ badge }}</span>
    </header>

    <div class="poo-cover__body">
      <div class="poo-cover__main">
        <slot />
      </div>
      <div class="poo-cover__graphic">
        <slot name="graphic" />
      </div>
    </div>

    <footer class="poo-cover__footer">
      <span>{{ footerLeft }}</span>
      <span>{{ footerRight }}</span>
    </footer>
  </div>
</template>

<style scoped>
.poo-cover {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr) auto;
  row-gap: 1rem;
}

.poo-cover__topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.poo-cover__badge {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--text-muted);
  border: 1px solid var(--border-subtle);
  border-radius: 999px;
  padding: 0.22rem 0.7rem;
  white-space: nowrap;
}

.poo-cover__body {
  display: grid;
  grid-template-columns: minmax(0, 1.12fr) minmax(0, 0.88fr);
  column-gap: 2rem;
  align-items: center;
  min-height: 0;
}

.poo-cover__main {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1rem;
  min-width: 0;
}

.poo-cover__graphic {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 0;
  min-height: 0;
}

.poo-cover__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding-top: 0.65rem;
  border-top: 1px solid var(--border-subtle);
  font-size: 0.73rem;
  color: var(--text-muted);
}
</style>
