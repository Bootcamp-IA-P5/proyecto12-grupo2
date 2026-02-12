import { useState, useRef } from 'react'

export default function VideoAnalyzer({ apiUrl, onAnalysisComplete }) {
    const [mode, setMode] = useState('youtube') // 'youtube' or 'upload'
    const [youtubeUrl, setYoutubeUrl] = useState('')
    const [selectedFile, setSelectedFile] = useState(null)
    const [isAnalyzing, setIsAnalyzing] = useState(false)
    const [progress, setProgress] = useState(0)
    const [currentStatus, setCurrentStatus] = useState(null)
    const [error, setError] = useState(null)
    const fileInputRef = useRef(null)

    const handleFileSelect = (e) => {
        const file = e.target.files?.[0]
        if (file) {
            setSelectedFile(file)
            setError(null)
        }
    }

    const startAnalysis = async () => {
        setError(null)
        setIsAnalyzing(true)
        setProgress(0)
        setCurrentStatus({ timestamp: 0, brands: {}, detected_seconds: 0 })

        try {
            let response

            if (mode === 'youtube') {
                if (!youtubeUrl) {
                    setError('Por favor ingresa una URL de YouTube')
                    setIsAnalyzing(false)
                    return
                }

                response = await fetch(`${apiUrl}/analyze-stream/?url=${encodeURIComponent(youtubeUrl)}`, {
                    method: 'POST',
                })
            } else {
                if (!selectedFile) {
                    setError('Por favor selecciona un archivo de video')
                    setIsAnalyzing(false)
                    return
                }

                const formData = new FormData()
                formData.append('file', selectedFile)

                response = await fetch(`${apiUrl}/analyze/`, {
                    method: 'POST',
                    body: formData,
                })
            }

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`)
            }

            // Parse NDJSON streaming response
            const reader = response.body.getReader()
            const decoder = new TextDecoder()
            let buffer = ''

            while (true) {
                const { done, value } = await reader.read()

                if (done) break

                buffer += decoder.decode(value, { stream: true })
                const lines = buffer.split('\n')
                buffer = lines.pop() // Keep incomplete line in buffer

                for (const line of lines) {
                    if (!line.trim()) continue

                    try {
                        const data = JSON.parse(line)

                        if (data.type === 'progress') {
                            setProgress(Math.min(data.progress || 0, 1))
                            setCurrentStatus({
                                timestamp: data.timestamp || 0,
                                brands: data.brands || {},
                                detected_seconds: data.detected_seconds || 0
                            })
                        } else if (data.type === 'complete') {
                            setProgress(1)
                            setIsAnalyzing(false)

                            // Pass results to parent without auto-saving
                            // User will decide if they want to save
                            onAnalysisComplete(data.result)
                        } else if (data.type === 'error') {
                            throw new Error(data.detail || 'Analysis error')
                        }
                    } catch (parseError) {
                        console.error('Error parsing NDJSON line:', parseError)
                    }
                }
            }
        } catch (err) {
            console.error('Analysis error:', err)
            setError(err.message || 'Error durante el análisis')
            setIsAnalyzing(false)
        }
    }

    return (
        <div className="fade-up">
            <div className="panel">
                <div className="panel-header">
                    <div>
                        <h2 className="panel-title">Analizar video</h2>
                        <p className="panel-subtitle">Elige la fuente y comienza el analisis en tiempo real.</p>
                    </div>
                </div>

                <div className="segmented">
                    <button
                        onClick={() => setMode('youtube')}
                        className={`segmented-btn ${mode === 'youtube' ? 'active' : ''}`}
                    >
                        URL de YouTube
                    </button>
                    <button
                        onClick={() => setMode('upload')}
                        className={`segmented-btn ${mode === 'upload' ? 'active' : ''}`}
                    >
                        Subir video
                    </button>
                </div>

                {mode === 'youtube' && (
                    <div style={{ marginTop: '1rem' }}>
                        <label className="panel-subtitle">URL de YouTube</label>
                        <input
                            type="text"
                            value={youtubeUrl}
                            onChange={(e) => setYoutubeUrl(e.target.value)}
                            placeholder="https://www.youtube.com/watch?v=..."
                            className="input"
                            disabled={isAnalyzing}
                        />
                    </div>
                )}

                {mode === 'upload' && (
                    <div style={{ marginTop: '1rem' }}>
                        <label className="panel-subtitle">Seleccionar video</label>
                        <input
                            ref={fileInputRef}
                            type="file"
                            accept="video/*"
                            onChange={handleFileSelect}
                            className="hidden"
                            disabled={isAnalyzing}
                        />
                        <button
                            onClick={() => fileInputRef.current?.click()}
                            className="dropzone"
                            disabled={isAnalyzing}
                        >
                            {selectedFile ? (
                                <div>
                                    <div style={{ fontWeight: 600 }}>{selectedFile.name}</div>
                                    <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                                        {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                                    </div>
                                </div>
                            ) : (
                                <div>
                                    <div style={{ fontWeight: 600 }}>Click para seleccionar video</div>
                                    <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                                        MP4, AVI, MOV, MKV
                                    </div>
                                </div>
                            )}
                        </button>
                    </div>
                )}

                {error && (
                    <div style={{ marginTop: '1rem' }} className="alert">
                        {error}
                    </div>
                )}

                <button
                    onClick={startAnalysis}
                    disabled={isAnalyzing}
                    className="btn-primary btn-full"
                    style={{ marginTop: '1.4rem' }}
                >
                    {isAnalyzing ? 'Analizando...' : 'Iniciar analisis'}
                </button>
            </div>

            {isAnalyzing && (
                <div className="panel">
                    <div className="panel-header">
                        <h3 className="panel-title">Analisis en progreso</h3>
                    </div>

                    <div style={{ marginBottom: '1rem' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem' }}>
                            <span style={{ color: 'var(--text-muted)' }}>Progreso</span>
                            <span>{Math.round(progress * 100)}%</span>
                        </div>
                        <div className="progress-track" style={{ marginTop: '0.5rem' }}>
                            <div className="progress-fill" style={{ width: `${progress * 100}%` }} />
                        </div>
                    </div>

                    {currentStatus && (
                        <div className="stat-grid">
                            <div className="stat-card">
                                <div className="stat-label">Tiempo actual</div>
                                <div className="stat-value">{currentStatus.timestamp.toFixed(1)}s</div>
                            </div>
                            <div className="stat-card">
                                <div className="stat-label">Tiempo detectado</div>
                                <div className="stat-value" style={{ color: 'var(--accent-2)' }}>
                                    {currentStatus.detected_seconds.toFixed(1)}s
                                </div>
                            </div>
                            <div className="stat-card">
                                <div className="stat-label">Marcas activas</div>
                                <div className="stat-value" style={{ color: 'var(--accent)' }}>
                                    {Object.keys(currentStatus.brands).length}
                                </div>
                            </div>
                        </div>
                    )}

                    {currentStatus && Object.keys(currentStatus.brands).length > 0 && (
                        <div style={{ marginTop: '1rem' }}>
                            <p className="panel-subtitle">Marcas detectadas</p>
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginTop: '0.5rem' }}>
                                {Object.entries(currentStatus.brands).map(([brand, count]) => (
                                    <span key={brand} className="tag">
                                        {brand} ({count})
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}
