import React, { useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Fish, Waves, Network, GitBranch, FileText } from 'lucide-react';
import './styles.css';
import { messages } from './i18n.messages.mjs';

type Locale = 'ko' | 'zh' | 'en';
type Mode = 'single' | 'multiverse';
type Stage = { name: string; provider: string; status: string; warnings?: string[] };
type ProviderKey = 'aquarium_native' | 'local_stub' | 'bettafish_cli' | 'mirofish_cli';
type StatusKey = 'completed' | 'degraded' | 'failed';
type RuntimeLevel = 'aquarium_native' | 'native_bounded' | 'real_provider_warning' | 'degraded_stub' | 'contract_only' | 'failed';
type GraphMemoryKey = 'native_pass' | 'warning' | 'not_configured' | 'not_native';
type JobStatus = 'queued' | 'running' | 'succeeded' | 'failed' | 'cancelled';
type RuntimeClaim = {
  real_integration: boolean;
  standalone_native: boolean;
  external_runner_dependency: boolean;
  runtime_level: RuntimeLevel;
  native_bounded_smoke: boolean;
  degraded: boolean;
  graph_engine_status?: 'aquarium_native' | 'legacy_runner' | 'not_available';
  graph_memory_status: GraphMemoryKey;
  long_running_multiverse_verified: boolean;
  mode_verified: Mode;
};
type Entity = { name: string; type: string; rationale: string };
type Persona = { name: string; role: string; stance: string };
type Universe = { name: string; variation: string; dominant_signal: string; events: string[] };
type RunResult = {
  run_id: string;
  mode: Mode;
  status: string;
  summary?: string[];
  stages?: Stage[];
  artifacts?: Record<string, string>;
  runtime_claim?: RuntimeClaim;
  seed?: { title: string; key_points: string[] };
  ecosystem?: { entities: Entity[]; relations: Record<string, string>[]; personas: Persona[] };
  simulation?: { universes: Universe[] };
  report?: { preview: string[]; path: string };
};
type JobResult = {
  job_id: string;
  run_id: string;
  status: JobStatus;
  progress: number;
  stage: string;
  attempts: number;
  error?: string | null;
  result?: RunResult | null;
};

type ResultTab = 'seed' | 'ecosystem' | 'currents' | 'report';

function App() {
  const [locale, setLocale] = useState<Locale>('ko');
  const [topic, setTopic] = useState('AI 검색엔진 시장 변화');
  const [mode, setMode] = useState<Mode>('multiverse');
  const [job, setJob] = useState<JobResult | null>(null);
  const [result, setResult] = useState<RunResult | null>(null);
  const [activeTab, setActiveTab] = useState<ResultTab>('seed');
  const [loading, setLoading] = useState(false);
  const [uiError, setUiError] = useState<string | null>(null);
  const t = messages[locale];
  const steps = useMemo(() => [
    [Fish, t.steps.seed], [Network, t.steps.map], [Waves, t.steps.current], [GitBranch, t.steps.observe], [FileText, t.steps.report],
  ] as const, [t]);

  async function pollJob(jobId: string) {
    const response = await fetch(`/api/jobs/${jobId}`);
    if (!response.ok) {
      setUiError(`job polling failed: ${response.status}`);
      setLoading(false);
      return;
    }
    const nextJob: JobResult = await response.json();
    nextJob.progress = Math.max(0, Math.min(100, nextJob.progress));
    setJob(nextJob);
    if (nextJob.result) setResult(nextJob.result);
    if (nextJob.status === 'queued' || nextJob.status === 'running') {
      window.setTimeout(() => pollJob(jobId).catch((error) => { setUiError(String(error)); setLoading(false); }), 500);
    } else {
      setLoading(false);
    }
  }

  async function startRun() {
    setLoading(true);
    setUiError(null);
    setResult(null);
    setJob(null);
    try {
      const response = await fetch('/api/runs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, locale, mode }),
      });
      if (!response.ok) throw new Error(`run request failed: ${response.status}`);
      const createdJob: JobResult = await response.json();
      setJob(createdJob);
      setActiveTab('seed');
      await pollJob(createdJob.job_id);
    } catch (error) {
      setUiError(String(error));
      setLoading(false);
    }
  }

  async function mutateJob(action: 'cancel' | 'retry' | 'resume') {
    if (!job) return;
    setUiError(null);
    try {
      const response = await fetch(`/api/jobs/${job.job_id}/${action}`, { method: 'POST' });
      if (!response.ok) {
        setUiError(`${action} failed: ${response.status}`);
        setLoading(false);
        return;
      }
      const nextJob: JobResult = await response.json();
      nextJob.progress = Math.max(0, Math.min(100, nextJob.progress));
      setJob(nextJob);
      if (action === 'cancel') {
        setLoading(false);
      } else {
        setLoading(true);
        await pollJob(nextJob.job_id);
      }
    } catch (error) {
      setUiError(String(error));
      setLoading(false);
    }
  }

  function renderTab() {
    if (!result) return null;
    if (activeTab === 'seed') {
      return <div className="insightGrid">
        {result.seed?.key_points?.map((point) => <article className="insightCard" key={point}><b>{t.resultTabs.seed}</b><p>{point}</p></article>)}
      </div>;
    }
    if (activeTab === 'ecosystem') {
      return <div className="insightGrid">
        <article className="insightCard"><b>{t.resultTabs.ecosystem}</b>{result.ecosystem?.entities?.map((entity) => <p key={entity.name}><strong>{entity.name}</strong> · {entity.type}<br/><small>{entity.rationale}</small></p>)}</article>
        <article className="insightCard"><b>Personas</b>{result.ecosystem?.personas?.map((persona) => <p key={persona.name}><strong>{persona.name}</strong> · {persona.role}<br/><small>{persona.stance}</small></p>)}</article>
        <article className="insightCard"><b>Relations</b>{result.ecosystem?.relations?.map((relation, index) => <p key={`${relation.source}-${relation.target}-${index}`}>{relation.source} → {relation.target}<br/><small>{relation.type}</small></p>)}</article>
      </div>;
    }
    if (activeTab === 'currents') {
      return <div className="insightGrid">
        {result.simulation?.universes?.map((universe) => <article className="insightCard" key={universe.name}>
          <b>{universe.name}</b><p className="stageHint">{universe.variation}</p><p>{universe.dominant_signal}</p>
          <ul>{universe.events.map((event) => <li key={event}>{event}</li>)}</ul>
        </article>)}
      </div>;
    }
    return <article className="insightCard reportPreview"><b>{t.resultTabs.report}</b>{result.report?.preview?.map((line) => <p key={line}>{line}</p>)}</article>;
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
        <p className="eyebrow">Standalone research × ecosystem × simulation runtime</p>
        <h1>{t.heroTitle}</h1>
        <p className="subtitle">{t.heroSubtitle}</p>
        <div className="composer">
          <input value={topic} onChange={(e) => setTopic(e.target.value)} placeholder={t.topicPlaceholder} />
          <div className="mode">
            <button className={mode === 'single' ? 'active' : ''} onClick={() => setMode('single')}>Single</button>
            <button className={mode === 'multiverse' ? 'active' : ''} onClick={() => setMode('multiverse')}>Multiverse</button>
          </div>
          <button className="primary" onClick={startRun} disabled={loading || !topic.trim()}>{loading ? '...' : t.startCta}</button>
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
        {!job && !result && <p>{t.emptyStatus}</p>}
        {uiError && <p className="errorBox">{uiError}</p>}
        {job && <div className={`jobPanel ${job.status}`}>
          <b>Job: {job.status.toUpperCase()}</b>
          <p>Job: {job.job_id} · Run: {job.run_id}</p>
          <p>Stage: {job.stage} · Attempts: {job.attempts}</p>
          <div className="progressBar"><span style={{ width: `${job.progress}%` }} /></div>
          <div className="jobActions">
            {(job.status === 'queued' || job.status === 'running') && <button onClick={() => mutateJob('cancel')}>Cancel</button>}
            {(job.status === 'failed' || job.status === 'cancelled') && <button onClick={() => mutateJob('retry')}>Retry</button>}
            {(job.status === 'failed' || job.status === 'cancelled') && <button onClick={() => mutateJob('resume')}>Resume</button>}
          </div>
          {job.error && <p className="warning">{job.error}</p>}
        </div>}
        {result && <div className="result">
          <b>{result.status.toUpperCase()}</b><p>Run: {result.run_id}</p><p>Mode: {result.mode}</p><p>{result.summary?.join(' ')}</p>
          {result.runtime_claim && <div className={`runtimeClaim ${result.runtime_claim.runtime_level}`}>
            <b>{t.runtimeTitle}</b>
            <p>{t.runtimeLevels[result.runtime_claim.runtime_level] ?? result.runtime_claim.runtime_level}</p>
            <div className="claimGrid">
              <span>{result.runtime_claim.real_integration ? t.realIntegrationOn : t.realIntegrationOff}</span>
              <span>{result.runtime_claim.standalone_native ? t.standaloneOn : t.standaloneOff}</span>
              <span>{t.evidenceLabels.graphEngine}: {result.runtime_claim.graph_engine_status === 'aquarium_native' ? t.evidenceLabels.aquariumNative : result.runtime_claim.graph_engine_status}</span>
              <span>{t.graphMemoryLabels[result.runtime_claim.graph_memory_status] ?? result.runtime_claim.graph_memory_status}</span>
              <span>{result.runtime_claim.long_running_multiverse_verified ? t.longRunOn : t.longRunOff}</span>
            </div>
          </div>}
          <div className="resultTabs">
            {(['seed', 'ecosystem', 'currents', 'report'] as ResultTab[]).map((tab) => <button className={activeTab === tab ? 'active' : ''} key={tab} onClick={() => setActiveTab(tab)}>{t.resultTabs[tab]}</button>)}
          </div>
          {renderTab()}
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
