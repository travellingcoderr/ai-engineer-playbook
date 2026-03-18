import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

type Message = {
  type: 'success' | 'error';
  text: string;
};

type HelpResult = {
  type: 'knowledge' | 'ticket';
  title: string;
  content: string;
  metadata: Record<string, string | null>;
};

type HelpResponse = {
  message: string;
  recommended_result: HelpResult | null;
  related_results: HelpResult[];
  used_tools: string[];
  has_match: boolean;
};

const NewTicket = () => {
  const navigate = useNavigate();
  const [userName, setUserName] = useState('');
  const [userEmail, setUserEmail] = useState('');
  const [loanNumber, setLoanNumber] = useState('');
  const [subject, setSubject] = useState('');
  const [category, setCategory] = useState('general');
  const [severity, setSeverity] = useState('medium');
  const [query, setQuery] = useState('');
  const [aiSuggestion, setAiSuggestion] = useState<HelpResponse | null>(null);
  const [helpLoading, setHelpLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState<Message | null>(null);
  const [createdTicketId, setCreatedTicketId] = useState<string | null>(null);
  const [showCreateConfirmation, setShowCreateConfirmation] = useState(false);

  const createTicket = async (status: 'open' | 'resolved') => {
    const payload = {
      user_id: userEmail.trim().toLowerCase(),
      user_email: userEmail.trim(),
      user_name: userName.trim(),
      subject: subject.trim(),
      description: query.trim(),
      category,
      severity,
      status,
      loan_id: loanNumber.trim() || null,
    };

    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/tickets/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    const result = await response.json();
    if (!response.ok) {
      throw new Error(result?.detail?.message || result?.message || 'Ticket creation failed.');
    }

    return result as { ticket_id?: string | null };
  };

  const validateForm = () => {
    if (!userName || !userEmail || !subject || !query) {
      setMessage({ type: 'error', text: 'Name, email, subject, and issue description are required.' });
      return false;
    }

    return true;
  };

  const handleInstantHelp = async () => {
    if (!validateForm()) {
      return;
    }

    setHelpLoading(true);
    setMessage(null);
    setCreatedTicketId(null);
    setAiSuggestion(null);
    setShowCreateConfirmation(false);

    const searchParams = new URLSearchParams({
      issue: query.trim(),
    });

    if (subject.trim()) {
      searchParams.set('subject', subject.trim());
    }

    if (category.trim()) {
      searchParams.set('category', category.trim());
    }

    if (loanNumber.trim()) {
      searchParams.set('loan_id', loanNumber.trim());
    }

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/knowledge/agent-assist?${searchParams.toString()}`,
      );
      const result: HelpResponse = await response.json();

      if (!response.ok) {
        throw new Error('Unable to get instant help right now.');
      }

      setAiSuggestion(result);
      setShowCreateConfirmation(true);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'Unknown error while requesting instant help.';
      setMessage({ type: 'error', text: errorMessage });
    } finally {
      setHelpLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    if (!showCreateConfirmation) {
      await handleInstantHelp();
      return;
    }

    setSubmitting(true);
    setMessage(null);
    setCreatedTicketId(null);

    try {
      const result = await createTicket('open');
      setCreatedTicketId(result.ticket_id ?? null);
      setMessage({ type: 'success', text: 'Ticket created successfully.' });
      setSubject('');
      setQuery('');
      setLoanNumber('');
      setAiSuggestion(null);
      setShowCreateConfirmation(false);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'Unknown error while connecting to the server.';
      setMessage({ type: 'error', text: `Failed to connect to the server: ${errorMessage}` });
    } finally {
      setSubmitting(false);
    }
  };

  const handleHelped = async () => {
    if (!validateForm()) {
      return;
    }

    setSubmitting(true);
    setMessage(null);
    setCreatedTicketId(null);

    try {
      const result = await createTicket('resolved');
      setCreatedTicketId(result.ticket_id ?? null);
      setMessage({ type: 'success', text: 'Issue resolved and ticket closed successfully.' });
      setTimeout(() => navigate('/'), 1000);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'Unknown error while resolving the issue.';
      setMessage({ type: 'error', text: errorMessage });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
        <div className="bg-slate-900 p-8 text-white">
          <h1 className="text-3xl font-bold tracking-tight">Create New Ticket</h1>
          <p className="mt-2 text-slate-400">
            Submit a support issue to the backend API and capture the returned ticket ID.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="p-8 space-y-6">
          {message && (
            <div
              className={`p-4 rounded-xl ${
                message.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
              }`}
            >
              {message.text}
              {createdTicketId && <div className="mt-2 font-semibold">Ticket ID: {createdTicketId}</div>}
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="text-sm font-semibold text-gray-700">Name</label>
              <input
                type="text"
                required
                className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none transition"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-semibold text-gray-700">Email</label>
              <input
                type="email"
                required
                className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none transition"
                value={userEmail}
                onChange={(e) => setUserEmail(e.target.value)}
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-semibold text-gray-700">Subject</label>
            <input
              type="text"
              required
              className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none transition"
              placeholder="Short summary of the issue"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-2">
              <label className="text-sm font-semibold text-gray-700">Loan Number</label>
              <input
                type="text"
                className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none transition"
                value={loanNumber}
                onChange={(e) => setLoanNumber(e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-semibold text-gray-700">Category</label>
              <select
                className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none transition"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
              >
                <option value="general">General</option>
                <option value="loan">Loan</option>
                <option value="pipeline">Pipeline</option>
                <option value="documents">Documents</option>
                <option value="billing">Billing</option>
              </select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-semibold text-gray-700">Severity</label>
              <select
                className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none transition"
                value={severity}
                onChange={(e) => setSeverity(e.target.value)}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-semibold text-gray-700">Describe your issue</label>
            <textarea
              required
              className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none transition"
              rows={5}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>

          <div className="flex flex-col sm:flex-row gap-4">
            <button
              type="submit"
              disabled={submitting || helpLoading}
              className={`px-5 py-3 rounded-xl font-semibold transition ${
                submitting || helpLoading ? 'bg-gray-400 text-white cursor-not-allowed' : 'bg-slate-900 text-white hover:bg-slate-800'
              }`}
            >
              {helpLoading
                ? 'Checking Instant Help...'
                : submitting
                  ? 'Creating Ticket...'
                  : showCreateConfirmation
                    ? 'Still Create Ticket'
                    : 'Create Ticket'}
            </button>
          </div>

          {aiSuggestion && (
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h3 className="text-blue-800 font-semibold mb-2">AI Suggestion</h3>
              <p className="text-blue-700">{aiSuggestion.message}</p>

              {aiSuggestion.recommended_result && (
                <div className="mt-4 rounded-xl bg-white/80 p-4 border border-blue-100">
                  <div className="text-xs font-semibold uppercase tracking-wide text-blue-500">
                    Recommended Match
                  </div>
                  <div className="mt-1 text-base font-semibold text-slate-900">
                    {aiSuggestion.recommended_result.title}
                  </div>
                  <p className="mt-2 text-sm text-slate-700">
                    {aiSuggestion.recommended_result.content}
                  </p>
                </div>
              )}

              {aiSuggestion.related_results.length > 0 && (
                <div className="mt-4 space-y-3">
                  <div className="text-sm font-semibold text-blue-800">Related Matches</div>
                  {aiSuggestion.related_results.map((result, index) => (
                    <div key={`${result.type}-${index}-${result.title}`} className="rounded-xl border border-blue-100 bg-white/80 p-4">
                      <div className="flex items-center justify-between gap-4">
                        <div className="font-medium text-slate-900">{result.title}</div>
                        <span className="rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-700">
                          {result.type}
                        </span>
                      </div>
                      <p className="mt-2 text-sm text-slate-700">{result.content}</p>
                    </div>
                  ))}
                </div>
              )}

              <div className="mt-4 rounded-xl border border-blue-100 bg-white/80 p-4">
                <div className="text-xs font-semibold uppercase tracking-wide text-blue-500">
                  Agent Trace
                </div>
                <div className="mt-3 space-y-2 text-sm text-slate-700">
                  <div>
                    Search path: <span className="font-semibold">LangGraph ReAct agent</span>
                  </div>
                  <div>
                    MCP tools called:{' '}
                    <span className="font-semibold">
                      {aiSuggestion.used_tools.length > 0 ? 'Yes' : 'No'}
                    </span>
                  </div>
                  {aiSuggestion.used_tools.length > 0 && (
                    <div className="flex flex-wrap gap-2 pt-1">
                      {aiSuggestion.used_tools.map((toolName) => (
                        <span
                          key={toolName}
                          className="rounded-full border border-blue-200 bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700"
                        >
                          {toolName}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              <p className="mt-3 text-sm text-blue-800">
                Review these suggestions first. If they do not solve the issue, use the button above to continue creating the ticket.
              </p>

              <div className="mt-4 flex flex-col sm:flex-row gap-3">
                <button
                  type="button"
                  onClick={handleHelped}
                  disabled={submitting}
                  className="px-4 py-2 rounded-xl bg-white text-blue-800 border border-blue-200 font-semibold hover:bg-blue-100 transition"
                >
                  {submitting ? 'Closing Ticket...' : 'This Helped'}
                </button>
              </div>
            </div>
          )}
        </form>
      </div>
    </div>
  );
};

export default NewTicket;
