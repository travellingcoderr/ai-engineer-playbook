import { useEffect, useState } from 'react';

type Ticket = {
  id: string;
  subject: string;
  status: string;
  severity: string;
  category: string;
  user_name: string;
  created_at: string;
};

const resolvedStatuses = new Set(['resolved', 'closed']);

const formatStatus = (status: string) =>
  status.replace(/_/g, ' ').replace(/\b\w/g, (char) => char.toUpperCase());

const formatSeverity = (severity: string) =>
  severity.replace(/\b\w/g, (char) => char.toUpperCase());

const getStatusBadgeClass = (status: string) => {
  const normalizedStatus = status.toLowerCase();

  if (resolvedStatuses.has(normalizedStatus)) {
    return 'bg-green-100 text-green-800';
  }

  if (normalizedStatus === 'in_progress') {
    return 'bg-amber-100 text-amber-800';
  }

  return 'bg-blue-100 text-blue-800';
};

const getSeverityClass = (severity: string) => {
  const normalizedSeverity = severity.toLowerCase();

  if (normalizedSeverity === 'critical') {
    return 'text-red-700';
  }

  if (normalizedSeverity === 'high') {
    return 'text-orange-600';
  }

  if (normalizedSeverity === 'medium') {
    return 'text-blue-600';
  }

  return 'text-slate-600';
};

const Dashboard = () => {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadTickets = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/tickets/`);
        const result = await response.json();

        if (!response.ok) {
          throw new Error(result?.detail?.message || 'Failed to load dashboard tickets.');
        }

        setTickets(Array.isArray(result) ? result : []);
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : 'Unknown error while loading dashboard data.';
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    void loadTickets();
  }, []);

  const totalTickets = tickets.length;
  const resolvedTickets = tickets.filter((ticket) =>
    resolvedStatuses.has(ticket.status.toLowerCase()),
  ).length;
  const activeTickets = totalTickets - resolvedTickets;

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Support Dashboard</h1>
        <p className="mt-2 text-slate-500">
          Live ticket data from the backend API.
        </p>
      </div>

      {error && (
        <div className="mb-6 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-red-700">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 bg-white rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-2">Total Tickets</h2>
          <p className="text-4xl font-bold text-blue-600">
            {loading ? '--' : totalTickets}
          </p>
        </div>
        <div className="p-6 bg-white rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-2">Active Issues</h2>
          <p className="text-4xl font-bold text-orange-500">
            {loading ? '--' : activeTickets}
          </p>
        </div>
        <div className="p-6 bg-white rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-2">Resolved</h2>
          <p className="text-4xl font-bold text-green-500">
            {loading ? '--' : resolvedTickets}
          </p>
        </div>
      </div>

      <div className="mt-8 bg-white rounded-lg shadow-md overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 border-b">ID</th>
              <th className="px-6 py-3 border-b">Subject</th>
              <th className="px-6 py-3 border-b">Customer</th>
              <th className="px-6 py-3 border-b">Status</th>
              <th className="px-6 py-3 border-b">Priority</th>
            </tr>
          </thead>
          <tbody>
            {loading && (
              <tr>
                <td className="px-6 py-8 border-b text-slate-500" colSpan={5}>
                  Loading tickets...
                </td>
              </tr>
            )}

            {!loading && tickets.length === 0 && (
              <tr>
                <td className="px-6 py-8 border-b text-slate-500" colSpan={5}>
                  No tickets found.
                </td>
              </tr>
            )}

            {!loading &&
              tickets.map((ticket) => (
                <tr key={ticket.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 border-b font-mono text-sm text-slate-600">
                    {ticket.id.slice(0, 8)}
                  </td>
                  <td className="px-6 py-4 border-b">
                    <div className="font-medium text-slate-900">{ticket.subject}</div>
                    <div className="text-sm text-slate-500">{ticket.category}</div>
                  </td>
                  <td className="px-6 py-4 border-b text-slate-700">{ticket.user_name}</td>
                  <td className="px-6 py-4 border-b">
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusBadgeClass(ticket.status)}`}
                    >
                      {formatStatus(ticket.status)}
                    </span>
                  </td>
                  <td className={`px-6 py-4 border-b font-medium ${getSeverityClass(ticket.severity)}`}>
                    {formatSeverity(ticket.severity)}
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dashboard;
