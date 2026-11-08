import { copyFileSync, existsSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const distDir = path.resolve(__dirname, "..", "dist");

if (existsSync(distDir)) {
  // Evita que Jekyll en GitHub Pages ignore carpetas con guiones bajos (_assets, etc.)
  writeFileSync(path.join(distDir, ".nojekyll"), "", "utf8");

  // Fallback SPA para GitHub Pages cuando se navega directamente a rutas de diapositivas (/2, /3...)
  const indexHtml = path.join(distDir, "index.html");
  const notFoundHtml = path.join(distDir, "404.html");
  if (existsSync(indexHtml) && !existsSync(notFoundHtml)) {
    copyFileSync(indexHtml, notFoundHtml);
  }

  // Configuración de headers MIME y SPA para Cloudflare Pages
  const headersContent = `/*.wasm
  Content-Type: application/wasm
  Cache-Control: public, max-age=31536000, immutable
`;
  writeFileSync(path.join(distDir, "_headers"), headersContent, "utf8");

  console.log("[postbuild] Artefactos estáticos configurados (.nojekyll, 404.html, _headers).");
}
