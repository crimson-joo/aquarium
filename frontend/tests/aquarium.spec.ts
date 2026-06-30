import { expect, test } from '@playwright/test';

test('creates a db-backed job and shows explorable result tabs', async ({ page }) => {
  const consoleErrors: string[] = [];
  page.on('console', (message) => {
    if (message.type() === 'error') consoleErrors.push(message.text());
  });

  await page.goto('/');
  await expect(page.getByRole('heading', { name: '가능한 미래를 하나의 수조에서 관찰하세요' })).toBeVisible();
  await page.getByRole('button', { name: '수조 준비하기' }).click();

  await expect(page.getByText(/Job: (QUEUED|RUNNING|SUCCEEDED)/)).toBeVisible();
  await expect(page.getByText('COMPLETED', { exact: true })).toBeVisible();
  await expect(page.getByText('Graphiti 기억: 아직 미연결')).toBeVisible();
  await expect(page.getByRole('button', { name: '조사 Seed' })).toBeVisible();
  await page.getByRole('button', { name: '생태계 지도' }).click();
  await expect(page.getByText('Personas')).toBeVisible();
  await page.getByRole('button', { name: '해류 관찰' }).click();
  await expect(page.getByText('Universe 1')).toBeVisible();
  await page.getByRole('button', { name: '리포트' }).click();
  await expect(page.getByText('# 시뮬레이션 보고서', { exact: true })).toBeVisible();
  expect(consoleErrors).toEqual([]);
});
