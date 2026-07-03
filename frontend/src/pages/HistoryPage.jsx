import React, { useEffect, useState } from 'react'

export default function HistoryPage() {
    const [history, setHistory] = useState([])
    const [loading, setLoading] = useState(true)
    const [selected, setSelected] = useState(null)

    useEffect(() => {
        fetch('/api/analysis/history?limit=50')
            .then(r => r.ok ? r.json().catch(() => ([])) : [])
            .then(data => { setHistory(Array.isArray(data) ? data : []); setLoading(false) })
            .catch(() => setLoading(false))
    }, [])

    const fetchDetail = async (sessionId) => {
        try {
            const res = await fetch(`/api/analysis/report/${sessionId}`)
            if (res.ok) {
                try {
                    setSelected(await res.json())
                } catch(e) {}
            }
        } catch (e) { }
    }

    return (
        <div className="animate-in">
            <div className="page-header">
                <h1 className="page-title">🗂️ Analysis History</h1>
                <p className="page-subtitle">All past gemstone analysis reports · {history.length} records</p>
            </div>

            {loading ? (
                <div className="empty-state">
                    <span className="empty-state-icon">⏳</span>
                    <div className="empty-state-title">Loading history...</div>
                </div>
            ) : history.length === 0 ? (
                <div className="empty-state">
                    <span className="empty-state-icon">🔮</span>
                    <div className="empty-state-title">No scans yet</div>
                    <div className="empty-state-sub">Run your first gemstone analysis in the scanner</div>
                </div>
            ) : (
                <div className="card">
                    <table className="mineral-table" style={{ width: '100%' }}>
                        <thead>
                            <tr>
                                <th>Gem Name</th>
                                <th>Treatment</th>
                                <th>Confidence</th>
                                <th>Natural %</th>
                                <th>USD Range</th>
                                <th>Cert ID</th>
                                <th>Mode</th>
                                <th>Time</th>
                            </tr>
                        </thead>
                        <tbody>
                            {history.map((r, i) => (
                                <tr key={i} className="history-row" onClick={() => fetchDetail(r.session_id)}>
                                    <td className="mineral-name-cell">{r.mineral_name}</td>
                                    <td style={{ fontSize: 12 }}>{r.treatment_type}</td>
                                    <td style={{ color: 'var(--accent)', fontWeight: 700 }}>
                                        {(r.confidence_score * 100).toFixed(1)}%
                                    </td>
                                    <td style={{ color: 'var(--success)' }}>
                                        {(r.natural_probability * 100).toFixed(1)}%
                                    </td>
                                    <td style={{ color: 'var(--gold)', fontSize: 12 }}>
                                        ${r.price_min_usd?.toLocaleString()} – ${r.price_max_usd?.toLocaleString()}
                                    </td>
                                    <td style={{ fontFamily: 'monospace', fontSize: 11, color: 'var(--text-muted)' }}>
                                        {r.blockchain_id}
                                    </td>
                                    <td>
                                        <span style={{
                                            padding: '2px 8px', borderRadius: 12, fontSize: 11, fontWeight: 600,
                                            background: r.mode === 'lab' ? 'rgba(245,200,66,0.1)' : r.mode === 'pro' ? 'rgba(124,92,252,0.1)' : 'rgba(34,214,163,0.1)',
                                            color: r.mode === 'lab' ? 'var(--gold)' : r.mode === 'pro' ? 'var(--primary)' : 'var(--success)',
                                        }}>{r.mode}</span>
                                    </td>
                                    <td style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                                        {new Date(r.created_at).toLocaleString()}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {/* Detail Modal */}
            {selected && (
                <div
                    style={{
                        position: 'fixed', inset: 0, background: 'rgba(4,5,13,0.85)',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        zIndex: 1000, padding: 32
                    }}
                    onClick={() => setSelected(null)}
                >
                    <div
                        className="card animate-in"
                        style={{ maxWidth: 600, width: '100%', maxHeight: '80vh', overflow: 'auto' }}
                        onClick={e => e.stopPropagation()}
                    >
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
                            <div className="gem-name" style={{ fontSize: 22 }}>{selected.mineral_name}</div>
                            <button
                                style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: 18 }}
                                onClick={() => setSelected(null)}
                            >✕</button>
                        </div>
                        {[
                            ['Session ID', selected.session_id],
                            ['Blockchain ID', selected.blockchain_id],
                            ['Chemical Formula', selected.chemical_formula],
                            ['Crystal System', selected.crystal_system],
                            ['Mohs Hardness', selected.mohs_hardness],
                            ['Natural Probability', selected.natural_probability ? `${(selected.natural_probability * 100).toFixed(1)}%` : '-'],
                            ['Treatment', selected.treatment_type],
                            ['Confidence', selected.confidence_score ? `${(selected.confidence_score * 100).toFixed(1)}%` : '-'],
                            ['USD Range', selected.price_min_usd ? `$${selected.price_min_usd.toLocaleString()} – $${selected.price_max_usd?.toLocaleString()}` : '-'],
                            ['LKR Range', selected.price_min_local ? `₨${selected.price_min_local?.toLocaleString()} – ₨${selected.price_max_local?.toLocaleString()}` : '-'],
                            ['Analyzed At', selected.created_at ? new Date(selected.created_at).toLocaleString() : '-'],
                        ].map(([label, value]) => (
                            <div key={label} style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0', borderBottom: '1px solid rgba(255,255,255,0.04)', fontSize: 12 }}>
                                <span style={{ color: 'var(--text-muted)' }}>{label}</span>
                                <span style={{ color: 'var(--text-secondary)', fontFamily: label.includes('ID') ? 'monospace' : 'inherit' }}>{value}</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    )
}
