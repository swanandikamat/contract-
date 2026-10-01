import React, { useState, useEffect } from 'react'
import axios from 'axios'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import Dashboard from './components/Dashboard'
import ClauseInspector from './components/ClauseInspector'
import DatasetView from './components/DatasetView'

const API_BASE = '/api/v1'

export default function App() {
  const [currentTab, setCurrentTab] = useState('dashboard')
  const [samples, setSamples] = useState([])
  const [selectedSample, setSelectedSample] = useState('')
  const [uploadedFile, setUploadedFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [backendConnected, setBackendConnected] = useState(true)

  useEffect(() => {
    fetchSamples()
  }, [])

  const fetchSamples = async () => {
    setError(null)
    try {
      let res
      try {
        res = await axios.get(`${API_BASE}/samples`)
      } catch {
        res = await axios.get('http://127.0.0.1:8000/api/v1/samples')
      }
      setSamples(res.data || [])
      setBackendConnected(true)
    } catch (err) {
      console.error('Failed to load sample dataset:', err)
      setBackendConnected(false)
    }
  }

  const handleAnalyze = async (sampleNameOverride = null) => {
    const sampleToRun = sampleNameOverride || selectedSample
    if (!uploadedFile && !sampleToRun) {
      setError('Please select a benchmark contract from the dataset or upload a document.')
      return
    }

    setLoading(true)
    setError(null)

    try {
      let res
      const base = API_BASE
      if (uploadedFile) {
        const formData = new FormData()
        formData.append('file', uploadedFile)
        try {
          res = await axios.post(`${base}/analyze`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
        } catch {
          res = await axios.post('http://127.0.0.1:8000/api/v1/analyze', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
        }
      } else {
        try {
          res = await axios.post(`${base}/analyze?sample_filename=${encodeURIComponent(sampleToRun)}`)
        } catch {
          res = await axios.post(`http://127.0.0.1:8000/api/v1/analyze?sample_filename=${encodeURIComponent(sampleToRun)}`)
        }
      }
      setAnalysisResult(res.data)
      // Switch automatically to Analysis Workspace after successful run
      setCurrentTab('analysis')
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Analysis failed. Ensure FastAPI backend is running on http://127.0.0.1:8000.'
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-layout">
      {/* Sidebar Navigation */}
      <Sidebar
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
        backendConnected={backendConnected}
        sampleCount={samples.length}
        onRetryBackend={fetchSamples}
      />

      {/* Main Content Area */}
      <div className="main-wrapper">
        <Header
          currentTab={currentTab}
          backendConnected={backendConnected}
          activeFilename={analysisResult?.filename}
        />

        <main className="content-body">
          {/* Global Loading Spinner Banner */}
          {loading && (
            <div className="panel" style={{ padding: '2.5rem', textAlign: 'center' }}>
              <div className="spinner-ring" style={{ width: '28px', height: '28px', margin: '0 auto 1rem auto' }} />
              <h3 style={{ fontSize: '1rem', fontWeight: '600', color: '#0f172a' }}>
                Executing RAG + LLM Risk Analysis...
              </h3>
              <p style={{ fontSize: '0.8rem', color: '#64748b', marginTop: '0.25rem' }}>
                Parsing document clauses $\rightarrow$ Embedding vectors $\rightarrow$ Searching ChromaDB $\rightarrow$ Synthesizing LLM context
              </p>
            </div>
          )}

          {/* Main View Router */}
          {!loading && (
            <>
              {currentTab === 'dashboard' && (
                <Dashboard
                  samples={samples}
                  selectedSample={selectedSample}
                  setSelectedSample={setSelectedSample}
                  uploadedFile={uploadedFile}
                  setUploadedFile={setUploadedFile}
                  onAnalyze={handleAnalyze}
                  loading={loading}
                  error={error}
                  analysisResult={analysisResult}
                  onNavigateToAnalysis={() => setCurrentTab('analysis')}
                />
              )}

              {currentTab === 'analysis' && (
                <ClauseInspector
                  analysisResult={analysisResult}
                />
              )}

              {currentTab === 'dataset' && (
                <DatasetView
                  samples={samples}
                  onAnalyze={(filename) => handleAnalyze(filename)}
                  setSelectedSample={setSelectedSample}
                  loading={loading}
                />
              )}
            </>
          )}
        </main>
      </div>
    </div>
  )
}
