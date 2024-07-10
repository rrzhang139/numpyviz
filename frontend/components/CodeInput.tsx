// ./components/CodeInput.tsx
import { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import 'codemirror/lib/codemirror.css';
import 'codemirror/mode/python/python';

const CodeMirror = dynamic(() => import('react-codemirror2').then(mod => mod.Controlled), { ssr: false });

export default function CodeInput({ onVisualize, errorLine }) {
  const [code, setCode] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onVisualize(code);
  };

  useEffect(() => {
    const editor = document.querySelector('.CodeMirror');
    if (editor && errorLine !== null) {
      editor.CodeMirror.operation(() => {
        editor.CodeMirror.eachLine((line) => {
          editor.CodeMirror.removeLineClass(line, 'background', 'line-error');
        });
        editor.CodeMirror.addLineClass(errorLine - 1, 'background', 'line-error');
      });
    }
  }, [errorLine]);

  return (
    <form onSubmit={handleSubmit}>
      <CodeMirror
        value={code}
        options={{
          mode: 'python',
          theme: 'default',
          lineNumbers: true,
        }}
        onBeforeChange={(editor, data, value) => {
          setCode(value);
        }}
      />
      <button type="submit" className="mt-2 px-4 py-2 bg-blue-500 text-white rounded">
        Visualize
      </button>
    </form>
  );
}
