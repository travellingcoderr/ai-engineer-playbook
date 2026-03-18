import { useState } from 'react';
import type { FormEvent } from 'react';

type SearchResult = {
  type: 'knowledge' | 'ticket';
  title: string;
  content: string;
  metadata: Record<string, string | null>;
};

type AgentSearchResponse = {
  answer: string;
  loan_id: string | null;
  query: string;
  related_results: SearchResult[];
  used_tools: string[];
};

const Search = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [answer, setAnswer] = useState<string | null>(null);
  const [usedTools, setUsedTools] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (e: FormEvent) => {
    e.preventDefault();

    if (!query.trim()) {
      setError('Enter a search term to look for documents or existing issues.');
      return;
    }

    setLoading(true);
    setError(null);
    setHasSearched(true);
    setAnswer(null);
    setUsedTools([]);

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/knowledge/agent-search?query=${encodeURIComponent(query.trim())}`,
      );
      const result = await response.json();

      if (!response.ok) {
        throw new Error(result?.detail?.message || 'Search request failed.');
      }

      const typedResult = result as AgentSearchResponse;
      setAnswer(typedResult.answer || null);
      setUsedTools(Array.isArray(typedResult.used_tools) ? typedResult.used_tools : []);
      setResults(Array.isArray(typedResult.related_results) ? typedResult.related_results : []);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'Unknown error while running search.';
      setError(errorMessage);
      setAnswer(null);
      setUsedTools([]);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-5xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Knowledge Search</h1>
        <p className="mt-2 text-slate-500">
          Search articles and similar support issues before creating a new ticket.
        </p>
      </div>

      <form onSubmit={handleSearch} className="max-w-3xl">
        <div className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search guidelines, documents, or previous tickets..."
            className="flex-1 rounded-xl border border-gray-200 px-4 py-3 shadow-sm focus:border-slate-900 focus:ring-2 focus:ring-slate-900/10 outline-none"
          />
          <button
            type="submit"
            disabled={loading}
            className={`px-5 py-3 rounded-xl font-semibold transition ${
              loading ? 'bg-gray-400 text-white cursor-not-allowed' : 'bg-slate-900 text-white hover:bg-slate-800'
            }`}
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </form>

      {error && (
        <div className="mt-6 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-red-700">
          {error}
        </div>
      )}

      <div className="mt-8 space-y-4">
        {loading && (
          <div className="rounded-2xl border border-slate-200 bg-white px-5 py-6 text-slate-500 shadow-sm">
            Running LangGraph search with MCP tools and knowledge retrieval...
          </div>
        )}

        {!loading && answer && (
          <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-5 shadow-sm">
            <div className="text-xs font-semibold uppercase tracking-wide text-emerald-600">
              Agent Answer
            </div>
            <p className="mt-2 text-slate-800">{answer}</p>
          </div>
        )}

        {!loading && hasSearched && (
          <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5 shadow-sm">
            <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">
              Agent Trace
            </div>
            <div className="mt-3 space-y-2 text-sm text-slate-700">
              <div>
                Search path: <span className="font-semibold">LangGraph ReAct agent</span>
              </div>
              <div>
                MCP tools called:{' '}
                <span className="font-semibold">
                  {usedTools.length > 0 ? 'Yes' : 'No'}
                </span>
              </div>
              {usedTools.length > 0 && (
                <div className="flex flex-wrap gap-2 pt-1">
                  {usedTools.map((toolName) => (
                    <span
                      key={toolName}
                      className="rounded-full border border-slate-300 bg-white px-3 py-1 text-xs font-semibold text-slate-700"
                    >
                      {toolName}
                    </span>
                  ))}
                </div>
              )}
              {usedTools.length === 0 && (
                <div className="text-slate-500">
                  The agent answered without invoking additional MCP or knowledge tools.
                </div>
              )}
            </div>
          </div>
        )}

        {!loading && hasSearched && !answer && results.length === 0 && !error && (
          <div className="rounded-2xl border border-slate-200 bg-white px-5 py-6 text-slate-500 shadow-sm">
            The agent did not find a useful answer or related results.
          </div>
        )}

        {!loading && results.length > 0 && (
          <div className="text-sm font-semibold text-slate-500 uppercase tracking-wide">
            Supporting Results
          </div>
        )}

        {!loading &&
          results.map((result, index) => (
            <div
              key={`${result.type}-${index}-${result.title}`}
              className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
            >
              <div className="flex items-center justify-between gap-4">
                <div>
                  <div className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                    {result.type === 'knowledge' ? 'Knowledge Match' : 'Existing Issue'}
                  </div>
                  <h3 className="mt-1 text-lg font-semibold text-slate-900">{result.title}</h3>
                </div>
                <span
                  className={`rounded-full px-3 py-1 text-xs font-semibold ${
                    result.type === 'knowledge'
                      ? 'bg-blue-100 text-blue-800'
                      : 'bg-amber-100 text-amber-800'
                  }`}
                >
                  {result.type}
                </span>
              </div>

              <p className="mt-3 text-slate-700">
                {result.content}
              </p>

              <div className="mt-4 flex flex-wrap gap-2 text-xs text-slate-500">
                {Object.entries(result.metadata)
                  .filter(([, value]) => value)
                  .map(([key, value]) => (
                    <span key={key} className="rounded-full bg-slate-100 px-3 py-1">
                      {key}: {String(value)}
                    </span>
                  ))}
              </div>
            </div>
          ))}
      </div>
    </div>
  );
};

export default Search;
