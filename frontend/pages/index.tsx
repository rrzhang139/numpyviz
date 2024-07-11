import React, { useState } from 'react';
import axios, { AxiosError } from 'axios';
import dynamic from 'next/dynamic';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

const CodeInput = dynamic(() => import('../components/CodeInput'), { ssr: false });

interface VisualizationResult {
  operation: string;
  input: string;
  output: string;
  video_url?: string;
}

export default function Home() {
  const [results, setResults] = useState<VisualizationResult[]>([]);
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [errorLine, setErrorLine] = useState<number | null>(null);
  const [videoKey, setVideoKey] = useState<number>(Date.now());

  const handleVisualize = async (code: string) => {
    setLoading(true);
    setError('');
    setErrorLine(null);

    try {
      const response = await axios.post<VisualizationResult[]>('/api/visualize', { code });
      setResults(response.data);
      setVideoKey(Date.now());
    } catch (err) {
      console.error(err);
      let errorMsg = 'An unknown error occurred';
      
      if (axios.isAxiosError(err)) {
        errorMsg = err.response?.data?.error || err.message;
      } else if (err instanceof Error) {
        errorMsg = err.message;
      }

      setError('Error processing code: ' + errorMsg);

      const lineMatch = errorMsg.match(/Line (\d+):/);
      if (lineMatch) {
        setErrorLine(parseInt(lineMatch[1], 10));
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">NumpyViz</h1>
      <div className="m-4 p-6 bg-blue-500 text-white rounded-lg shadow-lg hover:bg-blue-600 transition-colors">
        <h2 className="text-xl font-bold mb-2">Welcome to NumpyViz—a dynamic numpy visualizer!</h2>
        <p className="mb-4">Throw in some Numpy code and watch your operations come to life!</p>
        <p className="font-semibold mb-2">A few points to keep in mind:</p>
        <ol className="list-decimal list-inside space-y-2 pl-4">
          <li>The custom parser may not pick up on certain tokens and thus throw errors. Try to write the code in as pure numpy as possible. (e.g., no comments, module imports, etc.)</li>
          <li>Please be patient. The Manim render can be slow, it usually takes ~10-20 seconds for ~4-5 operations (depending on the complexity of the data).</li>
          <li>Enjoy exploring and visualizing your Numpy operations!</li>
        </ol>
        <p className="m-5">Special thanks to the Manim Community for their trusty documentation and amazing tool!</p>
      </div>
      <CodeInput onVisualize={handleVisualize} errorLine={errorLine} />
      {loading && <p className="text-blue-500 mt-4">Loading...</p>}
      {error && <p className="text-red-500 mt-4">{error}</p>}
      {results.map((result, index) => (
        <div key={index} className="mt-4 p-4 border rounded">
          <h2 className="font-bold">{result.operation}</h2>
          <p>Input: {result.input}</p>
          <p>Output: {result.output}</p>
          {result.video_url && (
            <div>
              <video 
                key={`${videoKey}-${index}`}
                controls 
                width="640" 
                height="360"
                onError={(e) => {
                  console.error("Video error:", e);
                  setError("Failed to load video");
                }}
              >
                <source src={`${API_URL}/video/${index}`} type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}