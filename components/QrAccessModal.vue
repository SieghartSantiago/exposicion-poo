<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import QRCode from "qrcode";

const props = withDefaults(
  defineProps<{
    showGuideLink?: boolean;
    showMotionToggle?: boolean;
  }>(),
  {
    showGuideLink: true,
    showMotionToggle: true,
  }
);

const isOpen = ref(false);
const targetMode = ref<"guia" | "slides">("guia");
const customOrigin = ref("https://poo-programacion1.pages.dev");
const qrSvg = ref("");
const reducedMotion = ref(false);
const copied = ref(false);

const basePath = computed(() => {
  const raw = import.meta.env.BASE_URL || "/";
  return raw.endsWith("/") ? raw : `${raw}/`;
});

onMounted(() => {
  if (typeof window !== "undefined") {
    customOrigin.value = window.location.origin;
    const savedMotion = localStorage.getItem("poo:reduced-motion") === "true";
    const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    reducedMotion.value = savedMotion || prefersReduced;
    if (savedMotion) {
      document.documentElement.dataset.reducedMotion = "true";
    }
  }
});

const fullTargetUrl = computed(() => {
  const cleanOrigin = customOrigin.value.trim().replace(/\/+$/, "");
  if (targetMode.value === "guia") {
    return `${cleanOrigin}${basePath.value}guia/index.html`;
  }
  return `${cleanOrigin}${basePath.value}`;
});

const guiaHref = computed(() => `${basePath.value}guia/index.html`);

async function renderQr() {
  try {
    qrSvg.value = await QRCode.toString(fullTargetUrl.value, {
      type: "svg",
      margin: 1,
      width: 204,
      color: {
        dark: "#090d16",
        light: "#f8fafc",
      },
    });
  } catch {
    qrSvg.value = "";
  }
}

watch([fullTargetUrl, isOpen], ([_, open]) => {
  if (open) {
    renderQr();
  }
});

function toggleReducedMotion() {
  reducedMotion.value = !reducedMotion.value;
  if (typeof document !== "undefined") {
    if (reducedMotion.value) {
      document.documentElement.dataset.reducedMotion = "true";
      localStorage.setItem("poo:reduced-motion", "true");
    } else {
      delete document.documentElement.dataset.reducedMotion;
      localStorage.setItem("poo:reduced-motion", "false");
    }
  }
}

async function copyLink() {
  if (typeof navigator !== "undefined" && navigator.clipboard) {
    await navigator.clipboard.writeText(fullTargetUrl.value);
    copied.value = true;
    setTimeout(() => {
      copied.value = false;
    }, 1800);
  }
}
</script>

<template>
  <div class="qr-toolbar">
    <button
      type="button"
      class="poo-btn poo-btn--primary"
      @click="isOpen = true"
      aria-haspopup="dialog"
    >
      <span>📱 Acceso QR</span>
    </button>

    <a v-if="props.showGuideLink" :href="guiaHref" target="_blank" rel="noopener" class="poo-btn">
      <span>📖 Guía Móvil</span>
    </a>

    <button
      v-if="props.showMotionToggle"
      type="button"
      class="poo-btn"
      :aria-pressed="reducedMotion"
      @click="toggleReducedMotion"
      title="Alternar animaciones reducidas"
    >
      <span>{{ reducedMotion ? "⚡ Movimiento: Reducido" : "✨ Movimiento: Fluido" }}</span>
    </button>

    <Teleport to="body">
      <div
        v-if="isOpen"
        class="qr-backdrop"
        role="dialog"
        aria-modal="true"
        aria-label="Acceso por código QR para estudiantes"
        @click.self="isOpen = false"
      >
        <div class="qr-dialog">
          <div class="qr-header">
            <div>
              <span class="poo-kicker">Acceso sin instalación · WebAssembly</span>
              <h3>Seguí la guía y ejecutá los ejemplos desde tu dispositivo</h3>
            </div>
            <button type="button" class="poo-btn" @click="isOpen = false" aria-label="Cerrar ventana QR">
              ✕ Cerrar
            </button>
          </div>

          <div class="qr-body">
            <div class="qr-box" v-html="qrSvg" aria-label="Código QR"></div>

            <div class="qr-controls">
              <p class="qr-desc">
                Escaneá el código para abrir la guía de lectura vertical adaptada a celulares o iniciar directamente los laboratorios Python en el navegador.
              </p>

              <div class="qr-mode-switch" role="group" aria-label="Destino del código QR">
                <button
                  type="button"
                  class="poo-btn"
                  :class="{ 'poo-btn--primary': targetMode === 'guia' }"
                  @click="targetMode = 'guia'"
                >
                  📱 Guía Móvil + Labs
                </button>
                <button
                  type="button"
                  class="poo-btn"
                  :class="{ 'poo-btn--primary': targetMode === 'slides' }"
                  @click="targetMode = 'slides'"
                >
                  🖥️ Diapositivas 16:9
                </button>
              </div>

              <label class="qr-label">
                URL base (dominio publicado o IP de red local):
                <input
                  v-model="customOrigin"
                  type="url"
                  class="qr-input"
                  placeholder="https://usuario.github.io"
                />
              </label>

              <div class="qr-url-row">
                <code class="qr-url-preview">{{ fullTargetUrl }}</code>
                <button type="button" class="poo-btn poo-btn--emerald" @click="copyLink">
                  {{ copied ? "✓ Copiado" : "Copiar enlace" }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.qr-toolbar {
  display: inline-flex;
  flex-shrink: 0;
  flex-wrap: nowrap;
  align-items: center;
  gap: 0.55rem;
}

.qr-backdrop {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(5, 8, 16, 0.84);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.qr-dialog {
  box-sizing: border-box;
  width: min(680px, 100%);
  background: #111827;
  border: 1px solid rgba(56, 189, 248, 0.4);
  border-radius: 16px;
  padding: 1.35rem 1.5rem;
  color: #f8fafc;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.72);
  font-family: var(--font-sans);
}

.qr-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.qr-header h3 {
  margin: 0.45rem 0 0 0;
  font-family: var(--font-display);
  font-size: 1.2rem;
  line-height: 1.25;
  color: #f8fafc;
}

.qr-body {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  gap: 1.25rem;
  align-items: center;
}

.qr-box {
  background: #f8fafc;
  padding: 0.65rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 220px;
  height: 220px;
}

.qr-box :deep(svg) {
  width: 100%;
  height: 100%;
  display: block;
}

.qr-desc {
  margin: 0 0 0.75rem 0;
  font-size: 0.86rem;
  line-height: 1.48;
  color: #cbd5e1;
}

.qr-mode-switch {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.qr-label {
  display: block;
  font-size: 0.76rem;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 0.65rem;
}

.qr-input {
  box-sizing: border-box;
  margin-top: 0.3rem;
  width: 100%;
  min-height: 40px;
  padding: 0.45rem 0.7rem;
  border-radius: 8px;
  border: 1px solid rgba(148, 163, 184, 0.35);
  background: #090d16;
  color: #f8fafc;
  font-family: var(--font-mono);
  font-size: 0.8rem;
}

.qr-url-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.qr-url-preview {
  flex: 1;
  min-width: 180px;
  padding: 0.45rem 0.65rem;
  background: #090d16;
  border-radius: 6px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #7dd3fc;
  overflow-x: auto;
  white-space: nowrap;
}

@media (max-width: 640px) {
  .qr-body {
    grid-template-columns: 1fr;
    justify-items: center;
  }
}
</style>
