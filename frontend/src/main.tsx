import React, { useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Fish, Waves, Network, GitBranch, FileText } from 'lucide-react';
import './styles.css';
import { messages } from './i18n.messages.mjs';

type Locale = 'ko' | 'zh' | 'en';
type Mode = 'single' | 'multiverse';
type Stage = { name: string; provider: string; status: string; warnings?: string[] };
type ProviderKey = 'local_stub' | 'bettafish_cli' | 'mirofish_cli';
type StatusKey = 'completed' | 'degraded' | 'failed';
type RunResult = { run_id: string; mode: Mode; status: string; summary?: string[]; stages?: Stage[]; artifacts?: Record<string, string> };

function App() {
  const [locale, setLocale] = useState<Locale>('ko');
  const [topic, setTopic] = useState('AI 검색엔진 시장 변화');
  const [mode, setMode] = useState<Mode>('multiverse');
  const [result, setResult] = useState<RunResult | null>(null);
  const [loading, setLoading] = useState(false);
  const t = messages[locale];
  const steps = useMemo(() => [
    [Fish, t.steps.seed], [Network, t.steps.map], [Waves, t.steps.current], [GitBranch, t.steps.observe], [FileText, t.steps.report],
  ] as const, [t]);

  async function startRun() {
    setLoading(true);
    setResult(null);
    try {
      const response = await fetch('/api/runs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, locale, mode }),
      });
      setResult(await response.json());
    } finally {
      setLoading(false);
    }
  }

  return <main className="shell">
    <nav className="nav">
      <div className="brand"><span className="orb" /> Aquarium</div>
      <select value={locale} onChange={(e) => setLocale(e.target.value as Locale)} aria-label="language">
        <option value="ko">한국어</option><option value="zh">中文</option><option value="en">English</option>
      </select>
    </nav>
    <section className="hero">
      <div>
        <p className="eyebrow">BettaFish report × MiroFish simulation</p>
        <h1>{t.heroTitle}</h1>
        <p className="subtitle">{t.heroSubtitle}</p>
        <div className="composer">
          <input value={topic} onChange={(e) => setTopic(e.target.value)} placeholder={t.topicPlaceholder} />
          <div className="mode">
            <button className={mode === 'single' ? 'active' : ''} onClick={() => setMode('single')}>Single</button>
            <button className={mode === 'multiverse' ? 'active' : ''} onClick={() => setMode('multiverse')}>Multiverse</button>
          </div>
          <button className="primary" onClick={startRun} disabled={loading}>{loading ? '...' : t.startCta}</button>
        </div>
      </div>
      <div className="tank" aria-label="aquarium visualization">
        <div className="current currentA" /><div className="current currentB" /><div className="fish f1" /><div className="fish f2" /><div className="fish f3" />
      </div>
    </section>
    <section className="workspace">
      <aside className="stepper">{steps.map(([Icon, label], index) => <div className="step" key={label}><Icon size={18}/><span>{index + 1}. {label}</span></div>)}</aside>
      <section className="panel">
        <h2>{t.statusTitle}</h2>
        {!result && <p>{t.emptyStatus}</p>}
        {result && <div className="result">
          <b>{result.status.toUpperCase()}</b><p>Run: {result.run_id}</p><p>Mode: {result.mode}</p><p>{result.summary?.join(' ')}</p>
          <div className="stageGrid">
            {result.stages?.map((stage) => {
              const providerLabel = t.providerLabels[stage.provider as ProviderKey] ?? stage.provider;
              const statusExplanation = t.statusExplanations[stage.status as StatusKey] ?? stage.status;
              return <div className="stageCard" key={stage.name}>
                <span className={`badge ${stage.status}`}>{stage.status}</span>
                <strong>{stage.name}</strong>
                <small>{providerLabel}</small>
                <p className="stageHint">{statusExplanation}</p>
                {!!stage.warnings?.length && <b className="sectionLabel">{t.warningsTitle}</b>}
                {stage.warnings?.map((warning) => <p className="warning" key={warning}>{warning}</p>)}
              </div>;
            })}
          </div>
          {result.artifacts && <div className="artifactList">
            <b className="sectionLabel">{t.artifactsTitle}</b>
            {Object.entries(result.artifacts).map(([name, path]) => <p key={name}><span>{name}</span><code>{path}</code></p>)}
          </div>}
        </div>}
      </section>
    </section>
  </main>;
}

createRoot(document.getElementById('root')!).render(<App />);
