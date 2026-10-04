import { useEffect } from 'react';

const SUFFIX = 'Testbook';

/**
 * Give each route its own <title> (WCAG 2.4.2). The title is the first thing a
 * screen reader reads on a page load and the label in the browser tab/history.
 */
export default function useDocumentTitle(title) {
  useEffect(() => {
    if (title) {
      document.title = `${title} - ${SUFFIX}`;
    }
  }, [title]);
}
