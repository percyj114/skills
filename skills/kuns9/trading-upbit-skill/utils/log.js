'use strict';
/**
 * Log Utility (utils/log.js)
 * MUST NOT write to stdout/stderr (JSON-only output is handled by skill.js).
 * Provide in-memory buffering if needed.
 */

function createLogBuffer() {
  const entries = [];
  return {
    entries,
    info: (message, extra = {}) => entries.push({ level: 'INFO', message, ...extra }),
    warn: (message, extra = {}) => entries.push({ level: 'WARN', message, ...extra }),
    error: (message, extra = {}) => entries.push({ level: 'ERROR', message, ...extra }),
  };
}

module.exports = { createLogBuffer };
