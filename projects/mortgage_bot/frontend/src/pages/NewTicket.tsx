import { useState } from 'react';

const NewTicket = () => {
  const [loanNumber, setLoanNumber] = useState('');
  const [query, setQuery] = useState('');
  const [aiSuggestion, setAiSuggestion] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    // Mimic AI search logic
    setTimeout(() => {
      setAiSuggestion("It looks like you're having trouble with the loan pipeline. We found 3 related knowledge articles. Try checking the 'Pipeline Visibility' settings in your profile.");
      setLoading(false);
    }, 1500);
  };

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Create New Ticket</h1>
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Loan Number</label>
          <input
            type="text"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            value={loanNumber}
            onChange={(e) => setLoanNumber(e.target.value)}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Describe your issue</label>
          <textarea
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            rows={4}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
        <button
          onClick={handleSearch}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
        >
          {loading ? 'AI is thinking...' : 'Get Instant Help'}
        </button>

        {aiSuggestion && (
          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h3 className="text-blue-800 font-semibold mb-2">AI Suggestion:</h3>
            <p className="text-blue-700">{aiSuggestion}</p>
            <div className="mt-4 flex space-x-4">
              <button className="text-sm font-medium text-blue-800 underline">This helped!</button>
              <button className="text-sm font-medium text-red-600 underline">Still need a ticket</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default NewTicket;
