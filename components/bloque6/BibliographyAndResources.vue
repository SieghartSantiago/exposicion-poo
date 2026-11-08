<script setup lang="ts">
import { computed } from "vue";
import QrAccessModal from "../QrAccessModal.vue";

const basePath = computed(() => {
  const raw = import.meta.env.BASE_URL || "/";
  return raw.endsWith("/") ? raw : `${raw}/`;
});

const labs = computed(() => [
  {
    code: "Lab 01",
    title: "Encapsulamiento e Invariantes",
    href: `${basePath.value}labs/01-encapsulamiento/run/index.html`,
  },
  {
    code: "Lab 02",
    title: "Herencia y Despacho Dinámico",
    href: `${basePath.value}labs/02-herencia-polimorfismo/run/index.html`,
  },
  {
    code: "Lab 03",
    title: "Patrón Strategy Intercambiable",
    href: `${basePath.value}labs/03-patron-strategy/run/index.html`,
  },
  {
    code: "Lab 04",
    title: "Comparación de 3 Paradigmas",
    href: `${basePath.value}labs/04-comparacion-paradigmas/run/index.html`,
  },
]);
</script>

<template>
  <div class="bib-grid">
    <!-- REFERENCIAS ACADÉMICAS -->
    <section class="bib-card">
      <span class="poo-kicker poo-kicker--class">Bibliografía y Fuentes Consultadas</span>
      <ul class="bib-list">
        <li>
          <strong>Dahl, O.-J., &amp; Nygaard, K. (1966).</strong> <em>SIMULA—an ALGOL-based simulation language</em>. Communications of the ACM, 9(9).
        </li>
        <li>
          <strong>Goldberg, A., &amp; Robson, D. (1983).</strong> <em>Smalltalk-80: The Language and its Implementation</em>. Addison-Wesley.
        </li>
        <li>
          <strong>Liskov, B. H., &amp; Wing, J. M. (1994).</strong> <em>A behavioral notion of subtyping</em>. ACM TOPLAS, 16(6).
        </li>
        <li>
          <strong>Gamma, E., Helm, R., Johnson, R., &amp; Vlissides, J. (1994).</strong> <em>Design Patterns: Elements of Reusable Object-Oriented Software</em>. Addison-Wesley.
        </li>
        <li>
          <strong>Stroustrup, B. (2013).</strong> <em>The C++ Programming Language</em> (4th ed.). Addison-Wesley.
        </li>
        <li>
          <strong>Martin, R. C. (2017).</strong> <em>Clean Architecture</em>. Prentice Hall.
        </li>
        <li>
          <strong>Ramalho, L. (2022).</strong> <em>Fluent Python</em> (2nd ed.). O'Reilly · &amp; <em>Python 3.12+ Data Model Docs</em>.
        </li>
      </ul>
    </section>

    <!-- ACCESO RÁPIDO A LOS 4 LABORATORIOS Y GUÍA -->
    <section class="bib-card bib-card--labs">
      <div class="bib-labs-top">
        <span class="poo-kicker poo-kicker--valid">Práctica Ejecutable en el Navegador</span>
        <h3>4 Laboratorios Python + Pyodide</h3>
        <div class="bib-lab-links">
          <a
            v-for="lab in labs"
            :key="lab.code"
            :href="lab.href"
            target="_blank"
            rel="noopener"
            class="bib-lab-btn"
          >
            <span class="bib-lab-code">{{ lab.code }}</span>
            <span class="bib-lab-name">{{ lab.title }}</span>
            <span class="bib-lab-arrow">↗</span>
          </a>
        </div>
      </div>

      <div class="bib-qr-row">
        <QrAccessModal :show-motion-toggle="false" />
      </div>
    </section>
  </div>
</template>

<style scoped>
.bib-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(0, 0.85fr);
  gap: 1.15rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.bib-card {
  box-sizing: border-box;
  height: 100%;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-top: 3px solid var(--accent-class);
  border-radius: var(--radius-md);
  padding: 0.9rem 1.05rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.55rem;
  min-width: 0;
}

.bib-card--labs {
  border-top-color: var(--accent-valid);
}

.bib-list {
  margin: 0;
  padding-left: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.34rem;
  font-size: 0.72rem;
  line-height: 1.38;
  color: var(--text-secondary);
}

.bib-labs-top {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
}

.bib-labs-top h3 {
  font-size: 1.02rem;
  line-height: 1.22;
  font-weight: 700;
}

.bib-lab-links {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.42rem;
}

.bib-lab-btn {
  box-sizing: border-box;
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: 0.55rem;
  padding: 0.45rem 0.68rem;
  border-radius: 8px;
  background: #0b1120;
  border: 1px solid var(--border-strong);
  border-style: solid !important;
  text-decoration: none !important;
  color: var(--text-primary);
  font-size: 0.75rem;
}

.bib-lab-btn:hover {
  border-color: var(--accent-valid);
  background: rgba(52, 211, 153, 0.1);
}

.bib-lab-code {
  font-family: var(--font-mono);
  font-size: 0.69rem;
  font-weight: 700;
  color: #6ee7b7;
}

.bib-lab-name {
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.bib-lab-arrow {
  color: var(--text-muted);
}

.bib-qr-row {
  padding-top: 0.45rem;
  border-top: 1px solid var(--border-subtle);
  display: flex;
  justify-content: flex-end;
}
</style>
