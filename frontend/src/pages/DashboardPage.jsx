import React, { useEffect, useState } from 'react'

export default function DashboardPage({ tier, onNavigate }) {
    const [history, setHistory] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetch('/api/analysis/history?limit=5')
            .then(r => r.ok ? r.json().catch(() => ([])) : [])
            .then(data => { setHistory(Array.isArray(data) ? data : []); setLoading(false) })
            .catch(() => setLoading(false))
    }, [])

    const totalScans = history.length
    const avgConf = history.length
        ? (history.reduce((s, r) => s + (r.confidence_score || 0), 0) / history.length * 100).toFixed(1)
        : '--'
    const gemNames = [...new Set(history.map(r => r.mineral_name))].length

    return (
        <div className="animate-in">
            <div className="page-header">
                <h1 className="page-title">🔬 DeepCrystal Dashboard</h1>
                <p className="page-subtitle">AI-powered mineral & gemstone forensic laboratory · Author: Sudeepa Wanigarathna</p>
            </div>

            {/* Stats */}
            <div className="dashboard-stats">
                <div className="stat-card">
                    <div className="stat-card-icon">💎</div>
                    <div className="stat-card-value">{loading ? '–' : totalScans}</div>
                    <div className="stat-card-label">Scans This Session</div>
                </div>
                <div className="stat-card">
                    <div className="stat-card-icon">🎯</div>
                    <div className="stat-card-value">{loading ? '–' : avgConf + '%'}</div>
                    <div className="stat-card-label">Avg. Confidence</div>
                </div>
                <div className="stat-card">
                    <div className="stat-card-icon">✨</div>
                    <div className="stat-card-value">{loading ? '–' : gemNames}</div>
                    <div className="stat-card-label">Unique Gems Found</div>
                </div>
                <div className="stat-card">
                    <div className="stat-card-icon">📚</div>
                    <div className="stat-card-value">30+</div>
                    <div className="stat-card-label">Database Minerals</div>
                </div>
            </div>

            {/* System Info Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 20, marginBottom: 28 }}>
                {[
                    {
                        icon: '🧠',
                        title: 'AI Models',
                        items: ['CNN: EfficientNet-B7', 'Vision Transformer', 'YOLO v8 (Inclusions)', 'GAN Anomaly Detection', 'Ensemble Regression']
                    },
                    {
                        icon: '🔬',
                        title: 'Detection Capabilities',
                        items: ['Natural vs. Synthetic', 'Heat Treatment', 'Glass/Resin Filling', 'Beryllium Diffusion', 'Fracture Detection', 'Inclusion Patterns']
                    },
                    {
                        icon: '📊',
                        title: 'Analysis Outputs',
                        items: ['Forensic Report', 'Price Estimation', 'Origin Prediction', 'Blockchain Certificate', 'QR Verification', 'Inclusion Mapping']
                    }
                ].map(({ icon, title, items }) => (
                    <div key={title} className="card">
                        <div className="section-title"><span className="section-title-icon">{icon}</span> {title}</div>
                        {items.map((item, i) => (
                            <div key={i} style={{ fontSize: 12, color: 'var(--text-secondary)', padding: '4px 0', borderBottom: '1px solid rgba(255,255,255,0.04)' }}>
                                ✓ {item}
                            </div>
                        ))}
                    </div>
                ))}
            </div>

            {/* Quick Start */}
            <div className="card" style={{ marginBottom: 24 }}>
                <div className="section-title"><span className="section-title-icon">🚀</span> Quick Start</div>
                <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }}>
                    {[
                        { label: '💎 Scan a Gemstone', desc: 'Upload image + manual inputs', page: 'scan' },
                        { label: '📚 Browse Minerals', desc: 'Search 30+ gem database', page: 'database' },
                        { label: '🗂️ View History', desc: 'Past analysis reports', page: 'history' },
                    ].map(({ label, desc, page }) => (
                        <div
                            key={page}
                            className="card"
                            style={{ flex: 1, minWidth: 200, cursor: 'pointer', background: 'rgba(124,92,252,0.06)', border: '1px solid var(--border-glow)' }}
                            onClick={() => onNavigate(page)}
                        >
                            <div style={{ fontSize: 15, fontWeight: 600, marginBottom: 4 }}>{label}</div>
                            <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>{desc}</div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Recent History */}
            {history.length > 0 && (
                <div className="card">
                    <div className="section-title"><span className="section-title-icon">🕐</span> Recent Scans</div>
                    <table className="mineral-table" style={{ width: '100%' }}>
                        <thead>
                            <tr>
                                <th>Gem</th>
                                <th>Treatment</th>
                                <th>Confidence</th>
                                <th>USD Range</th>
                                <th>Time</th>
                            </tr>
                        </thead>
                        <tbody>
                            {history.map((r, i) => (
                                <tr key={i}>
                                    <td className="mineral-name-cell">{r.mineral_name}</td>
                                    <td>{r.treatment_type}</td>
                                    <td style={{ color: 'var(--accent)', fontWeight: 700 }}>{(r.confidence_score * 100).toFixed(1)}%</td>
                                    <td>${r.price_min_usd?.toLocaleString()} – ${r.price_max_usd?.toLocaleString()}</td>
                                    <td style={{ color: 'var(--text-muted)', fontSize: 11 }}>{new Date(r.created_at).toLocaleTimeString()}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            <div className="disclaimer" style={{ marginTop: 24 }}>
                <span className="disclaimer-icon">⚠️</span>
                <div className="disclaimer-text">
                    <strong>Cerberus DeepCrystal v1.0</strong> · AI Screening System by Sudeepa Wanigarathna.
                    For high-value transactions, professional laboratory testing is recommended.
                </div>
            </div>
        </div>
    )
}
