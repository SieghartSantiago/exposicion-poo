<script setup lang="ts">
import SlideHeader from "../components/layout/SlideHeader.vue";

withDefaults(
  defineProps<{
    kicker?: string;
    kickerVariant?: "interface" | "problem" | "valid" | "class";
    title?: string;
    subtitle?: string;
    badge?: string;
  }>(),
  {
    kicker: "",
    kickerVariant: "interface",
    title: "",
    subtitle: "",
    badge: "",
  }
);
</script>

<template>
  <div class="slidev-layout poo-layout poo-diagram">
    <SlideHeader
      :kicker="kicker"
      :kicker-variant="kickerVariant"
      :title="title"
      :subtitle="subtitle"
      :badge="badge"
    />

    <div class="poo-diagram__stage">
      <slot />
    </div>

    <footer v-if="$slots.controls" class="poo-diagram__controls">
      <slot name="controls" />
    </footer>
  </div>
</template>

<style scoped>
.poo-diagram {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr) auto;
  row-gap: 0.85rem;
}

.poo-diagram__stage {
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
  min-height: 0;
  background: var(--bg-surface-2);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 1rem 1.25rem;
}

.poo-diagram__controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  min-width: 0;
}
</style>
