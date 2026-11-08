<script setup lang="ts">
import { computed } from "vue";
import { useSlideContext } from "@slidev/client";

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
</script>

<template>
  <div class="crisis-wrap">
    <nav class="crisis-nav" aria-label="Problemas de ingeniería de software">
      <button type="button" class="crisis-tab" :class="{ 'is-active': step === 0 }" @click="setStep(0)">
        1. Efecto dominó por datos expuestos
      </button>
      <button type="button" class="crisis-tab" :class="{ 'is-active': step === 1 }" @click="setStep(1)">
        2. Validaciones duplicadas y frágiles
      </button>
      <button type="button" class="crisis-tab" :class="{ 'is-active': step === 2 }" @click="setStep(2)">
        3. Respuesta POO: aislamiento por contrato
      </button>
    </nav>

    <div class="crisis-panel">
      <Transition name="poo-fade" mode="out-in">
        <!-- PASO 0 -->
        <div v-if="step === 0" key="c0" class="crisis-content">
          <div class="crisis-diagram">
            <svg viewBox="0 0 460 220" class="crisis-svg" role="img" aria-label="Acoplamiento a estructura expuesta">
              <rect x="155" y="16" width="150" height="54" rx="10" fill="rgba(251,113,133,0.14)" stroke="#fb7185" stroke-width="1.8" />
              <text x="230" y="38" text-anchor="middle" fill="#fda4af" style="font-size: 10.5px; font-weight: 700;">CAMBIO INTERNO</text>
              <text x="230" y="56" text-anchor="middle" fill="#f8fafc" style="font-family: var(--font-mono); font-size: 10px;">saldo_centavos: int</text>

              <line x1="190" y1="70" x2="80" y2="142" stroke="#fb7185" stroke-width="2" />
              <line x1="230" y1="70" x2="230" y2="142" stroke="#fb7185" stroke-width="2" />
              <line x1="270" y1="70" x2="380" y2="142" stroke="#fb7185" stroke-width="2" />

              <rect x="20" y="144" width="120" height="56" rx="9" fill="#111827" stroke="#fb7185" />
              <text x="80" y="168" text-anchor="middle" fill="#fda4af" style="font-size: 10px; font-weight: 700;">✗ módulo_caja.py</text>
              <text x="80" y="186" text-anchor="middle" fill="#cbd5e1" style="font-size: 9.5px;">Rompe lectura directa</text>

              <rect x="170" y="144" width="120" height="56" rx="9" fill="#111827" stroke="#fb7185" />
              <text x="230" y="168" text-anchor="middle" fill="#fda4af" style="font-size: 10px; font-weight: 700;">✗ reportes.py</text>
              <text x="230" y="186" text-anchor="middle" fill="#cbd5e1" style="font-size: 9.5px;">Cálculo ×100 erróneo</text>

              <rect x="320" y="144" width="120" height="56" rx="9" fill="#111827" stroke="#fb7185" />
              <text x="380" y="168" text-anchor="middle" fill="#fda4af" style="font-size: 10px; font-weight: 700;">✗ pagos_qr.py</text>
              <text x="380" y="186" text-anchor="middle" fill="#cbd5e1" style="font-size: 9.5px;">Requiere refactorizar</text>
            </svg>
          </div>
          <div class="crisis-text">
            <span class="poo-kicker poo-kicker--problem">Crisis del Software (1960–1970)</span>
            <h3>Acoplamiento a la representación física</h3>
            <p>
              Al crecer los sistemas a cientos de miles de líneas, permitir que decenas de rutinas leyeran directamente los campos internos convertía cualquier mejora de representación en una cascada de errores.
            </p>
            <div class="crisis-metric crisis-metric--bad">
              <span>1 cambio de estructura</span>
              <strong>→ N módulos rotos</strong>
            </div>
          </div>
        </div>

        <!-- PASO 1 -->
        <div v-else-if="step === 1" key="c1" class="crisis-content">
          <div class="crisis-diagram">
            <svg viewBox="0 0 460 220" class="crisis-svg" role="img" aria-label="Dispersión de reglas de negocio">
              <rect x="24" y="24" width="185" height="48" rx="8" fill="#111827" stroke="#fbbf24" />
              <text x="116" y="45" text-anchor="middle" fill="#fde68a" style="font-family: var(--font-mono); font-size: 10px;">if monto &gt; 0 and saldo &gt;= m:</text>
              <text x="116" y="61" text-anchor="middle" fill="#94a3b8" style="font-size: 9.5px;">sucursal.py (validado)</text>

              <rect x="24" y="88" width="185" height="48" rx="8" fill="#111827" stroke="#fbbf24" />
              <text x="116" y="109" text-anchor="middle" fill="#fde68a" style="font-family: var(--font-mono); font-size: 10px;">if saldo &gt;= monto:</text>
              <text x="116" y="125" text-anchor="middle" fill="#fda4af" style="font-size: 9.5px;">cajero.py (olvidó monto &gt; 0)</text>

              <rect x="24" y="152" width="185" height="48" rx="8" fill="#111827" stroke="#fb7185" />
              <text x="116" y="173" text-anchor="middle" fill="#fda4af" style="font-family: var(--font-mono); font-size: 10px;">cta["saldo"] -= monto</text>
              <text x="116" y="189" text-anchor="middle" fill="#fda4af" style="font-size: 9.5px;">lote_nocturno.py (sin filtro)</text>

              <line x1="212" y1="112" x2="268" y2="112" stroke="#fb7185" stroke-width="2" stroke-dasharray="4 3" />
              <rect x="272" y="68" width="166" height="88" rx="10" fill="rgba(251,113,133,0.12)" stroke="#fb7185" stroke-width="1.8" />
              <text x="355" y="102" text-anchor="middle" fill="#fda4af" style="font-size: 11px; font-weight: 700;">ESTADO CORRUPTO</text>
              <text x="355" y="126" text-anchor="middle" fill="#f8fafc" style="font-size: 10px;">Basta un solo olvido</text>
              <text x="355" y="142" text-anchor="middle" fill="#cbd5e1" style="font-size: 9.5px;">para violar la regla</text>
            </svg>
          </div>
          <div class="crisis-text">
            <span class="poo-kicker poo-kicker--problem">Fragilidad Operativa</span>
            <h3>Invariantes dispersas en todo el código</h3>
            <p>
              Cuando la validez de una entidad depende de que cada programador recuerde escribir el mismo <code>if</code> antes de mutar un dato, la consistencia del sistema queda librada a la disciplina manual.
            </p>
            <div class="crisis-metric crisis-metric--bad">
              <span>Validación repetida en K sitios</span>
              <strong>→ Alta deuda técnica</strong>
            </div>
          </div>
        </div>

        <!-- PASO 2 -->
        <div v-else key="c2" class="crisis-content">
          <div class="crisis-diagram">
            <svg viewBox="0 0 460 220" class="crisis-svg" role="img" aria-label="Confinamiento mediante interfaz pública">
              <rect x="18" y="28" width="110" height="44" rx="8" fill="#111827" stroke="#38bdf8" />
              <text x="73" y="54" text-anchor="middle" fill="#e0f2fe" style="font-size: 10px; font-weight: 600;">módulo_caja</text>
              <rect x="18" y="88" width="110" height="44" rx="8" fill="#111827" stroke="#38bdf8" />
              <text x="73" y="114" text-anchor="middle" fill="#e0f2fe" style="font-size: 10px; font-weight: 600;">reportes</text>
              <rect x="18" y="148" width="110" height="44" rx="8" fill="#111827" stroke="#38bdf8" />
              <text x="73" y="174" text-anchor="middle" fill="#e0f2fe" style="font-size: 10px; font-weight: 600;">pagos_qr</text>

              <line x1="130" y1="50" x2="196" y2="96" stroke="#38bdf8" stroke-width="1.8" />
              <line x1="130" y1="110" x2="196" y2="110" stroke="#38bdf8" stroke-width="1.8" />
              <line x1="130" y1="170" x2="196" y2="124" stroke="#38bdf8" stroke-width="1.8" />

              <rect x="198" y="36" width="96" height="148" rx="10" fill="rgba(56,189,248,0.15)" stroke="#38bdf8" stroke-width="2" />
              <text x="246" y="88" text-anchor="middle" fill="#7dd3fc" style="font-size: 10px; font-weight: 700;">CONTRATO</text>
              <text x="246" y="110" text-anchor="middle" fill="#f8fafc" style="font-family: var(--font-mono); font-size: 9.5px;">extraer()</text>
              <text x="246" y="130" text-anchor="middle" fill="#f8fafc" style="font-family: var(--font-mono); font-size: 9.5px;">saldo</text>

              <rect x="306" y="54" width="136" height="112" rx="10" fill="rgba(52,211,153,0.12)" stroke="#34d399" stroke-width="1.8" />
              <text x="374" y="86" text-anchor="middle" fill="#6ee7b7" style="font-size: 10px; font-weight: 700;">INTERIOR AISLADO</text>
              <text x="374" y="110" text-anchor="middle" fill="#cbd5e1" style="font-family: var(--font-mono); font-size: 9.5px;">_centavos: int</text>
              <text x="374" y="132" text-anchor="middle" fill="#34d399" style="font-size: 9.5px;">Cambiable sin</text>
              <text x="374" y="147" text-anchor="middle" fill="#34d399" style="font-size: 9.5px;">romper clientes</text>
            </svg>
          </div>
          <div class="crisis-text">
            <span class="poo-kicker poo-kicker--valid">Solución de Ingeniería</span>
            <h3>Confinamiento del estado y bajo acoplamiento</h3>
            <p>
              Al blindar los datos detrás de un contrato estable, la regla se programa y verifica en un único lugar, y el interior de la clase puede optimizarse libremente sin afectar al resto del equipo.
            </p>
            <div class="crisis-metric crisis-metric--good">
              <span>1 cambio interno</span>
              <strong>→ 0 clientes afectados</strong>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<style scoped>
.crisis-wrap {
  display: grid;
  grid-template-rows: 34px minmax(0, 1fr);
  row-gap: 0.7rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.crisis-nav {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.6rem;
}

.crisis-tab {
  height: 34px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background: var(--bg-surface);
  color: var(--text-muted);
  font-size: 0.73rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
}

.crisis-tab.is-active {
  background: var(--tint-interface);
  border-color: rgba(56, 189, 248, 0.55);
  color: #e0f2fe;
}

.crisis-panel {
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.crisis-content {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(0, 0.85fr);
  gap: 1.2rem;
  align-items: center;
  height: 100%;
}

.crisis-diagram {
  background: #090d16;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 0.6rem;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  box-sizing: border-box;
}

.crisis-svg {
  width: 100%;
  height: auto;
  max-height: 225px;
  display: block;
}

.crisis-text {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: 0.65rem;
}

.crisis-text h3 {
  font-size: 1.12rem;
  line-height: 1.24;
  font-weight: 700;
}

.crisis-text p {
  font-size: 0.82rem;
  line-height: 1.48;
  color: var(--text-secondary);
}

.crisis-metric {
  width: 100%;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.55rem 0.8rem;
  border-radius: 8px;
  font-size: 0.78rem;
}

.crisis-metric--bad {
  background: rgba(251, 113, 133, 0.12);
  border: 1px solid rgba(251, 113, 133, 0.4);
  color: #fecdd3;
}

.crisis-metric--good {
  background: rgba(52, 211, 153, 0.12);
  border: 1px solid rgba(52, 211, 153, 0.4);
  color: #d1fae5;
}
</style>
