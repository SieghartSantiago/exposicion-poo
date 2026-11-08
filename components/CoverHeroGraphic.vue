<template>
  <div class="hero-graphic" aria-hidden="true">
    <svg
      viewBox="0 0 390 300"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      class="hero-svg"
    >
      <defs>
        <linearGradient id="capsuleGrad" x1="125" y1="24" x2="374" y2="276" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#131c31" />
          <stop offset="100%" stop-color="#0b1120" />
        </linearGradient>
        <linearGradient id="interfaceBorder" x1="125" y1="24" x2="374" y2="276" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.75" />
          <stop offset="100%" stop-color="#818cf8" stop-opacity="0.65" />
        </linearGradient>
      </defs>

      <!-- Nodo Emisor: Mensaje -->
      <rect
        x="8"
        y="112"
        width="96"
        height="68"
        rx="10"
        fill="#111827"
        stroke="#38bdf8"
        stroke-opacity="0.55"
        stroke-width="1.5"
      />
      <text x="56" y="137" text-anchor="middle" fill="#7dd3fc" class="svg-label">MENSAJE</text>
      <text x="56" y="159" text-anchor="middle" fill="#f8fafc" class="svg-mono">extraer()</text>

      <!-- Flecha de paso de mensaje -->
      <line
        x1="104"
        y1="146"
        x2="136"
        y2="146"
        stroke="#38bdf8"
        stroke-width="2"
        stroke-dasharray="4 3"
      />
      <polygon points="135,141 144,146 135,151" fill="#38bdf8" />
      <circle cx="120" cy="146" r="3.5" fill="#38bdf8" class="signal-dot" />

      <!-- Cápsula del Objeto -->
      <rect
        x="146"
        y="22"
        width="234"
        height="256"
        rx="18"
        fill="url(#capsuleGrad)"
        stroke="url(#interfaceBorder)"
        stroke-width="2"
      />

      <!-- Encabezado de Objeto -->
      <text x="166" y="50" fill="#94a3b8" class="svg-label">INSTANCIA DE CLASE</text>
      <text x="166" y="72" fill="#f8fafc" class="svg-title">CuentaBancaria</text>

      <!-- Banda de Interfaz Pública -->
      <rect
        x="164"
        y="88"
        width="198"
        height="54"
        rx="10"
        fill="rgba(56, 189, 248, 0.1)"
        stroke="#38bdf8"
        stroke-opacity="0.4"
      />
      <text x="178" y="108" fill="#7dd3fc" class="svg-label">INTERFAZ PÚBLICA</text>
      <text x="178" y="128" fill="#e2e8f0" class="svg-mono-sm">depositar · extraer · saldo</text>

      <!-- Banda de Invariante -->
      <rect
        x="164"
        y="154"
        width="198"
        height="46"
        rx="10"
        fill="rgba(52, 211, 153, 0.1)"
        stroke="#34d399"
        stroke-opacity="0.45"
      />
      <text x="178" y="173" fill="#6ee7b7" class="svg-label">INVARIANTE PROTEGIDA</text>
      <text x="178" y="191" fill="#d1fae5" class="svg-mono-sm">self._saldo &gt;= 0.0</text>

      <!-- Banda de Estado Interno -->
      <rect
        x="164"
        y="212"
        width="198"
        height="48"
        rx="10"
        fill="rgba(129, 140, 248, 0.1)"
        stroke="#818cf8"
        stroke-opacity="0.4"
      />
      <text x="178" y="231" fill="#a5b4fc" class="svg-label">ESTADO INTERNO</text>
      <text x="178" y="249" fill="#f8fafc" class="svg-mono-sm">_saldo: 30_000.0</text>
    </svg>
  </div>
</template>

<style scoped>
.hero-graphic {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-svg {
  width: 100%;
  max-width: 390px;
  height: auto;
  display: block;
}

.svg-label {
  font-family: var(--font-sans);
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 0.08em;
}

.svg-title {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 800;
}

.svg-mono {
  font-family: var(--font-mono);
  font-size: 11.5px;
  font-weight: 600;
}

.svg-mono-sm {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 500;
}

.signal-dot {
  animation: pulseMove 2.2s ease-in-out infinite;
}

@keyframes pulseMove {
  0%,
  100% {
    transform: translateX(-10px);
    opacity: 0.45;
  }
  50% {
    transform: translateX(10px);
    opacity: 1;
  }
}
</style>
