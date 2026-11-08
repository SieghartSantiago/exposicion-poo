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
    kicker: "Laboratorio Interactivo · Python + WebAssembly",
    kickerVariant: "valid",
    title: "",
    subtitle: "",
    badge: "",
  }
);
</script>

<template>
  <div class="slidev-layout poo-layout poo-lab-entry">
    <SlideHeader
      :kicker="kicker"
      :kicker-variant="kickerVariant"
      :title="title"
      :subtitle="subtitle"
      :badge="badge"
    />

    <div class="poo-lab-entry__stage">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.poo-lab-entry {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  row-gap: 1rem;
}

.poo-lab-entry__stage {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
}
</style>
