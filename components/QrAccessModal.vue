<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
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
const customOrigin = ref("https://sieghartsantiago.github.io");
const qrSvg = ref("");
const reducedMotion = ref(false);
const copied = ref(false);

const basePath = computed(() => {
  const raw = import.meta.env.BASE_URL || "/";
  return raw.endsWith("/") ? raw : `${raw}/`;
});

onMounted(() => {
  if (typeof window !== "undefined") {
    if (
      window.location.origin &&
      window.location.origin !== "null" &&
      !window.location.origin.startsWith("file:")
    ) {
      customOrigin.value = window.location.origin;
    }
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
      width: 256,
      color: {
        dark: "#090d16",
        light: "#f8fafc",
      },
    });
  } catch {
    qrSvg.value = "";
  }
}

function closeModal() {
  isOpen.value = false;
}

function handleKeydown(event: KeyboardEvent) {
  if (event.key === "Escape" && isOpen.value) {
    closeModal();
  }
}

watch([fullTargetUrl, isOpen], ([_, open]) => {
  if (open) {
    renderQr();
  }
});

watch(isOpen, (open) => {
  if (typeof window !== "undefined") {
    if (open) {
      window.addEventListener("keydown", handleKeydown);
    } else {
      window.removeEventListener("keydown", handleKeydown);
    }
  }
});

onUnmounted(() => {
  if (typeof window !== "undefined") {
    window.removeEventListener("keydown", handleKeydown);
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
  try {
    if (typeof navigator !== "undefined" && navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(fullTargetUrl.value);
    } else if (typeof document !== "undefined") {
      const el = document.createElement("textarea");
      el.value = fullTargetUrl.value;
      el.setAttribute("readonly", "");
      el.style.position = "absolute";
      el.style.left = "-9999px";
      document.body.appendChild(el);
      el.select();
      document.execCommand("copy");
      document.body.removeChild(el);
    }
    copied.value = true;
    setTimeout(() => {
      copied.value = false;
    }, 1800);
  } catch (err) {
    console.warn("No se pudo copiar el enlace:", err);
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
        @click.self="closeModal"
      >
        <div class="qr-dialog" role="document">
          <header class="qr-header">
            <div class="qr-header__text">
              <span class="poo-kicker">Acceso sin instalación · WebAssembly</span>
              <h3 id="qr-dialog-title">Seguí la guía y ejecutá los ejemplos desde tu dispositivo</h3>
            </div>
            <button
              type="button"
              class="poo-btn qr-close-btn"
              @click="closeModal"
              aria-label="Cerrar ventana QR"
            >
              ✕ Cerrar
            </button>
          </header>

          <div class="qr-body">
            <div class="qr-box-container">
              <div class="qr-box" v-html="qrSvg" aria-label="Código QR"></div>
            </div>

            <div class="qr-controls">
              <p class="qr-desc">
                Escaneá el código para abrir la guía de lectura vertical adaptada a celulares o iniciar directamente los laboratorios Python en el navegador.
              </p>

              <div class="qr-mode-switch" role="group" aria-label="Destino del código QR">
                <button
                  type="button"
                  class="poo-btn qr-mode-btn"
                  :class="{ 'poo-btn--primary': targetMode === 'guia', 'is-active': targetMode === 'guia' }"
                  :aria-pressed="targetMode === 'guia'"
                  @click="targetMode = 'guia'"
                >
                  📱 Guía Móvil + Labs
                </button>
                <button
                  type="button"
                  class="poo-btn qr-mode-btn"
                  :class="{ 'poo-btn--primary': targetMode === 'slides', 'is-active': targetMode === 'slides' }"
                  :aria-pressed="targetMode === 'slides'"
                  @click="targetMode = 'slides'"
                >
                  🖥️ Diapositivas 16:9
                </button>
              </div>

              <label class="qr-label">
                <span>URL base (dominio publicado o IP de red local):</span>
                <input
                  v-model="customOrigin"
                  type="url"
                  class="qr-input"
                  placeholder="https://usuario.github.io"
                  autocomplete="off"
                  spellcheck="false"
                />
              </label>

              <div class="qr-url-row">
                <div class="qr-url-preview-wrapper">
                  <code class="qr-url-preview">{{ fullTargetUrl }}</code>
                </div>
                <button
                  type="button"
                  class="poo-btn poo-btn--emerald qr-copy-btn"
                  @click="copyLink"
                  :aria-label="copied ? 'Enlace copiado al portapapeles' : 'Copiar enlace al portapapeles'"
                >
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
  background: rgba(5, 8, 16, 0.86);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  box-sizing: border-box;
  overflow-y: auto;
  overscroll-behavior: contain;
}

.qr-dialog {
  box-sizing: border-box;
  width: min(680px, calc(100vw - 32px));
  max-width: 680px;
  max-height: calc(100dvh - 32px);
  margin: auto;
  background: #111827;
  border: 1px solid rgba(56, 189, 248, 0.38);
  border-radius: 16px;
  padding: 1.25rem 1.4rem;
  color: #f8fafc;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.75), 0 0 0 1px rgba(56, 189, 248, 0.12);
  font-family: var(--font-sans);
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.qr-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.85rem;
  margin-bottom: 0.85rem;
  flex-shrink: 0;
  min-width: 0;
  width: 100%;
}

.qr-header__text {
  flex: 1 1 auto;
  min-width: 0;
}

.qr-header__text :deep(.poo-kicker) {
  white-space: normal;
  max-width: 100%;
  display: inline-flex;
  font-size: 0.68rem;
  line-height: 1.25;
  padding: 0.2rem 0.55rem;
  margin-bottom: 0.3rem;
}

.qr-header h3 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.15rem;
  line-height: 1.25;
  color: #f8fafc;
  overflow-wrap: break-word;
  word-break: break-word;
}

.qr-close-btn {
  flex-shrink: 0;
  min-width: 76px;
  min-height: 38px;
  padding: 0.4rem 0.75rem;
  font-size: 0.76rem;
}

.qr-body {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  gap: 1.25rem;
  align-items: center;
  min-width: 0;
  width: 100%;
  flex: 1 1 auto;
  overflow-y: auto;
  min-height: 0;
  scrollbar-width: thin;
  scrollbar-color: rgba(56, 189, 248, 0.25) transparent;
}

.qr-box-container {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  min-width: 0;
}

.qr-box {
  background: #f8fafc;
  padding: 0.65rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 210px;
  height: 210px;
  aspect-ratio: 1 / 1;
  box-sizing: border-box;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
}

.qr-box :deep(svg) {
  width: 100%;
  height: 100%;
  display: block;
}

.qr-controls {
  display: flex;
  flex-direction: column;
  min-width: 0;
  width: 100%;
}

.qr-desc {
  margin: 0 0 0.7rem 0;
  font-size: 0.85rem;
  line-height: 1.45;
  color: #cbd5e1;
  overflow-wrap: break-word;
  word-break: break-word;
}

.qr-mode-switch {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.5rem;
  margin-bottom: 0.7rem;
  width: 100%;
  min-width: 0;
}

.qr-mode-btn {
  width: 100%;
  min-width: 0;
  min-height: 40px;
  padding: 0.45rem 0.5rem;
  font-size: 0.76rem;
  line-height: 1.25;
  white-space: normal;
  text-align: center;
  justify-content: center;
  border-radius: 8px;
  background: #0d1424;
  border-color: rgba(148, 163, 184, 0.28);
  color: #94a3b8;
  transition: all var(--duration-fast, 160ms) ease;
}

.qr-mode-btn.is-active,
.qr-mode-btn.poo-btn--primary {
  background: rgba(56, 189, 248, 0.18);
  border-color: rgba(56, 189, 248, 0.65);
  color: #e0f2fe;
  font-weight: 700;
  box-shadow: 0 0 12px rgba(56, 189, 248, 0.15);
}

.qr-label {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  font-size: 0.76rem;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 0.7rem;
  width: 100%;
  min-width: 0;
}

.qr-input {
  box-sizing: border-box;
  width: 100%;
  min-width: 0;
  min-height: 40px;
  padding: 0.45rem 0.7rem;
  border-radius: 8px;
  border: 1px solid rgba(148, 163, 184, 0.35);
  background: #090d16;
  color: #f8fafc;
  font-family: var(--font-mono);
  font-size: 0.78rem;
  transition: border-color var(--duration-fast, 160ms) ease, box-shadow var(--duration-fast, 160ms) ease;
}

.qr-input:focus {
  outline: none;
  border-color: var(--accent-interface, #38bdf8);
  box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.22);
}

.qr-url-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  min-width: 0;
}

.qr-url-preview-wrapper {
  flex: 1 1 0;
  min-width: 0;
  width: 0;
}

.qr-url-preview {
  display: block;
  box-sizing: border-box;
  width: 100%;
  min-width: 0;
  min-height: 38px;
  padding: 0.5rem 0.65rem;
  background: #090d16;
  border: 1px solid rgba(148, 163, 184, 0.25);
  border-radius: 6px;
  font-family: var(--font-mono);
  font-size: 0.74rem;
  line-height: 1.35;
  color: #7dd3fc;
  overflow-x: auto;
  white-space: nowrap;
  scrollbar-width: thin;
  scrollbar-color: rgba(56, 189, 248, 0.3) transparent;
}

.qr-copy-btn {
  flex-shrink: 0;
  min-width: 112px;
  min-height: 38px;
  white-space: nowrap;
}

/* ==========================================================================
   ADAPTACIONES RESPONSIVE (MÓVIL, TABLET, ORIENTACIÓN HORIZONTAL)
   ========================================================================== */

@media (max-width: 640px) {
  .qr-dialog {
    padding: 0.95rem 1rem;
    width: calc(100vw - 32px);
    border-radius: 14px;
  }

  .qr-header {
    margin-bottom: 0.55rem;
    gap: 0.5rem;
  }

  .qr-header h3 {
    font-size: 0.96rem;
  }

  .qr-close-btn {
    min-width: 66px;
    min-height: 36px;
    padding: 0.32rem 0.5rem;
    font-size: 0.72rem;
  }

  .qr-body {
    grid-template-columns: 1fr;
    gap: 0.65rem;
    justify-items: center;
  }

  .qr-box-container {
    width: 100%;
    display: flex;
    justify-content: center;
  }

  .qr-box {
    width: clamp(125px, 38vw, 160px);
    height: auto;
    aspect-ratio: 1 / 1;
    padding: 0.45rem;
    border-radius: 10px;
  }

  .qr-desc {
    text-align: center;
    font-size: 0.78rem;
    line-height: 1.38;
    margin-bottom: 0.5rem;
  }

  .qr-mode-switch {
    gap: 0.45rem;
    margin-bottom: 0.55rem;
  }

  .qr-mode-btn {
    min-height: 38px;
    font-size: 0.74rem;
    padding: 0.35rem 0.3rem;
  }

  .qr-label {
    font-size: 0.72rem;
    gap: 0.25rem;
    margin-bottom: 0.55rem;
  }

  .qr-input {
    min-height: 36px;
    font-size: 0.75rem;
    padding: 0.35rem 0.55rem;
  }

  .qr-url-row {
    flex-direction: column;
    align-items: stretch;
    gap: 0.45rem;
  }

  .qr-url-preview-wrapper {
    width: 100%;
    flex: none;
  }

  .qr-url-preview {
    min-height: 34px;
    font-size: 0.72rem;
    padding: 0.38rem 0.5rem;
  }

  .qr-copy-btn {
    width: 100%;
    min-height: 38px;
    font-size: 0.78rem;
    justify-content: center;
  }
}

@media (max-width: 360px) {
  .qr-dialog {
    padding: 0.75rem 0.8rem;
    border-radius: 12px;
  }

  .qr-header {
    margin-bottom: 0.45rem;
  }

  .qr-header h3 {
    font-size: 0.88rem;
    line-height: 1.2;
  }

  .qr-header__text :deep(.poo-kicker) {
    font-size: 0.6rem;
    padding: 0.15rem 0.4rem;
    margin-bottom: 0.2rem;
  }

  .qr-close-btn {
    min-width: 60px;
    min-height: 34px;
    padding: 0.25rem 0.4rem;
    font-size: 0.68rem;
  }

  .qr-box {
    width: 120px;
  }

  .qr-mode-btn {
    font-size: 0.68rem;
    min-height: 36px;
    padding: 0.25rem 0.2rem;
  }

  .qr-desc {
    font-size: 0.74rem;
    line-height: 1.32;
    margin-bottom: 0.45rem;
  }

  .qr-label {
    font-size: 0.7rem;
    margin-bottom: 0.45rem;
  }

  .qr-input {
    min-height: 34px;
    font-size: 0.72rem;
  }

  .qr-url-preview {
    min-height: 32px;
    font-size: 0.68rem;
  }

  .qr-copy-btn {
    min-height: 36px;
    font-size: 0.74rem;
  }
}

/* Optimización para orientación horizontal en celulares (pantallas con altura reducida) */
@media (max-height: 520px) and (orientation: landscape) {
  .qr-backdrop {
    padding: 8px;
  }

  .qr-dialog {
    padding: 0.75rem 1rem;
    max-height: calc(100vh - 16px);
  }

  .qr-header {
    margin-bottom: 0.45rem;
  }

  .qr-header h3 {
    font-size: 0.95rem;
  }

  .qr-body {
    grid-template-columns: auto minmax(0, 1fr);
    gap: 0.85rem;
    align-items: center;
  }

  .qr-box-container {
    width: auto;
  }

  .qr-box {
    width: clamp(110px, 28vh, 140px);
    height: auto;
    aspect-ratio: 1 / 1;
    padding: 0.4rem;
  }

  .qr-desc {
    display: none;
  }

  .qr-mode-switch {
    margin-bottom: 0.45rem;
  }

  .qr-mode-btn {
    min-height: 36px;
    font-size: 0.74rem;
    padding: 0.35rem 0.5rem;
  }

  .qr-label {
    margin-bottom: 0.45rem;
    font-size: 0.72rem;
  }

  .qr-input {
    min-height: 36px;
    font-size: 0.74rem;
    padding: 0.35rem 0.55rem;
  }

  .qr-url-row {
    flex-direction: row;
    gap: 0.45rem;
  }

  .qr-url-preview-wrapper {
    flex: 1 1 0;
    width: 0;
  }

  .qr-url-preview {
    min-height: 36px;
    padding: 0.38rem 0.55rem;
  }

  .qr-copy-btn {
    width: auto;
    min-height: 36px;
    padding: 0.38rem 0.75rem;
    font-size: 0.76rem;
  }
}
</style>
