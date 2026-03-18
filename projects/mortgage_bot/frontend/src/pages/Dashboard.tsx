

const Dashboard = () => {
  return (
    <div className="p-8">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 bg-white rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-2">Total Tickets</h2>
          <p className="text-4xl font-bold text-blue-600">24</p>
        </div>
        <div className="p-6 bg-white rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-2">Active Issues</h2>
          <p className="text-4xl font-bold text-orange-500">8</p>
        </div>
        <div className="p-6 bg-white rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-2">Resolved</h2>
          <p className="text-4xl font-bold text-green-500">16</p>
        </div>
      </div>
      <div className="mt-8 bg-white rounded-lg shadow-md overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 border-b">ID</th>
              <th className="px-6 py-3 border-b">Subject</th>
              <th className="px-6 py-3 border-b">Status</th>
              <th className="px-6 py-3 border-b">Priority</th>
            </tr>
          </thead>
          <tbody>
            <tr className="hover:bg-gray-50">
              <td className="px-6 py-4 border-b">T-101</td>
              <td className="px-6 py-4 border-b">Loan not appearing in pipeline</td>
              <td className="px-6 py-4 border-b"><span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">Open</span></td>
              <td className="px-6 py-4 border-b text-red-600 font-medium">High</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dashboard;
