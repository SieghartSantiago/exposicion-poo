<script setup lang="ts">
import SlideHeader from "../components/layout/SlideHeader.vue";

withDefaults(
  defineProps<{
    kicker?: string;
    kickerVariant?: "interface" | "problem" | "valid" | "class";
    title?: string;
    subtitle?: string;
    badge?: string;
    leftLabel?: string;
    rightLabel?: string;
  }>(),
  {
    kicker: "",
    kickerVariant: "interface",
    title: "",
    subtitle: "",
    badge: "",
    leftLabel: "Implementación A",
    rightLabel: "Implementación B",
  }
);
</script>

<template>
  <div class="slidev-layout poo-layout poo-comparison">
    <SlideHeader
      :kicker="kicker"
      :kicker-variant="kickerVariant"
      :title="title"
      :subtitle="subtitle"
      :badge="badge"
    />

    <div class="poo-comparison__grid">
      <section class="poo-comparison__panel poo-comparison__panel--left">
        <div class="poo-comparison__label poo-comparison__label--left">{{ leftLabel }}</div>
        <div class="poo-comparison__content">
          <slot name="left" />
        </div>
      </section>

      <section class="poo-comparison__panel poo-comparison__panel--right">
        <div class="poo-comparison__label poo-comparison__label--right">{{ rightLabel }}</div>
        <div class="poo-comparison__content">
          <slot name="right" />
        </div>
      </section>
    </div>

    <footer v-if="$slots.bottom" class="poo-comparison__bottom">
      <slot name="bottom" />
    </footer>
  </div>
</template>

<style scoped>
.poo-comparison {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr) auto;
  row-gap: 0.85rem;
}

.poo-comparison__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  column-gap: var(--grid-gap);
  align-items: stretch;
  min-width: 0;
  min-height: 0;
}

.poo-comparison__panel {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
  min-width: 0;
  min-height: 0;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 0.85rem 1rem;
}

.poo-comparison__panel--left {
  border-top: 3px solid var(--accent-problem);
}

.poo-comparison__panel--right {
  border-top: 3px solid var(--accent-valid);
}

.poo-comparison__label {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  white-space: nowrap;
}

.poo-comparison__label--left {
  color: #fda4af;
}

.poo-comparison__label--right {
  color: #6ee7b7;
}

.poo-comparison__content {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
  min-height: 0;
}

.poo-comparison__bottom {
  min-width: 0;
}
</style>
