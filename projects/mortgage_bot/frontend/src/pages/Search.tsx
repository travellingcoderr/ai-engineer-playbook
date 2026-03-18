

const Search = () => {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Knowledge Search</h1>
      <div className="max-w-xl">
        <div className="flex space-x-2">
          <input
            type="text"
            placeholder="Search guidelines, documents, or tickets..."
            className="flex-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          />
          <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">Search</button>
        </div>
      </div>
      <div className="mt-8 space-y-4">
        {[1, 2, 3].map((i) => (
          <div key={i} className="p-4 bg-white rounded-lg shadow-sm border hover:border-blue-500 cursor-pointer">
            <h3 className="font-semibold text-blue-600">Document Title {i}</h3>
            <p className="text-sm text-gray-500">Last updated 2 days ago • Guidelines</p>
            <p className="mt-2 text-gray-700">Detailed text snippet from the document chunk explaining mortgage guidelines...</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Search;
