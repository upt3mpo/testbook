/**
 * Unit tests for relationshipEvents.js
 *
 * This module lets one view (e.g. Followers) tell another (e.g. Feed)
 * that a block/unblock happened, using a browser CustomEvent plus a
 * localStorage timestamp as a fallback for views that were unmounted
 * when the event fired. These tests cover both channels and the
 * defensive fallback when localStorage/window aren't usable.
 */

import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
  BLOCK_EVENT_STORAGE_KEY,
  BLOCK_STATUS_EVENT,
  broadcastBlockStatusChange,
} from '../../utils/relationshipEvents';

describe('broadcastBlockStatusChange', () => {
  let setItemSpy;

  beforeEach(() => {
    setItemSpy = vi.spyOn(window.localStorage, 'setItem');
  });

  afterEach(() => {
    setItemSpy.mockRestore();
  });

  it('dispatches a CustomEvent carrying the given detail', () => {
    const received = [];
    const handler = (event) => received.push(event.detail);
    window.addEventListener(BLOCK_STATUS_EVENT, handler);

    broadcastBlockStatusChange({ username: 'mikechen', isBlocked: true });

    window.removeEventListener(BLOCK_STATUS_EVENT, handler);
    expect(received).toEqual([{ username: 'mikechen', isBlocked: true }]);
  });

  it('records a timestamp in localStorage under the shared storage key', () => {
    broadcastBlockStatusChange({ username: 'mikechen', isBlocked: true });

    expect(setItemSpy).toHaveBeenCalledWith(BLOCK_EVENT_STORAGE_KEY, expect.any(String));
  });

  it('still dispatches the event when localStorage.setItem throws', () => {
    setItemSpy.mockImplementation(() => {
      throw new Error('QuotaExceededError');
    });
    const received = [];
    const handler = (event) => received.push(event.detail);
    window.addEventListener(BLOCK_STATUS_EVENT, handler);

    expect(() =>
      broadcastBlockStatusChange({ username: 'mikechen', isBlocked: false })
    ).not.toThrow();

    window.removeEventListener(BLOCK_STATUS_EVENT, handler);
    expect(received).toEqual([{ username: 'mikechen', isBlocked: false }]);
  });
});
