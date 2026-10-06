import React from 'react';

/**
 * The last line of defence against a blank page.
 *
 * If anything in the tree throws while rendering, React unmounts the whole app and leaves an
 * empty document: nothing to see, and nothing for a screen reader to read. This shows a plain
 * explanation instead, moves focus to it so assistive technology announces it, and offers a way
 * out. It is a safety net: bugs should still be fixed, not hidden (A11Y-019 was one).
 */
class ErrorBoundary extends React.Component {
  state = { failed: false };

  static getDerivedStateFromError() {
    return { failed: true };
  }

  componentDidCatch(error, info) {
    console.error('The app crashed while rendering:', error, info?.componentStack);
    document.title = 'Something went wrong - Testbook';
  }

  render() {
    if (!this.state.failed) return this.props.children;

    return (
      <main className="error-boundary" data-testid="error-boundary">
        {/* A ref callback runs when the heading mounts, whether the crash happened on first render
            or later, so focus always lands here and assistive technology reads it out. */}
        <h1 ref={(heading) => heading?.focus()} tabIndex={-1}>
          Something went wrong
        </h1>
        <p>
          Testbook hit an unexpected problem and could not show this page. Your work on other pages
          is not affected.
        </p>
        <button type="button" className="btn btn-primary" onClick={() => window.location.reload()}>
          Reload the page
        </button>
      </main>
    );
  }
}

export default ErrorBoundary;
