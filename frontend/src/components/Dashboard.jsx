import React from 'react'
import { Upload, Play, FileText, ArrowRight } from 'lucide-react'

export default function Dashboard({
  samples = [],
  selectedSample,
  setSelectedSample,
  uploadedFile,
  setUploadedFile,
  onAnalyze,
  loading,
  error,
  analysisResult,
  onNavigateToAnalysis
}) {
  const cleanSamples = samples.filter(s => s.category === 'CLEAN')
  const probSamples = samples.filter(s => s.category === 'PROB')

  return (
    <div>
      {/* Overview Stat Blocks */}
      <div className="stats-grid">
        <div className="stat-box">
          <div className="stat-label">Benchmark Contracts</div>
          <div className="stat-value">{samples.length}</div>
          <div className="stat-subtext">10 Clean / 10 High Risk</div>
        </div>

        <div className="stat-box">
          <div className="stat-label">Vector Store Index</div>
          <div className="stat-value">210 Clauses</div>
          <div className="stat-subtext">ChromaDB Semantic Store</div>
        </div>

        <div className="stat-box">
          <div className="stat-label">Active Analysis</div>
          <div className="stat-value">
            {analysisResult ? (
              <span style={{ color: analysisResult.summary?.is_problematic ? '#991b1b' : '#166534' }}>
                {analysisResult.summary?.overall_risk_score} / 100
              </span>
            ) : (
              '--'
            )}
          </div>
          <div className="stat-subtext">
            {analysisResult ? analysisResult.filename : 'No active document'}
          </div>
        </div>

        <div className="stat-box">
          <div className="stat-label">RAG Engine</div>
          <div className="stat-value" style={{ fontSize: '1.1rem', marginTop: '0.5rem', fontWeight: '600' }}>
            Gemini 1.5 Pro
          </div>
          <div className="stat-subtext">Contextual Reasoner</div>
        </div>
      </div>

      {/* Primary Input Panel: Upload or Select Benchmark Contract */}
      <div className="panel">
        <div className="panel-header">
          <div className="panel-title">
            <FileText size={18} />
            <span>Select or Upload Contract for Analysis</span>
          </div>
        </div>
        <div className="panel-body">
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
            {/* Left side: Benchmark Selection */}
            <div>
              <div className="form-group">
                <label className="form-label">CLEAN Contracts (Low Risk Benchmark)</label>
                <select
                  className="form-select"
                  value={selectedSample}
                  onChange={(e) => {
                    setSelectedSample(e.target.value)
                    setUploadedFile(null)
                    if (e.target.value) onAnalyze(e.target.value)
                  }}
                >
                  <option value="">-- Choose CLEAN Contract --</option>
                  {cleanSamples.map(s => (
                    <option key={s.filename} value={s.filename}>{s.filename}</option>
                  ))}
                </select>
              </div>

              <div className="form-group" style={{ marginTop: '1rem' }}>
                <label className="form-label">PROB Contracts (High Risk Benchmark)</label>
                <select
                  className="form-select"
                  value={selectedSample}
                  onChange={(e) => {
                    setSelectedSample(e.target.value)
                    setUploadedFile(null)
                    if (e.target.value) onAnalyze(e.target.value)
                  }}
                >
                  <option value="">-- Choose PROB Contract --</option>
                  {probSamples.map(s => (
                    <option key={s.filename} value={s.filename}>{s.filename}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Right side: Custom Document Dropzone */}
            <div>
              <label className="form-label">Upload Custom Document (.docx, .pdf, .txt)</label>
              <div
                className="upload-dropzone"
                onClick={() => document.getElementById('dashboard-file-input').click()}
              >
                <Upload size={24} style={{ color: '#64748b', marginBottom: '0.35rem' }} />
                <div style={{ fontWeight: '600', color: '#0f172a', fontSize: '0.85rem' }}>
                  {uploadedFile ? uploadedFile.name : 'Click to browse or drop file here'}
                </div>
                <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.2rem' }}>
                  Supports Microsoft Word (.docx), PDF, or Plain Text
                </div>
                <input
                  id="dashboard-file-input"
                  type="file"
                  accept=".docx,.pdf,.txt"
                  style={{ display: 'none' }}
                  onChange={(e) => {
                    if (e.target.files[0]) {
                      setUploadedFile(e.target.files[0])
                      setSelectedSample('')
                    }
                  }}
                />
              </div>

              {uploadedFile && (
                <button
                  className="btn btn-primary"
                  style={{ marginTop: '0.75rem', width: '100%' }}
                  onClick={() => onAnalyze()}
                  disabled={loading}
                >
                  {loading ? <span className="spinner-ring" /> : <Play size={14} />}
                  <span>Run Analysis on Uploaded File</span>
                </button>
              )}
            </div>
          </div>

          {error && (
            <div className="btn-danger" style={{ marginTop: '1rem', padding: '0.75rem', borderRadius: '4px', fontSize: '0.825rem' }}>
              {error}
            </div>
          )}
        </div>
      </div>

      {/* Active / Recent Analysis Quick Banner */}
      {analysisResult && (
        <div className="panel" style={{ borderLeft: '4px solid #0f172a' }}>
          <div className="panel-body" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: '#64748b', fontWeight: '600' }}>
                Latest Analysis Result
              </div>
              <div style={{ fontSize: '1.05rem', fontWeight: '700', color: '#0f172a', marginTop: '0.1rem' }}>
                {analysisResult.filename}
              </div>
              <div style={{ display: 'flex', gap: '0.75rem', marginTop: '0.35rem', fontSize: '0.8rem' }}>
                <span>Risk Index: <strong>{analysisResult.summary?.overall_risk_score} / 100</strong></span>
                <span>•</span>
                <span>Flagged Clauses: <strong>{analysisResult.summary?.flagged_count}</strong></span>
                <span>•</span>
                <span>Classification: <strong className={analysisResult.summary?.is_problematic ? 'badge badge-high' : 'badge badge-clean'}>{analysisResult.summary?.classification}</strong></span>
              </div>
            </div>

            <button className="btn btn-primary" onClick={onNavigateToAnalysis}>
              <span>Inspect Findings Workspace</span>
              <ArrowRight size={14} />
            </button>
          </div>
        </div>
      )}

      {/* Benchmark Contracts Quick Table */}
      <div className="panel">
        <div className="panel-header">
          <div className="panel-title">Benchmark Dataset Overview</div>
          <span style={{ fontSize: '0.75rem', color: '#64748b' }}>20 Contract Files</span>
        </div>
        <div className="table-container">
          <table className="enterprise-table">
            <thead>
              <tr>
                <th>Contract Filename</th>
                <th>Ground Truth Category</th>
                <th>Source Path</th>
                <th style={{ textAlign: 'right' }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {samples.slice(0, 8).map((s) => (
                <tr key={s.filename}>
                  <td style={{ fontWeight: '600', color: '#0f172a' }}>{s.filename}</td>
                  <td>
                    {s.category === 'CLEAN' ? (
                      <span className="badge badge-clean">CLEAN (Low Risk)</span>
                    ) : (
                      <span className="badge badge-high">PROB (High Risk)</span>
                    )}
                  </td>
                  <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: '#64748b' }}>
                    {s.relative_path}
                  </td>
                  <td style={{ textAlign: 'right' }}>
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={() => {
                        setSelectedSample(s.filename)
                        setUploadedFile(null)
                        onAnalyze(s.filename)
                      }}
                      disabled={loading}
                    >
                      Analyze
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
