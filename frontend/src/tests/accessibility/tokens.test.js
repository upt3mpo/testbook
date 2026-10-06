/**
 * Design-token contrast guard.
 *
 * Every text/background pair that the stylesheet can produce must meet WCAG AA, in EVERY theme.
 * This is a layer-4 test (a plain unit test, no browser): it reads the CSS custom properties
 * and checks the maths. It would have caught A11Y-016, where white text on the dark-theme accent
 * colour was 3.45:1 and nobody had ever scanned dark mode.
 *
 * If you add a colour token, add its pairs here. If a pair fails, change the token, not the test.
 */

import { describe, expect, it } from 'vitest';
// ?raw gives the stylesheet's text exactly as written, with no processing.
import css from '../../index.css?raw';
import { contrastRatio, parseThemeTokens } from '../helpers/contrast.js';

const themes = parseThemeTokens(css);

const WHITE = '#ffffff';

// [description, foreground token (or literal colour), background token (or literal colour)]
const PAIRS = [
  ['body text on the page', '--text-primary', '--bg-primary'],
  ['body text on cards and the app background', '--text-primary', '--bg-secondary'],
  ['text on a secondary button', '--text-primary', '--bg-hover'],
  ['secondary text on the page', '--text-secondary', '--bg-primary'],
  ['secondary text on the app background', '--text-secondary', '--bg-secondary'],
  ['links (accent as text)', '--accent-color', '--bg-primary'],
  ['white text on a primary button (accent fill)', WHITE, '--accent-fill'],
  ['white text on a primary button, hovered', WHITE, '--accent-fill-hover'],
  ['white text on a danger button', WHITE, '--danger-color'],
  ['error message text on the page', '--error-text', '--bg-primary'],
];

const colour = (theme, tokenOrLiteral) =>
  tokenOrLiteral.startsWith('--') ? themes[theme][tokenOrLiteral] : tokenOrLiteral;

describe.each(['light', 'dark'])('design token contrast (%s theme)', (theme) => {
  it.each(PAIRS)('%s meets WCAG AA (4.5:1)', (_description, foreground, background) => {
    const fg = colour(theme, foreground);
    const bg = colour(theme, background);
    expect(fg, `${foreground} is not defined in the ${theme} theme`).toBeDefined();
    expect(bg, `${background} is not defined in the ${theme} theme`).toBeDefined();

    const ratio = contrastRatio(fg, bg);
    expect(
      ratio,
      `${foreground} (${fg}) on ${background} (${bg}) is ${ratio.toFixed(2)}:1, needs 4.5:1`
    ).toBeGreaterThanOrEqual(4.5);
  });
});

describe('the token parser', () => {
  it('finds both themes, and dark inherits what it does not redefine', () => {
    expect(themes.light['--bg-primary']).toBe('#ffffff');
    expect(themes.dark['--bg-primary']).not.toBe(themes.light['--bg-primary']);
    // --danger-color is only defined for light, so dark falls back to it.
    expect(themes.dark['--danger-color']).toBe(themes.light['--danger-color']);
  });
});
