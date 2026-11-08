import { execFileSync } from "node:child_process";
import {
  cpSync,
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, "..");
const labsSrcDir = path.join(rootDir, "labs");
const labsOutDir = path.join(rootDir, "public", "labs");

function buildChildEnv() {
  const venvDirs = [
    path.join(rootDir, ".venv", "Scripts"),
    path.join(rootDir, ".venv", "bin"),
  ].filter((dir) => existsSync(dir));

  const currentPath = process.env.PATH || process.env.Path || "";
  const mergedPath = [...venvDirs, currentPath].filter(Boolean).join(path.delimiter);

  return {
    ...process.env,
    PATH: mergedPath,
    Path: mergedPath,
  };
}

function resolveMarimoExecutable() {
  const candidates = [
    path.join(rootDir, ".venv", "Scripts", "marimo.exe"),
    path.join(rootDir, ".venv", "bin", "marimo"),
    "marimo",
  ];
  for (const candidate of candidates) {
    if (candidate === "marimo" || existsSync(candidate)) {
      return candidate;
    }
  }
  return "marimo";
}

function toSlug(filename) {
  return filename
    .replace(/^lab_/, "")
    .replace(/\.py$/, "")
    .replace(/_/g, "-");
}

function deduplicateSharedAssets(exportDir, sharedDir) {
  const localAssets = path.join(exportDir, "assets");
  const sharedAssets = path.join(sharedDir, "assets");
  const indexHtmlPath = path.join(exportDir, "index.html");

  if (!existsSync(localAssets) || !existsSync(indexHtmlPath)) {
    return;
  }

  mkdirSync(sharedAssets, { recursive: true });
  cpSync(localAssets, sharedAssets, { recursive: true });

  rmSync(localAssets, { recursive: true, force: true });

  const html = readFileSync(indexHtmlPath, "utf8")
    .replaceAll("./assets/", "../../shared/assets/")
    .replaceAll('"auto_instantiate": false', '"auto_instantiate": true')
    .replace(
      '"ai": {"allow_provider_config": true, "custom_providers": {}, "enabled": true',
      '"ai": {"allow_provider_config": false, "custom_providers": {}, "enabled": false'
    );
  writeFileSync(indexHtmlPath, html, "utf8");
}

function main() {
  const marimoBin = resolveMarimoExecutable();
  const childEnv = buildChildEnv();
  const labFiles = readdirSync(labsSrcDir)
    .filter((f) => /^lab_.*\.py$/.test(f))
    .sort();

  if (labFiles.length === 0) {
    console.log("[build-labs] No se encontraron archivos lab_*.py en labs/.");
    return;
  }

  rmSync(labsOutDir, { recursive: true, force: true });
  mkdirSync(labsOutDir, { recursive: true });
  const sharedDir = path.join(labsOutDir, "shared");

  for (const file of labFiles) {
    const slug = toSlug(file);

    console.log(`[build-labs] Verificando DAG de ${file}...`);
    execFileSync(marimoBin, ["check", file], {
      cwd: labsSrcDir,
      env: childEnv,
      stdio: "inherit",
    });

    const runDir = path.join(labsOutDir, slug, "run");
    const editDir = path.join(labsOutDir, slug, "edit");
    mkdirSync(runDir, { recursive: true });
    mkdirSync(editDir, { recursive: true });

    console.log(`[build-labs] Exportando ${slug} -> Modo Interactivo (run)...`);
    execFileSync(
      marimoBin,
      [
        "export",
        "html-wasm",
        file,
        "-o",
        runDir,
        "--mode",
        "run",
        "--no-show-code",
        "--no-sandbox",
        "-f",
      ],
      { cwd: labsSrcDir, env: childEnv, stdio: "inherit" }
    );
    deduplicateSharedAssets(runDir, sharedDir);

    console.log(`[build-labs] Exportando ${slug} -> Modo Laboratorio Editable (edit)...`);
    execFileSync(
      marimoBin,
      [
        "export",
        "html-wasm",
        file,
        "-o",
        editDir,
        "--mode",
        "edit",
        "--show-code",
        "--no-sandbox",
        "-f",
      ],
      { cwd: labsSrcDir, env: childEnv, stdio: "inherit" }
    );
    deduplicateSharedAssets(editDir, sharedDir);
  }

  console.log(
    `[build-labs] Compilación WASM finalizada (${labFiles.length} laboratorio(s), assets deduplicados en /labs/shared/).`
  );
}

main();
