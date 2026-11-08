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
    kicker: "Síntesis y Decisiones de Diseño",
    kickerVariant: "class",
    title: "",
    subtitle: "",
    badge: "",
  }
);
</script>

<template>
  <div class="slidev-layout poo-layout poo-conclusions">
    <SlideHeader
      :kicker="kicker"
      :kicker-variant="kickerVariant"
      :title="title"
      :subtitle="subtitle"
      :badge="badge"
    />

    <div class="poo-conclusions__body">
      <slot />
    </div>

    <footer v-if="$slots.footer" class="poo-conclusions__footer">
      <slot name="footer" />
    </footer>
  </div>
</template>

<style scoped>
.poo-conclusions {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.poo-conclusions__body {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.85rem;
  min-width: 0;
  min-height: 0;
}

.poo-conclusions__footer {
  padding-top: 0.65rem;
  border-top: 1px solid var(--border-subtle);
  font-size: 0.78rem;
  color: var(--text-muted);
}
</style>
