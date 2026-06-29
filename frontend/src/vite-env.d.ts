/// <reference types="vite/client" />
declare module './i18n.messages.mjs' {
  export const messages: Record<'ko' | 'zh' | 'en', {
    heroTitle: string;
    heroSubtitle: string;
    startCta: string;
    statusTitle: string;
    emptyStatus: string;
    topicPlaceholder: string;
    steps: Record<'seed' | 'map' | 'current' | 'observe' | 'report', string>;
  }>;
}
