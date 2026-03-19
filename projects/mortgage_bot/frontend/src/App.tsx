import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import NewTicket from './pages/NewTicket';
import Search from './pages/Search';
import DocumentUpload from './pages/DocumentUpload';
import Instrumentation from './pages/Instrumentation';
import Jobs from './pages/Jobs';

const App = () => {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 flex">
        {/* Sidebar */}
        <div className="w-72 bg-slate-900 text-white flex flex-col shadow-xl">
          <div className="p-6 text-xl font-bold border-b border-slate-800 tracking-tight">
            Mortgage Support Dashboard
          </div>
          <nav className="flex-1 mt-6">
            <Link to="/" className="block px-6 py-3 hover:bg-slate-800 transition">Dashboard</Link>
            <Link to="/new-ticket" className="block px-6 py-3 hover:bg-slate-800 transition">New Ticket</Link>
            <Link to="/upload" className="block px-6 py-3 hover:bg-slate-800 transition">Document Upload</Link>
            <Link to="/search" className="block px-6 py-3 hover:bg-slate-800 transition">Search Knowledge</Link>
            <Link to="/jobs" className="block px-6 py-3 hover:bg-slate-800 transition">Jobs</Link>
            <Link to="/instrumentation" className="block px-6 py-3 hover:bg-slate-800 transition">Instrumentation</Link>
          </nav>
          <div className="p-6 border-t border-slate-800 text-sm text-slate-400">
            Powered by LangGraph ReAct
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/new-ticket" element={<NewTicket />} />
            <Route path="/upload" element={<DocumentUpload />} />
            <Route path="/search" element={<Search />} />
            <Route path="/jobs" element={<Jobs />} />
            <Route path="/instrumentation" element={<Instrumentation />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
