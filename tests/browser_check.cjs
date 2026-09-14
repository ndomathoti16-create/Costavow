// Run against two local previews; see docs/DEVELOPMENT.md. No production JS is shipped.
const assert = require('node:assert/strict');
const { mkdir } = require('node:fs/promises');
const { chromium } = require('playwright');
const appURL = 'http://127.0.0.1:8527';
const siteURL = 'http://127.0.0.1:8528';
const widths = [320, 390, 768, 1024, 1440, 1920];

async function fits(page, label) {
  const failures = await page.evaluate(() => {
    const issues = [];
    for (const e of [document.documentElement, ...document.querySelectorAll('[data-testid="stMain"]')]) {
      if (e.scrollWidth > e.clientWidth + 2) issues.push(`page overflow ${e.scrollWidth}/${e.clientWidth}`);
    }
    for (const e of document.querySelectorAll('.metrora-driver-row,.metrora-decision-row,.metrora-report-answers article,.metrora-source-strip,.costavow-scenario')) {
      const box = e.getBoundingClientRect();
      if (box.width && (box.left < -1 || box.right > innerWidth + 1)) issues.push(`offscreen ${e.className}`);
    }
    for (const row of document.querySelectorAll('.metrora-driver-row[open]')) {
      const head = row.querySelector('.metrora-driver-head').getBoundingClientRect();
      const body = row.querySelector('.metrora-driver-body').getBoundingClientRect();
      if (head.width < 180 || head.bottom > body.top + 1) issues.push('driver heading overlaps evidence');
      for (const cell of row.querySelectorAll('.metrora-driver-body > div')) {
        const label = cell.querySelector('small')?.getBoundingClientRect();
        const value = cell.querySelector('strong,p')?.getBoundingClientRect();
        if (label && value && label.bottom > value.top) issues.push('driver label overlaps value');
      }
    }
    for (const e of document.querySelectorAll('[data-testid="stMetricValue"] > div,[data-testid="stMetricLabel"] [data-testid="stMarkdownContainer"]')) {
      if (e.scrollWidth > e.clientWidth + 2) issues.push(`truncated metric ${e.textContent}`);
    }
    for (const chart of document.querySelectorAll('[data-testid="stPlotlyChart"]')) {
      const box = chart.getBoundingClientRect();
      if (!box.width || !box.height) continue;
      const title = chart.querySelector('.gtitle')?.getBoundingClientRect();
      if (title && (title.left < box.left || title.right > box.right)) issues.push('clipped chart title');
      const legend = chart.querySelector('.legend')?.getBoundingClientRect();
      const axis = chart.querySelector('.xtitle')?.getBoundingClientRect();
      if (legend && axis && legend.left < axis.right && legend.right > axis.left && legend.top < axis.bottom - 1 && legend.bottom > axis.top + 1) issues.push('chart axis title overlaps legend');
    }
    return issues;
  });
  assert.deepEqual(failures, [], label);
}

(async () => {
  await mkdir('build/browser-checks', { recursive: true });
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.COSTAVOW_BROWSER_PATH ? { executablePath: process.env.COSTAVOW_BROWSER_PATH } : {}),
  });
  const errors = [];
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, reducedMotion: 'reduce' });
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(siteURL);
    await page.locator('.workspace-preview img').waitFor();
    assert.equal(await page.locator('h1').count(), 1);
    assert.equal(await page.locator('script').count(), 0);
    await page.keyboard.press('Tab');
    assert.equal(await page.locator(':focus').innerText(), 'Skip to content');
    await page.keyboard.press('Enter');
    for (const width of widths) {
      await page.setViewportSize({ width, height: 1000 });
      await fits(page, `public site at ${width}`);
      assert(await page.locator('img').evaluateAll(images => images.every(img => img.complete && img.naturalWidth > 0)));
      const targets = await page.locator('a,summary').evaluateAll(elements => elements.filter(e => {
        const r = e.getBoundingClientRect();
        return r.width && r.height && !e.classList.contains('skip-link') && r.height < 24;
      }).map(e => e.textContent));
      assert.deepEqual(targets, [], `small website controls at ${width}`);
      await page.screenshot({ path: `build/browser-checks/site-${width}.png`, fullPage: true });
    }
    for (const summary of await page.locator('summary').all()) {
      await summary.click();
      assert.equal(await summary.evaluate(e => e.parentElement.open), true);
      await summary.click();
    }
    for (const id of ['workflow', 'evidence', 'main']) assert.equal(await page.locator(`#${id}`).count(), 1);
    console.log('PASS public site: six widths, keyboard entry, image loads, native FAQs, targets');

    await page.setViewportSize({ width: 1440, height: 1000 });
    await page.goto(appURL);
    await page.getByRole('button', { name: 'Open hidden future risk', exact: true }).waitFor();
    for (const width of widths) {
      await page.setViewportSize({ width, height: 1000 });
      await fits(page, `scenario chooser at ${width}`);
      if (width <= 900) {
        const cardWidths = await page.locator('.costavow-scenario').evaluateAll(cards => cards.map(e => e.getBoundingClientRect().width));
        assert(cardWidths.every(card => card >= width - 110), `scenario cards too narrow at ${width}`);
      }
      await page.screenshot({ path: `build/browser-checks/chooser-${width}.png` });
    }
    await page.getByRole('button', { name: 'Open hidden future risk', exact: true }).click();
    await page.getByText('Current window spend', { exact: true }).waitFor();
    await page.setViewportSize({ width: 1440, height: 1000 });
    const labels = await page.locator('.st-key-workspace-navigation button p').evaluateAll(es => es.map(e => ({width:e.clientWidth,height:e.clientHeight})));
    assert(labels.every(e => e.width > 100 && e.height < 35), 'sidebar navigation labels must fit on one line');
    const destinations = ['Overview', 'Explore spend', 'Forecast & alerts', 'Decisions', 'Reports & exports', 'Data settings'];
    for (const destination of destinations) {
      await page.setViewportSize({ width: 1440, height: 1000 });
      await page.keyboard.press(`Control+Alt+${destinations.indexOf(destination) + 1}`);
      const heading = { 'Explore spend': 'Spend explorer', Decisions: 'Decision register' }[destination] || destination;
      await page.getByRole('heading', { name: heading, exact: true }).waitFor();
      await page.locator('[data-test-script-state="notRunning"]').waitFor();
      assert.equal(await page.locator('[data-testid="stException"]').count(), 0, destination);
      assert.equal(await page.locator('[data-testid="stFileUploader"]').count(), 0, destination);
      assert.equal(await page.locator('.metrora-topbar-mark img').evaluate(e => e.complete && e.naturalWidth > 0), true);
      const slug = destination.toLowerCase().replace(/[^a-z]+/g, '-');
      for (const width of widths) {
        await page.setViewportSize({ width, height: 1000 });
        // Plotly responds asynchronously to container resize.
        await page.waitForTimeout(300);
        await fits(page, `${destination} at ${width}`);
        if ([390, 1440].includes(width)) {
          await page.locator('.metrora-workspace-page-title').scrollIntoViewIfNeeded();
          await page.screenshot({ path: `build/browser-checks/${slug}-${width}.png` });
          const evidence = page.locator('.metrora-driver-row').first();
          if (await evidence.count()) {
            await evidence.locator('summary').click();
            await fits(page, `${destination} expanded evidence at ${width}`);
            await evidence.screenshot({ path: `build/browser-checks/${slug}-evidence-${width}.png` });
            await evidence.locator('summary').click();
          }
        }
      }
      console.log(`PASS ${destination}: six widths, readable evidence, complete metrics, no uploads`);
    }
    await page.setViewportSize({ width: 390, height: 844 });
    await page.keyboard.press('Control+Alt+3');
    await page.locator('[data-test-script-state="notRunning"]').waitFor();
    for (const name of ['Forecast', 'Anomalies', 'Budgets', 'Ownership', 'Unit economics', 'Governance']) {
      const tab = page.getByRole('tab', { name, exact: true });
      await tab.click();
      await page.locator('[data-test-script-state="notRunning"]').waitFor();
      for (const width of [320, 390, 768, 1440]) {
        await page.setViewportSize({ width, height: 1000 });
        await page.waitForTimeout(300);
        await fits(page, `planning tab ${name} at ${width}`);
      }
      const panel = page.getByRole('tabpanel', { name, exact: true });
      await panel.screenshot({ path: `build/browser-checks/plan-${name.replaceAll(' ', '-')}.png` });
    }
    await page.keyboard.press('Control+Alt+4');
    await page.locator('[data-test-script-state="notRunning"]').waitFor();
    const receipt = page.getByRole('button', { name: 'Download decision receipt (HTML)', exact: true });
    const [download] = await Promise.all([page.waitForEvent('download'), receipt.click()]);
    assert.equal(await download.failure(), null);
    await download.saveAs('build/browser-checks/decision-receipt.html');
    assert.deepEqual(errors, []);
    await page.keyboard.press('Control+Alt+5');
    await page.getByRole('button', { name: 'Download cleaned data (CSV)', exact: true }).waitFor();
    const [csv] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Download cleaned data (CSV)', exact: true }).click()]);
    assert.equal(await csv.failure(), null);
    await csv.saveAs('build/browser-checks/cleaned.csv');
    assert.deepEqual(errors, []);
    console.log('PASS native navigation shortcuts, decision receipt and deferred CSV export; no browser JavaScript errors');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
