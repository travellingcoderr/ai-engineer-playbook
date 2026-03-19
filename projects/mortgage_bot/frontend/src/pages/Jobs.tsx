import { useEffect, useState } from 'react';

type Job = {
  id: string;
  job_id: string;
  queue_name: string;
  task_name: string;
  status: string;
  document_id: string | null;
  error_message: string | null;
  enqueued_at: string;
  started_at: string | null;
  completed_at: string | null;
  updated_at: string;
};

const getStatusClass = (status: string) => {
  if (status === 'completed') return 'bg-green-100 text-green-800';
  if (status === 'processing') return 'bg-amber-100 text-amber-800';
  if (status === 'failed') return 'bg-red-100 text-red-800';
  return 'bg-blue-100 text-blue-800';
};

const Jobs = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadJobs = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/jobs?limit=100`);
        const result = await response.json();

        if (!response.ok) {
          throw new Error(result?.detail || 'Failed to load worker jobs.');
        }

        setJobs(Array.isArray(result) ? result : []);
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : 'Unknown error while loading jobs.';
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    void loadJobs();
  }, []);

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Worker Jobs</h1>
        <p className="mt-2 text-slate-500">
          Track queued, processing, completed, and failed background jobs handled by the worker.
        </p>
      </div>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-red-700">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="rounded-2xl bg-white p-6 shadow-md">
          <div className="text-sm font-semibold text-slate-500">Queued</div>
          <div className="mt-3 text-3xl font-bold text-slate-900">
            {loading ? '--' : jobs.filter((job) => job.status === 'queued').length}
          </div>
        </div>
        <div className="rounded-2xl bg-white p-6 shadow-md">
          <div className="text-sm font-semibold text-slate-500">Processing</div>
          <div className="mt-3 text-3xl font-bold text-slate-900">
            {loading ? '--' : jobs.filter((job) => job.status === 'processing').length}
          </div>
        </div>
        <div className="rounded-2xl bg-white p-6 shadow-md">
          <div className="text-sm font-semibold text-slate-500">Completed</div>
          <div className="mt-3 text-3xl font-bold text-slate-900">
            {loading ? '--' : jobs.filter((job) => job.status === 'completed').length}
          </div>
        </div>
        <div className="rounded-2xl bg-white p-6 shadow-md">
          <div className="text-sm font-semibold text-slate-500">Failed</div>
          <div className="mt-3 text-3xl font-bold text-slate-900">
            {loading ? '--' : jobs.filter((job) => job.status === 'failed').length}
          </div>
        </div>
      </div>

      <div className="rounded-2xl bg-white p-6 shadow-md overflow-hidden">
        <h2 className="text-lg font-semibold text-slate-900">Recent Jobs</h2>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-4 py-3">Job ID</th>
                <th className="px-4 py-3">Queue</th>
                <th className="px-4 py-3">Task</th>
                <th className="px-4 py-3">Document</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Enqueued</th>
                <th className="px-4 py-3">Started</th>
                <th className="px-4 py-3">Completed</th>
                <th className="px-4 py-3">Error</th>
              </tr>
            </thead>
            <tbody>
              {jobs.map((job) => (
                <tr key={job.id} className="border-t border-slate-100">
                  <td className="px-4 py-3 font-mono text-slate-700">{job.job_id}</td>
                  <td className="px-4 py-3">{job.queue_name}</td>
                  <td className="px-4 py-3">{job.task_name}</td>
                  <td className="px-4 py-3">{job.document_id || '-'}</td>
                  <td className="px-4 py-3">
                    <span className={`rounded-full px-2 py-1 text-xs font-semibold ${getStatusClass(job.status)}`}>
                      {job.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-slate-600">{new Date(job.enqueued_at).toLocaleString()}</td>
                  <td className="px-4 py-3 text-slate-600">{job.started_at ? new Date(job.started_at).toLocaleString() : '-'}</td>
                  <td className="px-4 py-3 text-slate-600">{job.completed_at ? new Date(job.completed_at).toLocaleString() : '-'}</td>
                  <td className="px-4 py-3 text-red-700">{job.error_message || '-'}</td>
                </tr>
              ))}
              {!loading && jobs.length === 0 && (
                <tr>
                  <td className="px-4 py-6 text-slate-500" colSpan={9}>
                    No worker jobs recorded yet.
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

export default Jobs;
