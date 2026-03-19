import { useEffect, useState } from 'react';

type SummaryBucket = {
  calls: number;
  cost_usd: number;
  feature?: string;
  tokens: number;
  workflow_type?: string;
};

type InstrumentationSummary = {
  avg_latency_ms: number;
  by_feature: SummaryBucket[];
  by_workflow: SummaryBucket[];
  completion_tokens: number;
  prompt_tokens: number;
  success_rate: number;
  total_calls: number;
  total_cost_usd: number;
  total_tokens: number;
};

type InstrumentationEvent = {
  id: string;
  trace_id: string;
  request_id: string;
  feature: string;
  workflow_type: string;
  step_name: string;
  model: string;
  provider: string;
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
  cost_usd: number;
  latency_ms: number;
  success: boolean;
  created_at: string;
};

const Instrumentation = () => {
  const [summary, setSummary] = useState<InstrumentationSummary | null>(null);
  const [events, setEvents] = useState<InstrumentationEvent[]>([]);
  const [workflowFilter, setWorkflowFilter] = useState<string>('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadInstrumentation = async () => {
      try {
        setLoading(true);
        setError(null);

        const [summaryResponse, eventsResponse] = await Promise.all([
          fetch(`${import.meta.env.VITE_API_URL}/api/instrumentation/summary`),
          fetch(`${import.meta.env.VITE_API_URL}/api/instrumentation/events?limit=50`),
        ]);

        const summaryResult = await summaryResponse.json();
        const eventsResult = await eventsResponse.json();

        if (!summaryResponse.ok) {
          throw new Error(summaryResult?.detail || 'Failed to load instrumentation summary.');
        }

        if (!eventsResponse.ok) {
          throw new Error(eventsResult?.detail || 'Failed to load instrumentation events.');
        }

        setSummary(summaryResult as InstrumentationSummary);
        setEvents(Array.isArray(eventsResult) ? eventsResult : []);
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : 'Unknown error while loading instrumentation.';
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    void loadInstrumentation();
  }, []);

  const workflowOptions = ['all', 'langgraph', 'crewai', 'rag_search', 'worker_ingestion'];
  const filteredEvents = workflowFilter === 'all'
    ? events
    : events.filter((event) => event.workflow_type === workflowFilter);

  const filteredSummary = {
    total_calls: filteredEvents.length,
    total_tokens: filteredEvents.reduce((sum, event) => sum + event.total_tokens, 0),
    total_cost_usd: filteredEvents.reduce((sum, event) => sum + event.cost_usd, 0),
    avg_latency_ms: filteredEvents.length
      ? filteredEvents.reduce((sum, event) => sum + event.latency_ms, 0) / filteredEvents.length
      : 0,
    success_rate: filteredEvents.length
      ? filteredEvents.filter((event) => event.success).length / filteredEvents.length
      : 0,
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">LLM Instrumentation</h1>
        <p className="mt-2 text-slate-500">
          Track token usage, latency, and estimated model cost across LangGraph and CrewAI flows.
        </p>
      </div>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-red-700">
          {error}
        </div>
      )}

      <div className="rounded-2xl bg-white p-6 shadow-md">
        <div className="text-sm font-semibold text-slate-500">Workflow Filter</div>
        <div className="mt-4 flex flex-wrap gap-3">
          {workflowOptions.map((option) => (
            <button
              key={option}
              type="button"
              onClick={() => setWorkflowFilter(option)}
              className={`rounded-full px-4 py-2 text-sm font-semibold transition ${
                workflowFilter === option
                  ? 'bg-slate-900 text-white'
                  : 'bg-slate-50 text-slate-700 border border-slate-200 hover:border-slate-300'
              }`}
            >
              {option}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-6">
        <div className="rounded-2xl bg-white p-6 shadow-md">
          <div className="text-sm font-semibold text-slate-500">Total Calls</div>
          <div className="mt-3 text-3xl font-bold text-slate-900">
            {loading ? '--' : filteredSummary.total_calls}
          </div>
        </div>
        <div className="rounded-2xl bg-white p-6 shadow-md">
          <div className="text-sm font-semibold text-slate-500">Total Tokens</div>
          <div className="mt-3 text-3xl font-bold text-slate-900">
            {loading ? '--' : filteredSummary.total_tokens}
          </div>
        </div>
        <div className="rounded-2xl bg-white p-6 shadow-md">
          <div className="text-sm font-semibold text-slate-500">Estimated Cost</div>
          <div className="mt-3 text-3xl font-bold text-slate-900">
            {loading ? '--' : `$${filteredSummary.total_cost_usd.toFixed(4)}`}
          </div>
        </div>
        <div className="rounded-2xl bg-white p-6 shadow-md">
          <div className="text-sm font-semibold text-slate-500">Avg Latency</div>
          <div className="mt-3 text-3xl font-bold text-slate-900">
            {loading ? '--' : `${filteredSummary.avg_latency_ms.toFixed(1)} ms`}
          </div>
        </div>
        <div className="rounded-2xl bg-white p-6 shadow-md">
          <div className="text-sm font-semibold text-slate-500">Success Rate</div>
          <div className="mt-3 text-3xl font-bold text-slate-900">
            {loading ? '--' : `${(filteredSummary.success_rate * 100).toFixed(1)}%`}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <div className="rounded-2xl bg-white p-6 shadow-md">
          <h2 className="text-lg font-semibold text-slate-900">By Feature</h2>
          <div className="mt-4 space-y-3">
            {(summary?.by_feature ?? []).map((row) => (
              <div key={row.feature} className="rounded-xl border border-slate-200 p-4">
                <div className="font-semibold text-slate-900">{row.feature}</div>
                <div className="mt-2 text-sm text-slate-600">
                  Calls: {row.calls} | Tokens: {row.tokens} | Cost: ${row.cost_usd.toFixed(4)}
                </div>
              </div>
            ))}
            {!loading && summary && summary.by_feature.length === 0 && (
              <div className="text-sm text-slate-500">No feature metrics recorded yet.</div>
            )}
          </div>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-md">
          <h2 className="text-lg font-semibold text-slate-900">By Workflow</h2>
          <div className="mt-4 space-y-3">
            {(summary?.by_workflow ?? []).map((row) => (
              <div key={row.workflow_type} className="rounded-xl border border-slate-200 p-4">
                <div className="font-semibold text-slate-900">{row.workflow_type}</div>
                <div className="mt-2 text-sm text-slate-600">
                  Calls: {row.calls} | Tokens: {row.tokens} | Cost: ${row.cost_usd.toFixed(4)}
                </div>
              </div>
            ))}
            {!loading && summary && summary.by_workflow.length === 0 && (
              <div className="text-sm text-slate-500">No workflow metrics recorded yet.</div>
            )}
          </div>
        </div>
      </div>

      <div className="rounded-2xl bg-white p-6 shadow-md overflow-hidden">
        <h2 className="text-lg font-semibold text-slate-900">Recent Invocations</h2>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-4 py-3">Time</th>
                <th className="px-4 py-3">Feature</th>
                <th className="px-4 py-3">Workflow</th>
                <th className="px-4 py-3">Step</th>
                <th className="px-4 py-3">Model</th>
                <th className="px-4 py-3">Tokens</th>
                <th className="px-4 py-3">Cost</th>
                <th className="px-4 py-3">Latency</th>
                <th className="px-4 py-3">Success</th>
              </tr>
            </thead>
            <tbody>
              {filteredEvents.map((event) => (
                <tr key={event.id} className="border-t border-slate-100">
                  <td className="px-4 py-3 text-slate-600">{new Date(event.created_at).toLocaleString()}</td>
                  <td className="px-4 py-3">{event.feature}</td>
                  <td className="px-4 py-3">{event.workflow_type}</td>
                  <td className="px-4 py-3">{event.step_name}</td>
                  <td className="px-4 py-3">{event.model}</td>
                  <td className="px-4 py-3">{event.total_tokens}</td>
                  <td className="px-4 py-3">${event.cost_usd.toFixed(4)}</td>
                  <td className="px-4 py-3">{event.latency_ms.toFixed(1)} ms</td>
                  <td className="px-4 py-3">
                    <span
                      className={`rounded-full px-2 py-1 text-xs font-semibold ${
                        event.success ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {event.success ? 'Success' : 'Failed'}
                    </span>
                  </td>
                </tr>
              ))}
              {!loading && filteredEvents.length === 0 && (
                <tr>
                  <td className="px-4 py-6 text-slate-500" colSpan={9}>
                    No LLM invocation records available for this workflow filter.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Instrumentation;
