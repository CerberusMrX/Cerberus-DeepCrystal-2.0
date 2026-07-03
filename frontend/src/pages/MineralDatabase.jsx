import React, { useState, useEffect } from 'react'

export default function MineralDatabase() {
    const [minerals, setMinerals] = useState([])
    const [query, setQuery] = useState('')
    const [loading, setLoading] = useState(false)
    const [selected, setSelected] = useState(null)
    const [seeded, setSeeded] = useState(false)

    const fetchMinerals = async (q = '') => {
        setLoading(true)
        try {
            const url = q ? `/api/database/search?q=${encodeURIComponent(q)}&limit=50` : '/api/database/?limit=50'
            const res = await fetch(url)
            if (res.ok) {
                try {
                    const data = await res.json()
                    setMinerals(data)
                    setSeeded(true)
                } catch(e) {}
            }
        } catch (e) { }
        setLoading(false)
    }

    useEffect(() => { fetchMinerals() }, [])

    const handleSearch = (e) => {
        e.preventDefault()
        fetchMinerals(query)
    }

    const fetchDetail = async (name) => {
        try {
            const res = await fetch(`/api/database/${encodeURIComponent(name)}`)
            if (res.ok) {
                try {
                    setSelected(await res.json())
                } catch(e) {}
            }
        } catch (e) { }
    }

    const seedDB = async () => {
        setLoading(true)
        try {
            // Trigger the seed by calling backend init
            await fetch('/api/database/?limit=1')
            await fetchMinerals()
        } catch (e) { }
        setLoading(false)
    }

    return (
        <div className="animate-in">
            <div className="page-header">
                <h1 className="page-title">📚 Mineral Database</h1>
                <p className="page-subtitle">Comprehensive gemstone & mineral reference library · {minerals.length} records loaded</p>
            </div>

            <form className="db-search-bar" onSubmit={handleSearch}>
                <input
                    className="db-search-input"
                    placeholder="Search by name, chemical formula, crystal system..."
                    value={query}
                    onChange={e => setQuery(e.target.value)}
                />
                <button type="submit" className="db-filter-btn">🔍 Search</button>
                <button type="button" className="db-filter-btn" onClick={() => { setQuery(''); fetchMinerals('') }}>
                    Reset
                </button>
            </form>

            <div style={{ display: 'grid', gridTemplateColumns: selected ? '1fr 1fr' : '1fr', gap: 20 }}>
                {/* Table */}
                <div className="card" style={{ overflow: 'auto' }}>
                    {loading ? (
                        <div className="empty-state">
                            <span className="empty-state-icon">⏳</span>
                            <div className="empty-state-title">Loading database...</div>
                        </div>
                    ) : minerals.length === 0 ? (
                        <div className="empty-state">
                            <span className="empty-state-icon">📚</span>
                            <div className="empty-state-title">No minerals found</div>
                            <div className="empty-state-sub">Seed the database by running a scan first</div>
                        </div>
                    ) : (
                        <table className="mineral-table">
                            <thead>
                                <tr>
                                    <th>Mineral / Gem</th>
                                    <th>Formula</th>
                                    <th>Crystal System</th>
                                    <th>Mohs</th>
                                    <th>Category</th>
                                    <th>Price (USD/ct)</th>
                                </tr>
                            </thead>
                            <tbody>
                                {minerals.map((m, i) => (
                                    <tr key={i} className="history-row" onClick={() => fetchDetail(m.name || m.mineral_name)}>
                                        <td className="mineral-name-cell">{m.name || m.mineral_name}</td>
                                        <td className="formula-cell">{m.chemical_formula || m.formula}</td>
                                        <td>{m.crystal_system}</td>
                                        <td>{m.mohs_hardness}</td>
                                        <td>{m.category}</td>
                                        <td style={{ color: 'var(--success)', fontWeight: 600 }}>{m.price_range || 'N/A'}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                </div>

                {/* Detail Panel */}
                {selected && (
                    <div className="card animate-in">
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
                            <div className="gem-name" style={{ fontSize: 24 }}>{selected.name}</div>
                            <button
                                style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: 18 }}
                                onClick={() => setSelected(null)}
                            >✕</button>
                        </div>
                        <div className="formula-cell" style={{ marginBottom: 12 }}>{selected.chemical_formula}</div>

                        {[
                            ['Crystal System', selected.crystal_system],
                            ['Mohs Hardness', selected.mohs_hardness],
                            ['Specific Gravity', selected.specific_gravity],
                            ['Refractive Index', selected.refractive_index],
                            ['Luster', selected.luster],
                            ['Cleavage', selected.cleavage],
                            ['Fracture', selected.fracture],
                            ['Streak', selected.streak],
                            ['Transparency', selected.transparency],
                            ['Geological Class', selected.geological_class],
                            ['UV Fluorescence', selected.uv_fluorescence],
                            ['Known Origins', selected.known_origins],
                            ['Common Treatments', selected.common_treatments],
                            ['Synthetic Methods', selected.synthetic_methods],
                            ['Price Range', selected.price_range],
                        ].filter(([, v]) => v && v !== 'N/A').map(([label, value]) => (
                            <div key={label} style={{
                                display: 'flex', justifyContent: 'space-between', padding: '6px 0',
                                borderBottom: '1px solid rgba(255,255,255,0.04)', fontSize: 12
                            }}>
                                <span style={{ color: 'var(--text-muted)', fontWeight: 500 }}>{label}</span>
                                <span style={{ color: 'var(--text-secondary)', textAlign: 'right', maxWidth: '60%' }}>{value}</span>
                            </div>
                        ))}

                        {selected.description && (
                            <div style={{ marginTop: 12, padding: 12, background: 'rgba(255,255,255,0.02)', borderRadius: 8, fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.6 }}>
                                {selected.description}
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    )
}
