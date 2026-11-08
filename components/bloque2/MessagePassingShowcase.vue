<script setup lang="ts">
import { computed } from "vue";
import { useSlideContext } from "@slidev/client";
import PythonCodePanel from "../common/PythonCodePanel.vue";

const { $clicks } = useSlideContext();

type Step = 0 | 1 | 2;

const step = computed<Step>(() => {
  const n = Number($clicks?.value ?? 0);
  if (n <= 0) return 0;
  if (n === 1) return 1;
  return 2;
});

function setStep(s: Step) {
  if ($clicks) $clicks.value = s;
}

const data = {
  0: {
    tab: "1. Colaboración por mensajes",
    file: "colaboracion_objetos.py",
    status: "Paso de mensajes",
    accent: "interface" as const,
    lines: [
      "class Producto:",
      "    def __init__(self, nombre: str, stock: int) -> None:",
      "        self.nombre = nombre",
      "        self._stock = stock",
      "",
      "    def reservar(self, unidades: int) -> None:",
      "        if unidades <= 0 or unidades > self._stock:",
      '            raise ValueError("Stock insuficiente")',
      "        self._stock -= unidades",
      "",
      "class Carrito:",
      "    def agregar(self, prod: Producto, cant: int) -> None:",
      "        prod.reservar(cant)  # Mensaje al receptor",
    ],
    kicker: "Interacción entre Objetos",
    title: "Invocación de métodos en vez de tocar campos",
    bullets: [
      "<code>Carrito</code> no escribe <code>prod._stock -= cant</code> por su cuenta.",
      "Envía el mensaje <code>prod.reservar(cant)</code> y delega en <code>Producto</code> la protección de su propio stock.",
      "Si no alcanza el stock, <code>Producto</code> rechaza la operación antes de quedar negativo.",
    ],
    trace: 'teclado = Producto("Teclado", 5) -> carrito.agregar(teclado, 2) -> stock queda en 3',
  },
  1: {
    tab: "2. Identidad (<code>is</code>) vs Igualdad (<code>==</code>)",
    file: "identidad_vs_igualdad.py",
    status: "Referencias en Python",
    accent: "class" as const,
    lines: [
      "from dataclasses import dataclass",
      "",
      "@dataclass",
      "class Punto2D:",
      "    x: float",
      "    y: float",
      "",
      "p1 = Punto2D(3.0, 4.0)",
      "p2 = Punto2D(3.0, 4.0)  # Otra instancia con igual estado",
      "alias = p1              # Misma referencia que p1",
      "",
      "print(p1 == p2)         # True  (mismo valor lógico)",
      "print(p1 is p2)         # False (distinto objeto)",
      "print(p1 is alias)      # True  (mismo id en memoria)",
    ],
    kicker: "Semántica de Referencias",
    title: "Dos preguntas distintas: ¿es el mismo o vale igual?",
    bullets: [
      "El operador <code>is</code> compara identidad de objeto (si dos referencias apuntan a la misma instancia).",
      "El operador <code>==</code> invoca <code>__eq__()</code> para comparar equivalencia de contenido o valor.",
      "Mutar <code>alias.x = 9.0</code> modifica <code>p1.x</code>, pero deja intacto a <code>p2.x</code>.",
    ],
    trace: "p1 == p2 -> True  |  p1 is p2 -> False  |  p1 is alias -> True",
  },
  2: {
    tab: "3. Efecto colateral por alias",
    file: "cuidado_con_alias.py",
    status: "Prevención de bugs",
    accent: "valid" as const,
    lines: [
      "class GrupoLaboratorio:",
      "    def __init__(self, alumnos: list[str]) -> None:",
      "        # Copia defensiva al construir la instancia:",
      "        self._alumnos = list(alumnos)",
      "",
      "    @property",
      "    def integrantes(self) -> tuple[str, ...]:",
      "        # Devuelve tupla inmutable hacia afuera:",
      "        return tuple(self._alumnos)",
      "",
      'lista_ext = ["Ana", "Bruno"]',
      "grupo = GrupoLaboratorio(lista_ext)",
      'lista_ext.append("Intruso")  # No afecta a grupo',
      "assert len(grupo.integrantes) == 2",
    ],
    kicker: "Buena Práctica en Python",
    title: "Copias defensivas para resguardar referencias",
    bullets: [
      "Como las listas en Python se pasan por referencia de objeto, guardar <code>self._alumnos = alumnos</code> compartiría la misma lista externa.",
      "Copiar al ingresar (<code>list(...)</code>) y exponer <code>tuple(...)</code> evita mutaciones accidentales desde afuera.",
    ],
    trace: 'grupo.integrantes -> ("Ana", "Bruno") intacto pese a mutar lista_ext',
  },
};

const cur = computed(() => data[step.value]);
</script>

<template>
  <div class="mp-stage">
    <nav class="mp-nav" aria-label="Ejemplos de referencias y mensajes">
      <button
        v-for="idx in ([0, 1, 2] as Step[])"
        :key="idx"
        type="button"
        class="mp-btn"
        :class="{ 'is-active': step === idx }"
        @click="setStep(idx)"
        v-html="data[idx].tab"
      />
    </nav>

    <div class="mp-grid">
      <PythonCodePanel
        :file-name="cur.file"
        :status-text="cur.status"
        :accent="cur.accent"
        :lines="cur.lines"
        :state-key="step"
      />

      <div class="mp-right">
        <Transition name="poo-fade" mode="out-in">
          <article :key="step" class="mp-card">
            <div class="mp-top">
              <span class="poo-kicker" v-html="cur.kicker" />
              <h3 v-html="cur.title" />
            </div>

            <ul class="mp-list">
              <li v-for="b in cur.bullets" :key="b" v-html="b" />
            </ul>

            <div class="mp-trace">
              <span>Salida verificada:</span>
              <code>{{ cur.trace }}</code>
            </div>
          </article>
        </Transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
.mp-stage {
  display: grid;
  grid-template-rows: 34px minmax(0, 1fr);
  row-gap: 0.7rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.mp-nav {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.6rem;
}

.mp-btn {
  height: 34px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background: var(--bg-surface);
  color: var(--text-muted);
  font-size: 0.72rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
}

.mp-btn.is-active {
  background: var(--tint-interface);
  border-color: rgba(56, 189, 248, 0.55);
  color: #e0f2fe;
}

.mp-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.12fr) minmax(0, 0.88fr);
  gap: 1.15rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.mp-right {
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.mp-card {
  box-sizing: border-box;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.7rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-top: 3px solid var(--accent-interface);
  border-radius: var(--radius-md);
  padding: 0.95rem 1.05rem;
}

.mp-top {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.4rem;
}

.mp-top h3 {
  font-size: 1.03rem;
  line-height: 1.24;
  font-weight: 700;
}

.mp-list {
  margin: 0;
  padding-left: 1.05rem;
  display: flex;
  flex-direction: column;
  gap: 0.42rem;
  font-size: 0.78rem;
  line-height: 1.42;
  color: var(--text-secondary);
}

.mp-trace {
  background: #0b1120;
  border: 1px solid rgba(52, 211, 153, 0.35);
  border-radius: 8px;
  padding: 0.52rem 0.72rem;
  display: flex;
  flex-direction: column;
  gap: 0.22rem;
}

.mp-trace span {
  font-size: 0.67rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  font-weight: 700;
}

.mp-trace code {
  font-family: var(--font-mono);
  font-size: 0.71rem;
  color: #6ee7b7;
  background: transparent;
  border: none;
  padding: 0;
  white-space: normal;
}
</style>
