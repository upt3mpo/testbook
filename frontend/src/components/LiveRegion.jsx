import React, { useEffect, useState } from 'react';

/**
 * A single, always-mounted polite live region for announcing changes that have
 * no visible message of their own (a reaction was added, a post was deleted, the
 * page changed). Screen readers only announce changes to a live region that
 * already exists in the DOM, which is why this is mounted once at the app root
 * instead of being created on demand.
 */
const listeners = new Set();

export function announce(message) {
  listeners.forEach((listener) => listener(message));
}

function LiveRegion() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Clear first so announcing the same text twice in a row still fires.
    const listener = (next) => {
      setMessage('');
      setTimeout(() => setMessage(next), 50);
    };
    listeners.add(listener);
    return () => listeners.delete(listener);
  }, []);

  return (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
      data-testid="live-region"
    >
      {message}
    </div>
  );
}

export default LiveRegion;
