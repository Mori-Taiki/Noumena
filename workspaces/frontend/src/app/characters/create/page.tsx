
'use client';

import { useState, FormEvent } from 'react';

export default function CreateCharacterPage() {
  const [name, setName] = useState('');
  const [llmProvider, setLlmProvider] = useState('');
  const [personality, setPersonality] = useState('');
  const [background, setBackground] = useState('');
  const [message, setMessage] = useState('');
  const [isError, setIsError] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setMessage('');
    setIsError(false);

    const characterData = {
      name,
      llm_provider: llmProvider,
      personality,
      background,
      values: {},
      emotions: {},
      desires: {},
    };

    // NOTE: This assumes the backend is running and accessible at this URL.
    // In a real setup, this would go through a proxy or an API client.
    const apiUrl = 'http://localhost:5001/api/characters';

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(characterData),
      });

      if (response.status === 201) {
        const result = await response.json();
        setMessage(`Character created successfully! ID: ${result.id}`);
        // Clear form
        setName('');
        setLlmProvider('');
        setPersonality('');
        setBackground('');
      } else {
        const errorData = await response.json();
        setIsError(true);
        setMessage(`Error: ${response.status} - ${JSON.stringify(errorData)}`);
      }
    } catch (error) {
      setIsError(true);
      setMessage(`An unexpected error occurred: ${error}`);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-24">
      <h1 className="text-4xl font-bold mb-8">Create New Character</h1>
      <form onSubmit={handleSubmit} className="w-full max-w-lg">
        <div className="flex flex-wrap -mx-3 mb-6">
          <div className="w-full md:w-1/2 px-3 mb-6 md:mb-0">
            <label className="block uppercase tracking-wide text-xs font-bold mb-2" htmlFor="name">
              Name
            </label>
            <input
              className="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
          <div className="w-full md:w-1/2 px-3">
            <label className="block uppercase tracking-wide text-xs font-bold mb-2" htmlFor="llm-provider">
              LLM Provider
            </label>
            <input
              className="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white"
              id="llm-provider"
              type="text"
              value={llmProvider}
              onChange={(e) => setLlmProvider(e.target.value)}
              required
            />
          </div>
        </div>
        <div className="flex flex-wrap -mx-3 mb-6">
          <div className="w-full px-3">
            <label className="block uppercase tracking-wide text-xs font-bold mb-2" htmlFor="personality">
              Personality
            </label>
            <textarea
              className="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"
              id="personality"
              rows={4}
              value={personality}
              onChange={(e) => setPersonality(e.target.value)}
            />
          </div>
        </div>
        <div className="flex flex-wrap -mx-3 mb-6">
          <div className="w-full px-3">
            <label className="block uppercase tracking-wide text-xs font-bold mb-2" htmlFor="background">
              Background
            </label>
            <textarea
              className="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"
              id="background"
              rows={4}
              value={background}
              onChange={(e) => setBackground(e.target.value)}
            />
          </div>
        </div>
        <div className="flex items-center justify-between">
          <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="submit"
          >
            Create Character
          </button>
        </div>
      </form>
      {message && (
        <div className={`mt-6 p-4 rounded ${isError ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
          {message}
        </div>
      )}
    </main>
  );
}
