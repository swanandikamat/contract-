import React, { useState } from 'react'
import { AlertTriangle, CheckCircle, Database, MapPin, Search, FileText } from 'lucide-react'
import VectorMatchModal from './VectorMatchModal'

export default function ClauseInspector({ analysisResult }) {
  const [activeModalClause, setActiveModalClause] = useState(null)
  const [selectedClauseId, setSelectedClauseId] = useState(null)
  const [filterCategory, setFilterCategory] = useState('ALL') // ALL, HIGH, MED, CLEAN
  const [searchQuery, setSearchQuery] = useState('')

  if (!analysisResult) {
    return (
      <div className="panel">
        <div className="empty-state">
          <FileText size={40} className="empty-state-icon" />
          <div className="empty-state-title">No Contract Analysis Loaded</div>
          <div className="empty-state-desc">
            Select a benchmark dataset contract or upload a document to begin analysis.
          </div>
        </div>
      </div>
    )
  }

  const { filename, character_count, clause_count, summary = {}, clauses = [] } = analysisResult
  
  // Set default selected clause if none
  const currentSelectedClause = clauses.find(c => c.clause_id === selectedClauseId) || clauses[0] || null

  // Filter clauses based on severity and search query
  const filteredClauses = clauses.filter(c => {
    const analysis = c.analysis || {}
    const severity = (analysis.severity || 'NONE').toUpperCase()
    
    // Category filter
    if (filterCategory === 'HIGH' && severity !== 'HIGH') return false
    if (filterCategory === 'MED' && severity !== 'MEDIUM') return false
    if (filterCategory === 'CLEAN' && analysis.is_risky) return false

    // Search filter
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase()
      const matchHeader = c.header?.toLowerCase().includes(q)
      const matchText = c.text?.toLowerCase().includes(q)
      const matchCategory = analysis.category?.toLowerCase().includes(q)
      return matchHeader || matchText || matchCategory
    }
    return true
  })

  // Risk category aggregations
  const highRiskCount = clauses.filter(c => c.analysis?.severity === 'HIGH').length
  const medRiskCount = clauses.filter(c => c.analysis?.severity === 'MEDIUM').length
  const cleanCount = clauses.filter(c => !c.analysis?.is_risky).length

  return (
    <div>
      {/* Top Executive Summary Panel */}
      <div className="panel">
        <div className="panel-header">
          <div className="panel-title">
            <span>Executive Risk Summary ({filename})</span>
          </div>
          <span className="badge badge-neutral">
            {character_count.toLocaleString()} Characters • {clause_count} Clauses
          </span>
        </div>
        <div className="panel-body">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem', marginBottom: '1.25rem' }}>
            <div className="stat-box" style={{ borderLeft: '3px solid #0f172a' }}>
              <div className="stat-label">Overall Risk Score</div>
              <div className="stat-value" style={{ color: summary.is_problematic ? '#991b1b' : '#166534' }}>
                {summary.overall_risk_score} / 100
              </div>
              <div className="stat-subtext">Composite RAG Index</div>
            </div>

            <div className="stat-box" style={{ borderLeft: '3px solid #cbd5e1' }}>
              <div className="stat-label">Classification</div>
              <div style={{ marginTop: '0.4rem' }}>
                {summary.is_problematic ? (
                  <span className="badge badge-high"><AlertTriangle size={12} /> {summary.classification}</span>
                ) : (
                  <span className="badge badge-clean"><CheckCircle size={12} /> {summary.classification}</span>
                )}
              </div>
              <div className="stat-subtext">Ground Truth Category</div>
            </div>

            <div className="stat-box" style={{ borderLeft: '3px solid #cbd5e1' }}>
              <div className="stat-label">Risk Breakdown</div>
              <div style={{ display: 'flex', gap: '0.4rem', marginTop: '0.4rem' }}>
                <span className="badge badge-high">{highRiskCount} High</span>
                <span className="badge badge-med">{medRiskCount} Med</span>
                <span className="badge badge-clean">{cleanCount} Clean</span>
              </div>
              <div className="stat-subtext">Total Flagged: {summary.flagged_count}</div>
            </div>
          </div>

          <div style={{ backgroundColor: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '4px', padding: '0.85rem 1rem', fontSize: '0.85rem', color: '#334155', lineHeight: '1.6' }}>
            <strong style={{ color: '#0f172a', display: 'block', marginBottom: '0.2rem' }}>RAG Contextual Assessment Rationale:</strong>
            {summary.summary}
          </div>
        </div>
      </div>

      {/* Two-Column Inspector Workspace */}
      <div className="analysis-workspace">
        {/* LEFT COLUMN: Clause Directory & Search Filter */}
        <div className="clause-nav-panel">
          <div className="clause-nav-header">
            <span>Clause Directory ({filteredClauses.length})</span>
            <span style={{ fontSize: '0.75rem', color: '#64748b' }}>Total {clauses.length}</span>
          </div>

          <div style={{ padding: '0.75rem', borderBottom: '1px solid #e2e8f0', backgroundColor: '#ffffff' }}>
            {/* Category Filter Tabs */}
            <div className="filter-tabs">
              <button
                className={`tab-btn ${filterCategory === 'ALL' ? 'active' : ''}`}
                onClick={() => setFilterCategory('ALL')}
              >
                All ({clauses.length})
              </button>
              <button
                className={`tab-btn ${filterCategory === 'HIGH' ? 'active' : ''}`}
                onClick={() => setFilterCategory('HIGH')}
              >
                High ({highRiskCount})
              </button>
              <button
                className={`tab-btn ${filterCategory === 'MED' ? 'active' : ''}`}
                onClick={() => setFilterCategory('MED')}
              >
                Med ({medRiskCount})
              </button>
              <button
                className={`tab-btn ${filterCategory === 'CLEAN' ? 'active' : ''}`}
                onClick={() => setFilterCategory('CLEAN')}
              >
                Clean ({cleanCount})
              </button>
            </div>

            {/* Search Input */}
            <div style={{ position: 'relative' }}>
              <Search size={14} style={{ position: 'absolute', left: '0.6rem', top: '0.55rem', color: '#94a3b8' }} />
              <input
                type="text"
                className="form-input"
                style={{ paddingLeft: '2rem', fontSize: '0.8rem' }}
                placeholder="Search clause text or header..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>

          <div className="clause-nav-list">
            {filteredClauses.length === 0 ? (
              <div style={{ padding: '1.5rem', textAlign: 'center', color: '#94a3b8', fontSize: '0.8rem' }}>
                No clauses match the selected filter.
              </div>
            ) : (
              filteredClauses.map((c) => {
                const analysis = c.analysis || {}
                const isRisky = analysis.is_risky
                const severity = analysis.severity || 'NONE'
                const isSelected = currentSelectedClause && currentSelectedClause.clause_id === c.clause_id

                return (
                  <div
                    key={c.clause_id}
                    className={`clause-nav-item ${isSelected ? 'active' : ''}`}
                    onClick={() => setSelectedClauseId(c.clause_id)}
                  >
                    <div>
                      <div className="clause-nav-title">
                        [{c.clause_id}] {c.header}
                      </div>
                      <div className="clause-nav-meta">
                        Page {c.page_number} • {analysis.category || 'General'}
                      </div>
                    </div>

                    <div>
                      {isRisky ? (
                        <span className={`badge ${severity === 'HIGH' ? 'badge-high' : 'badge-med'}`}>
                          {severity}
                        </span>
                      ) : (
                        <span className="badge badge-clean">CLEAN</span>
                      )}
                    </div>
                  </div>
                )
              })
            )}
          </div>
        </div>

        {/* RIGHT COLUMN: Clause Findings Detail & Grounded Evidence */}
        <div>
          {currentSelectedClause ? (
            <div className="clause-detail-card">
              <div className="clause-detail-header">
                <div>
                  <span style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: '#64748b', fontWeight: '600', letterSpacing: '0.05em' }}>
                    Section {currentSelectedClause.page_number} • {currentSelectedClause.clause_id}
                  </span>
                  <h3 style={{ fontSize: '1.1rem', fontWeight: '700', color: '#0f172a', marginTop: '0.1rem' }}>
                    {currentSelectedClause.header}
                  </h3>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  {currentSelectedClause.analysis?.is_risky ? (
                    <span className={`badge ${currentSelectedClause.analysis?.severity === 'HIGH' ? 'badge-high' : 'badge-med'}`}>
                      {currentSelectedClause.analysis?.severity} RISK
                    </span>
                  ) : (
                    <span className="badge badge-clean">CLEAN</span>
                  )}

                  <span className="badge badge-neutral">
                    Confidence: {Math.round((currentSelectedClause.analysis?.confidence_score || 0.8) * 100)}%
                  </span>

                  <button
                    className="btn btn-secondary btn-sm"
                    onClick={() => setActiveModalClause(currentSelectedClause)}
                  >
                    <Database size={12} />
                    <span>Vector Matches ({currentSelectedClause.vector_matches?.length || 0})</span>
                  </button>
                </div>
              </div>

              {/* Verbatim Document Language & Location */}
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.35rem' }}>
                  <span style={{ fontSize: '0.8rem', fontWeight: '600', color: '#0f172a' }}>
                    Verbatim Document Language
                  </span>
                  <span style={{ fontSize: '0.75rem', color: '#64748b', display: 'flex', alignItems: 'center', gap: '0.2rem' }}>
                    <MapPin size={12} /> Page {currentSelectedClause.page_number}
                  </span>
                </div>
                <div className="verbatim-quote-box">
                  "{currentSelectedClause.text}"
                </div>
              </div>

              {/* Risk Analysis Rationale */}
              <div className="rationale-box">
                <span style={{ fontSize: '0.8rem', fontWeight: '600', color: '#0f172a', display: 'block', marginBottom: '0.25rem' }}>
                  Contextual Risk Reasoning & Defect Analysis:
                </span>
                <p style={{ fontSize: '0.85rem', color: '#334155', lineHeight: '1.5' }}>
                  {currentSelectedClause.analysis?.explanation}
                </p>

                {currentSelectedClause.analysis?.defect_type && (
                  <div style={{ marginTop: '0.5rem', fontSize: '0.785rem', color: '#64748b' }}>
                    <strong>Flagged Defect Category:</strong> {currentSelectedClause.analysis.defect_type}
                  </div>
                )}
              </div>

              {/* Suggested Redline */}
              {currentSelectedClause.analysis?.suggested_redline && (
                <div className="redline-section">
                  <strong style={{ display: 'block', marginBottom: '0.25rem', color: '#166534' }}>
                    Suggested Redline / Recommended Amendment:
                  </strong>
                  {currentSelectedClause.analysis.suggested_redline}
                </div>
              )}
            </div>
          ) : (
            <div className="panel">
              <div className="empty-state">
                <div className="empty-state-title">Select a clause from the directory</div>
                <div className="empty-state-desc">Choose any clause on the left to inspect verbatim quotes and RAG evidence.</div>
              </div>
            </div>
          )}
        </div>
      </div>

      {activeModalClause && (
        <VectorMatchModal
          clause={activeModalClause}
          onClose={() => setActiveModalClause(null)}
        />
      )}
    </div>
  )
}
