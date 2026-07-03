import React, { useEffect, useState } from 'react'

const COUNTRY_FLAGS = {
    'Myanmar': '🇲🇲', 'Sri Lanka': '🇱🇰', 'Mozambique': '🇲🇿', 'Thailand': '🇹🇭',
    'Madagascar': '🇲🇬', 'Kashmir': '🇮🇳', 'Colombia': '🇨🇴', 'Zambia': '🇿🇲',
    'Brazil': '🇧🇷', 'Zimbabwe': '🇿🇼', 'Tanzania': '🇹🇿', 'Russia': '🇷🇺',
    'Russia (Ural)': '🇷🇺', 'Canada': '🇨🇦', 'South Africa': '🇿🇦', 'Australia': '🇦🇺',
    'Botswana': '🇧🇼', 'Kenya': '🇰🇪', 'Nigeria': '🇳🇬', 'Pakistan': '🇵🇰',
    'Vietnam': '🇻🇳', 'Afghanistan': '🇦🇫', 'India': '🇮🇳', 'USA': '🇺🇸',
    'Other': '🌍', 'Worldwide': '🌍', 'Tanzania (Merelani)': '🇹🇿',
    'Brazil (Paraíba)': '🇧🇷',
}

function ConfidenceMeter({ value }) {
    const pct = Math.round(value * 100)
    const r = 56
    const circ = 2 * Math.PI * r
    const dashOffset = circ * (1 - value)
    const color = value > 0.85 ? '#22d6a3' : value > 0.65 ? '#7c5cfc' : '#ffb347'

    return (
        <div className="confidence-meter">
            <svg width="140" height="140" viewBox="0 0 140 140">
                <circle cx="70" cy="70" r={r} fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="10" />
                <circle
                    cx="70" cy="70" r={r}
                    fill="none"
                    stroke={color}
                    strokeWidth="10"
                    strokeDasharray={circ}
                    strokeDashoffset={dashOffset}
                    strokeLinecap="round"
                    style={{ filter: `drop-shadow(0 0 8px ${color})`, transition: 'stroke-dashoffset 1s ease' }}
                />
            </svg>
            <div className="confidence-center">
                <span className="confidence-value">{pct}%</span>
                <span className="confidence-label">Confidence</span>
            </div>
        </div>
    )
}

function ProgressBar({ label, value, className }) {
    return (
        <div className="progress-item">
            <div className="progress-header">
                <span className="progress-name">{label}</span>
                <span className="progress-val">{(value * 100).toFixed(1)}%</span>
            </div>
            <div className="progress-track">
                <div
                    className={`progress-fill ${className}`}
                    style={{ width: `${value * 100}%` }}
                />
            </div>
        </div>
    )
}

export default function ReportDashboard({ report }) {
    const [visible, setVisible] = useState(false)
    useEffect(() => { setTimeout(() => setVisible(true), 100) }, [report])

    if (!report) return null

    const t = report.treatment_analysis || {}
    const inc = report.inclusion_analysis || {}
    const crack = report.crack_assessment || {}
    const price = report.price_estimation || {}
    const origins = report.origin_predictions || []

    const inclItems = [
        ['curved_growth_lines', 'Curved Growth Lines'],
        ['gas_bubbles', 'Gas Bubbles'],
        ['rutile_silk', 'Rutile Silk'],
        ['fracture_filling', 'Fracture Filling'],
        ['flame_fusion_indicators', 'Flame Fusion'],
        ['heat_treatment_markers', 'Heat Treatment Markers'],
        ['fingerprint_inclusions', 'Fingerprint Inclusions'],
        ['needles', 'Needles'],
        ['crystals', 'Crystals'],
        ['feathers', 'Feathers'],
    ]

    return (
        <div className={`animate-in`} style={{ opacity: visible ? 1 : 0, transition: 'opacity 0.4s' }}>
            {/* ── Blockchain Cert Banner ── */}
            <div className="cert-card" style={{ marginBottom: 20 }}>
                <span className="cert-icon">🔐</span>
                <div style={{ flex: 1 }}>
                    <div className="cert-label">Cerberus DeepCrystal Blockchain Certificate</div>
                    <div className="cert-id">{report.blockchain_id}</div>
                    <div className="cert-hash">SHA-256: Session {report.session_id?.slice(0, 16)}...</div>
                </div>
                {report.qr_code_url ? (
                    <img src={report.qr_code_url} alt="QR Code" className="qr-img" />
                ) : (
                    <div className="qr-fallback">📱</div>
                )}
            </div>

            {/* ── Gem Identity Banner ── */}
            <div className="gem-banner" style={{ marginBottom: 20 }}>
                <div className="gem-name">{report.mineral_name}</div>
                <div className="gem-formula">{report.chemical_formula}</div>
                <div className="gem-tags">
                    <span className="gem-tag tag-system">⬡ {report.crystal_system}</span>
                    <span className="gem-tag tag-class">{report.geological_class}</span>
                    {report.natural_probability > 0.6
                        ? <span className="gem-tag tag-nat">✓ Likely Natural</span>
                        : <span className="gem-tag tag-synth">⚠ Possible Synthetic</span>
                    }
                    <span className="gem-tag tag-category">Mohs {report.mohs_hardness}</span>
                </div>
            </div>

            <div className="report-grid">
                {/* ── Physical Properties ── */}
                <div className="card">
                    <div className="section-title"><span className="section-title-icon">🧪</span> Physical Properties</div>
                    <div className="stat-grid">
                        <div className="stat-chip">
                            <div className="stat-value">{report.mohs_hardness}</div>
                            <div className="stat-label">Mohs Hardness</div>
                        </div>
                        <div className="stat-chip">
                            <div className="stat-value">{report.specific_gravity}</div>
                            <div className="stat-label">Specific Gravity</div>
                        </div>
                        <div className="stat-chip">
                            <div className="stat-value" style={{ fontSize: 13 }}>{report.optical_properties?.refractive_index || 'N/A'}</div>
                            <div className="stat-label">Refractive Index</div>
                        </div>
                        <div className="stat-chip">
                            <div className="stat-value" style={{ fontSize: 13 }}>{report.optical_properties?.luster || 'N/A'}</div>
                            <div className="stat-label">Luster</div>
                        </div>
                        <div className="stat-chip" style={{ gridColumn: '1 / -1' }}>
                            <div className="stat-value" style={{ fontSize: 13 }}>{report.optical_properties?.transparency || 'N/A'}</div>
                            <div className="stat-label">Transparency</div>
                        </div>
                    </div>
                    
                    {report.color_analysis && (
                        <div style={{ marginTop: 24, padding: '16px', background: 'rgba(255,255,255,0.03)', borderRadius: 12 }}>
                            <div className="section-title" style={{ fontSize: 12, marginBottom: 8 }}>🎨 Computer Vision Color Analysis</div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                                <div className="color-palette">
                                    {report.color_analysis.palette_hex.map((c, i) => (
                                        <div key={i} className="color-swatch" style={{ background: c }} title={`Color ${i+1}: ${c}`} />
                                    ))}
                                </div>
                                <div style={{ flex: 1 }}>
                                    <div style={{ fontSize: 12, color: 'var(--text-secondary)' }}>
                                        {report.color_analysis.description}
                                    </div>
                                    <div className="color-score-bar">
                                        <div className="color-score-fill" style={{ width: `${report.color_analysis.color_quality_score * 100}%` }} />
                                    </div>
                                    <div style={{ fontSize: 10, color: 'var(--text-muted)', marginTop: 4, textAlign: 'right' }}>
                                        Color Quality Factor: {(report.color_analysis.color_quality_score).toFixed(2)}x
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                    
                    <div style={{ marginTop: 16 }}>
                        <div className="section-title"><span className="section-title-icon">🔬</span> AI Methods Used</div>
                        <div className="method-tags">
                            {(report.method_used || []).map((m, i) => (
                                <span key={i} className="method-tag">{m}</span>
                            ))}
                        </div>
                    </div>
                </div>

                {/* ── Confidence ── */}
                <div className="card" style={{ textAlign: 'center' }}>
                    <div className="section-title" style={{ justifyContent: 'center' }}>
                        <span className="section-title-icon">🎯</span> Confidence Score
                    </div>
                    <ConfidenceMeter value={report.confidence_score} />
                    <div style={{ marginTop: 16 }}>
                        <div className="section-title" style={{ justifyContent: 'center', marginBottom: 12 }}>
                            Natural / Synthetic
                        </div>
                        <ProgressBar label="Natural" value={report.natural_probability} className="fill-natural" />
                        <ProgressBar label="Synthetic" value={report.synthetic_probability} className="fill-synthetic" />
                    </div>
                </div>

                {/* ── Treatment Analysis ── */}
                <div className="card">
                    <div className="section-title"><span className="section-title-icon">⚗️</span> Treatment Analysis</div>
                    <div style={{ marginBottom: 12, padding: '6px 12px', background: 'rgba(255,255,255,0.03)', borderRadius: 8, fontSize: 13, fontWeight: 600 }}>
                        Dominant: <span style={{ color: 'var(--accent)' }}>{t.dominant_treatment}</span>
                    </div>
                    <div className="progress-list">
                        <ProgressBar label="Natural (Untreated)" value={t.natural || 0} className="fill-natural" />
                        <ProgressBar label="Heat Treated" value={t.heat_treated || 0} className="fill-heat" />
                        <ProgressBar label="Glass Filled" value={t.glass_filled || 0} className="fill-glass" />
                        <ProgressBar label="Beryllium Diffusion" value={t.diffusion_treated || 0} className="fill-diffusion" />
                        <ProgressBar label="Resin Filled" value={t.resin_filled || 0} className="fill-other" />
                        <ProgressBar label="Laser Drilled" value={t.laser_drilled || 0} className="fill-other" />
                        <ProgressBar label="Coated" value={t.coated || 0} className="fill-other" />
                        <ProgressBar label="Synthetic" value={t.synthetic || 0} className="fill-synthetic" />
                    </div>
                </div>

                {/* ── Price Estimation ── */}
                <div className="card">
                    <div className="section-title"><span className="section-title-icon">💰</span> Market Value Estimate</div>
                    <div className="price-panel" style={{ marginBottom: 16 }}>
                        <div className="price-box price-usd">
                            <div className="price-currency">USD (International)</div>
                            <div className="price-range-val">${(price.min_usd || 0).toLocaleString()} – ${(price.max_usd || 0).toLocaleString()}</div>
                            <div style={{ fontSize: 10, color: 'var(--text-muted)', marginTop: 4 }}>per carat</div>
                        </div>
                        <div className="price-box price-lkr">
                            <div className="price-currency">LKR (Local)</div>
                            <div className="price-range-val">₨{(price.min_local || 0).toLocaleString()} – ₨{(price.max_local || 0).toLocaleString()}</div>
                            <div style={{ fontSize: 10, color: 'var(--text-muted)', marginTop: 4 }}>per carat</div>
                        </div>
                    </div>
                    <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>
                        <div className="section-title" style={{ fontSize: 11, marginBottom: 8 }}>Pricing Factors</div>
                        {(price.factors || []).map((f, i) => (
                            <div key={i} style={{ marginBottom: 4, padding: '4px 8px', background: 'rgba(255,255,255,0.02)', borderRadius: 4 }}>• {f}</div>
                        ))}
                    </div>
                </div>

                {/* ── Origin Prediction ── */}
                <div className="card">
                    <div className="section-title"><span className="section-title-icon">🌍</span> Origin Prediction</div>
                    <div className="origin-list">
                        {origins.map((o, i) => (
                            <div key={i} className="origin-item">
                                <span className="origin-flag">{COUNTRY_FLAGS[o.country] || '🌍'}</span>
                                <span className="origin-name">{o.country}</span>
                                <div className="progress-track" style={{ flex: 1, width: 'auto' }}>
                                    <div className="progress-fill fill-other" style={{ width: `${o.probability * 100}%` }} />
                                </div>
                                <span className="origin-prob">{(o.probability * 100).toFixed(1)}%</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* ── Crack & Damage ── */}
                <div className="card">
                    <div className="section-title"><span className="section-title-icon">🔍</span> Crack & Damage Assessment</div>
                    <div style={{
                        padding: '10px 16px',
                        background: 'rgba(124,92,252,0.06)',
                        borderRadius: 8,
                        marginBottom: 14,
                        fontSize: 13,
                        fontWeight: 600,
                        color: 'var(--text-primary)'
                    }}>
                        Clarity: <span style={{ color: 'var(--accent)' }}>{crack.overall_clarity_grade || 'N/A'}</span>
                    </div>
                    <div className="progress-list">
                        <ProgressBar label="Surface Cracks" value={crack.surface_cracks || 0} className="fill-synthetic" />
                        <ProgressBar label="Internal Fractures" value={crack.internal_fractures || 0} className="fill-heat" />
                        <ProgressBar label="Chips" value={crack.chips || 0} className="fill-diffusion" />
                        <ProgressBar label="Abrasions" value={crack.abrasions || 0} className="fill-other" />
                    </div>
                    <div style={{ marginTop: 12, fontSize: 12, color: 'var(--text-muted)', fontStyle: 'italic' }}>
                        {crack.damage_description}
                    </div>
                </div>

                {/* ── Inclusion Analysis ── */}
                <div className="card report-full">
                    <div className="section-title"><span className="section-title-icon">🔬</span> Inclusion Pattern Analysis</div>
                    <div style={{ marginBottom: 12, fontSize: 12, color: 'var(--text-muted)', fontStyle: 'italic' }}>
                        {inc.summary}
                    </div>
                    <div className="inclusion-grid">
                        {inclItems.map(([key, label]) => (
                            <div key={key} className="inclusion-item">
                                <span className="inclusion-name">{label}</span>
                                <div className="inclusion-bar">
                                    <div className="inclusion-fill" style={{ width: `${((inc[key] || 0) * 100).toFixed(0)}%` }} />
                                </div>
                                <span className="inclusion-val">{((inc[key] || 0) * 100).toFixed(1)}%</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* ── Recommendations ── */}
                <div className="card report-full">
                    <div className="section-title"><span className="section-title-icon">📋</span> Recommendations</div>
                    <div className="recommendation-list">
                        {(report.recommendations || []).map((r, i) => (
                            <div key={i} className="recommendation-item">{r}</div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}
