// BeQuite tell sweep: paste into the browser console or a browser tool's JavaScript runner.
// Read-only. Returns measured values and the owner's design tells found on the rendered page.
(() => {
  const cs = (e) => getComputedStyle(e);
  const vis = [...document.querySelectorAll('body *')].filter((e) => e.getClientRects().length && cs(e).visibility !== 'hidden');
  const textEls = vis.filter((e) => [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1));
  const tally = (arr) => Object.entries(arr.reduce((m, v) => ((m[v] = (m[v] || 0) + 1), m), {})).sort((a, b) => b[1] - a[1]);
  const heads = textEls.filter((e) => /^H[1-3]$/.test(e.tagName));
  const bodyText = textEls.filter((e) => /^(P|LI|SPAN|A|TD)$/.test(e.tagName));
  const isGrad = (e) => cs(e).backgroundImage.includes('gradient');
  const hueOf = (c) => { const m = c.match(/\d+/g); if (!m) return null; const [r, g, b] = m.map(Number);
    const mx = Math.max(r, g, b), mn = Math.min(r, g, b); if (mx === mn) return null;
    let h = mx === r ? (g - b) / (mx - mn) : mx === g ? 2 + (b - r) / (mx - mn) : 4 + (r - g) / (mx - mn); return (h * 60 + 360) % 360; };
  const gradColors = vis.filter(isGrad).map((e) => (cs(e).backgroundImage.match(/rgba?\([^)]+\)|#[0-9a-f]{3,8}/gi) || []));
  const purpleBlue = gradColors.filter((cols) => { const hs = cols.map(hueOf).filter((h) => h !== null); return hs.some((h) => h >= 255 && h <= 290) && hs.some((h) => h >= 200 && h < 255); }).length;
  const tells = {
    gradientHeadlineText: heads.filter((e) => cs(e).webkitBackgroundClip === 'text' || cs(e).backgroundClip === 'text').length,
    purpleToBlueGradients: purpleBlue,
    numberedSectionLabels: textEls.filter((e) => /^0\d\b/.test(e.textContent.trim())).length,
    glassCards: vis.filter((e) => { const r = e.getBoundingClientRect(); return (cs(e).backdropFilter || '').includes('blur')
      && !['fixed', 'sticky'].includes(cs(e).position) && r.width > 200 && r.height > 120; }).length,
    thinBodyBoldHeadings: (() => { const b = tally(bodyText.map((e) => +cs(e).fontWeight))[0]; const h = tally(heads.map((e) => +cs(e).fontWeight))[0];
      return b && h && +b[0] <= 300 && +h[0] >= 700 ? `body ${b[0]} / headings ${h[0]}` : null; })(),
    emojiAsIcons: textEls.filter((e) => /^\p{Extended_Pictographic}/u.test(e.textContent.trim())).length,
    oneRadiusEverywhere: (() => { const r = tally(vis.map((e) => cs(e).borderTopLeftRadius).filter((x) => x !== '0px')); return r.length === 1 ? r[0][0] : null; })(),
    leftBorderNoteBoxes: vis.filter((e) => parseFloat(cs(e).borderLeftWidth) >= 3 && cs(e).borderRightWidth === '0px' && e.textContent.trim().length > 20).length,
  };
  const h1 = document.querySelector('h1');
  return {
    viewport: `${innerWidth}x${innerHeight}`,
    horizontalScroll: document.documentElement.scrollWidth > innerWidth,
    h1: h1 && { text: h1.textContent.trim().slice(0, 60), size: cs(h1).fontSize, weight: cs(h1).fontWeight, tracking: cs(h1).letterSpacing,
      lines: Math.round(h1.getBoundingClientRect().height / (parseFloat(cs(h1).lineHeight) || parseFloat(cs(h1).fontSize) * 1.2)) },
    families: tally(textEls.map((e) => cs(e).fontFamily.split(',')[0].trim())).slice(0, 3),
    weights: tally(textEls.map((e) => cs(e).fontWeight)).slice(0, 5),
    sizes: tally(textEls.map((e) => Math.round(parseFloat(cs(e).fontSize)))).slice(0, 8),
    radii: tally(vis.map((e) => cs(e).borderTopLeftRadius).filter((x) => x !== '0px')).slice(0, 5),
    tellsFound: Object.fromEntries(Object.entries(tells).filter(([, v]) => v)),
  };
})();
