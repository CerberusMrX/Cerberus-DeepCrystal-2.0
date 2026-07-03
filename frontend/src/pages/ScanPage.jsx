import React, { useState, useRef, useCallback } from 'react'
import ReportDashboard from '../components/ReportDashboard'

const MODE_INFO = {
    free: { label: 'Free Basic', desc: '3 scans/day · Basic ID + Confidence', class: 'active-free' },
    pro: { label: 'Pro Trader', desc: 'Full analysis · QR Cert · History', class: 'active-pro' },
    lab: { label: 'Lab License', desc: 'Spectral inputs · Research mode · API', class: 'active-lab' },
}

export default function ScanPage({ tier }) {
    const [mode, setMode] = useState(tier || 'pro')
    const [images, setImages] = useState([])
    const [dragOver, setDragOver] = useState(false)
    const [scanning, setScanning] = useState(false)
    const [report, setReport] = useState(null)
    const [error, setError] = useState(null)
    const [logs, setLogs] = useState([])
    const fileInputRef = useRef(null)

    const [manualInputs, setManualInputs] = useState({
        refractive_index: '',
        specific_gravity: '',
        pleochroism: '',
        magnetism: '',
        streak: '',
        hardness_result: '',
        carat_weight: '',
        uv_fluorescence: '',
    })

    const handleFiles = useCallback((files) => {
        const valid = Array.from(files).filter(f => f.type.startsWith('image/'))
        if (!valid.length) return
        const previewURLs = valid.map(f => ({
            file: f,
            url: URL.createObjectURL(f),
            name: f.name,
        }))
        setImages(previewURLs)
        setReport(null)
        setError(null)
    }, [])

    const handleDrop = (e) => {
        e.preventDefault()
        setDragOver(false)
        handleFiles(e.dataTransfer.files)
    }

    const handleInputChange = (field, value) => {
        setManualInputs(prev => ({ ...prev, [field]: value }))
    }

    const runScan = async () => {
        if (!images.length) {
            setError('Please upload at least one gemstone image.')
            return
        }
        setScanning(true)
        setError(null)
        setReport(null)
        setLogs(['[SYSTEM] Initializing Cerberus AI Engine...'])
        
        let logInterval = null
        
        try {
            const formData = new FormData()
            formData.append('image', images[0].file)
            formData.append('mode', mode)

            // Clean manual inputs: only include non-empty values
            const cleanInputs = {}
            Object.entries(manualInputs).forEach(([k, v]) => {
                if (v !== '') {
                    const numFields = ['refractive_index', 'specific_gravity', 'hardness_result', 'carat_weight']
                    cleanInputs[k] = numFields.includes(k) ? parseFloat(v) || v : v
                }
            })
            formData.append('manual_data', JSON.stringify(cleanInputs))

            // Simulate realistic logs while waiting for backend
            const fakeLogs = [
                '[VISION] Loading openai/clip-vit-large-patch14...',
                '[VISION] Running zero-shot gem identification...',
                '[VISION] Analyzing multi-label inclusions (10 prompts)...',
                '[VISION] Analyzing treatment signatures (8 prompts)...',
                '[COLOR] Running KMeans clustering on image pixels...',
                '[COLOR] Extracted dominant hue and color quality score...',
                '[MATH] Applying deterministic regression for market valuation...',
                '[BLOCKCHAIN] Securing forensic hash and generating QR code...',
            ]
            let logIdx = 0
            logInterval = setInterval(() => {
                if (logIdx < fakeLogs.length) {
                    setLogs(prev => [...prev, fakeLogs[logIdx]])
                    logIdx++
                }
            }, 600)

            const res = await fetch('/api/analysis/scan', {
                method: 'POST',
                body: formData,
            })
            if (!res.ok) {
                let errData;
                try { errData = await res.json() } catch(e) {}
                throw new Error(errData?.detail || `Analysis failed (Status: ${res.status})`)
            }
            let data;
            try { data = await res.json() } catch(e) { throw new Error("Invalid response from server") }
            clearInterval(logInterval)
            setLogs(prev => [...prev, '[SYSTEM] Analysis Complete.'])
            setReport(data)
        } catch (err) {
            clearInterval(logInterval)
            setError(err.message || 'Could not connect to the analysis engine. Ensure the backend is running.')
        } finally {
            setScanning(false)
        }
    }

    return (
        <div className="animate-in">
            <div className="page-header">
                <h1 className="page-title">💎 Gem Scanner</h1>
                <p className="page-subtitle">Upload gemstone images and enter manual test data for AI forensic analysis</p>
            </div>

            {/* Mode Selector */}
            <div className="mode-selector">
                {Object.entries(MODE_INFO).map(([key, info]) => (
                    <button
                        key={key}
                        className={`mode-btn ${mode === key ? info.class : ''}`}
                        onClick={() => setMode(key)}
                    >
                        <div>{info.label}</div>
                        <div style={{ fontSize: '10px', opacity: 0.7, marginTop: 2 }}>{info.desc}</div>
                    </button>
                ))}
            </div>

            {/* Upload + Manual */}
            <div className="upload-section">
                {/* Upload Zone */}
                <div className="card">
                    <div
                        className={`upload-zone ${dragOver ? 'drag-over' : ''}`}
                        onDragOver={e => { e.preventDefault(); setDragOver(true) }}
                        onDragLeave={() => setDragOver(false)}
                        onDrop={handleDrop}
                        onClick={() => fileInputRef.current?.click()}
                    >
                        <input
                            ref={fileInputRef}
                            type="file"
                            accept="image/*"
                            multiple
                            style={{ display: 'none' }}
                            onChange={e => handleFiles(e.target.files)}
                        />
                        {images.length === 0 ? (
                            <>
                                <span className="upload-icon">🔮</span>
                                <div className="upload-title">Drop Gemstone Images Here</div>
                                <div className="upload-subtitle">Supports photo, macro, UV fluorescence, microscope images</div>
                                <div className="upload-types">
                                    {['Photo', 'Macro', 'UV Image', 'Microscope'].map(t => (
                                        <span key={t} className="type-tag">{t}</span>
                                    ))}
                                </div>
                            </>
                        ) : (
                            <>
                                <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', justifyContent: 'center', marginBottom: 12 }}>
                                    {images.slice(0, 3).map((img, i) => (
                                        <div key={i} className="image-preview" style={{ width: 160, height: 120 }}>
                                            <img src={img.url} alt={img.name} />
                                            <div className="preview-overlay">
                                                <span className="preview-label">{img.name}</span>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                                <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>
                                    {images.length} image(s) loaded · Click to change
                                </div>
                            </>
                        )}
                    </div>

                    {/* Spectral data input (Lab mode) */}
                    {mode === 'lab' && (
                        <div style={{ marginTop: 16 }}>
                            <div className="panel-title">🔬 Spectral Data Input</div>
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginTop: 12 }}>
                                {[
                                    { label: 'Raman Shift (cm⁻¹)', field: 'raman', placeholder: 'e.g. 418' },
                                    { label: 'FTIR Peak (cm⁻¹)', field: 'ftir', placeholder: 'e.g. 3309' },
                                    { label: 'UV-Vis (nm)', field: 'uv_vis', placeholder: 'e.g. 550' },
                                ].map(({ label, field, placeholder }) => (
                                    <div key={field} className="form-group">
                                        <label className="form-label">{label}</label>
                                        <input className="form-input" placeholder={placeholder} />
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>

                {/* Manual Panel */}
                <div className="card manual-panel">
                    <div className="panel-title">⚗️ Gemological Test Inputs</div>
                    <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 12 }}>
                        Optional — improves confidence score
                    </div>

                    {[
                        { label: 'Refractive Index', field: 'refractive_index', placeholder: 'e.g. 1.762', type: 'number' },
                        { label: 'Specific Gravity', field: 'specific_gravity', placeholder: 'e.g. 4.00', type: 'number' },
                        { label: 'Mohs Hardness Result', field: 'hardness_result', placeholder: 'e.g. 9.0', type: 'number' },
                        { label: 'Carat Weight', field: 'carat_weight', placeholder: 'e.g. 2.5', type: 'number' },
                        { label: 'Streak Color', field: 'streak', placeholder: 'e.g. White', type: 'text' },
                    ].map(({ label, field, placeholder, type }) => (
                        <div key={field} className="form-group">
                            <label className="form-label">{label}</label>
                            <input
                                className="form-input"
                                type={type}
                                step="any"
                                placeholder={placeholder}
                                value={manualInputs[field]}
                                onChange={e => handleInputChange(field, e.target.value)}
                            />
                        </div>
                    ))}

                    <div className="form-group">
                        <label className="form-label">Pleochroism</label>
                        <select
                            className="form-select"
                            value={manualInputs.pleochroism}
                            onChange={e => handleInputChange('pleochroism', e.target.value)}
                        >
                            <option value="">Select...</option>
                            <option>None</option>
                            <option>Weak</option>
                            <option>Moderate</option>
                            <option>Strong</option>
                            <option>Trichroic</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label className="form-label">UV Fluorescence</label>
                        <select
                            className="form-select"
                            value={manualInputs.uv_fluorescence}
                            onChange={e => handleInputChange('uv_fluorescence', e.target.value)}
                        >
                            <option value="">Select...</option>
                            <option>Inert</option>
                            <option>Weak Blue</option>
                            <option>Strong Blue</option>
                            <option>Red</option>
                            <option>Orange</option>
                            <option>Yellow-Green</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label className="form-label">Magnetism</label>
                        <select
                            className="form-select"
                            value={manualInputs.magnetism}
                            onChange={e => handleInputChange('magnetism', e.target.value)}
                        >
                            <option value="">Select...</option>
                            <option>None</option>
                            <option>Weak</option>
                            <option>Moderate</option>
                            <option>Strong</option>
                        </select>
                    </div>
                </div>
            </div>

            {/* Error */}
            {error && (
                <div style={{
                    background: 'rgba(255,68,102,0.08)',
                    border: '1px solid rgba(255,68,102,0.3)',
                    borderRadius: 'var(--radius-sm)',
                    padding: '12px 16px',
                    color: 'var(--danger)',
                    fontSize: 13,
                    marginBottom: 16
                }}>
                    ⚠️ {error}
                </div>
            )}

            {/* Scan Button */}
            <button
                className={`scan-btn ${scanning ? 'scanning' : ''}`}
                onClick={runScan}
                disabled={scanning}
                style={{ marginBottom: 16 }}
            >
                {scanning ? (
                    <><span className="loader" /> Running AI Forensic Analysis...</>
                ) : (
                    <> 🔬 Analyze Gemstone</>
                )}
            </button>
            
            {/* Terminal logs */}
            {logs.length > 0 && !report && (
                <div className="scan-terminal">
                    {logs.map((log, i) => (
                        <div key={i} className="terminal-line">{log}</div>
                    ))}
                    {scanning && <div className="terminal-line" style={{ animation: 'none' }}>_</div>}
                </div>
            )}

            {/* Report */}
            {report && <ReportDashboard report={report} />}

            {/* Disclaimer always shown */}
            <div className="disclaimer">
                <span className="disclaimer-icon">⚠️</span>
                <div className="disclaimer-text">
                    <strong>AI Screening Result.</strong> Cerberus DeepCrystal uses advanced machine learning for screening purposes only.
                    For high-value transactions, professional laboratory testing (GIA, Gübelin, SSEF, AGL) is strongly recommended.
                </div>
            </div>
        </div>
    )
}
