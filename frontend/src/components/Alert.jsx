import React, { useEffect, useRef } from 'react';

/**
 * Inline message that assistive technology announces when it appears.
 *
 * type="error"   -> role="alert"  (assertive: interrupts, for failures)
 * type="success" -> role="status" (polite: waits, for confirmations)
 *
 * `focusOnMount` also moves keyboard focus to the message. Use it for form
 * submission errors: the submit button is disabled while the request runs, so
 * focus would otherwise fall back to <body> and the user would lose their place.
 */
function Alert({ type = 'error', focusOnMount = false, className = '', children, ...rest }) {
  const ref = useRef(null);

  useEffect(() => {
    if (focusOnMount) {
      ref.current?.focus();
    }
  }, [focusOnMount]);

  return (
    <div
      ref={ref}
      role={type === 'error' ? 'alert' : 'status'}
      tabIndex={-1}
      className={`${type} ${className}`.trim()}
      {...rest}
    >
      {children}
    </div>
  );
}

export default Alert;
