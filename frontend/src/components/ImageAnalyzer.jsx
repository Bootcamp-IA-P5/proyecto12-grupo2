import { useState } from 'react'

export default function ImageAnalyzer({ apiUrl, onAnalysisComplete }) {
    const [selectedFile, setSelectedFile] = useState(null)
    const [previewUrl, setPreviewUrl] = useState(null)
    const [isAnalyzing, setIsAnalyzing] = useState(false)

    const handleFileChange = (e) => {
        const file = e.target.files?.[0]
        if (!file) return

        // Validate file type
        if (!file.type.startsWith('image/')) {
            alert('Por favor selecciona un archivo de imagen válido')
            return
        }

        setSelectedFile(file)

        // Create preview URL
        const reader = new FileReader()
        reader.onload = (event) => {
            setPreviewUrl(event.target.result)
        }
        reader.readAsDataURL(file)
    }

    const handleAnalyze = async () => {
        if (!selectedFile) {
            alert('Por favor selecciona una imagen')
            return
        }

        setIsAnalyzing(true)

        try {
            const formData = new FormData()
            formData.append('file', selectedFile)

            const response = await fetch(`${apiUrl}/analyze-image/`, {
                method: 'POST',
                body: formData
            })

            if (!response.ok) {
                throw new Error(`Error ${response.status}: ${response.statusText}`)
            }

            const result = await response.json()

            if (result.status === 'success') {
                // Backend already returns the correct structure
                onAnalysisComplete(result)
            } else {
                alert('Error en el análisis de la imagen')
            }

        } catch (error) {
            console.error('Analysis error:', error)
            alert(`Error al analizar la imagen: ${error.message}`)
        } finally {
            setIsAnalyzing(false)
        }
    }

    const handleClear = () => {
        setSelectedFile(null)
        setPreviewUrl(null)
    }

    return (
        <div className="fade-up" style={{ display: 'grid', gap: '1.5rem' }}>
            <div className="panel">
                <div className="panel-header">
                    <div>
                        <h3 className="panel-title">Analizar imagen</h3>
                        <p className="panel-subtitle">
                            Sube una imagen para detectar marcas en ella
                        </p>
                    </div>
                </div>

                <div style={{ display: 'grid', gap: '1rem' }}>
                    {/* File Input */}
                    <div>
                        <label htmlFor="image-upload" className="btn-primary" style={{ cursor: 'pointer', display: 'inline-block' }}>
                            {selectedFile ? 'Cambiar imagen' : 'Seleccionar imagen'}
                        </label>
                        <input
                            id="image-upload"
                            type="file"
                            accept="image/*"
                            onChange={handleFileChange}
                            style={{ display: 'none' }}
                        />
                        {selectedFile && (
                            <span style={{ marginLeft: '1rem', color: 'var(--text-muted)' }}>
                                {selectedFile.name}
                            </span>
                        )}
                    </div>

                    {/* Image Preview */}
                    {previewUrl && (
                        <div className="panel" style={{
                            padding: '1rem',
                            display: 'flex',
                            justifyContent: 'center',
                            alignItems: 'center',
                            background: 'rgba(0,0,0,0.2)'
                        }}>
                            <img
                                src={previewUrl}
                                alt="Preview"
                                style={{
                                    maxWidth: '100%',
                                    maxHeight: '400px',
                                    borderRadius: '8px'
                                }}
                            />
                        </div>
                    )}

                    {/* Action Buttons */}
                    <div style={{ display: 'flex', gap: '0.6rem' }}>
                        <button
                            onClick={handleAnalyze}
                            disabled={!selectedFile || isAnalyzing}
                            className="btn-primary"
                            style={{
                                opacity: (!selectedFile || isAnalyzing) ? 0.5 : 1,
                                cursor: (!selectedFile || isAnalyzing) ? 'not-allowed' : 'pointer'
                            }}
                        >
                            {isAnalyzing ? 'Analizando...' : 'Analizar imagen'}
                        </button>
                        {selectedFile && !isAnalyzing && (
                            <button onClick={handleClear} className="btn-secondary">
                                Limpiar
                            </button>
                        )}
                    </div>
                </div>
            </div>

            {/* Instructions Panel */}
            <div className="panel">
                <div className="panel-header">
                    <h4 className="panel-title">Instrucciones</h4>
                </div>
                <ul style={{
                    padding: '0 0 0 1.5rem',
                    margin: 0,
                    color: 'var(--text-muted)',
                    lineHeight: 1.8
                }}>
                    <li>Selecciona una imagen en formato JPG, PNG o similar</li>
                    <li>La imagen debe contener marcas visibles para ser detectadas</li>
                    <li>El análisis puede tardar unos segundos dependiendo del tamaño</li>
                    <li>Los resultados mostrarán todas las marcas detectadas con su confianza</li>
                </ul>
            </div>
        </div>
    )
}
