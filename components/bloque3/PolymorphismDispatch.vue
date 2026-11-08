<script setup lang="ts">
import { computed } from "vue";
import { useSlideContext } from "@slidev/client";
import PythonCodePanel from "../common/PythonCodePanel.vue";

const { $clicks } = useSlideContext();

type Step = 0 | 1 | 2 | 3;

const step = computed<Step>(() => {
  const n = Number($clicks?.value ?? 0);
  if (n <= 0) return 0;
  if (n === 1) return 1;
  if (n === 2) return 2;
  return 3;
});

function setStep(s: Step) {
  if ($clicks) $clicks.value = s;
}

const codeSteps: Record<Step, { file: string; status: string; accent: "problem" | "valid" | "class" | "interface"; lines: string[] }> = {
  0: {
    file: "01_condicional_acoplado.py",
    status: "Rígido ante cambios",
    accent: "problem",
    lines: [
      "# Problema: preguntar el tipo concreto en cada cobro",
      "def cobrar_pedido(medio: object, monto: float) -> str:",
      "    if isinstance(medio, PagoTarjeta):",
      "        return medio.autorizar_cuotas(monto)",
      "    elif isinstance(medio, PagoTransferencia):",
      "        return medio.debitar_cbu(monto)",
      "    elif isinstance(medio, PagoQR):",
      "        return medio.generar_token_qr(monto)",
      '    raise TypeError("Medio no soportado")',
      "",
      "# Agregar PagoCripto obliga a editar esta función!",
    ],
  },
  1: {
    file: "02_despacho_dinamico.py",
    status: "Enlace tardío",
    accent: "valid",
    lines: [
      "from typing import Protocol",
      "",
      "class MedioPago(Protocol):",
      "    def cobrar(self, monto: float) -> str: ...",
      "",
      "def procesar_pagos(lote: list[MedioPago], m: float) -> None:",
      "    for medio in lote:",
      "        # La implementación se resuelve en EJECUCIÓN:",
      "        print(medio.cobrar(m))",
      "",
      "# PagoTarjeta().cobrar(m)  |  PagoQR().cobrar(m)",
    ],
  },
  2: {
    file: "03_mecanismo_resolucion.py",
    status: "vtable vs Duck Typing",
    accent: "class",
    lines: [
      "class PagoTarjeta:",
      "    def cobrar(self, monto: float) -> str:",
      '        return f"Tarjeta: ${monto:,.0f} aprobado"',
      "",
      "class PagoQR:",
      "    def cobrar(self, monto: float) -> str:",
      '        return f"QR interoperable: ${monto:,.0f} OK"',
      "",
      "# Python busca 'cobrar' en el tipo real del receptor",
      "# (type(medio).__dict__ -> MRO) en tiempo de ejecución.",
    ],
  },
  3: {
    file: "04_variantes_polimorfismo.py",
    status: "3 Familias distintas",
    accent: "interface",
    lines: [
      "# 1. Subtipado / Protocolos (Despacho dinámico):",
      "def pagar(m: MedioPago) -> str: return m.cobrar(1000.0)",
      "",
      "# 2. Paramétrico (Genéricos independientes del tipo T):",
      "def primero[T](items: list[T]) -> T:",
      "    return items[0]",
      "",
      "# 3. Ad-Hoc (Sobrecarga de operadores / singledispatch):",
      "print(10 + 20)        # Suma entera -> 30",
      'print("POO" + "!")    # Concatenación -> "POO!"',
    ],
  },
};

const cur = computed(() => codeSteps[step.value]);
</script>

<template>
  <div class="poly-stage">
    <nav class="poly-nav" aria-label="Etapas de polimorfismo">
      <button type="button" class="poly-btn" :class="{ 'is-active': step === 0 }" @click="setStep(0)">
        1. Problema <code>if</code>/<code>isinstance</code>
      </button>
      <button type="button" class="poly-btn" :class="{ 'is-active': step === 1 }" @click="setStep(1)">
        2. Despacho dinámico
      </button>
      <button type="button" class="poly-btn" :class="{ 'is-active': step === 2 }" @click="setStep(2)">
        3. ¿Cómo se resuelve?
      </button>
      <button type="button" class="poly-btn" :class="{ 'is-active': step === 3 }" @click="setStep(3)">
        4. Tipos de polimorfismo
      </button>
    </nav>

    <div class="poly-grid">
      <PythonCodePanel
        :file-name="cur.file"
        :status-text="cur.status"
        :accent="cur.accent"
        :lines="cur.lines"
        :state-key="step"
      />

      <div class="poly-right">
        <Transition name="poo-fade" mode="out-in">
          <article v-if="step === 0" key="p0" class="poly-card poly-card--problem">
            <span class="poo-kicker poo-kicker--problem">El Problema</span>
            <h3>Ramificaciones por tipo en el cliente</h3>
            <p class="poly-p">
              Cuando el código emisor inspecciona manualmente de qué clase es cada objeto, concentra el conocimiento de todos los casos concretos y se vuelve frágil ante extensiones.
            </p>
            <div class="poly-badge-box">
              Cada medio de pago nuevo exige abrir y modificar la función central.
            </div>
          </article>

          <article v-else-if="step === 1" key="p1" class="poly-card poly-card--valid">
            <span class="poo-kicker poo-kicker--valid">Despacho Dinámico (Late Binding)</span>
            <h3>Un mismo mensaje, múltiples respuestas</h3>
            <div class="poly-dispatch">
              <div class="poly-call"><code>medio.cobrar(5000)</code></div>
              <div class="poly-targets">
                <div class="poly-target"><code>PagoTarjeta</code> → <span>ejecuta <code>PagoTarjeta.cobrar</code></span></div>
                <div class="poly-target"><code>PagoTransferencia</code> → <span>ejecuta <code>PagoTransferencia.cobrar</code></span></div>
                <div class="poly-target"><code>PagoQR</code> → <span>ejecuta <code>PagoQR.cobrar</code></span></div>
              </div>
            </div>
            <p class="poly-p">
              <code>procesar_pagos</code> no cambia nunca aunque mañana sumemos 10 medios nuevos.
            </p>
          </article>

          <article v-else-if="step === 2" key="p2" class="poly-card poly-card--class">
            <span class="poo-kicker poo-kicker--class">Mecanismo bajo el capó</span>
            <h3>Lenguajes compilados vs. Python</h3>
            <ul class="poly-list">
              <li>
                <strong>C++ / Java / C# (<code>vptr → vtable</code>):</strong> cada instancia polimórfica guarda un puntero oculto hacia la tabla de métodos virtuales de su clase concreta (salto indirecto en <code>O(1)</code>).
              </li>
              <li>
                <strong>Python (enlace dinámico y <em>duck typing</em>):</strong> resuelve el atributo en tiempo de ejecución sobre <code>type(obj)</code> siguiendo su <code>MRO</code>; <code>typing.Protocol</code> permite verificar el contrato estáticamente sin exigir herencia nominal.
              </li>
            </ul>
          </article>

          <article v-else key="p3" class="poly-card poly-card--interface">
            <span class="poo-kicker">Precisión Conceptual</span>
            <h3>No todo polimorfismo es despacho dinámico</h3>
            <ul class="poly-list">
              <li>
                <strong>De subtipado / inclusión:</strong> propio de POO; selecciona el método en ejecución según la clase receptora.
              </li>
              <li>
                <strong>Paramétrico (Genéricos):</strong> un mismo algoritmo opera uniformemente para cualquier tipo <code>T</code> sin cambiar de conducta por tipo.
              </li>
              <li>
                <strong>Ad-Hoc (Sobrecarga):</strong> un mismo nombre u operador (<code>+</code>) invoca funciones distintas según los tipos de sus operandos.
              </li>
            </ul>
          </article>
        </Transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
.poly-stage {
  display: grid;
  grid-template-rows: 34px minmax(0, 1fr);
  row-gap: 0.7rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.poly-nav {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.55rem;
}

.poly-btn {
  height: 34px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background: var(--bg-surface);
  color: var(--text-muted);
  font-size: 0.71rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
}

.poly-btn.is-active {
  background: var(--tint-valid);
  border-color: rgba(52, 211, 153, 0.55);
  color: #d1fae5;
}

.poly-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(0, 0.92fr);
  gap: 1.15rem;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.poly-right {
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.poly-card {
  box-sizing: border-box;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.6rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 0.95rem 1.05rem;
}

.poly-card--problem {
  border-top: 3px solid var(--accent-problem);
}

.poly-card--valid {
  border-top: 3px solid var(--accent-valid);
}

.poly-card--class {
  border-top: 3px solid var(--accent-class);
}

.poly-card--interface {
  border-top: 3px solid var(--accent-interface);
}

.poly-card h3 {
  font-size: 1.03rem;
  line-height: 1.24;
  font-weight: 700;
}

.poly-p {
  font-size: 0.78rem;
  line-height: 1.43;
  color: var(--text-secondary);
}

.poly-badge-box {
  background: rgba(251, 113, 133, 0.1);
  border: 1px solid rgba(251, 113, 133, 0.35);
  border-radius: 8px;
  padding: 0.6rem 0.75rem;
  font-size: 0.77rem;
  color: #fecdd3;
}

.poly-dispatch {
  display: flex;
  flex-direction: column;
  gap: 0.42rem;
}

.poly-call {
  background: rgba(56, 189, 248, 0.12);
  border: 1px solid rgba(56, 189, 248, 0.4);
  border-radius: 7px;
  padding: 0.38rem 0.65rem;
  text-align: center;
  font-size: 0.78rem;
}

.poly-targets {
  display: flex;
  flex-direction: column;
  gap: 0.32rem;
}

.poly-target {
  background: #0b1120;
  border: 1px solid var(--border-subtle);
  border-radius: 7px;
  padding: 0.36rem 0.6rem;
  font-size: 0.73rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.4rem;
}

.poly-target span {
  color: var(--text-secondary);
}

.poly-list {
  margin: 0;
  padding-left: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.42rem;
  font-size: 0.76rem;
  line-height: 1.4;
  color: var(--text-secondary);
}
</style>
