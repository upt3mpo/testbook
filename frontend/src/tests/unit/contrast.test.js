/**
 * Unit tests for the contrast helper (src/tests/helpers/contrast.js).
 *
 * Known reference values come from the WCAG definitions and from real Testbook colours.
 * See Lab 2's accessibility step for how these tests are built up, and why the boundary cases
 * (a pair just under and just over 4.5:1) matter most.
 */

import { describe, expect, it } from 'vitest';
import { contrastRatio, hexToRgb, passesAA, relativeLuminance } from '../helpers/contrast.js';

describe('hexToRgb', () => {
  it('reads six-digit and three-digit hex, with or without the #', () => {
    expect(hexToRgb('#1264d0')).toEqual([18, 100, 208]);
    expect(hexToRgb('fff')).toEqual([255, 255, 255]);
    expect(hexToRgb('#0a0')).toEqual([0, 170, 0]);
  });

  it.each(['', '#12', '#12345', 'blue', '#gggggg', null])('rejects %j', (bad) => {
    expect(() => hexToRgb(bad)).toThrow(/Invalid hex colour/);
  });
});

describe('relativeLuminance', () => {
  it('is 0 for black and 1 for white', () => {
    expect(relativeLuminance('#000000')).toBe(0);
    expect(relativeLuminance('#ffffff')).toBeCloseTo(1, 10);
  });
});

describe('contrastRatio', () => {
  it('is 21:1 for black on white and 1:1 for a colour on itself', () => {
    expect(contrastRatio('#000000', '#ffffff')).toBeCloseTo(21, 5);
    expect(contrastRatio('#2d88ff', '#2d88ff')).toBeCloseTo(1, 10);
  });

  it('does not depend on which colour is the foreground', () => {
    expect(contrastRatio('#1264d0', '#ffffff')).toBe(contrastRatio('#ffffff', '#1264d0'));
  });

  // Real Testbook colours. The first two are the dark-theme bug (A11Y-016) and its fix.
  it.each([
    ['#ffffff', '#2d88ff', 3.46],
    ['#ffffff', '#1668d9', 5.23],
    ['#ffffff', '#1264d0', 5.59],
    ['#d32f2f', '#18191a', 3.54],
  ])('%s on %s is about %s:1', (foreground, background, expected) => {
    // toBeCloseTo(x, 2) compares to two decimal places. Never compare floats with toBe().
    expect(contrastRatio(foreground, background)).toBeCloseTo(expected, 2);
  });
});

describe('passesAA: the boundary matters most', () => {
  it('#767676 on white (4.54:1) passes; #777777 (4.48:1) fails, though they look identical', () => {
    expect(passesAA('#767676', '#ffffff')).toBe(true);
    expect(passesAA('#777777', '#ffffff')).toBe(false);
  });

  it('is not rounded: 4.48 is not "close enough" to 4.5', () => {
    expect(contrastRatio('#777777', '#ffffff')).toBeLessThan(4.5);
    expect(contrastRatio('#777777', '#ffffff')).toBeGreaterThan(4.4);
  });

  it('only needs 3:1 for large text', () => {
    // 3.46:1: fails for normal text, passes for large text.
    expect(passesAA('#ffffff', '#2d88ff')).toBe(false);
    expect(passesAA('#ffffff', '#2d88ff', { largeText: true })).toBe(true);
  });
});
