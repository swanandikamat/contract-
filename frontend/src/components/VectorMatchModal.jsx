import React from 'react'
import { X, Search, Database } from 'lucide-react'

export default function VectorMatchModal({ clause, onClose }) {
  if (!clause) return null

  const matches = clause.vector_matches || []

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-box" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Database size={16} style={{ color: '#0f172a' }} />
            <h3 style={{ fontSize: '0.95rem', fontWeight: '600', color: '#0f172a' }}>
              ChromaDB Semantic Vector Matches ({clause.clause_id})
            </h3>
          </div>
          <button
            onClick={onClose}
            style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#64748b', display: 'flex', alignItems: 'center' }}
          >
            <X size={18} />
          </button>
        </div>

        <div className="modal-body">
          <p style={{ fontSize: '0.8rem', color: '#64748b', marginBottom: '1rem' }}>
            Top semantically similar reference clauses retrieved from ChromaDB collection indexed from 20 benchmark contracts:
          </p>

          {matches.length === 0 ? (
            <div className="empty-state" style={{ padding: '2rem 1rem' }}>
              <Search size={24} className="empty-state-icon" />
              <div className="empty-state-title">No Vector Matches Found</div>
              <div className="empty-state-desc">No semantically similar clauses were retrieved above the distance threshold.</div>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              {matches.map((m, idx) => {
                const meta = m.metadata || {}
                const isProb = meta.ground_truth_label === 'PROB'
                const simPct = Math.round((m.similarity_score || 0) * 100)

                return (
                  <div
                    key={idx}
                    style={{
                      border: '1px solid #e2e8f0',
                      borderRadius: '4px',
                      padding: '0.85rem',
                      backgroundColor: isProb ? '#fef2f2' : '#f0fdf4'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                        {isProb ? (
                          <span className="badge badge-high">Reference PROB Risk Clause</span>
                        ) : (
                          <span className="badge badge-clean">Reference CLEAN Clause</span>
                        )}
                        <span style={{ fontSize: '0.75rem', color: '#64748b' }}>
                          • Source: {meta.source_filename}
                        </span>
                      </div>
                      <span className="badge badge-neutral" style={{ fontSize: '0.725rem' }}>
                        Similarity: {simPct}%
                      </span>
                    </div>

                    <div className="verbatim-quote-box" style={{ marginTop: '0', backgroundColor: '#ffffff', borderLeftColor: isProb ? '#fca5a5' : '#bbf7d0' }}>
                      "{m.text}"
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>

        <div className="modal-footer">
          <button className="btn btn-secondary btn-sm" onClick={onClose}>
            Close Window
          </button>
        </div>
      </div>
    </div>
  )
}
