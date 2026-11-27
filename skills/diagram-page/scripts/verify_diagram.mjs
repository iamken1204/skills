#!/usr/bin/env node
// Renders a diagram page in Chromium for each language, measures every visible SVG text,
// reports layout faults, and saves screenshots for visual review.
//
// usage: node verify_diagram.mjs <page.html> [--output-dir <dir>]
// exit status: 0 no errors, 1 errors found, 2 could not run

import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { existsSync, mkdirSync, readdirSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const LANGUAGES = ['en', 'tw'];
const VIEWPORT = { width: 1456, height: 1000 };
const PADDING = 4; // minimum gap between text and the edge of the box that holds it

function loadChromium() {
  const require = createRequire(import.meta.url);
  const candidates = ['playwright', 'playwright-core'];
  try {
    const globalRoot = execSync('npm root -g', { encoding: 'utf8' }).trim();
    candidates.push(
      path.join(globalRoot, 'playwright'),
      path.join(globalRoot, 'playwright-core'),
      path.join(globalRoot, '@playwright/cli/node_modules/playwright-core'),
    );
  } catch {
    // npm is absent; only locally installed packages can be tried
  }
  for (const candidate of candidates) {
    try {
      return require(candidate).chromium;
    } catch {
      // try the next location
    }
  }
  throw new Error('playwright is not installed; run: npm install -g playwright-core');
}

// Headless-shell builds already in the Playwright cache, newest first.
function cachedHeadlessShells() {
  const cache = process.env.PLAYWRIGHT_BROWSERS_PATH
    ?? (process.platform === 'darwin' ? path.join(os.homedir(), 'Library/Caches/ms-playwright')
      : process.platform === 'win32' ? path.join(os.homedir(), 'AppData/Local/ms-playwright')
        : path.join(os.homedir(), '.cache/ms-playwright'));
  if (!existsSync(cache)) return [];
  const binary = process.platform === 'win32' ? 'chrome-headless-shell.exe' : 'chrome-headless-shell';
  return readdirSync(cache)
    .filter((name) => name.startsWith('chromium_headless_shell-'))
    .sort((a, b) => Number(b.split('-')[1]) - Number(a.split('-')[1]))
    .flatMap((name) => readdirSync(path.join(cache, name))
      .map((platformDir) => path.join(cache, name, platformDir, binary)))
    .filter((file) => existsSync(file));
}

// The bundled browser first; if this Playwright release expects a build that is not
// downloaded, any cached headless shell instead.
async function launchBrowser(chromium) {
  try {
    return await chromium.launch();
  } catch (error) {
    for (const executablePath of cachedHeadlessShells()) {
      try {
        return await chromium.launch({ executablePath });
      } catch {
        // try the next cached build
      }
    }
    throw new Error(`${error.message.split('\n')[0]}\nrun: npx playwright install chromium-headless-shell`);
  }
}

function parseArguments(argv) {
  const args = { page: null, outputDir: null };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--output-dir') args.outputDir = argv[++i];
    else args.page = argv[i];
  }
  if (!args.page) throw new Error('usage: node verify_diagram.mjs <page.html> [--output-dir <dir>]');
  args.page = path.resolve(args.page);
  if (!existsSync(args.page)) throw new Error(`no such file: ${args.page}`);
  args.outputDir = path.resolve(args.outputDir ?? path.dirname(args.page));
  return args;
}

// Runs inside the page. Returns { errors, warnings } for the language shown now.
function inspectDiagram(padding) {
  const svg = document.querySelector('svg.diagram');
  if (!svg) return { errors: ['no svg.diagram on the page'], warnings: [] };
  const view = svg.viewBox.baseVal;
  const errors = [];
  const warnings = [];
  const visible = (el) => el.getClientRects().length > 0 && !el.closest('defs');
  const rectOf = (el) => {
    const b = el.getBBox();
    return { x: b.x, y: b.y, r: b.x + b.width, b: b.y + b.height };
  };
  const intersects = (a, b, slack = 0) =>
    a.x < b.r - slack && b.x < a.r - slack && a.y < b.b - slack && b.y < a.b - slack;
  const inside = (inner, outer, gap) =>
    inner.x >= outer.x + gap && inner.r <= outer.r - gap && inner.y >= outer.y + gap && inner.b <= outer.b - gap;
  const fmt = (r) => `[${Math.round(r.x)},${Math.round(r.y)} → ${Math.round(r.r)},${Math.round(r.b)}]`;

  const texts = [...svg.querySelectorAll('text')].filter(visible).map((el) => ({
    el, box: rectOf(el), label: el.textContent.trim(), badge: el.classList.contains('sk'),
  }));
  const frames = [...svg.querySelectorAll('rect')].filter(visible).map((el) => ({ el, box: rectOf(el) }))
    .filter((f) => f.box.r - f.box.x >= 30);
  const circles = [...svg.querySelectorAll('circle')].filter(visible).map((el) => rectOf(el));

  for (const t of texts) {
    if (!inside(t.box, { x: view.x, y: view.y, r: view.x + view.width, b: view.y + view.height }, 2)) {
      errors.push(`"${t.label}" ${fmt(t.box)} runs outside the viewBox`);
    }
  }
  for (let i = 0; i < texts.length; i++) {
    for (let j = i + 1; j < texts.length; j++) {
      if (intersects(texts[i].box, texts[j].box, 1)) {
        errors.push(`"${texts[i].label}" overlaps "${texts[j].label}" ${fmt(texts[i].box)}`);
      }
    }
  }
  // Text must sit wholly inside a frame or wholly outside it, never across its border.
  for (const t of texts) {
    if (t.badge) continue;
    for (const f of frames) {
      if (!intersects(t.box, f.box, 0.5)) continue;
      if (!inside(t.box, f.box, 0)) {
        errors.push(`"${t.label}" ${fmt(t.box)} crosses the border of the box ${fmt(f.box)}`);
      } else if (f.box.b - f.box.y >= 30 && !inside(t.box, f.box, padding)) {
        warnings.push(`"${t.label}" is within ${padding}px of the edge of the box ${fmt(f.box)}`);
      }
    }
  }
  // Wires: every path drawn with a stroke and only M/H/V/L commands.
  const segments = [];
  for (const p of svg.querySelectorAll('path')) {
    if (!visible(p) || p.closest('marker, pattern')) continue;
    const d = p.getAttribute('d') || '';
    if (/[^MHVL0-9.,\s-]/i.test(d) || /[a-z]/.test(d.replace(/[MHVL]/g, ''))) continue;
    let x = 0, y = 0;
    for (const [, cmd, args] of d.matchAll(/([MHVL])\s*([-0-9.,\s]+)/g)) {
      const n = args.trim().split(/[\s,]+/).map(Number);
      if (cmd === 'M') { x = n[0]; y = n[1]; continue; }
      const nx = cmd === 'H' ? n[0] : cmd === 'L' ? n[0] : x;
      const ny = cmd === 'V' ? n[0] : cmd === 'L' ? n[1] : y;
      segments.push({ x: Math.min(x, nx), y: Math.min(y, ny), r: Math.max(x, nx), b: Math.max(y, ny), end: { x: nx, y: ny }, hasMarker: p.hasAttribute('marker-end') });
      x = nx; y = ny;
    }
  }
  for (const t of texts) {
    if (t.badge) continue;
    const grown = { x: t.box.x - 2, y: t.box.y - 2, r: t.box.r + 2, b: t.box.b + 2 };
    for (const s of segments) {
      const line = { x: s.x - 0.8, y: s.y - 0.8, r: s.r + 0.8, b: s.b + 0.8 };
      if (intersects(grown, line)) {
        errors.push(`"${t.label}" ${fmt(t.box)} touches a wire ${fmt(s)}`);
        break;
      }
    }
  }
  // Step badges that collide with text.
  for (const c of circles) {
    for (const t of texts) {
      if (!t.badge && intersects(t.box, c, 0.5)) errors.push(`"${t.label}" overlaps a badge or dot ${fmt(c)}`);
    }
  }
  // An arrowhead should land on a box edge.
  const paths = [...svg.querySelectorAll('path[marker-end]')].filter(visible);
  for (const p of paths) {
    const len = p.getTotalLength();
    const tip = p.getPointAtLength(len);
    const touching = frames.some((f) => {
      const near = (v, lo, hi) => v >= lo - 4 && v <= hi + 4;
      const onVertical = (Math.abs(tip.x - f.box.x) <= 4 || Math.abs(tip.x - f.box.r) <= 4) && near(tip.y, f.box.y, f.box.b);
      const onHorizontal = (Math.abs(tip.y - f.box.y) <= 4 || Math.abs(tip.y - f.box.b) <= 4) && near(tip.x, f.box.x, f.box.r);
      return onVertical || onHorizontal;
    });
    if (!touching) warnings.push(`an arrow ending at (${Math.round(tip.x)},${Math.round(tip.y)}) does not land on a box edge`);
  }
  return { errors: [...new Set(errors)], warnings: [...new Set(warnings)] };
}

// Runs inside the page: every .en element in the diagram needs a .tw twin at the same place.
function inspectTranslations() {
  const svg = document.querySelector('svg.diagram');
  const key = (el) => `${el.tagName}@${el.getAttribute('x')},${el.getAttribute('y')}`;
  const chinese = new Set([...svg.querySelectorAll('.tw')].map(key));
  const english = new Set([...svg.querySelectorAll('.en')].map(key));
  const missing = [];
  for (const el of svg.querySelectorAll('.en')) if (!chinese.has(key(el))) missing.push(`no Chinese for "${el.textContent}" at ${key(el)}`);
  for (const el of svg.querySelectorAll('.tw')) if (!english.has(key(el))) missing.push(`no English for "${el.textContent}" at ${key(el)}`);
  const pageEn = document.querySelectorAll('main > :not(figure) .en, header .en').length;
  const pageTw = document.querySelectorAll('main > :not(figure) .tw, header .tw').length;
  if (pageEn !== pageTw) missing.push(`the page has ${pageEn} English and ${pageTw} Chinese blocks outside the diagram`);
  return missing;
}

async function main() {
  const args = parseArguments(process.argv.slice(2));
  const chromium = loadChromium();
  mkdirSync(args.outputDir, { recursive: true });
  const stem = path.basename(args.page, path.extname(args.page));
  const browser = await launchBrowser(chromium);
  let errorCount = 0;
  try {
    for (const scheme of ['light', 'dark']) {
      const context = await browser.newContext({ viewport: VIEWPORT, deviceScaleFactor: 2, colorScheme: scheme });
      const page = await context.newPage();
      await page.goto(pathToFileURL(args.page).href);
      if (scheme === 'light') {
        for (const problem of await page.evaluate(inspectTranslations)) {
          console.log(`ERROR  [both] ${problem}`);
          errorCount++;
        }
      }
      for (const language of LANGUAGES) {
        await page.click(`[data-set-lang="${language}"]`);
        await page.evaluate(() => document.fonts.ready);
        if (scheme === 'light') {
          const { errors, warnings } = await page.evaluate(inspectDiagram, PADDING);
          for (const e of errors) console.log(`ERROR  [${language}] ${e}`);
          for (const w of warnings) console.log(`WARN   [${language}] ${w}`);
          errorCount += errors.length;
        }
        const suffix = scheme === 'dark' ? '-dark' : '';
        const figure = path.join(args.outputDir, `${stem}-diagram-${language}${suffix}.png`);
        await page.locator('figure').screenshot({ path: figure });
        console.log(`saved  ${figure}`);
        if (scheme === 'light') {
          const full = path.join(args.outputDir, `${stem}-page-${language}.png`);
          await page.screenshot({ path: full, fullPage: true });
          console.log(`saved  ${full}`);
        }
      }
      await context.close();
    }
  } finally {
    await browser.close();
  }
  console.log(errorCount === 0 ? 'PASS   no layout errors' : `FAIL   ${errorCount} layout errors`);
  process.exit(errorCount === 0 ? 0 : 1);
}

main().catch((error) => {
  console.error(error.message);
  process.exit(2);
});
