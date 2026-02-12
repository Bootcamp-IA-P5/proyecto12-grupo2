import { useState } from 'react'
import './App.css'
import VideoAnalyzer from './components/VideoAnalyzer'
import ImageAnalyzer from './components/ImageAnalyzer'
import ResultsView from './components/ResultsView'
import ModelInfo from './components/ModelInfo'
import SavedAnalyses from './components/SavedAnalyses'

function App() {
  const [activeTab, setActiveTab] = useState('analyze')
  const [results, setResults] = useState(null)
  const [isFromDatabase, setIsFromDatabase] = useState(false)

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:9000'

  const handleAnalysisComplete = (analysisResults) => {
    setResults(analysisResults)
    setIsFromDatabase(false) // New analysis, not saved yet
    setActiveTab('results')
  }

  const loadSavedAnalysis = (analysis) => {
    setResults(analysis)
    setIsFromDatabase(true) // Loaded from database
    setActiveTab('results')
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="container topbar-inner">
          <div className="brand">
            <div className="brand-mark">
              <img
                src="/Gemini_Generated_Image_9t5mla9t5mla9t5m.png"
                alt="KUMO VISION logo"
                className="brand-logo"
              />
            </div>
            <div>
              <div className="brand-title">KUMO VISION</div>
              <div className="brand-subtitle">Computer vision para exposicion de marca en video</div>
            </div>
          </div>
          <ModelInfo apiUrl={API_URL} />
        </div>
      </header>

      <section className="hero">
        <div className="container hero-inner">
          <div className="fade-up">
            <div className="eyebrow">Kumo Vision Suite</div>
            <h1 className="hero-title">Control preciso de visibilidad y exposicion de marca</h1>
            <p className="hero-subtitle">
              Analiza videos en streaming, mide exposicion por segundo y obtienes un reporte claro para equipos de
              marketing y data. Diseñado para flujos reales de investigacion y produccion.
            </p>
            <div className="hero-actions">
              <button className="btn-primary" onClick={() => setActiveTab('analyze')}>
                Iniciar analisis
              </button>
              <button className="btn-secondary" onClick={() => setActiveTab('saved')}>
                Ver historico
              </button>
            </div>
            <div className="hero-badges">
              <span className="badge">YOLO + FastAPI</span>
              <span className="badge">NDJSON en tiempo real</span>
              <span className="badge">Pipeline reproducible</span>
              <span className="badge">Ready para MLOps</span>
            </div>
          </div>
          <div className="hero-panel fade-up">
            <div className="hero-logo">
              <img
                src="/Gemini_Generated_Image_9t5mla9t5mla9t5m.png"
                alt="KUMO VISION"
              />
            </div>
            <h3 className="panel-title">Flujo operativo</h3>
            <p className="panel-subtitle">Del video al insight en una sola corrida.</p>
            <ul className="pipeline">
              <li><span className="pipeline-dot" /> Ingesta YouTube o archivo local</li>
              <li><span className="pipeline-dot" /> Deteccion frame a frame</li>
              <li><span className="pipeline-dot" /> Metricas de exposicion por marca</li>
              <li><span className="pipeline-dot" /> Graficos, imagenes y resumen ejecutivo</li>
            </ul>
          </div>
        </div>
      </section>

      <div className="container">
        <nav className="tabs" aria-label="Secciones principales">
          <button
            onClick={() => setActiveTab('analyze')}
            className={`tab ${activeTab === 'analyze' ? 'active' : ''}`}
          >
            Nuevo analisis
          </button>
          <button
            onClick={() => setActiveTab('image')}
            className={`tab ${activeTab === 'image' ? 'active' : ''}`}
          >
            Analizar imagen
          </button>
          <button
            onClick={() => setActiveTab('results')}
            disabled={!results}
            className={`tab ${activeTab === 'results' && results ? 'active' : ''}`}
          >
            Resultados actuales
          </button>
          <button
            onClick={() => setActiveTab('saved')}
            className={`tab ${activeTab === 'saved' ? 'active' : ''}`}
          >
            Analisis guardados
          </button>
        </nav>
      </div>

      <main className="container content">
        {activeTab === 'analyze' && (
          <VideoAnalyzer apiUrl={API_URL} onAnalysisComplete={handleAnalysisComplete} />
        )}
        {activeTab === 'image' && (
          <ImageAnalyzer apiUrl={API_URL} onAnalysisComplete={handleAnalysisComplete} />
        )}
        {activeTab === 'results' && results && (
          <ResultsView
            results={results}
            apiUrl={API_URL}
            onBack={() => setActiveTab('analyze')}
            initialIsSaved={isFromDatabase}
          />
        )}

        {activeTab === 'saved' && (
          <SavedAnalyses apiUrl={API_URL} onLoadAnalysis={loadSavedAnalysis} />
        )}
      </main>

      <footer className="footer">
        <div className="container">
          <div className="topbar-inner">
            <p>© 2026 KUMO VISION - Grupo 2 Bootcamp IA</p>
            <p>YOLO · FastAPI · PostgreSQL · Vite</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
