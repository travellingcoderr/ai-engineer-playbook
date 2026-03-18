import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const DocumentUpload = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !title) return;

    setUploading(true);
    setMessage(null);

    const formData = new FormData();
    formData.append('file', file);

    // Note: FastAPI expects title and description as query params in current implementation
    // or we can adjust backend to read from form data. 
    // Given current backend: async def upload_document(title: str, description: str = None, file: UploadFile = File(...))

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/knowledge/upload?title=${encodeURIComponent(title)}&description=${encodeURIComponent(description)}`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        setMessage({ type: 'success', text: 'Document uploaded successfully! Processing started.' });
        setTitle('');
        setDescription('');
        setFile(null);
        setTimeout(() => navigate('/'), 3000);
      } else {
        const error = await response.json();
        setMessage({ type: 'error', text: `Upload failed: ${error.detail || 'Unknown error'}` });
      }
    } catch (err: any) {
      setMessage({ type: 'error', text: `Failed to connect to the server: ${err.message || 'Unknown error'}` });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
        <div className="bg-slate-900 p-8 text-white">
          <h1 className="text-3xl font-bold tracking-tight">Upload Knowledge Document</h1>
          <p className="mt-2 text-slate-400">Add documents to the Mortgage Bot's knowledge base for RAG.</p>
        </div>

        <form onSubmit={handleSubmit} className="p-8 space-y-6">
          {message && (
            <div className={`p-4 rounded-xl ${message.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
              {message.text}
            </div>
          )}

          <div className="space-y-2">
            <label className="text-sm font-semibold text-gray-700">Document Title</label>
            <input
              type="text"
              required
              className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none transition"
              placeholder="e.g., FHA Loan Requirements 2024"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-semibold text-gray-700">Description (Optional)</label>
            <textarea
              className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none transition"
              rows={3}
              placeholder="Brief overview of the document content..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-semibold text-gray-700">File</label>
            <div className="relative group">
              <input
                type="file"
                required
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
              />
              <div className={`w-full px-4 py-12 rounded-2xl border-2 border-dashed transition flex flex-col items-center justify-center space-y-3 ${file ? 'border-slate-900 bg-slate-50' : 'border-gray-300 group-hover:border-slate-400'}`}>
                <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center text-slate-600">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                <div className="text-sm text-gray-600 font-medium">
                  {file ? file.name : 'Click to upload or drag and drop'}
                </div>
                <div className="text-xs text-gray-400">PDF, TXT, or Markdown supported</div>
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={uploading || !file || !title}
            className={`w-full py-4 rounded-xl font-bold text-white transition shadow-lg ${uploading || !file || !title ? 'bg-gray-400 cursor-not-allowed' : 'bg-slate-900 hover:bg-slate-800 active:scale-[0.98]'}`}
          >
            {uploading ? 'Uploading and Queueing...' : 'Upload Document'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default DocumentUpload;
