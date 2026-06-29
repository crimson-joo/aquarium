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

test('all locales explain real, stub, degraded, and failed stage states', () => {
  for (const locale of ['ko', 'zh', 'en']) {
    assert.match(messages[locale].providerLabels.local_stub, /stub|demo|데모|대체|本地|演示/i);
    assert.match(messages[locale].providerLabels.bettafish_cli, /BettaFish/);
    assert.match(messages[locale].providerLabels.mirofish_cli, /MiroFish/);
    assert.ok(messages[locale].statusExplanations.completed);
    assert.ok(messages[locale].statusExplanations.degraded);
    assert.ok(messages[locale].statusExplanations.failed);
    assert.ok(messages[locale].warningsTitle);
    assert.ok(messages[locale].artifactsTitle);
  }
});
