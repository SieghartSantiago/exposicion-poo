<script setup lang="ts">
import SlideHeader from "../components/layout/SlideHeader.vue";

withDefaults(
  defineProps<{
    kicker?: string;
    kickerVariant?: "interface" | "problem" | "valid" | "class";
    title?: string;
    subtitle?: string;
    badge?: string;
    columns?: 1 | 2 | 3;
  }>(),
  {
    kicker: "",
    kickerVariant: "interface",
    title: "",
    subtitle: "",
    badge: "",
    columns: 2,
  }
);
</script>

<template>
  <div class="slidev-layout poo-layout poo-concept">
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

    <div class="poo-concept__main" :data-cols="columns">
      <slot />
    </div>

    <footer v-if="$slots.footer" class="poo-concept__footer">
      <slot name="footer" />
    </footer>
  </div>
</template>

<style scoped>
.poo-concept {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr) auto;
  row-gap: 1rem;
}

.poo-concept__main {
  display: grid;
  gap: var(--grid-gap);
  align-content: start;
  min-width: 0;
  min-height: 0;
}

.poo-concept__main[data-cols="1"] {
  grid-template-columns: minmax(0, 1fr);
}

.poo-concept__main[data-cols="2"] {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.poo-concept__main[data-cols="3"] {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.poo-concept__footer {
  min-width: 0;
}
</style>
