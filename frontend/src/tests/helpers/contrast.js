/**
 * WCAG colour contrast, as a small pure function.
 *
 * The contrast ratio decides whether text is readable against its background. WCAG 2.2
 * success criterion 1.4.3 requires 4.5:1 for normal text and 3:1 for large text (and 1.4.11
 * requires 3:1 for user interface boundaries and focus indicators).
 *
 * Formulas are from the WCAG definitions of "relative luminance" and "contrast ratio":
 *   https://www.w3.org/TR/WCAG22/#dfn-relative-luminance
 *   https://www.w3.org/TR/WCAG22/#dfn-contrast-ratio
 *
 * Used by tokens.test.js to check every colour pair in the design tokens, and the subject of
 * Lab 2's accessibility step.
 */

const HEX = /^#?([0-9a-f]{3}|[0-9a-f]{6})$/i;

/** Convert "#rgb" or "#rrggbb" (the # is optional) to [r, g, b], each 0-255. */
export function hexToRgb(hex) {
  const match = HEX.exec(String(hex).trim());
  if (!match) throw new Error(`Invalid hex colour: ${hex}`);
  let digits = match[1];
  if (digits.length === 3) digits = [...digits].map((d) => d + d).join('');
  return [0, 2, 4].map((i) => parseInt(digits.slice(i, i + 2), 16));
}

/** One sRGB channel (0-255) to its linear-light value, per the WCAG definition. */
function linearise(channel) {
  const c = channel / 255;
  return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
}

/** Relative luminance: 0 for black, 1 for white. */
export function relativeLuminance(hex) {
  const [r, g, b] = hexToRgb(hex).map(linearise);
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

/** Contrast ratio between two colours, from 1 (identical) to 21 (black on white). */
export function contrastRatio(colourA, colourB) {
  const [lighter, darker] = [relativeLuminance(colourA), relativeLuminance(colourB)].sort(
    (a, b) => b - a
  );
  return (lighter + 0.05) / (darker + 0.05);
}

/**
 * Does the pair meet WCAG AA? Note the ratio is NOT rounded: WCAG treats 4.499 as a fail.
 * Large text (18pt, or 14pt bold) only needs 3:1.
 */
export function passesAA(foreground, background, { largeText = false } = {}) {
  return contrastRatio(foreground, background) >= (largeText ? 3 : 4.5);
}

/**
 * Read the colour custom properties from a stylesheet's `:root` block and its dark theme block.
 * Returns { light, dark }; dark falls back to the light value for anything it does not redefine.
 */
export function parseThemeTokens(css) {
  const read = (selector) => {
    const escaped = selector.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const block = new RegExp(`${escaped}\\s*\\{([^}]*)\\}`).exec(css);
    if (!block) throw new Error(`No ${selector} block found in the stylesheet`);
    return Object.fromEntries(
      [...block[1].matchAll(/(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{3,6})\b/g)].map((m) => [m[1], m[2]])
    );
  };
  const light = read(':root');
  return { light, dark: { ...light, ...read("[data-theme='dark']") } };
}
