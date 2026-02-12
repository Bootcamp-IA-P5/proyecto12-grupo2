import { useState, useEffect } from 'react'

export default function ModelInfo({ apiUrl }) {
    const [modelInfo, setModelInfo] = useState(null)
    const [isOpen, setIsOpen] = useState(false)
    const [loading, setLoading] = useState(false)

    const loadModelInfo = async () => {
        if (modelInfo) {
            setIsOpen(true)
            return
        }

        setLoading(true)
        try {
            const response = await fetch(`${apiUrl}/model-info/`)
            const data = await response.json()
            setModelInfo(data)
            setIsOpen(true)
        } catch (err) {
            console.error('Error loading model info:', err)
        } finally {
            setLoading(false)
        }
    }

    return (
        <>
            <button
                onClick={loadModelInfo}
                className="btn-ghost"
                disabled={loading}
            >
                {loading ? 'Cargando...' : 'Info del modelo'}
            </button>

            {isOpen && modelInfo && (
                <div className="modal-overlay" onClick={() => setIsOpen(false)}>
                    <div className="modal" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h3>Informacion del modelo</h3>
                            <button onClick={() => setIsOpen(false)} className="btn-ghost">Cerrar</button>
                        </div>

                        <div style={{ padding: '1.5rem', display: 'grid', gap: '1rem' }}>
                            <div className="stat-card">
                                <div className="stat-label">Modelo</div>
                                <div className="stat-value">{modelInfo.model_name || 'YOLO'}</div>
                            </div>

                            <div className="stat-card">
                                <div className="stat-label">Umbral de confianza</div>
                                <div className="stat-value">{modelInfo.confidence_threshold || 0.5}</div>
                            </div>

                            <div className="stat-card">
                                <div className="stat-label">Marcas detectables ({modelInfo.brands?.length || 0})</div>
                                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginTop: '0.6rem' }}>
                                    {modelInfo.brands?.map((brand) => (
                                        <span key={brand} className="tag">{brand}</span>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </>
    )
}
