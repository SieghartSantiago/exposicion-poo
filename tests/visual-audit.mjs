import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, "..");
const distDir = path.join(rootDir, "dist");
const outDir =
  process.env.AUDIT_OUT_DIR ||
  "C:/Users/santi/.gemini/antigravity/brain/a9582384-000b-45d4-a88a-0292f37d7c76";
const shotsSubDir = path.join(outDir, "fase2_screenshots");

fs.mkdirSync(outDir, { recursive: true });
fs.rmSync(shotsSubDir, { recursive: true, force: true });
fs.mkdirSync(shotsSubDir, { recursive: true });

const SLIDE_SPECS = [
  { slide: 1, clicks: 0, name: "Portada" },
  { slide: 2, clicks: 2, name: "Paradigma y POO" },
  { slide: 3, clicks: 2, name: "Problemas de Ingenieria" },
  { slide: 4, clicks: 5, name: "Linea de Tiempo Historica" },
  { slide: 5, clicks: 3, name: "Anatomia de Clase" },
  { slide: 6, clicks: 3, name: "Instanciacion y Referencias" },
  { slide: 7, clicks: 2, name: "Paso de Mensajes e Identidad" },
  { slide: 8, clicks: 2, name: "Pilar 1 Abstraccion" },
  { slide: 9, clicks: 2, name: "Pilar 2 Encapsulamiento" },
  { slide: 10, clicks: 0, name: "Lab 01 Launchpad" },
  { slide: 11, clicks: 2, name: "Pilar 3 Herencia" },
  { slide: 12, clicks: 2, name: "Composicion vs Herencia" },
  { slide: 13, clicks: 3, name: "Pilar 4 Polimorfismo" },
  { slide: 14, clicks: 0, name: "Lab 02 Launchpad" },
  { slide: 15, clicks: 4, name: "Principios SOLID" },
  { slide: 16, clicks: 2, name: "Patron Strategy" },
  { slide: 17, clicks: 1, name: "Patrones Adapter y Decorator" },
  { slide: 18, clicks: 0, name: "Lab 03 Launchpad" },
  { slide: 19, clicks: 2, name: "Trade-offs y Memoria" },
  { slide: 20, clicks: 2, name: "Comparacion 3 Paradigmas" },
  { slide: 21, clicks: 0, name: "Lab 04 Launchpad" },
  { slide: 22, clicks: 0, name: "Conclusiones" },
  { slide: 23, clicks: 0, name: "Bibliografia y Recursos" },
];

const MIME_TYPES = {
  ".html": "text/html; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".mjs": "application/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".wasm": "application/wasm",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".ico": "image/x-icon",
  ".woff2": "font/woff2",
  ".woff": "font/woff",
  ".ttf": "font/ttf",
};

function startStaticServer(directory) {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const reqUrl = new URL(req.url || "/", "http://127.0.0.1");
      let pathname = decodeURIComponent(reqUrl.pathname);
      if (pathname.endsWith("/")) pathname += "index.html";

      let filePath = path.join(directory, pathname);
      if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
        const htmlCandidate = path.join(filePath, "index.html");
        if (fs.existsSync(htmlCandidate)) {
          filePath = htmlCandidate;
        } else {
          // SPA fallback para rutas de Slidev (/1 .. /23)
          filePath = path.join(directory, "index.html");
        }
      }

      try {
        const data = fs.readFileSync(filePath);
        const ext = path.extname(filePath).toLowerCase();
        res.writeHead(200, {
          "Content-Type": MIME_TYPES[ext] || "application/octet-stream",
          "Cache-Control": "no-cache",
        });
        res.end(data);
      } catch {
        res.writeHead(404);
        res.end("Not found");
      }
    });

    server.listen(0, "127.0.0.1", () => {
      const addr = server.address();
      resolve({
        server,
        baseUrl: `http://127.0.0.1:${addr.port}`,
      });
    });
  });
}

async function auditSlideGeometry(page, slideNum, stepNum, viewportLabel) {
  return page.evaluate(
    ({ sNum, stNum, vpLabel }) => {
      const issues = [];
      const pageEl = document.querySelector(`.slidev-page-${sNum}`);
      const layout = pageEl ? pageEl.querySelector(".slidev-layout") : null;

      if (!layout) {
        return {
          ok: false,
          issues: [`No se encontró .slidev-page-${sNum} .slidev-layout (${vpLabel})`],
          stageRects: null,
        };
      }

      const layoutRect = layout.getBoundingClientRect();
      const rawText = layout.innerText || "";

      // 1. Detectar componentes Vue o HTML literal sin renderizar
      const rawHtmlPatterns = [
        "<code",
        "</code>",
        "<div",
        "</div>",
        "<span",
        "<QrAccessModal",
        "<CoverHeroGraphic",
        "<EncapsulationShowcase",
        "<LabLaunchpad",
        "<ParadigmShiftVisualizer",
        "<SoftwareCrisisDiagram",
        "<HistoryTimeline",
        "<ClassAnatomyStepper",
        "<ObjectInstancesDiagram",
        "<MessagePassingShowcase",
        "<AbstractionContractSplit",
        "<InheritanceShowcase",
        "<CompositionVsInheritance",
        "<PolymorphismDispatch",
        "<SolidInteractiveMap",
        "<StrategyShowcase",
        "<AdapterDecoratorSplit",
        "<TradeoffsMatrix",
        "<ParadigmTriadComparison",
        "<ConclusionsSynthesis",
        "<BibliographyAndResources",
      ];
      for (const pat of rawHtmlPatterns) {
        if (rawText.includes(pat)) {
          issues.push(`HTML/Vue sin renderizar detectado ("${pat}") en slide ${sNum} step ${stNum}`);
        }
      }

      // 2. Verificar que todos los elementos visibles quepan dentro de .slidev-layout
      const selectors =
        "h1, h2, h3, p, li, pre, code, button, a, header, footer, section, article, nav, svg, table";
      const descendants = Array.from(layout.querySelectorAll(selectors));

      for (const el of descendants) {
        const style = window.getComputedStyle(el);
        if (
          style.display === "none" ||
          style.visibility === "hidden" ||
          parseFloat(style.opacity) === 0
        ) {
          continue;
        }
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) continue;

        const tol = 2.0;
        if (
          r.left < layoutRect.left - tol ||
          r.right > layoutRect.right + tol ||
          r.top < layoutRect.top - tol ||
          r.bottom > layoutRect.bottom + tol
        ) {
          const cls = typeof el.className === "string" ? el.className : "";
          issues.push(
            `Desborde fuera de diapositiva (${vpLabel} s${sNum}:${stNum}): <${el.tagName.toLowerCase()} class="${cls}"> rect=${JSON.stringify(
              {
                l: Math.round(r.left),
                t: Math.round(r.top),
                r: Math.round(r.right),
                b: Math.round(r.bottom),
              }
            )} vs slide=${JSON.stringify({
              l: Math.round(layoutRect.left),
              t: Math.round(layoutRect.top),
              r: Math.round(layoutRect.right),
              b: Math.round(layoutRect.bottom),
            })}`
          );
        }
      }

      // 2b. Verificar que todo <text> dentro de <svg> quepa dentro del propio <svg>
      const svgs = Array.from(layout.querySelectorAll("svg"));
      for (const svg of svgs) {
        const sr = svg.getBoundingClientRect();
        if (sr.width === 0 || sr.height === 0) continue;
        for (const tEl of Array.from(svg.querySelectorAll("text"))) {
          const tr = tEl.getBoundingClientRect();
          if (tr.width === 0 || tr.height === 0) continue;
          if (
            tr.left < sr.left - 3 ||
            tr.right > sr.right + 3 ||
            tr.top < sr.top - 3 ||
            tr.bottom > sr.bottom + 3
          ) {
            issues.push(
              `Texto SVG fuera de su <svg> (${vpLabel} s${sNum}:${stNum}): "${tEl.textContent?.trim()}"`
            );
          }
        }
      }

      // 3. Verificar desborde interno (scrollWidth / scrollHeight) en tarjetas y paneles de código
      const boxSelector = [
        ".py-code-panel",
        ".py-code-panel__pre",
        ".encap-code-panel",
        ".encap-pre",
        ".encap-card",
        ".mode-card",
        ".poo-slide-header",
        ".b1-card",
        ".sc-card",
        ".tl-card",
        ".anat-card",
        ".oi-svg-card",
        ".oi-side-card",
        ".mp-card",
        ".abs-card",
        ".inh-card",
        ".ci-card",
        ".poly-card",
        ".sol-card",
        ".str-card",
        ".ad-card",
        ".to-card",
        ".tri-card",
        ".syn-card",
        ".bib-card",
      ].join(", ");

      const boxContainers = Array.from(layout.querySelectorAll(boxSelector));
      for (const box of boxContainers) {
        const clsName = (box.className || "").toString().split(" ")[0] || box.tagName;
        if (box.scrollWidth > box.clientWidth + 2) {
          issues.push(
            `Desborde horizontal interno (${vpLabel} s${sNum}:${stNum}) en .${clsName} (${box.scrollWidth}px > ${box.clientWidth}px)`
          );
        }
        if (box.scrollHeight > box.clientHeight + 2) {
          issues.push(
            `Desborde vertical interno (${vpLabel} s${sNum}:${stNum}) en .${clsName} (${box.scrollHeight}px > ${box.clientHeight}px)`
          );
        }
      }

      // 4. Detectar superposiciones no intencionales entre hermanos directos
      const allParents = [
        layout,
        ...Array.from(layout.querySelectorAll("div, section, header, footer, nav, article")),
      ];
      for (const parent of allParents) {
        const children = Array.from(parent.children).filter((ch) => {
          const st = window.getComputedStyle(ch);
          return (
            st.display !== "none" &&
            st.display !== "inline" &&
            st.visibility !== "hidden" &&
            parseFloat(st.opacity) > 0.05 &&
            st.position !== "fixed" &&
            st.position !== "absolute"
          );
        });

        for (let i = 0; i < children.length; i++) {
          for (let j = i + 1; j < children.length; j++) {
            const a = children[i].getBoundingClientRect();
            const b = children[j].getBoundingClientRect();
            const xOverlap = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left));
            const yOverlap = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
            if (xOverlap > 1.5 && yOverlap > 1.5) {
              issues.push(
                `Superposición entre hermanos (${vpLabel} s${sNum}:${stNum}): <${children[
                  i
                ].tagName.toLowerCase()}> y <${children[j].tagName.toLowerCase()}> (${Math.round(
                  xOverlap
                )}x${Math.round(yOverlap)}px)`
              );
            }
          }
        }
      }

      // 5. Capturar geometría para validar estabilidad en animaciones (CLS = 0)
      const headerEl = layout.querySelector(".poo-slide-header");
      const stageEl =
        layout.querySelector(".poo-code-explain__full > *") ||
        layout.querySelector(".poo-lab-entry__stage > *") ||
        layout.querySelector(".poo-conclusions__body > *");
      const codeEl = layout.querySelector(".py-code-panel, .encap-code-panel");

      const stageRects = {};
      if (headerEl) {
        const r = headerEl.getBoundingClientRect();
        stageRects.header = { x: r.x, y: r.y, w: r.width, h: r.height };
      }
      if (stageEl) {
        const r = stageEl.getBoundingClientRect();
        stageRects.stage = { x: r.x, y: r.y, w: r.width, h: r.height };
      }
      if (codeEl) {
        const r = codeEl.getBoundingClientRect();
        stageRects.code = { x: r.x, y: r.y, w: r.width, h: r.height };
      }

      return {
        ok: issues.length === 0,
        issues,
        stageRects: Object.keys(stageRects).length > 0 ? stageRects : null,
      };
    },
    { sNum: slideNum, stNum: stepNum, vpLabel: viewportLabel }
  );
}

async function runAudit() {
  const { server, baseUrl } = await startStaticServer(distDir);
  console.log(`[audit] Servidor estático activo en ${baseUrl}`);

  const browser = await chromium.launch({ channel: "chrome", headless: true });
  const report = {
    summary: {
      slidesAudited: SLIDE_SPECS.length,
      desktopStatesAudited: 0,
      desktopFailures: 0,
      mobileViewportsAudited: 0,
      labsAudited: 0,
    },
    desktopIssues: [],
    animationShifts: [],
    mobileGuide: [],
    labsWasm: [],
    consoleErrors: [],
    allPassed: true,
  };

  try {
    // =========================================================================
    // A. AUDITORÍA GEOMÉTRICA DE LAS 23 DIAPOSITIVAS EN 3 RESOLUCIONES DESKTOP
    // =========================================================================
    const desktopViewports = [
      { width: 1366, height: 768, label: "1366x768" },
      { width: 1920, height: 1080, label: "1920x1080" },
      { width: 1280, height: 720, label: "1280x720" },
    ];

    for (const vp of desktopViewports) {
      console.log(`[audit] Auditando 23 diapositivas en resolución ${vp.label}...`);
      const context = await browser.newContext({
        viewport: { width: vp.width, height: vp.height },
      });
      const page = await context.newPage();

      page.on("console", (msg) => {
        if (msg.type() === "error") {
          report.consoleErrors.push(`[slides ${vp.label}] ${msg.text()}`);
        }
      });
      page.on("pageerror", (err) => {
        report.consoleErrors.push(`[slides pageerror ${vp.label}] ${err.message}`);
      });

      for (const spec of SLIDE_SPECS) {
        await page.goto(`${baseUrl}/${spec.slide}`, { waitUntil: "domcontentloaded" });
        await page.waitForSelector(`.slidev-page-${spec.slide} .slidev-layout`, {
          state: "visible",
          timeout: 15000,
        });
        await page.waitForTimeout(420);

        const rectsHistory = [];

        for (let step = 0; step <= spec.clicks; step++) {
          if (step > 0) {
            await page.keyboard.press("ArrowRight");
            await page.waitForTimeout(340);
          }

          const res = await auditSlideGeometry(page, spec.slide, step, vp.label);
          report.summary.desktopStatesAudited += 1;

          if (res.stageRects) {
            rectsHistory.push({ step, rects: res.stageRects });
          }

          // Guardar capturas de referencia en 1366x768 (paso inicial y paso final) o ante cualquier fallo
          const shouldSaveReference =
            (vp.label === "1366x768" && (step === 0 || step === spec.clicks)) ||
            (vp.label !== "1366x768" && step === spec.clicks && [1, 4, 6, 13, 15, 20, 23].includes(spec.slide));

          if (shouldSaveReference || !res.ok) {
            const prefix = res.ok ? "slide" : "FAIL";
            const shotPath = path.join(
              shotsSubDir,
              `${prefix}_${vp.label}_s${String(spec.slide).padStart(2, "0")}_step${step}.png`
            );
            await page.screenshot({ path: shotPath });
          }

          if (!res.ok) {
            report.summary.desktopFailures += 1;
            report.desktopIssues.push({
              viewport: vp.label,
              slide: spec.slide,
              name: spec.name,
              step,
              issues: res.issues,
            });
          }
        }

        // Verificar estabilidad de contenedores entre pasos de animación (CLS <= 1.0px)
        if (rectsHistory.length > 1) {
          const base = rectsHistory[0].rects;
          for (let idx = 1; idx < rectsHistory.length; idx++) {
            const cur = rectsHistory[idx].rects;
            const diffs = [];
            for (const key of ["header", "stage"]) {
              if (base[key] && cur[key]) {
                diffs.push(
                  Math.abs(cur[key].x - base[key].x),
                  Math.abs(cur[key].y - base[key].y),
                  Math.abs(cur[key].w - base[key].w),
                  Math.abs(cur[key].h - base[key].h)
                );
              }
            }
            const maxDiff = diffs.length > 0 ? Math.max(...diffs) : 0;
            if (maxDiff > 1.0) {
              report.summary.desktopFailures += 1;
              report.animationShifts.push({
                viewport: vp.label,
                slide: spec.slide,
                step: rectsHistory[idx].step,
                maxDiffPx: Number(maxDiff.toFixed(2)),
              });
            }
          }
        }

        // Probar modal QR en la portada en 1366x768
        if (vp.label === "1366x768" && spec.slide === 1) {
          await page.click('.slidev-page-1 button:has-text("Acceso QR")');
          await page.waitForSelector(".qr-dialog svg", { state: "visible" });
          await page.waitForTimeout(250);
          await page.screenshot({
            path: path.join(shotsSubDir, "slide_1366x768_s01_qr_modal.png"),
          });
          await page.click('.qr-dialog button[aria-label="Cerrar ventana QR"]');
          await page.waitForTimeout(200);
        }
      }

      await context.close();
    }

    // =========================================================================
    // B. AUDITORÍA DE GUÍA DE LECTURA MÓVIL (375x812, 390x844, 768x1024)
    // =========================================================================
    const mobileViewports = [
      { width: 375, height: 812, label: "375x812" },
      { width: 390, height: 844, label: "390x844" },
      { width: 768, height: 1024, label: "768x1024" },
    ];

    for (const vp of mobileViewports) {
      console.log(`[audit] Auditando Guía Móvil en ${vp.label}...`);
      const context = await browser.newContext({
        viewport: { width: vp.width, height: vp.height },
      });
      const page = await context.newPage();

      page.on("console", (msg) => {
        if (msg.type() === "error") {
          report.consoleErrors.push(`[guia ${vp.label}] ${msg.text()}`);
        }
      });

      await page.goto(`${baseUrl}/guia/index.html`, { waitUntil: "networkidle" });
      await page.waitForTimeout(350);

      // Abrir los bloques desplegables <details> para verificar que tampoco desborden abiertos
      await page.evaluate(() => {
        document.querySelectorAll("details").forEach((d) => {
          d.open = true;
        });
      });
      await page.waitForTimeout(200);

      const shot = path.join(shotsSubDir, `guia_mobile_${vp.label}.png`);
      await page.screenshot({ path: shot, fullPage: false });

      const check = await page.evaluate(() => {
        const issues = [];
        if (document.documentElement.scrollWidth > window.innerWidth + 1) {
          issues.push(
            `Desborde horizontal en guía móvil: scrollWidth=${document.documentElement.scrollWidth} > innerWidth=${window.innerWidth}`
          );
        }
        const touchTargets = Array.from(document.querySelectorAll(".btn, .toc-link"));
        for (const btn of touchTargets) {
          const r = btn.getBoundingClientRect();
          if (r.height < 42) {
            issues.push(
              `Área táctil insuficiente (${Math.round(r.height)}px) en "${btn.textContent?.trim()}"`
            );
          }
        }
        const labLinks = Array.from(document.querySelectorAll('a[href*="/labs/"]'));
        if (labLinks.length < 8) {
          issues.push(`Se esperaban 8 enlaces a laboratorios (4 run + 4 edit), encontrados: ${labLinks.length}`);
        }
        return { ok: issues.length === 0, issues, labLinksCount: labLinks.length };
      });

      report.summary.mobileViewportsAudited += 1;
      report.mobileGuide.push({ viewport: vp.label, ...check, screenshot: shot });
      await context.close();
    }

    // =========================================================================
    // C. AUDITORÍA FUNCIONAL PYODIDE (WASM) EN LOS 4 LABORATORIOS PYTHON
    // =========================================================================
    const labChecks = [
      {
        slug: "01-encapsulamiento",
        expectedTexts: ['cuenta["saldo"] = -$15,000.00', "cuenta.saldo = $30,000.00"],
        testSwitchToggleText: "Saldo Bruno Díaz",
      },
      {
        slug: "02-herencia-polimorfismo",
        expectedTexts: ["Despacho Dinámico Activo", "Facturación Total del Lote", "EnvioRefrigerado"],
        testSwitchToggleText: null,
      },
      {
        slug: "03-patron-strategy",
        expectedTexts: [
          "Estrategia Delegada",
          "Intercambio dinámico sobre el mismo Pedido",
          "Beneficio Estudiante",
        ],
        testSwitchToggleText: null,
      },
      {
        slug: "04-comparacion-paradigmas",
        expectedTexts: ["Verificación de equivalencia", "EXACTA", "Orientado a Objetos"],
        testSwitchToggleText: null,
      },
    ];

    for (const lab of labChecks) {
      console.log(`[audit] Ejecutando Pyodide WASM en ${lab.slug} (modo run)...`);
      const labCtx = await browser.newContext({ viewport: { width: 1366, height: 768 } });
      const labPage = await labCtx.newPage();

      labPage.on("pageerror", (err) => {
        report.consoleErrors.push(`[${lab.slug} run pageerror] ${err.message}`);
      });

      await labPage.goto(`${baseUrl}/labs/${lab.slug}/run/index.html`, {
        waitUntil: "domcontentloaded",
      });

      await labPage.waitForFunction(
        (texts) => {
          const lower = document.body.innerText.toLowerCase();
          return texts.every((t) => lower.includes(t.toLowerCase()));
        },
        lab.expectedTexts,
        { timeout: 90000 }
      );
      await labPage.waitForTimeout(500);

      const desktopShot = path.join(shotsSubDir, `lab_${lab.slug}_run_1366x768.png`);
      await labPage.screenshot({ path: desktopShot });

      let reactiveVerified = false;
      if (lab.testSwitchToggleText) {
        const sw = labPage.locator('[role="switch"]').first();
        await sw.click();
        await labPage.waitForFunction(
          (txt) => !document.body.innerText.includes(txt),
          lab.testSwitchToggleText,
          { timeout: 15000 }
        );
        await sw.click();
        await labPage.waitForFunction(
          (txt) => document.body.innerText.includes(txt),
          lab.testSwitchToggleText,
          { timeout: 15000 }
        );
        reactiveVerified = true;
      }

      // Verificar ausencia de desborde horizontal en móvil 375x812
      await labPage.setViewportSize({ width: 375, height: 812 });
      await labPage.waitForTimeout(350);
      const mobileOverflow = await labPage.evaluate(() => {
        const sw = document.documentElement.scrollWidth;
        const iw = window.innerWidth;
        return { sw, iw, ok: sw <= iw + 2 };
      });
      const mobileShot = path.join(shotsSubDir, `lab_${lab.slug}_run_375x812.png`);
      await labPage.screenshot({ path: mobileShot });

      report.summary.labsAudited += 1;
      report.labsWasm.push({
        slug: lab.slug,
        mode: "run",
        ok: mobileOverflow.ok,
        pyodideExecuted: true,
        reactiveVerified,
        mobileCheck375: mobileOverflow,
        issues: mobileOverflow.ok
          ? []
          : [`Desborde horizontal en ${lab.slug} móvil: ${mobileOverflow.sw} > ${mobileOverflow.iw}`],
        screenshot: desktopShot,
      });

      await labCtx.close();
    }

    // Verificar modo editable (Sandbox CodeMirror + auto-instantiation) en Lab 03 (Strategy)
    console.log("[audit] Ejecutando Pyodide WASM en 03-patron-strategy (modo edit)...");
    const editCtx = await browser.newContext({ viewport: { width: 1366, height: 768 } });
    const editPage = await editCtx.newPage();

    editPage.on("pageerror", (err) => {
      report.consoleErrors.push(`[03-patron-strategy edit pageerror] ${err.message}`);
    });

    await editPage.goto(`${baseUrl}/labs/03-patron-strategy/edit/index.html`, {
      waitUntil: "domcontentloaded",
    });

    await editPage.waitForFunction(
      () => {
        const lower = document.body.innerText.toLowerCase();
        return (
          lower.includes("estrategia delegada") &&
          lower.includes("convenio docente / investigador")
        );
      },
      null,
      { timeout: 90000 }
    );
    await editPage.waitForTimeout(500);

    const editorCount = await editPage.locator(".cm-editor").count();
    const editShot = path.join(shotsSubDir, "lab_03-patron-strategy_edit_1366x768.png");
    await editPage.screenshot({ path: editShot });

    report.summary.labsAudited += 1;
    report.labsWasm.push({
      slug: "03-patron-strategy",
      mode: "edit",
      ok: editorCount >= 3,
      pyodideExecuted: true,
      codeCellsRendered: editorCount,
      issues:
        editorCount >= 3
          ? []
          : [`Se esperaban >= 3 celdas Python editables, se encontraron ${editorCount}`],
      screenshot: editShot,
    });

    await editCtx.close();
  } finally {
    await browser.close();
    server.close();
  }

  if (
    report.desktopIssues.length > 0 ||
    report.animationShifts.length > 0 ||
    report.mobileGuide.some((m) => !m.ok) ||
    report.labsWasm.some((l) => !l.ok) ||
    report.consoleErrors.length > 0
  ) {
    report.allPassed = false;
  }

  const reportJsonPath = path.join(outDir, "visual_audit_fase2_results.json");
  fs.writeFileSync(reportJsonPath, JSON.stringify(report, null, 2), "utf8");
  console.log(JSON.stringify(report, null, 2));

  if (!report.allPassed) {
    process.exitCode = 1;
  }
}

runAudit();
