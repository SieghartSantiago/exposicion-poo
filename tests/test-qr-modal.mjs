import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, "..");
const distDir = path.join(rootDir, "dist");
const outDir = path.join(rootDir, "tests", "qr_screenshots");
fs.mkdirSync(outDir, { recursive: true });

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
};

function startServer(basePrefix = "") {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const reqUrl = new URL(req.url || "/", "http://127.0.0.1");
      let pathname = decodeURIComponent(reqUrl.pathname);
      if (basePrefix && pathname.startsWith(basePrefix)) {
        pathname = pathname.slice(basePrefix.length);
      }
      if (pathname.endsWith("/")) pathname += "index.html";
      let filePath = path.join(distDir, pathname);
      if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
        const indexHtml = path.join(filePath, "index.html");
        if (fs.existsSync(indexHtml)) {
          filePath = indexHtml;
        } else {
          filePath = path.join(distDir, "index.html");
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
      resolve({ server, baseUrl: `http://127.0.0.1:${server.address().port}` });
    });
  });
}

const REQUIRED_VIEWPORTS = [
  { width: 320, height: 568, label: "320x568 (iPhone SE 1st)" },
  { width: 360, height: 800, label: "360x800 (Android Galaxy)" },
  { width: 375, height: 812, label: "375x812 (iPhone X/11/12 mini)" },
  { width: 390, height: 844, label: "390x844 (iPhone 12/13/14)" },
  { width: 412, height: 915, label: "412x915 (Pixel 7 / Galaxy S21)" },
  { width: 768, height: 1024, label: "768x1024 (iPad Portrait)" },
  { width: 1366, height: 768, label: "1366x768 (Laptop HD)" },
  { width: 1920, height: 1080, label: "1920x1080 (FHD Desktop)" },
  { width: 844, height: 390, label: "844x390 (Mobile Landscape)" },
];

async function runTestSuite() {
  const isGithubBuild = fs.existsSync(path.join(distDir, "index.html")) &&
    fs.readFileSync(path.join(distDir, "index.html"), "utf8").includes("/exposicion-poo/");
  const basePrefix = isGithubBuild ? "/exposicion-poo" : "";

  const { server, baseUrl } = await startServer(basePrefix);
  console.log(`[test:qr] Servidor de prueba en ${baseUrl}${basePrefix}`);

  const browser = await chromium.launch({ channel: "chrome", headless: true });
  const results = [];
  let allPassed = true;

  try {
    for (const vp of REQUIRED_VIEWPORTS) {
      console.log(`[test:qr] Evaluando: ${vp.label} (${vp.width}x${vp.height})...`);

      const context = await browser.newContext({
        viewport: { width: vp.width, height: vp.height },
        permissions: ["clipboard-read", "clipboard-write"],
      });
      const page = await context.newPage();

      const pageErrors = [];
      page.on("pageerror", (err) => {
        if (!err.message.includes("Wake Lock")) {
          pageErrors.push(err.message);
        }
      });
      page.on("console", (msg) => {
        if (msg.type() === "error" && !msg.text().includes("Wake Lock")) {
          pageErrors.push(msg.text());
        }
      });

      await page.goto(`${baseUrl}${basePrefix}/1`, { waitUntil: "domcontentloaded" });
      await page.waitForSelector('.slidev-page-1 button:has-text("Acceso QR")', { state: "visible" });
      await page.waitForTimeout(300);

      // 1. Abrir modal
      await page.click('.slidev-page-1 button:has-text("Acceso QR")');
      await page.waitForSelector(".qr-dialog", { state: "visible" });
      await page.waitForSelector(".qr-box svg", { state: "visible" });
      await page.waitForTimeout(250);

      // 2 & 3. Inspección geométrica en modo "Guía Móvil + Labs"
      const geomGuia = await page.evaluate(() => {
        const dialog = document.querySelector(".qr-dialog");
        const closeBtn = document.querySelector('.qr-dialog button[aria-label="Cerrar ventana QR"]');
        const qrBox = document.querySelector(".qr-box");
        const qrSvg = qrBox?.querySelector("svg");
        const modeSwitch = document.querySelector(".qr-mode-switch");
        const btnGuia = modeSwitch?.querySelectorAll("button")[0];
        const btnSlides = modeSwitch?.querySelectorAll("button")[1];
        const urlCode = document.querySelector(".qr-url-preview");
        const copyBtn = document.querySelector(".qr-url-row button");

        const vw = window.innerWidth;
        const vh = window.innerHeight;
        const scrollW = document.documentElement.scrollWidth;

        const dR = dialog.getBoundingClientRect();
        const cR = closeBtn.getBoundingClientRect();
        const qR = qrBox.getBoundingClientRect();
        const gR = btnGuia.getBoundingClientRect();
        const sR = btnSlides.getBoundingClientRect();
        const uR = urlCode.getBoundingClientRect();
        const cpR = copyBtn.getBoundingClientRect();

        const issues = [];

        if (scrollW > vw + 1) {
          issues.push(`Desbordamiento horizontal en documento: scrollWidth=${scrollW} > vw=${vw}`);
        }
        if (dR.left < 0 || dR.right > vw + 1) {
          issues.push(`Modal desborda pantalla: left=${Math.round(dR.left)}, right=${Math.round(dR.right)} vs vw=${vw}`);
        }
        if (cR.right > dR.right + 1) {
          issues.push(`Botón Cerrar sobresale del modal: closeRight=${Math.round(cR.right)} > modalRight=${Math.round(dR.right)}`);
        }
        if (cR.top < 0 || cR.bottom > vh) {
          issues.push(`Botón Cerrar cortado verticalmente`);
        }

        const qrRatioDiff = Math.abs(qR.width - qR.height);
        if (qrRatioDiff > 1.5) {
          issues.push(`QR no es cuadrado: width=${Math.round(qR.width)} != height=${Math.round(qR.height)}`);
        }

        if (vw <= 640 && vh > 520) {
          const dialogCenter = (dR.left + dR.right) / 2;
          const qrCenter = (qR.left + qR.right) / 2;
          if (Math.abs(dialogCenter - qrCenter) > 4) {
            issues.push(`QR no centrado horizontalmente en móvil`);
          }
        }

        if (uR.right > dR.right + 1) {
          issues.push(`URL preview desborda modal: urlRight=${Math.round(uR.right)} > modalRight=${Math.round(dR.right)}`);
        }
        if (cpR.right > dR.right + 1 || cpR.left < dR.left - 1) {
          issues.push(`Botón Copiar enlace desborda modal`);
        }
        if (cpR.height < 36) {
          issues.push(`Botón Copiar enlace con área táctil insuficiente: ${Math.round(cpR.height)}px`);
        }

        return {
          issues,
          urlText: urlCode?.textContent?.trim(),
          qrSvgHtml: qrSvg?.outerHTML,
          dialogRect: { x: dR.x, y: dR.y, w: dR.width, h: dR.height },
          closeRect: { x: cR.x, y: cR.y, w: cR.width, h: cR.height },
          qrRect: { x: qR.x, y: qR.y, w: qR.width, h: qR.height },
        };
      });

      if (!geomGuia.urlText.includes("guia/index.html")) {
        geomGuia.issues.push(`URL en modo Guía no contiene 'guia/index.html'`);
      }

      const shotGuiaPath = path.join(outDir, `qr_${vp.width}x${vp.height}_guia.png`);
      await page.screenshot({ path: shotGuiaPath });

      // 4. Seleccionar «Diapositivas 16:9»
      await page.click('.qr-mode-switch button:has-text("Diapositivas 16:9")');
      await page.waitForTimeout(250);

      // 5, 6, 7. Comprobaciones en modo Diapositivas
      const geomSlides = await page.evaluate((prevGuiaH) => {
        const dialog = document.querySelector(".qr-dialog");
        const closeBtn = document.querySelector('.qr-dialog button[aria-label="Cerrar ventana QR"]');
        const qrBox = document.querySelector(".qr-box");
        const qrSvg = qrBox?.querySelector("svg");
        const urlCode = document.querySelector(".qr-url-preview");
        const copyBtn = document.querySelector(".qr-url-row button");

        const vw = window.innerWidth;
        const scrollW = document.documentElement.scrollWidth;

        const dR = dialog.getBoundingClientRect();
        const cR = closeBtn.getBoundingClientRect();
        const uR = urlCode.getBoundingClientRect();
        const cpR = copyBtn.getBoundingClientRect();

        const issues = [];

        if (scrollW > vw + 1) issues.push(`Desbordamiento horizontal en Slides`);
        if (cR.right > dR.right + 1) issues.push(`Botón Cerrar sobresale en Slides`);
        if (uR.right > dR.right + 1) issues.push(`URL preview desborda en Slides`);
        if (cpR.right > dR.right + 1) issues.push(`Botón Copiar desborda en Slides`);

        const heightJump = Math.abs(dR.height - prevGuiaH);
        if (heightJump > 4.0) {
          issues.push(`Salto brusco de altura al alternar: diff=${heightJump.toFixed(1)}px`);
        }

        return {
          issues,
          urlText: urlCode?.textContent?.trim(),
          qrSvgHtml: qrSvg?.outerHTML,
        };
      }, geomGuia.dialogRect.h);

      if (geomSlides.urlText.includes("guia/index.html")) {
        geomSlides.issues.push(`URL en Slides no debe tener 'guia/index.html'`);
      }

      if (geomGuia.qrSvgHtml === geomSlides.qrSvgHtml) {
        geomSlides.issues.push(`QR no cambió al alternar opciones`);
      }

      const shotSlidesPath = path.join(outDir, `qr_${vp.width}x${vp.height}_slides.png`);
      await page.screenshot({ path: shotSlidesPath });

      // Probar botón de copia
      await page.click('.qr-url-row button');
      await page.waitForTimeout(100);
      const copyBtnText = await page.evaluate(() => {
        return document.querySelector(".qr-url-row button")?.textContent?.trim();
      });
      if (!copyBtnText?.includes("Copiado")) {
        geomSlides.issues.push(`Feedback de copia inesperado: "${copyBtnText}"`);
      }

      // Probar cierre de modal
      await page.click('.qr-dialog button[aria-label="Cerrar ventana QR"]');
      await page.waitForTimeout(200);
      const isClosed = await page.evaluate(() => document.querySelector(".qr-dialog") === null);
      if (!isClosed) {
        geomSlides.issues.push(`El modal no se cerró correctamente`);
      }

      const allIssues = [...geomGuia.issues, ...geomSlides.issues, ...pageErrors];
      const passed = allIssues.length === 0;
      if (!passed) allPassed = false;

      results.push({ viewport: vp.label, passed, issues: allIssues });
      console.log(`[test:qr] ${vp.label}: ${passed ? "OK" : "FALLÓ (" + allIssues.join("; ") + ")"}`);

      await context.close();
    }
  } finally {
    await browser.close();
    server.close();
  }

  console.log(`\n[test:qr] Resultado global: ${allPassed ? "TODAS LAS PRUEBAS PASARON EXITOSAMENTE" : "HUBO FALLOS"}`);
  if (!allPassed) process.exitCode = 1;
}

runTestSuite();
