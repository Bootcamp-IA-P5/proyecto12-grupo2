import { useState, useEffect } from 'react'

export default function SavedAnalyses({ apiUrl, onLoadAnalysis }) {
    const [analyses, setAnalyses] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        loadAnalyses()
    }, [])

    const loadAnalyses = async () => {
        setLoading(true)
        setError(null)

        try {
            // Note: Necesitamos agregar un endpoint para listar todos los análisis
            // Por ahora mostramos un mensaje
            setAnalyses([])
            setLoading(false)
        } catch (err) {
            console.error('Error loading analyses:', err)
            setError('Error al cargar análisis guardados')
            setLoading(false)
        }
    }

    const loadAnalysisById = async (videoId) => {
        try {
            const response = await fetch(`${apiUrl}/results/${videoId}`)

            if (response.ok) {
                const data = await response.json()
                onLoadAnalysis(data)
            } else {
                alert('No se pudo cargar el análisis')
            }
        } catch (err) {
            console.error('Error:', err)
            alert('Error al cargar el análisis')
        }
    }

    const deleteAnalysis = async (videoId) => {
        if (!window.confirm('¿Estás seguro de eliminar este análisis?')) return

        try {
            const response = await fetch(`${apiUrl}/results/${videoId}`, {
                method: 'DELETE'
            })

            if (response.ok) {
                setAnalyses(analyses.filter(a => a.video_id !== videoId))
                alert('Análisis eliminado correctamente')
            } else {
                alert('Error al eliminar el análisis')
            }
        } catch (err) {
            console.error('Error:', err)
            alert('Error al eliminar el análisis')
        }
    }

    if (loading) {
        return (
            <div className="panel" style={{ textAlign: 'center' }}>
                <div style={{ marginBottom: '1rem' }}>Cargando analisis guardados...</div>
            </div>
        )
    }

    if (error) {
        return (
            <div className="panel">
                <div className="alert">{error}</div>
                <button onClick={loadAnalyses} className="btn-secondary" style={{ marginTop: '1rem' }}>
                    Reintentar
                </button>
            </div>
        )
    }

    return (
        <div className="fade-up" style={{ display: 'grid', gap: '1.5rem' }}>
            <div className="panel">
                <div className="panel-header">
                    <div>
                        <h2 className="panel-title">Analisis guardados</h2>
                        <p className="panel-subtitle">Historial de ejecuciones almacenadas en la base.</p>
                    </div>
                    <button onClick={loadAnalyses} className="btn-secondary">Actualizar</button>
                </div>
            </div>

            {analyses.length === 0 ? (
                <div className="panel" style={{ textAlign: 'center' }}>
                    <h3 className="panel-title">No hay analisis guardados</h3>
                    <p className="panel-subtitle" style={{ marginTop: '0.5rem' }}>
                        Los analisis se almacenaran automaticamente cuando finalice el proceso.
                    </p>
                    <p className="panel-subtitle" style={{ marginTop: '0.5rem' }}>
                        Nota: falta el endpoint GET /results/ en el backend.
                    </p>
                </div>
            ) : (
                <div className="grid-3">
                    {analyses.map((analysis) => (
                        <div key={analysis.video_id} className="panel">
                            <div style={{ marginBottom: '0.8rem' }}>
                                <h3 className="panel-title">{analysis.title}</h3>
                                <p className="panel-subtitle">{new Date(analysis.processed_at).toLocaleString()}</p>
                            </div>

                            <div className="stat-grid" style={{ marginBottom: '1rem' }}>
                                <div>
                                    <div className="stat-label">Duracion</div>
                                    <div className="stat-value" style={{ fontSize: '1.1rem' }}>
                                        {analysis.total_duration?.toFixed(1)}s
                                    </div>
                                </div>
                                <div>
                                    <div className="stat-label">Visibilidad</div>
                                    <div className="stat-value" style={{ fontSize: '1.1rem', color: 'var(--accent-2)' }}>
                                        {analysis.visibility_percentage?.toFixed(1)}%
                                    </div>
                                </div>
                                <div>
                                    <div className="stat-label">Marcas</div>
                                    <div className="stat-value" style={{ fontSize: '1.1rem' }}>
                                        {Object.keys(analysis.brands || {}).length}
                                    </div>
                                </div>
                            </div>

                            <div style={{ display: 'flex', gap: '0.5rem' }}>
                                <button
                                    onClick={() => loadAnalysisById(analysis.video_id)}
                                    className="btn-primary btn-full"
                                >
                                    Ver detalles
                                </button>
                                <button
                                    onClick={() => deleteAnalysis(analysis.video_id)}
                                    className="btn-danger"
                                >
                                    Borrar
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
