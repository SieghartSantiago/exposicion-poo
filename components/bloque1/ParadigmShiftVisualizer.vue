<script setup lang="ts">
import { computed } from "vue";
import { useSlideContext } from "@slidev/client";

const { $clicks } = useSlideContext();

type Step = 0 | 1 | 2;

const activeStep = computed<Step>(() => {
  const n = Number($clicks?.value ?? 0);
  if (n <= 0) return 0;
  if (n === 1) return 1;
  return 2;
});

function goStep(s: Step) {
  if ($clicks) $clicks.value = s;
}

const tabs: { id: Step; label: string }[] = [
  { id: 0, label: "1. ¿Qué es un paradigma?" },
  { id: 1, label: "2. Procedural vs. Objetos" },
  { id: 2, label: "3. ¿Cuándo conviene POO?" },
];
</script>

<template>
  <div class="b1-stage">
    <nav class="b1-stepper" aria-label="Etapas conceptuales">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        type="button"
        class="b1-step-btn"
        :class="{ 'is-active': activeStep === tab.id }"
        @click="goStep(tab.id)"
        v-html="tab.label"
      />
    </nav>

    <div class="b1-body">
      <Transition name="poo-fade" mode="out-in">
        <!-- PASO 0: QUÉ ES UN PARADIGMA Y QUÉ PROPONE POO -->
        <div v-if="activeStep === 0" key="p0" class="b1-grid-2">
          <article class="b1-card b1-card--cyan">
            <span class="poo-kicker">Definición Base</span>
            <h3>¿Qué es un paradigma de programación?</h3>
            <p class="b1-lead">
              Es un <strong>marco conceptual</strong> que define cómo estructuramos los datos, cómo expresamos las acciones y qué reglas gobiernan el cambio de estado de un programa.
            </p>
            <div class="b1-triad">
              <div class="b1-pill">
                <strong>Imperativo</strong>
                <span>Secuencia de órdenes sobre variables</span>
              </div>
              <div class="b1-pill b1-pill--active">
                <strong>Orientado a Objetos</strong>
                <span>Red de objetos que colaboran por mensajes</span>
              </div>
              <div class="b1-pill">
                <strong>Funcional</strong>
                <span>Composición de funciones puras sin mutación</span>
              </div>
            </div>
          </article>

          <article class="b1-card b1-card--indigo">
            <span class="poo-kicker poo-kicker--class">Idea Central de POO</span>
            <h3>Unificar estado y comportamiento</h3>
            <svg viewBox="0 0 380 155" class="b1-svg" role="img" aria-label="Esquema de un objeto">
              <rect x="8" y="28" width="112" height="96" rx="10" fill="#0d1424" stroke="#38bdf8" stroke-width="1.5" />
              <text x="64" y="64" text-anchor="middle" fill="#7dd3fc" style="font-size: 11px; font-weight: 700;">MENSAJE</text>
              <text x="64" y="88" text-anchor="middle" fill="#f8fafc" style="font-family: var(--font-mono); font-size: 11px;">depositar()</text>

              <line x1="124" y1="76" x2="168" y2="76" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 3" />
              <polygon points="172,76 164,71 164,81" fill="#38bdf8" />

              <rect x="176" y="10" width="194" height="134" rx="12" fill="#111827" stroke="#818cf8" stroke-width="1.8" />
              <text x="273" y="32" text-anchor="middle" fill="#a5b4fc" style="font-size: 10.5px; font-weight: 700;">OBJETO AUTÓNOMO</text>
              <rect x="192" y="42" width="162" height="40" rx="7" fill="rgba(56,189,248,0.12)" stroke="rgba(56,189,248,0.4)" />
              <text x="273" y="66" text-anchor="middle" fill="#e0f2fe" style="font-size: 10.5px; font-weight: 600;">Métodos (Comportamiento)</text>
              <rect x="192" y="90" width="162" height="40" rx="7" fill="rgba(52,211,153,0.12)" stroke="rgba(52,211,153,0.4)" />
              <text x="273" y="114" text-anchor="middle" fill="#d1fae5" style="font-size: 10.5px; font-weight: 600;">Atributos + Invariante (Estado)</text>
            </svg>
            <p class="b1-note">
              En vez de funciones sueltas modificando registros externos, cada entidad protege la validez de sus propios datos.
            </p>
          </article>
        </div>

        <!-- PASO 1: CONTRASTE PROCEDURAL VS OBJETOS -->
        <div v-else-if="activeStep === 1" key="p1" class="b1-grid-2">
          <article class="b1-card b1-card--amber">
            <span class="poo-kicker poo-kicker--problem">Enfoque Procedural Clásico</span>
            <h3>Procedimientos activos + datos pasivos</h3>
            <svg viewBox="0 0 380 135" class="b1-svg" role="img" aria-label="Modelo procedural">
              <rect x="14" y="16" width="110" height="32" rx="7" fill="#1e293b" stroke="#94a3b8" />
              <text x="69" y="36" text-anchor="middle" fill="#f8fafc" style="font-family: var(--font-mono); font-size: 10.5px;">debitar(cta)</text>
              <rect x="14" y="56" width="110" height="32" rx="7" fill="#1e293b" stroke="#94a3b8" />
              <text x="69" y="76" text-anchor="middle" fill="#f8fafc" style="font-family: var(--font-mono); font-size: 10.5px;">auditar(cta)</text>
              <rect x="14" y="96" width="110" height="32" rx="7" fill="#1e293b" stroke="#94a3b8" />
              <text x="69" y="116" text-anchor="middle" fill="#f8fafc" style="font-family: var(--font-mono); font-size: 10.5px;">ajustar(cta)</text>

              <line x1="126" y1="32" x2="218" y2="68" stroke="#fbbf24" stroke-width="1.6" />
              <line x1="126" y1="72" x2="218" y2="72" stroke="#fbbf24" stroke-width="1.6" />
              <line x1="126" y1="112" x2="218" y2="76" stroke="#fbbf24" stroke-width="1.6" />

              <rect x="222" y="34" width="144" height="76" rx="10" fill="rgba(251,191,36,0.1)" stroke="#fbbf24" stroke-width="1.6" />
              <text x="294" y="62" text-anchor="middle" fill="#fde68a" style="font-size: 10.5px; font-weight: 700;">ESTRUCTURA ABIERTA</text>
              <text x="294" y="86" text-anchor="middle" fill="#f8fafc" style="font-family: var(--font-mono); font-size: 10.5px;">dict / struct</text>
            </svg>
            <ul class="b1-bullets">
              <li>Admite modularidad mediante módulos y tipos abstractos.</li>
              <li>Pero si la estructura queda expuesta, cambiar sus campos exige revisar cada función cliente.</li>
            </ul>
          </article>

          <article class="b1-card b1-card--emerald">
            <span class="poo-kicker poo-kicker--valid">Enfoque Orientado a Objetos</span>
            <h3>Frontera contractual por entidad</h3>
            <svg viewBox="0 0 380 135" class="b1-svg" role="img" aria-label="Modelo orientado a objetos">
              <rect x="14" y="20" width="148" height="96" rx="10" fill="#0d1424" stroke="#38bdf8" stroke-width="1.6" />
              <text x="88" y="44" text-anchor="middle" fill="#7dd3fc" style="font-size: 10.5px; font-weight: 700;">Pedido</text>
              <text x="88" y="68" text-anchor="middle" fill="#cbd5e1" style="font-family: var(--font-mono); font-size: 10px;">_items, _estado</text>
              <text x="88" y="92" text-anchor="middle" fill="#34d399" style="font-family: var(--font-mono); font-size: 10px;">confirmar()</text>

              <line x1="164" y1="68" x2="212" y2="68" stroke="#34d399" stroke-width="2" />
              <polygon points="216,68 208,63 208,73" fill="#34d399" />
              <text x="190" y="56" text-anchor="middle" fill="#94a3b8" style="font-size: 9.5px;">mensaje</text>

              <rect x="218" y="20" width="148" height="96" rx="10" fill="#0d1424" stroke="#34d399" stroke-width="1.6" />
              <text x="292" y="44" text-anchor="middle" fill="#6ee7b7" style="font-size: 10.5px; font-weight: 700;">CuentaBancaria</text>
              <text x="292" y="68" text-anchor="middle" fill="#cbd5e1" style="font-family: var(--font-mono); font-size: 10px;">_saldo &gt;= 0</text>
              <text x="292" y="92" text-anchor="middle" fill="#38bdf8" style="font-family: var(--font-mono); font-size: 10px;">extraer(monto)</text>
            </svg>
            <ul class="b1-bullets">
              <li>Los datos internos quedan resguardados detrás de una interfaz pública.</li>
              <li>La representación interna puede evolucionar sin romper a los colaboradores.</li>
            </ul>
          </article>
        </div>

        <!-- PASO 2: CUÁNDO CONVIENE UTILIZAR POO -->
        <div v-else key="p2" class="b1-grid-3">
          <article class="b1-card b1-card--cyan">
            <span class="poo-kicker">Dominio 01</span>
            <h3>Interfaces Gráficas y Videojuegos</h3>
            <p class="b1-lead">
              Ventanas, botones, cámaras y actores mantienen posición, estado visual y reaccionan a eventos mediante métodos uniformes (<code>dibujar()</code>, <code>al_hacer_clic()</code>).
            </p>
          </article>

          <article class="b1-card b1-card--indigo">
            <span class="poo-kicker poo-kicker--class">Dominio 02</span>
            <h3>Sistemas de Negocio con Reglas Estrictas</h3>
            <p class="b1-lead">
              Banca, logística, salud o comercio electrónico donde cuentas, envíos y pólizas deben preservar invariantes auditables a lo largo de su ciclo de vida.
            </p>
          </article>

          <article class="b1-card b1-card--emerald">
            <span class="poo-kicker poo-kicker--valid">Dominio 03</span>
            <h3>Arquitecturas Extensibles en Equipo</h3>
            <p class="b1-lead">
              Proyectos medianos y grandes donde múltiples desarrolladores integran pasarelas, sensores o estrategias nuevas apoyándose en contratos estables.
            </p>
          </article>
        </div>
      </Transition>
    </div>
  </div>
</template>

<style scoped>
.b1-stage {
  display: grid;
  grid-template-rows: 34px minmax(0, 1fr);
  row-gap: 0.7rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.b1-stepper {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.6rem;
}

.b1-step-btn {
  height: 34px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background: var(--bg-surface);
  color: var(--text-muted);
  font-size: 0.74rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
}

.b1-step-btn.is-active {
  background: var(--tint-interface);
  border-color: rgba(56, 189, 248, 0.55);
  color: #e0f2fe;
}

.b1-body {
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.b1-grid-2 {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.1rem;
  height: 100%;
}

.b1-grid-3 {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  height: 100%;
}

.b1-card {
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.55rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 0.9rem 1.05rem;
  min-width: 0;
  min-height: 0;
}

.b1-card--cyan {
  border-top: 3px solid var(--accent-interface);
}

.b1-card--indigo {
  border-top: 3px solid var(--accent-class);
}

.b1-card--emerald {
  border-top: 3px solid var(--accent-valid);
}

.b1-card--amber {
  border-top: 3px solid var(--accent-state);
}

.b1-card h3 {
  font-size: 1.04rem;
  line-height: 1.25;
  font-weight: 700;
}

.b1-lead {
  font-size: 0.82rem;
  line-height: 1.48;
  color: var(--text-secondary);
}

.b1-note {
  font-size: 0.77rem;
  line-height: 1.4;
  color: var(--text-muted);
}

.b1-svg {
  width: 100%;
  height: auto;
  max-height: 150px;
  display: block;
}

.b1-triad {
  display: flex;
  flex-direction: column;
  gap: 0.42rem;
}

.b1-pill {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  padding: 0.44rem 0.68rem;
  border-radius: 8px;
  background: #0b1120;
  border: 1px solid var(--border-subtle);
  font-size: 0.74rem;
}

.b1-pill strong {
  color: var(--text-primary);
  white-space: nowrap;
}

.b1-pill span {
  color: var(--text-muted);
  text-align: right;
}

.b1-pill--active {
  border-color: rgba(56, 189, 248, 0.5);
  background: rgba(56, 189, 248, 0.1);
}

.b1-pill--active span {
  color: #bae6fd;
}

.b1-bullets {
  margin: 0;
  padding-left: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  font-size: 0.77rem;
  line-height: 1.4;
  color: var(--text-secondary);
}
</style>
