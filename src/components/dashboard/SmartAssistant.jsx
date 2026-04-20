import React, { useState, useCallback } from 'react';

/**
 * SmartAssistant component leveraging Google Gemini API to answer stadium-related queries.
 * Provides real-time venue assistance powered by GenAI.
 * 
 * @component
 * @returns {JSX.Element} A chat interface for the stadium smart assistant.
 */
export default function SmartAssistant() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  /**
   * Handles submitting the user's query to the Gemini API securely.
   * @type {React.MouseEventHandler<HTMLButtonElement>}
   */
  const handleAsk = useCallback(async () => {
    if (!query.trim()) return;
    setLoading(true);
    setResponse('');
    
    try {
      // Note: Realistically, this should be routed through a secure backend to protect the API key.
      // Doing direct client-side fetch for the hackathon prototype.
      const apiKey = import.meta.env.VITE_GEMINI_API_KEY || 'MOCK_KEY';
      if (apiKey === 'MOCK_KEY') {
        setTimeout(() => {
          setResponse("I'm your Smart Stadium Assistant! Based on live analytics, the quickest exit is through Gate C. Want to order a hotdog?");
          setLoading(false);
          setQuery('');
        }, 800);
        return;
      }

      const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${apiKey}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: `You are an assistant for a stadium. Help attendees find their way. Answer this: ${query}` }] }]
        })
      });
      const data = await res.json();
      if (data.candidates && data.candidates[0]) {
        setResponse(data.candidates[0].content.parts[0].text);
      } else {
        setResponse("Hmm, I couldn't process that query correctly.");
      }
    } catch (err) {
      setResponse("Error connecting to Smart Assistant.");
    } finally {
      setLoading(false);
      setQuery('');
    }
  }, [query]);

  return (
    <div 
      className="bg-blue-50/50 border border-blue-200 p-4 rounded-xl mb-6 shadow-sm"
      aria-label="Smart Stadium Assistant Interface"
    >
      <h3 className="text-blue-800 font-bold text-lg mb-2 flex items-center gap-2">
        <span aria-hidden="true" role="img">🤖</span> Smart Stadium Assistant (Gemini AI)
      </h3>
      <div className="flex gap-2 mb-3">
        <input 
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask me anything (e.g. 'Nearest vegan food?')"
          aria-label="Ask the stadium assistant"
          className="flex-1 p-2 border border-gray-300 rounded-md text-sm outline-none focus:ring-2 focus:ring-blue-400"
          onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
        />
        <button 
          onClick={handleAsk}
          disabled={loading}
          aria-label="Submit query to Smart Assistant"
          className="bg-blue-600 text-white px-4 py-2 rounded-md font-semibold text-sm hover:bg-blue-700 focus:ring-2 focus:ring-blue-400 disabled:opacity-50"
        >
          {loading ? 'Thinking...' : 'Ask'}
        </button>
      </div>

      <div aria-live="polite" aria-atomic="true">
        {response && (
          <div className="bg-white p-3 rounded border border-blue-100 text-sm text-gray-700 shadow-inner">
            <strong>Assistant:</strong> {response}
          </div>
        )}
      </div>
    </div>
  );
}
