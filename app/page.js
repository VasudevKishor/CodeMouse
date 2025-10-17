// app/page.js

"use client"; // 👈 THIS IS THE MOST IMPORTANT LINE

import React, { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

export default function HomePage() {
  const [inputCode, setInputCode] = useState('');
  const [resultCode, setResultCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    setError(null);
    setResultCode('');

    try {
      const response = await fetch('/api/muse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: inputCode }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.error || 'An error occurred while fetching data.');
      }
      const data = await response.json();
      setResultCode(data.alternatives);

    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-6 md:p-12 bg-gray-900 text-white font-sans">
      <div className="w-full max-w-4xl">
        <h1 className="text-4xl md:text-5xl font-bold text-center mb-2">CodeMuse</h1>
        <p className="text-center text-gray-400 mb-8">Paste your code to discover new perspectives.</p>

        <form onSubmit={handleSubmit}>
          <textarea
            className="w-full h-64 p-4 font-mono text-sm bg-gray-800 border border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none resize-y"
            value={inputCode}
            onChange={(e) => setInputCode(e.target.value)}
            placeholder={`def find_evens(numbers):\n    evens = []\n    for num in numbers:\n        if num % 2 == 0:\n            evens.append(num)\n    return evens`}
          />
          <button
            type="submit"
            disabled={isLoading || !inputCode}
            className="w-full mt-4 px-4 py-3 bg-blue-600 text-white font-semibold rounded-md transition-colors hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Thinking...' : 'Muse'}
          </button>
        </form>

        <div className="mt-8 min-h-[200px]">
          {error && <div className="p-4 bg-red-900/50 border border-red-700 rounded-md text-red-300">{error}</div>}
          {isLoading && <div className="text-center text-gray-400">Generating alternatives...</div>}
          {resultCode && (
              <SyntaxHighlighter language="python" style={vscDarkPlus} customStyle={{ borderRadius: '0.375rem', padding: '1rem', border: '1px solid #4A5568' }}>
                {resultCode}
              </SyntaxHighlighter>
          )}
        </div>
      </div>
    </main>
  );
}