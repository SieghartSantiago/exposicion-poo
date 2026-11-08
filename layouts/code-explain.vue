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
  <div class="slidev-layout poo-layout poo-code-explain">
    <SlideHeader
      :kicker="kicker"
      :kicker-variant="kickerVariant"
      :title="title"
      :subtitle="subtitle"
      :badge="badge"
    >
      <template #meta>
        <slot name="meta" />
      </template>
    </SlideHeader>

    <div v-if="$slots.code || $slots.explain" class="poo-code-explain__split">
      <section class="poo-code-explain__code">
        <slot name="code" />
      </section>
      <aside class="poo-code-explain__explain">
        <slot name="explain" />
      </aside>
    </div>

    <div v-else class="poo-code-explain__full">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.poo-code-explain {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  row-gap: 0.85rem;
}

.poo-code-explain__split {
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(0, 0.92fr);
  column-gap: var(--grid-gap);
  align-items: stretch;
  min-width: 0;
  min-height: 0;
}

.poo-code-explain__code,
.poo-code-explain__explain,
.poo-code-explain__full {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
}
</style>
