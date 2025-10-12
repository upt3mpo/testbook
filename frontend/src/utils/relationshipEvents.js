export const BLOCK_STATUS_EVENT = 'testbook:block-status-changed';
export const BLOCK_EVENT_STORAGE_KEY = 'testbook:last-block-change';

/**
 * Broadcast a block/unblock status change so other views (like the feed)
 * can refresh any cached relationship-dependent data.
 */
export function broadcastBlockStatusChange(detail) {
  if (typeof window === 'undefined') {
    return;
  }

  try {
    window.localStorage.setItem(
      BLOCK_EVENT_STORAGE_KEY,
      Date.now().toString()
    );
  } catch (err) {
    // localStorage might be unavailable (Safari private mode, etc.)
    console.warn('Failed to record block status change timestamp', err);
  }

  try {
    window.dispatchEvent(new CustomEvent(BLOCK_STATUS_EVENT, { detail }));
  } catch (err) {
    console.warn('Failed to broadcast block status change', err);
  }
}
