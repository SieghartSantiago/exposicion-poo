<script setup lang="ts">
import { computed } from "vue";
import { useSlideContext } from "@slidev/client";

const { $clicks } = useSlideContext();

interface Era {
  year: string;
  lang: string;
  authors: string;
  tag: string;
  contribution: string;
  tradeoff: string;
  snippet: string;
}

const eras: Era[] = [
  {
    year: "1967",
    lang: "Simula 67",
    authors: "Ole-Johan Dahl y Kristen Nygaard (Noruega)",
    tag: "Génesis de Clase y Herencia",
    contribution:
      "Introduce por primera vez <code>class</code>, subclases e instancias para simular procesos discretos (puertos, tráfico, redes).",
    tradeoff:
      "Sentó las bases de la abstracción de datos, aunque aún carecía de ocultamiento estricto de atributos.",
    snippet: "Class Vehiculo(velocidad); Begin ... End;",
  },
  {
    year: "1972–80",
    lang: "Smalltalk",
    authors: "Alan Kay, Adele Goldberg y Dan Ingalls (Xerox PARC)",
    tag: "Orientación a Objetos Pura",
    contribution:
      "Acuña el término POO: todo valor es un objeto (incluso números y clases) y toda operación es envío dinámico de mensajes (<em>late binding</em>).",
    tradeoff:
      "Inspiró las interfaces gráficas modernas (ventanas, íconos), con mayor costo de interpretación en máquina virtual.",
    snippet: "cuenta depositar: 5000.",
  },
  {
    year: "1985",
    lang: "C++",
    authors: "Bjarne Stroustrup (Bell Labs)",
    tag: "Abstracción de Costo Cero",
    contribution:
      "Integra clases, constructores/destructores y métodos <code>virtual</code> (<code>vtable</code>/<code>vptr</code>) manteniendo compatibilidad y velocidad de C.",
    tradeoff:
      "Permite alojar objetos tanto en la pila (<code>stack</code>) como en el <code>heap</code>, exigiendo gestión cuidadosa de memoria y punteros.",
    snippet: "virtual double calcularCosto() const;",
  },
  {
    year: "1991",
    lang: "Python",
    authors: "Guido van Rossum",
    tag: "Multiparadigma y Legibilidad",
    contribution:
      "Funciones, módulos y clases son objetos de primera clase. Combina clases, tipado dinámico (<em>duck typing</em>), protocolos y orden <code>C3 MRO</code>.",
    tradeoff:
      "Prioriza expresividad y productividad; emplea convenciones (<code>_atributo</code>) en lugar de modificadores privados estrictos.",
    snippet: "def extraer(self, monto: float) -> None:",
  },
  {
    year: "1995",
    lang: "Java",
    authors: "James Gosling (Sun Microsystems)",
    tag: "Máquina Virtual e Interfaces",
    contribution:
      "Populariza la recolección automática de basura (<em>Garbage Collector</em>), herencia simple de clase e implementación múltiple de <code>interface</code>.",
    tradeoff:
      "Elimina errores de aritmética de punteros a cambio de mayor huella de memoria en la JVM.",
    snippet: "public interface Pagable { void cobrar(); }",
  },
  {
    year: "2000+",
    lang: "C# y Síntesis Moderna",
    authors: "Anders Hejlsberg y evolución multiparadigma",
    tag: "Objetos + Tipos por Valor + Funcional",
    contribution:
      "Integra propiedades nativas, <code>struct</code> por valor en pila, genéricos y consultas funcionales (<code>LINQ</code> / <code>Streams</code> / <code>Protocol</code>).",
    tradeoff:
      "Consolida la práctica actual: combinar objetos en la arquitectura con transformaciones inmutables en los métodos.",
    snippet: "public decimal Saldo { get; private set; }",
  },
];

const activeIdx = computed(() => {
  const raw = Number($clicks?.value ?? 0);
  return Math.min(Math.max(raw, 0), eras.length - 1);
});

const current = computed(() => eras[activeIdx.value]);

function selectEra(idx: number) {
  if ($clicks) $clicks.value = idx;
}
</script>

<template>
  <div class="tl-stage">
    <!-- Línea de tiempo horizontal interactiva -->
    <nav class="tl-track" aria-label="Línea de tiempo histórica de POO">
      <button
        v-for="(era, idx) in eras"
        :key="era.year"
        type="button"
        class="tl-node"
        :class="{ 'is-active': idx === activeIdx, 'is-past': idx < activeIdx }"
        @click="selectEra(idx)"
      >
        <span class="tl-year">{{ era.year }}</span>
        <span class="tl-dot" />
        <span class="tl-lang">{{ era.lang }}</span>
      </button>
    </nav>

    <!-- Tarjeta de detalle de altura invariable -->
    <div class="tl-detail">
      <Transition name="poo-fade" mode="out-in">
        <article :key="current.year" class="tl-card">
          <div class="tl-card__left">
            <div class="tl-meta">
              <span class="poo-kicker">{{ current.year }} · {{ current.tag }}</span>
            </div>
            <h3 class="tl-title">{{ current.lang }}</h3>
            <p class="tl-authors">{{ current.authors }}</p>
            <p class="tl-desc" v-html="current.contribution" />
          </div>

          <div class="tl-card__right">
            <div class="tl-box tl-box--code">
              <span class="tl-box__label">Huella sintáctica representativa</span>
              <code>{{ current.snippet }}</code>
            </div>
            <div class="tl-box tl-box--tradeoff">
              <span class="tl-box__label">Compromiso de ingeniería (Trade-off)</span>
              <p v-html="current.tradeoff" />
            </div>
          </div>
        </article>
      </Transition>
    </div>
  </div>
</template>

<style scoped>
.tl-stage {
  display: grid;
  grid-template-rows: 74px minmax(0, 1fr);
  row-gap: 0.9rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.tl-track {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 0.5rem;
  align-items: center;
}

.tl-node {
  box-sizing: border-box;
  height: 70px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.26rem;
  background: #090d16;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  cursor: pointer;
  padding: 0.35rem;
  color: var(--text-muted);
}

.tl-node.is-past {
  border-color: rgba(56, 189, 248, 0.32);
  color: var(--text-secondary);
}

.tl-node.is-active {
  background: rgba(56, 189, 248, 0.14);
  border-color: var(--accent-interface);
  color: var(--text-primary);
}

.tl-year {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 700;
}

.tl-dot {
  width: 9px;
  height: 9px;
  border-radius: 999px;
  background: #475569;
}

.tl-node.is-past .tl-dot {
  background: #38bdf8;
}

.tl-node.is-active .tl-dot {
  background: #34d399;
  box-shadow: 0 0 0 3px rgba(52, 211, 153, 0.25);
}

.tl-lang {
  font-size: 0.72rem;
  font-weight: 700;
  white-space: nowrap;
}

.tl-detail {
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.tl-card {
  box-sizing: border-box;
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
  gap: 1.2rem;
  height: 100%;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-top: 3px solid var(--accent-interface);
  border-radius: var(--radius-md);
  padding: 1rem 1.15rem;
}

.tl-card__left {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.45rem;
}

.tl-title {
  font-size: 1.35rem;
  line-height: 1.15;
  font-weight: 800;
}

.tl-authors {
  font-size: 0.76rem;
  font-weight: 600;
  color: #7dd3fc;
}

.tl-desc {
  font-size: 0.83rem;
  line-height: 1.48;
  color: var(--text-secondary);
}

.tl-card__right {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.65rem;
}

.tl-box {
  box-sizing: border-box;
  border-radius: var(--radius-sm);
  padding: 0.68rem 0.85rem;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.tl-box--code {
  background: #090d16;
  border: 1px solid rgba(129, 140, 248, 0.36);
}

.tl-box--code code {
  font-family: var(--font-mono);
  font-size: 0.76rem;
  color: #a5b4fc;
  background: transparent;
  border: none;
  padding: 0;
}

.tl-box--tradeoff {
  background: rgba(52, 211, 153, 0.08);
  border: 1px solid rgba(52, 211, 153, 0.34);
  flex: 1;
  justify-content: center;
}

.tl-box--tradeoff p {
  font-size: 0.79rem;
  line-height: 1.44;
  color: var(--text-secondary);
}

.tl-box__label {
  font-size: 0.67rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}
</style>
