import React, { useState, useEffect } from 'react'
import './index.css'
import ScanPage from './pages/ScanPage'
import MineralDatabase from './pages/MineralDatabase'
import HistoryPage from './pages/HistoryPage'
import DashboardPage from './pages/DashboardPage'

const NAV_ITEMS = [
  { id: 'dashboard', icon: '🔬', label: 'Dashboard' },
  { id: 'scan', icon: '💎', label: 'Gem Scanner' },
  { id: 'database', icon: '📚', label: 'Mineral Database' },
  { id: 'history', icon: '🗂️', label: 'History' },
]

const TIERS = ['free', 'pro', 'lab']
const TIER_LABELS = { free: '⚡ Free', pro: '💼 Pro Trader', lab: '🔬 Lab License' }

function App() {
  const [page, setPage] = useState('scan')
  const [tier, setTier] = useState('pro')
  const [theme, setTheme] = useState('night')

  useEffect(() => {
    try {
      const saved = localStorage.getItem('dd_theme') || 'night'
      setTheme(saved)
      if (saved === 'day' || saved === 'alt') document.documentElement.setAttribute('data-theme', saved)
      else document.documentElement.removeAttribute('data-theme')
    } catch (e) {}
  }, [])

  function toggleTheme() {
    const order = ['night', 'day', 'alt']
    const next = order[(order.indexOf(theme) + 1) % order.length]
    setTheme(next)
    try { localStorage.setItem('dd_theme', next) } catch (e) {}
    if (next === 'day' || next === 'alt') document.documentElement.setAttribute('data-theme', next)
    else document.documentElement.removeAttribute('data-theme')
  }

  return (
    <div className="app-container">
      {/* ── Sidebar ── */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <div className="logo-mark">
            <div className="logo-icon">💎</div>
            <div>
              <div style={{display:'flex',alignItems:'center',gap:8}}>
                <div className="logo-text">Cerberus</div>
                <span className="logo-version">v 2.0</span>
              </div>
              <div className="logo-sub">DeepCrystal AI System</div>
            </div>
          </div>
        </div>
        <div className="sidebar-author">✦ Sudeepa Wanigarathna</div>

        <nav className="sidebar-nav">
          {NAV_ITEMS.map(item => (
            <div
              key={item.id}
              className={`nav-item ${page === item.id ? 'active' : ''}`}
              onClick={() => setPage(item.id)}
            >
              <span className="nav-icon">{item.icon}</span>
              <span>{item.label}</span>
            </div>
          ))}
        </nav>

        <div className="sidebar-tier">
          <div
            className="tier-badge"
            onClick={() => setTier(TIERS[(TIERS.indexOf(tier) + 1) % TIERS.length])}
            title="Click to cycle tiers"
          >
            {TIER_LABELS[tier]}
          </div>
        </div>

        <div className="sidebar-branding">
          <div style={{display:'flex',flexDirection:'column',alignItems:'center',gap:8}}>
            <div style={{display:'flex',alignItems:'center',gap:12}}>
              <div className="branding-logo">
                <span className="branding-highlight">Serendib</span>ware
              </div>
              <button
                title="Toggle theme"
                onClick={toggleTheme}
                style={{padding:'6px 10px',borderRadius:10,border:'none',cursor:'pointer'}}
              >
                {theme === 'day' ? '🌙' : theme === 'alt' ? '🌈' : '☀️'}
              </button>
            </div>
            <div style={{display:'flex',gap:8,alignItems:'center'}}>
              <a href="https://serendibware.com" target="_blank" rel="noopener noreferrer" style={{color:'var(--text-secondary)',fontSize:12,textDecoration:'underline'}}>
                serendibware.com
              </a>
            </div>
          </div>
        </div>
      </aside>

      {/* ── Main Content ── */}
      <main className="main-content">
        {page === 'dashboard' && <DashboardPage tier={tier} onNavigate={setPage} />}
        {page === 'scan' && <ScanPage tier={tier} />}
        {page === 'database' && <MineralDatabase />}
        {page === 'history' && <HistoryPage />}
      </main>
    </div>
  )
}

export default App
