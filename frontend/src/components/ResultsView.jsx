import { useState } from 'react'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'

const COLORS = [
    '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
    '#ec4899', '#14b8a6', '#f97316', '#06b6d4', '#84cc16'
]

const RADIAN = Math.PI / 180

const safeNumber = (value) => {
    const parsed = Number(value)
    return Number.isFinite(parsed) ? parsed : 0
}

const safeText = (value, fallback) => {
    if (value === undefined || value === null || value === '') return fallback
    return value
}

const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, name }) => {
    const radius = innerRadius + (outerRadius - innerRadius) * 0.6
    const x = cx + radius * Math.cos(-midAngle * RADIAN)
    const y = cy + radius * Math.sin(-midAngle * RADIAN)

    return (
        <text
            x={x}
            y={y}
            fill="#f7f1e8"
            textAnchor={x > cx ? 'start' : 'end'}
            dominantBaseline="central"
            fontSize={12}
        >
            {`${name} ${(percent * 100).toFixed(0)}%`}
        </text>
    )
}

export default function ResultsView({ results, apiUrl, onBack, initialIsSaved = false }) {
    const [selectedImage, setSelectedImage] = useState(null)
    const [isSaved, setIsSaved] = useState(initialIsSaved)
    const [isSaving, setIsSaving] = useState(false)

    if (!results) return null

    const {
        video_id,
        title,
        total_duration,
        total_exposure_time,
        visibility_percentage,
        brands
    } = results

    const safeTitle = safeText(title, 'Resultado de analisis')
    const safeVideoId = safeText(video_id, 'N/A')
    const safeTotalDuration = safeNumber(total_duration)
    const safeExposureTime = safeNumber(total_exposure_time)
    const safeVisibility = safeNumber(visibility_percentage)
    const brandMap = brands && typeof brands === 'object' ? brands : {}

    // Prepare data for pie chart
    const chartData = Object.entries(brandMap).map(([brand, data]) => ({
        name: brand,
        value: safeNumber(data?.exposure_time),
        percentage: safeNumber(data?.visibility)
    }))

    const handleSaveAnalysis = async () => {
        if (isSaved) return // Already saved

        setIsSaving(true)
        try {
            const response = await fetch(`${apiUrl}/save-analysis/?video_id=${encodeURIComponent(video_id)}`, {
                method: 'POST'
            })

            if (response.ok) {
                setIsSaved(true)
                alert('✅ Análisis guardado correctamente')
            } else {
                alert('Error al guardar el análisis')
            }
        } catch (err) {
            console.error('Error:', err)
            alert('Error al guardar el análisis')
        } finally {
            setIsSaving(false)
        }
    }

    const handleDeleteAnalysis = async () => {
        if (!isSaved) {
            alert('Este análisis no está guardado en la base de datos')
            return
        }

        if (!window.confirm('¿Estás seguro de eliminar este análisis?')) return

        try {
            const response = await fetch(`${apiUrl}/results/${video_id}`, {
                method: 'DELETE'
            })

            if (response.ok) {
                setIsSaved(false)
                alert('Análisis eliminado correctamente')
                onBack()
            } else {
                alert('Error al eliminar el análisis')
            }
        } catch (err) {
            console.error('Error:', err)
            alert('Error al eliminar el análisis')
        }
    }

    return (
        <div className="fade-up" style={{ display: 'grid', gap: '1.5rem' }}>
            <div className="panel">
                <div className="panel-header">
                    <div>
                        <h2 className="panel-title">{safeTitle}</h2>
                        <p className="panel-subtitle">
                            ID: {safeVideoId}
                            {isSaved && (
                                <span style={{
                                    marginLeft: '1rem',
                                    padding: '0.25rem 0.6rem',
                                    background: 'var(--accent-2)',
                                    borderRadius: '6px',
                                    fontSize: '0.75rem',
                                    fontWeight: 'bold'
                                }}>
                                    ✓ GUARDADO
                                </span>
                            )}
                        </p>
                    </div>
                    <div style={{ display: 'flex', gap: '0.6rem' }}>
                        <button onClick={onBack} className="btn-secondary">Volver</button>
                        <button
                            onClick={handleSaveAnalysis}
                            disabled={isSaved || isSaving}
                            className="btn-primary"
                            style={{
                                opacity: (isSaved || isSaving) ? 0.5 : 1,
                                cursor: (isSaved || isSaving) ? 'not-allowed' : 'pointer'
                            }}
                        >
                            {isSaving ? 'Guardando...' : isSaved ? '✓ Guardado' : 'Guardar análisis'}
                        </button>
                        <button
                            onClick={handleDeleteAnalysis}
                            className="btn-danger"
                            disabled={!isSaved}
                            style={{
                                opacity: !isSaved ? 0.5 : 1,
                                cursor: !isSaved ? 'not-allowed' : 'pointer'
                            }}
                        >
                            Eliminar
                        </button>
                    </div>
                </div>
            </div>

            <div className="stat-grid">
                <div className="stat-card">
                    <div className="stat-label">Duracion total</div>
                    <div className="stat-value">{safeTotalDuration.toFixed(1)}s</div>
                </div>
                <div className="stat-card">
                    <div className="stat-label">Exposicion de marcas</div>
                    <div className="stat-value" style={{ color: 'var(--accent-2)' }}>
                        {safeExposureTime.toFixed(1)}s
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-label">Visibilidad</div>
                    <div className="stat-value" style={{ color: 'var(--accent)' }}>
                        {safeVisibility.toFixed(1)}%
                    </div>
                </div>
            </div>

            <div className="grid-2">
                <div className="panel">
                    <div className="panel-header">
                        <h3 className="panel-title">Distribucion de visibilidad</h3>
                    </div>
                    {chartData.length > 0 ? (
                        <div className="chart-shell">
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie
                                        data={chartData}
                                        cx="50%"
                                        cy="50%"
                                        labelLine={false}
                                        label={renderCustomizedLabel}
                                        outerRadius={110}
                                        fill="#8884d8"
                                        dataKey="value"
                                    >
                                        {chartData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                    <Tooltip
                                        contentStyle={{
                                            background: '#0f172a',
                                            border: '1px solid rgba(255, 255, 255, 0.1)',
                                            borderRadius: '12px',
                                            color: '#f7f1e8'
                                        }}
                                    />
                                    <Legend
                                        formatter={(value) => <span style={{ color: '#f7f1e8' }}>{value}</span>}
                                    />
                                </PieChart>
                            </ResponsiveContainer>
                        </div>
                    ) : (
                        <p className="panel-subtitle">No hay datos de marcas</p>
                    )}
                </div>

                <div className="panel">
                    <div className="panel-header">
                        <h3 className="panel-title">Detalles por marca</h3>
                    </div>
                    <div style={{ display: 'grid', gap: '0.8rem' }}>
                        {Object.entries(brandMap).map(([brand, data], index) => (
                            <div key={brand} className="stat-card">
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        <span
                                            style={{
                                                width: '10px',
                                                height: '10px',
                                                borderRadius: '999px',
                                                background: COLORS[index % COLORS.length]
                                            }}
                                        />
                                        <strong>{brand}</strong>
                                    </div>
                                    <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                                        {safeNumber(data?.detections)} detecciones
                                    </span>
                                </div>
                                <div className="stat-grid" style={{ marginTop: '0.6rem' }}>
                                    <div>
                                        <div className="stat-label">Tiempo de exposicion</div>
                                        <div className="stat-value" style={{ fontSize: '1.2rem' }}>
                                            {safeNumber(data?.exposure_time).toFixed(1)}s
                                        </div>
                                    </div>
                                    <div>
                                        <div className="stat-label">Visibilidad</div>
                                        <div className="stat-value" style={{ fontSize: '1.2rem', color: 'var(--accent-2)' }}>
                                            {safeNumber(data?.visibility).toFixed(1)}%
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            <div className="panel">
                <div className="panel-header">
                    <h3 className="panel-title">Imagenes detectadas</h3>
                </div>
                <div className="image-grid">
                    {Object.entries(brandMap).map(([brand, data]) =>
                        (Array.isArray(data?.sample_images) ? data.sample_images : []).slice(0, 3).map((imgPath, idx) => (
                            <div
                                key={`${brand}-${idx}`}
                                className="image-card"
                                onClick={() => setSelectedImage({ brand, path: imgPath })}
                                role="button"
                                tabIndex={0}
                            >
                                <img
                                    src={`${apiUrl}${imgPath}`}
                                    alt={`${brand} detection`}
                                    onError={(e) => {
                                        e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"%3E%3Crect fill="%2320212e" width="100" height="100"/%3E%3Ctext x="50" y="50" text-anchor="middle" fill="%23cfc6b6" font-size="12"%3ENo image%3C/text%3E%3C/svg%3E'
                                    }}
                                />
                                <div className="image-caption">{brand}</div>
                            </div>
                        ))
                    )}
                </div>
            </div>

            {selectedImage && (
                <div className="modal-overlay" onClick={() => setSelectedImage(null)}>
                    <div className="modal" onClick={(event) => event.stopPropagation()}>
                        <div className="modal-header">
                            <h4>{selectedImage.brand}</h4>
                            <button className="btn-ghost" onClick={() => setSelectedImage(null)}>
                                Cerrar
                            </button>
                        </div>
                        <img src={`${apiUrl}${selectedImage.path}`} alt={selectedImage.brand} />
                    </div>
                </div>
            )}
        </div>
    )
}
