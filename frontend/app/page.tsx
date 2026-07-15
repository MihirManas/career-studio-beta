"use client";

import { useState } from "react";

export default function Home() {
  const [rawText, setRawText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const processKnowledge = async () => {
    if (!rawText) return alert("Please enter some text.");
    setLoading(true);
    try {
      // Connect to Render Backend URL
      // Make sure the environment variable points to the Render backend URL
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "https://career-studio-beta.onrender.com";
      
      const uploadRes = await fetch(`${API_URL}/api/v1/knowledge/upload`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_id: "test-user-123",
            source_type: "raw_text",
            raw_text: rawText
        })
      });
      const uploadData = await uploadRes.json();
      
      if (!uploadData.model_id) throw new Error("Upload failed.");
      
      const genRes = await fetch(`${API_URL}/api/v1/knowledge/generate-artifact`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            model_id: uploadData.model_id,
            artifact_type: "article"
        })
      });
      const genData = await genRes.json();
      
      setResult({
        model: uploadData.knowledge_model,
        artifact: genData.artifact
      });
    } catch (err: any) {
      alert("Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="max-w-4xl mx-auto py-12 px-6">
      <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Career Studio (Dry Run)</h1>
        <p className="text-gray-500 mb-6">Upload your raw knowledge to generate an AI Career Artifact.</p>
        
        <textarea 
          value={rawText}
          onChange={(e) => setRawText(e.target.value)}
          placeholder="Paste your raw project notes or resume experience here..."
          className="w-full h-40 p-4 border border-gray-200 rounded-lg mb-4 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
        />
        
        <button 
          onClick={processKnowledge}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 px-6 rounded-lg transition-colors disabled:opacity-50"
        >
          {loading ? "Processing Pipeline..." : "Extract & Generate"}
        </button>
      </div>

      {result && (
        <div className="mt-8 space-y-6">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
             <h3 className="text-xl font-bold mb-4">Article Preview</h3>
             <div 
               className="prose max-w-none"
               dangerouslySetInnerHTML={{ __html: result.artifact.html }} 
             />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
               <h3 className="text-lg font-bold mb-4">Knowledge Model JSON</h3>
               <pre className="text-xs bg-gray-50 p-4 rounded overflow-x-auto">
                 {JSON.stringify(result.model, null, 2)}
               </pre>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
               <h3 className="text-lg font-bold mb-4">Explainable AI Quality Score</h3>
               <pre className="text-xs bg-gray-50 p-4 rounded overflow-x-auto">
                 {JSON.stringify(result.artifact.quality_scores, null, 2)}
               </pre>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
