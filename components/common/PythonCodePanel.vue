<script setup lang="ts">
import { computed } from "vue";
import { highlightPythonLine } from "../../utils/pythonHighlighter";

const props = withDefaults(
  defineProps<{
    fileName: string;
    statusText?: string;
    accent?: "interface" | "class" | "valid" | "problem" | "state";
    lines: string[];
    stateKey?: string | number;
    highlightIndices?: number[];
    compact?: boolean;
  }>(),
  {
    statusText: "",
    accent: "class",
    stateKey: 0,
    highlightIndices: () => [],
    compact: false,
  }
);

const highlighted = computed(() =>
  props.lines.map((line, index) => ({
    html: highlightPythonLine(line),
    active: props.highlightIndices.includes(index),
  }))
);
</script>

<template>
  <section class="py-code-panel" :data-accent="props.accent" :class="{ 'is-compact': props.compact }">
    <header class="py-code-panel__bar">
      <span class="py-code-panel__file">{{ props.fileName }}</span>
      <span v-if="props.statusText" class="py-code-panel__status" :data-accent="props.accent">
        {{ props.statusText }}
      </span>
    </header>

    <div class="py-code-panel__body">
      <Transition name="poo-fade" mode="out-in">
        <pre :key="props.stateKey" class="py-code-panel__pre"><code
          ><span
            v-for="(item, idx) in highlighted"
            :key="idx"
            class="py-code-panel__line"
            :class="{ 'is-highlighted': item.active }"
            v-html="item.html"
          /></code></pre>
      </Transition>
    </div>
  </section>
</template>

<style scoped>
.py-code-panel {
  box-sizing: border-box;
  display: grid;
  grid-template-rows: 32px minmax(0, 1fr);
  height: 100%;
  min-width: 0;
  min-height: 0;
  background: #0b1120;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
}

.py-code-panel[data-accent="interface"] {
  border-color: rgba(56, 189, 248, 0.38);
}

.py-code-panel[data-accent="class"] {
  border-color: rgba(129, 140, 248, 0.4);
}

.py-code-panel[data-accent="valid"] {
  border-color: rgba(52, 211, 153, 0.4);
}

.py-code-panel[data-accent="problem"] {
  border-color: rgba(251, 113, 133, 0.38);
}

.py-code-panel[data-accent="state"] {
  border-color: rgba(251, 191, 36, 0.38);
}

.py-code-panel__bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  padding: 0 0.85rem;
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(17, 24, 39, 0.88);
  border-radius: var(--radius-md) var(--radius-md) 0 0;
}

.py-code-panel__file {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--text-secondary);
  white-space: nowrap;
}

.py-code-panel__status {
  font-size: 0.66rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  white-space: nowrap;
}

.py-code-panel__status[data-accent="interface"] {
  color: #7dd3fc;
}

.py-code-panel__status[data-accent="class"] {
  color: #a5b4fc;
}

.py-code-panel__status[data-accent="valid"] {
  color: #6ee7b7;
}

.py-code-panel__status[data-accent="problem"] {
  color: #fda4af;
}

.py-code-panel__status[data-accent="state"] {
  color: #fde68a;
}

.py-code-panel__body {
  padding: 0.6rem 0.85rem;
  display: flex;
  align-items: flex-start;
  min-width: 0;
  min-height: 0;
}

.py-code-panel.is-compact .py-code-panel__body {
  padding: 0.48rem 0.75rem;
}

.py-code-panel__pre {
  margin: 0;
  width: 100%;
  font-family: var(--font-mono);
  font-size: 0.74rem;
  line-height: 1.4;
  color: #f8fafc;
  background: transparent;
}

.py-code-panel.is-compact .py-code-panel__pre {
  font-size: 0.7rem;
  line-height: 1.36;
}

.py-code-panel__line {
  display: block;
  white-space: pre;
  padding: 0 0.25rem;
  border-radius: 4px;
}

.py-code-panel__line.is-highlighted {
  background: rgba(56, 189, 248, 0.13);
  box-shadow: inset 2px 0 0 var(--accent-interface);
}

:deep(.tok-kw) {
  color: #c084fc;
  font-weight: 600;
}

:deep(.tok-type) {
  color: #38bdf8;
}

:deep(.tok-str) {
  color: #6ee7b7;
}

:deep(.tok-num) {
  color: #fbbf24;
}

:deep(.tok-dec) {
  color: #f472b6;
}

:deep(.tok-com) {
  color: #94a3b8;
  font-style: italic;
}
</style>
