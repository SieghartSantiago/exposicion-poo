<script setup lang="ts">
import { computed } from "vue";
import { useSlideContext } from "@slidev/client";

const props = withDefaults(
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

const { $frontmatter } = useSlideContext();

const resolvedTitle = computed(
  () => props.title || String(($frontmatter as Record<string, unknown>)?.title || "")
);
const resolvedKicker = computed(
  () => props.kicker || String(($frontmatter as Record<string, unknown>)?.kicker || "")
);
const resolvedBadge = computed(
  () => props.badge || String(($frontmatter as Record<string, unknown>)?.badge || "")
);
const resolvedSubtitle = computed(
  () => props.subtitle || String(($frontmatter as Record<string, unknown>)?.subtitle || "")
);
const resolvedVariant = computed(() => {
  const fmVar = ($frontmatter as Record<string, unknown>)?.kickerVariant as
    | "interface"
    | "problem"
    | "valid"
    | "class"
    | undefined;
  return fmVar || props.kickerVariant;
});
</script>

<template>
  <header v-if="resolvedTitle || resolvedKicker" class="poo-slide-header">
    <div v-if="resolvedKicker || resolvedBadge || $slots.meta" class="poo-slide-header__meta">
      <span
        v-if="resolvedKicker"
        class="poo-kicker"
        :class="{
          'poo-kicker--problem': resolvedVariant === 'problem',
          'poo-kicker--valid': resolvedVariant === 'valid',
          'poo-kicker--class': resolvedVariant === 'class',
        }"
        v-html="resolvedKicker"
      />
      <div class="poo-slide-header__right">
        <slot name="meta" />
        <span v-if="resolvedBadge" class="poo-slide-header__badge" v-html="resolvedBadge" />
      </div>
    </div>

    <h1 v-if="resolvedTitle" class="poo-slide-header__title" v-html="resolvedTitle" />
    <p v-if="resolvedSubtitle" class="poo-slide-header__subtitle" v-html="resolvedSubtitle" />
  </header>
</template>

<style scoped>
.poo-slide-header {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  min-width: 0;
}

.poo-slide-header__meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  min-width: 0;
}

.poo-slide-header__right {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 0;
}

.poo-slide-header__badge {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  line-height: 1.2;
  color: var(--text-muted);
  white-space: nowrap;
}

.poo-slide-header__title {
  font-size: 1.55rem;
  line-height: 1.18;
  font-weight: 800;
  color: var(--text-primary);
}

.poo-slide-header__subtitle {
  font-size: 0.88rem;
  line-height: 1.4;
  color: var(--text-secondary);
  max-width: 72ch;
}
</style>
