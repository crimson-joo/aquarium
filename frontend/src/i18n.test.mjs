import test from 'node:test';
import assert from 'node:assert/strict';
import { messages } from './i18n.messages.mjs';

test('all locales expose core navigation copy', () => {
  for (const locale of ['ko', 'zh', 'en']) {
    assert.ok(messages[locale].heroTitle);
    assert.ok(messages[locale].steps.seed);
    assert.ok(messages[locale].startCta);
  }
});
