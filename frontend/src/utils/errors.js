/**
 * Turn an API error into a message a person can read.
 *
 * Testbook's API returns errors in two shapes, and the UI has to cope with both:
 *   - a plain string:  { "detail": "Email already registered" }
 *   - a list of validation issues from the framework (HTTP 422):
 *       { "detail": [{ "type": "missing", "loc": ["body", "username"], "msg": "Field required" }] }
 *
 * Rendering the second shape directly crashes React ("Objects are not valid as a React child")
 * and leaves a blank page. This is audit finding A11Y-019.
 *
 * Messages name the field that is wrong (WCAG 3.3.1 Error Identification) and, where we can,
 * say how to fix it (3.3.3 Error Suggestion).
 */

/** "display_name" -> "Display name" */
const humanise = (field) => field.replace(/_/g, ' ').replace(/^./, (c) => c.toUpperCase());

/** The field a validation issue is about: the last string in `loc`, ignoring where it came from. */
function fieldOf(issue) {
  const places = new Set(['body', 'query', 'path', 'header', 'cookie']);
  const loc = Array.isArray(issue.loc) ? issue.loc : [];
  const field = [...loc].reverse().find((part) => typeof part === 'string' && !places.has(part));
  return field ? humanise(field) : '';
}

const asSentence = (text) => {
  const trimmed = String(text).trim();
  if (!trimmed) return '';
  const capitalised = trimmed.charAt(0).toUpperCase() + trimmed.slice(1);
  return /[.!?]$/.test(capitalised) ? capitalised : `${capitalised}.`;
};

function describeIssue(issue) {
  if (typeof issue === 'string') return asSentence(issue);
  if (!issue || typeof issue !== 'object') return '';

  const field = fieldOf(issue);
  const message = typeof issue.msg === 'string' ? issue.msg : '';

  if (issue.type === 'missing')
    return field ? `${field} is required.` : 'A required field is missing.';
  if (/email/i.test(message) || /email/i.test(field)) {
    return 'Enter a valid email address, for example name@example.com.';
  }
  if (!message) return field ? `${field} is not valid.` : '';
  return field ? `${field}: ${asSentence(message)}` : asSentence(message);
}

/**
 * @param {unknown} error - what a request threw (an axios error, or anything else)
 * @param {string} fallback - what to show when the error carries nothing usable
 * @returns {string} always a string, so it is always safe to render
 */
export function getErrorMessage(error, fallback) {
  const detail = error?.response?.data?.detail;

  if (typeof detail === 'string' && detail.trim()) return detail;

  if (Array.isArray(detail)) {
    const messages = detail.map(describeIssue).filter(Boolean);
    if (messages.length > 0) return messages.join(' ');
  }

  return fallback;
}
