<script setup lang="ts">
import { computed } from "vue";
import { useSlideContext } from "@slidev/client";
import PythonCodePanel from "../common/PythonCodePanel.vue";

const { $clicks } = useSlideContext();

interface SolidItem {
  letter: string;
  short: string;
  idea: string;
  problem: string;
  benefit: string;
  lines: string[];
}

const items: SolidItem[] = [
  {
    letter: "S",
    short: "Responsabilidad Única",
    idea: "Separar motivos de cambio independientes en clases cohesivas.",
    problem:
      "Si <code>Factura</code> calcula impuestos, formatea PDF y guarda en disco, un cambio visual arriesga romper el cálculo fiscal.",
    benefit: "Cada clase cambia por una sola razón: <code>Factura</code> calcula, <code>ExportadorPDF</code> presenta.",
    lines: [
      "# Cohesivo: cada clase tiene una razón de cambio",
      "class Factura:",
      "    def __init__(self, neto: float) -> None:",
      "        self.neto = neto",
      "",
      "    def total_con_iva(self) -> float:",
      "        return round(self.neto * 1.21, 2)",
      "",
      "class ExportadorTexto:",
      "    def renderizar(self, f: Factura) -> str:",
      '        return f"Total a pagar: ${f.total_con_iva()}"',
    ],
  },
  {
    letter: "O",
    short: "Abierto / Cerrado",
    idea: "Permitir nuevas variantes agregando clases, sin reescribir lo probado.",
    problem:
      "Abrir el liquidador principal para insertar otro <code>elif</code> ante cada promoción nueva introduce regresiones.",
    benefit: "El núcleo depende de un contrato abstracto y permanece cerrado a modificaciones.",
    lines: [
      "class ReglaEnvio(Protocol):",
      "    def costo(self, km: float) -> float: ...",
      "",
      "class EnvioBicicleta:",
      "    def costo(self, km: float) -> float:",
      "        return 1200.0 + km * 40.0",
      "",
      "# Sumamos EnvioBicicleta sin editar Checkout!",
      "def total_envio(regla: ReglaEnvio, km: float) -> float:",
      "    return regla.costo(km)",
    ],
  },
  {
    letter: "L",
    short: "Sustitución de Liskov",
    idea: "Un subtipo debe cumplir todo lo que el cliente espera del supertipo.",
    problem:
      "Si <code>Cuadrado</code> hereda de <code>Rectangulo</code> y mutar <code>ancho</code> altera también <code>alto</code>, rompe algoritmos que asumen lados independientes.",
    benefit: "Modelar ambas como figuras inmutables con <code>area()</code> preserva los contratos sin sorpresas.",
    lines: [
      "class Figura(Protocol):",
      "    def area(self) -> float: ...",
      "",
      "@dataclass(frozen=True)",
      "class Rectangulo:",
      "    ancho: float; alto: float",
      "    def area(self) -> float: return self.ancho * self.alto",
      "",
      "@dataclass(frozen=True)",
      "class Cuadrado:",
      "    lado: float",
      "    def area(self) -> float: return self.lado ** 2",
    ],
  },
  {
    letter: "I",
    short: "Segregación de Interfaces",
    idea: "Preferir contratos pequeños y específicos antes que interfaces gigantes.",
    problem:
      "Obligar a <code>ImpresoraBasica</code> a implementar <code>escanear()</code> y <code>enviar_fax()</code> la fuerza a lanzar <code>NotImplementedError</code>.",
    benefit: "Cada cliente pide únicamente la capacidad que realmente necesita.",
    lines: [
      "class Imprimible(Protocol):",
      "    def imprimir(self, doc: str) -> None: ...",
      "",
      "class Escaneable(Protocol):",
      "    def escanear(self) -> str: ...",
      "",
      "# Solo implementa lo que realmente sabe hacer:",
      "class ImpresoraTermica:",
      "    def imprimir(self, doc: str) -> None:",
      "        print(doc)",
    ],
  },
  {
    letter: "D",
    short: "Inversión de Dependencias",
    idea: "Las reglas de negocio dependen de abstracciones, no de motores técnicos.",
    problem:
      "Instanciar <code>sqlite3</code> adentro de <code>ServicioAlumnos</code> impide probar la lógica en memoria o migrar de motor.",
    benefit: "Inyectar el repositorio por constructor desacopla el dominio de la infraestructura.",
    lines: [
      "class RepositorioNotas(Protocol):",
      "    def guardar(self, legajo: str, nota: int) -> None: ...",
      "",
      "class ServicioActas:",
      "    def __init__(self, repo: RepositorioNotas) -> None:",
      "        self._repo = repo  # Inyección por contrato",
      "",
      "    def aprobar(self, legajo: str, nota: int) -> None:",
      "        if nota >= 6:",
      "            self._repo.guardar(legajo, nota)",
    ],
  },
];

const idx = computed(() => {
  const n = Number($clicks?.value ?? 0);
  return Math.min(Math.max(n, 0), items.length - 1);
});

const cur = computed(() => items[idx.value]);

function go(i: number) {
  if ($clicks) $clicks.value = i;
}
</script>

<template>
  <div class="sol-stage">
    <nav class="sol-nav" aria-label="Principios SOLID">
      <button
        v-for="(it, i) in items"
        :key="it.letter"
        type="button"
        class="sol-tab"
        :class="{ 'is-active': i === idx }"
        @click="go(i)"
      >
        <span class="sol-letter">{{ it.letter }}</span>
        <span class="sol-name" v-html="it.short" />
      </button>
    </nav>

    <div class="sol-grid">
      <PythonCodePanel
        :file-name="`solid_${cur.letter.toLowerCase()}.py`"
        :status-text="cur.short"
        accent="class"
        :lines="cur.lines"
        :state-key="cur.letter"
      />

      <div class="sol-right">
        <Transition name="poo-fade" mode="out-in">
          <article :key="cur.letter" class="sol-card">
            <div class="sol-top">
              <span class="poo-kicker poo-kicker--class">Principio {{ cur.letter }} · {{ cur.short }}</span>
              <h3 v-html="cur.idea" />
            </div>

            <div class="sol-box sol-box--bad">
              <strong>Qué dolor evita</strong>
              <p v-html="cur.problem" />
            </div>

            <div class="sol-box sol-box--good">
              <strong>Mejora obtenida</strong>
              <p v-html="cur.benefit" />
            </div>
          </article>
        </Transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sol-stage {
  display: grid;
  grid-template-rows: 42px minmax(0, 1fr);
  row-gap: 0.7rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.sol-nav {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 0.45rem;
}

.sol-tab {
  height: 42px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background: #090d16;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  cursor: pointer;
  padding: 0 0.4rem;
}

.sol-tab.is-active {
  background: var(--tint-class);
  border-color: rgba(129, 140, 248, 0.6);
  color: var(--text-primary);
}

.sol-letter {
  font-family: var(--font-mono);
  font-size: 0.88rem;
  font-weight: 800;
  color: #38bdf8;
}

.sol-name {
  font-size: 0.67rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sol-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(0, 0.92fr);
  gap: 1.15rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.sol-right {
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.sol-card {
  box-sizing: border-box;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.6rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-top: 3px solid var(--accent-class);
  border-radius: var(--radius-md);
  padding: 0.95rem 1.05rem;
}

.sol-top {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.4rem;
}

.sol-top h3 {
  font-size: 0.98rem;
  line-height: 1.28;
  font-weight: 700;
}

.sol-box {
  border-radius: 8px;
  padding: 0.55rem 0.72rem;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.sol-box strong {
  font-size: 0.69rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.sol-box p {
  font-size: 0.76rem;
  line-height: 1.4;
}

.sol-box--bad {
  background: rgba(251, 113, 133, 0.09);
  border: 1px solid rgba(251, 113, 133, 0.34);
}

.sol-box--bad strong {
  color: #fda4af;
}

.sol-box--good {
  background: rgba(52, 211, 153, 0.09);
  border: 1px solid rgba(52, 211, 153, 0.34);
}

.sol-box--good strong {
  color: #6ee7b7;
}
</style>
