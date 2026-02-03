import React, { useState, useRef, useEffect } from 'react'

export default function DemoSection() {
    const [imagePreview, setImagePreview] = useState(null)
    const [isProcessing, setIsProcessing] = useState(false)
    const [results, setResults] = useState(null)
    const [cameraActive, setCameraActive] = useState(false)
    const [realtimeResults, setRealtimeResults] = useState(null)
    const videoRef = useRef(null)
    const canvasRef = useRef(null)
    const streamRef = useRef(null)

    // Usar variable de entorno de Vite
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

    const handleImageUpload = (e) => {
        const file = e.target.files?.[0]
        if (file) {
            const reader = new FileReader()
            reader.onload = (event) => {
                setImagePreview(event.target.result)
                setResults(null)
            }
            reader.readAsDataURL(file)
        }
    }

    const startCamera = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } }
            })
            streamRef.current = stream
            if (videoRef.current) {
                videoRef.current.srcObject = stream
            }
            setCameraActive(true)
            setImagePreview(true)
            setResults(true)
            analyzeFrame()
        } catch (err) {
            alert('No se pudo acceder a la cámara: ' + err.message)
        }
    }

    const stopCamera = () => {
        if (streamRef.current) {
            streamRef.current.getTracks().forEach(track => track.stop())
        }
        setCameraActive(false)
        setRealtimeResults(null)
    }

    const analyzeFrame = () => {
        if (!cameraActive || !videoRef.current || !canvasRef.current) return

        const canvas = canvasRef.current
        const ctx = canvas.getContext('2d')
        const video = videoRef.current

        ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

        // Enviar frame al API cada 500ms
        canvas.toBlob(async (blob) => {
            try {
                const formData = new FormData()
                formData.append('file', blob, 'frame.jpg')

                const response = await fetch(`${API_URL}/detect/image`, {
                    method: 'POST',
                    body: formData
                })

                if (response.ok) {
                    const data = await response.json()

                    if (data.total_detections > 0) {
                        const detectedLogos = data.detections.map(det => ({
                            name: det.class_name,
                            confidence: det.confidence,
                            icon: getIconForLogo(det.class_name)
                        }))

                        setRealtimeResults({
                            logos: data.total_detections,
                            confidence: detectedLogos[0]?.confidence || 0,
                            detectedLogos: detectedLogos
                        })
                    }
                }
            } catch (err) {
                console.error('Error en análisis de frame:', err)
            }
        }, 'image/jpeg', 0.8)

        if (cameraActive) {
            setTimeout(analyzeFrame, 500)
        }
    }

    useEffect(() => {
        if (cameraActive) {
            analyzeFrame()
        }
        return () => {
            if (cameraActive) {
                stopCamera()
            }
        }
    }, [cameraActive])

    const handleDetect = async () => {
        if (!imagePreview) return

        setIsProcessing(true)
        try {
            // Convertir data URL a blob
            const dataUrlToBlob = (dataUrl) => {
                const arr = dataUrl.split(',')
                const mime = arr[0].match(/:(.*?);/)[1]
                const bstr = atob(arr[1])
                let n = bstr.length
                const u8arr = new Uint8Array(n)
                while (n--) {
                    u8arr[n] = bstr.charCodeAt(n)
                }
                return new Blob([u8arr], { type: mime })
            }

            const blob = dataUrlToBlob(imagePreview)

            // Crear FormData
            const formData = new FormData()
            formData.append('file', blob, 'image.jpg')

            // Enviar al API
            const apiResponse = await fetch(`${API_URL}/detect/image`, {
                method: 'POST',
                body: formData
            })

            if (!apiResponse.ok) {
                const errorData = await apiResponse.json()
                throw new Error(errorData.detail || 'Error en la detección')
            }

            const data = await apiResponse.json()

            // Transformar respuesta del API al formato esperado
            const detectedLogos = data.detections.map(det => ({
                name: det.class_name,
                confidence: det.confidence,
                icon: getIconForLogo(det.class_name)
            }))

            setResults({
                logos: data.total_detections,
                confidence: detectedLogos.length > 0 ? detectedLogos[0].confidence : 0,
                processingTime: '245ms',
                detectedLogos: detectedLogos
            })
        } catch (err) {
            alert('Error al detectar logos: ' + err.message + '\n\nAsegúrate de que el servidor API esté corriendo en puerto 8000')
            console.error('Error:', err)
        } finally {
            setIsProcessing(false)
        }
    }

    const getIconForLogo = (logoName) => {
        const icons = {
            'apple': '🍎',
            'nike': '✔️',
            'google': '🔍',
            'microsoft': '🪟',
            'amazon': '📦',
            'facebook': '📘',
            'tesla': '⚡',
            'twitter': '𝕏',
            'instagram': '📷',
            'tiktok': '🎵'
        }
        return icons[logoName.toLowerCase()] || '🏷️'
    }

    return (
        <section id="demo" className="min-h-screen py-32 px-4 bg-gradient-to-b from-blue-900 to-slate-900 relative overflow-hidden flex items-center">
            <div className="absolute inset-0">
                <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl"></div>
            </div>

            <div className="container mx-auto max-w-3xl relative z-10 w-full">
                <h2 className="text-5xl font-black text-center mb-6 gradient-text">
                    Prueba el Demo
                </h2>
                <p className="text-center text-cyan-300 text-lg mb-20">
                    Carga imagenes, videos o usa tu cámara en tiempo real
                </p>

                <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-cyan-500/30 rounded-2xl p-12 glow">
                    {/* Pestañas */}
                    <div className="flex gap-4 mb-10 border-b border-cyan-500/20 pb-4">
                        <button
                            onClick={() => {
                                if (cameraActive) stopCamera()
                                setCameraActive(false)
                            }}
                            className={`px-6 py-2 rounded-lg font-semibold transition ${!cameraActive ? 'bg-cyan-500 text-white' : 'text-cyan-300 hover:text-cyan-100'}`}
                        >
                            📁 Imagen
                        </button>
                        <button
                            onClick={() => !cameraActive ? startCamera() : stopCamera()}
                            className={`px-6 py-2 rounded-lg font-semibold transition ${cameraActive ? 'bg-cyan-500 text-white' : 'text-cyan-300 hover:text-cyan-100'}`}
                        >
                            📷 Cámara en Vivo
                        </button>
                    </div>

                    {/* Modo Imagen */}
                    {!cameraActive && (
                        <>
                            <div className="mb-10">
                                <label className="block text-lg font-bold text-cyan-100 mb-6">
                                    📁 Selecciona una imagen
                                </label>
                                <input
                                    type="file"
                                    accept="all/*"
                                    onChange={handleImageUpload}
                                    disabled={isProcessing}
                                    className="w-full px-6 py-4 bg-slate-700/50 border-2 border-cyan-500/50 hover:border-cyan-400 rounded-xl cursor-pointer text-cyan-200 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-cyan-500 file:text-white file:font-bold file:cursor-pointer hover:file:bg-cyan-400 transition"
                                />
                            </div>

                            {imagePreview && (
                                <div className="mb-12 rounded-xl overflow-hidden border border-cyan-500/30">
                                    <img
                                        src={imagePreview}
                                        alt="Preview"
                                        className="w-full max-h-96 object-contain bg-slate-900 py-6"
                                    />
                                </div>
                            )}

                            <button
                                onClick={handleDetect}
                                disabled={!imagePreview || isProcessing}
                                className="w-full bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-400 hover:to-blue-400 disabled:from-slate-600 disabled:to-slate-700 disabled:opacity-50 font-bold py-4 px-6 rounded-xl transition transform hover:scale-105 disabled:hover:scale-100 text-white text-lg"
                            >
                                {isProcessing ? (
                                    <span className="flex items-center justify-center gap-2">
                                        <span className="animate-spin">⏳</span>
                                        Analizando imagen...
                                    </span>
                                ) : (
                                    '🔍 Detectar Logos'
                                )}
                            </button>
                        </>
                    )}

                    {/* Modo Cámara */}
                    {cameraActive && (
                        <>
                            <div className="mb-10 rounded-xl overflow-hidden border border-cyan-500/30">
                                <div className="relative bg-slate-900">
                                    <video
                                        ref={videoRef}
                                        autoPlay
                                        playsInline
                                        className="w-full max-h-96 object-cover"
                                    />
                                    <canvas ref={canvasRef} className="hidden" width={1280} height={720} />
                                    <div className="absolute top-4 right-4 bg-red-500/80 text-white px-3 py-1 rounded-lg text-sm font-semibold animate-pulse flex items-center gap-2">
                                        🔴 En vivo
                                    </div>
                                </div>
                            </div>

                            <button
                                onClick={stopCamera}
                                className="w-full bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 font-bold py-4 px-6 rounded-xl transition transform hover:scale-105 text-white text-lg mb-10"
                            >
                                🛑 Detener Cámara
                            </button>
                        </>
                    )}

                    {/* Resultados Imagen */}
                    {results && !cameraActive && (
                        <div className="mb-10 space-y-8">
                            <div className="bg-slate-900/50 border border-cyan-500/50 rounded-xl p-8">
                                <h3 className="text-lg font-bold text-cyan-100 mb-6">Resumen de Detección</h3>
                                <div className="grid grid-cols-3 gap-6">
                                    <div className="text-center">
                                        <div className="text-4xl font-black gradient-text mb-2">{results.logos}</div>
                                        <p className="text-cyan-300/80 text-sm">Logos Detectados</p>
                                    </div>
                                    <div className="text-center">
                                        <div className="text-4xl font-black gradient-text mb-2">{results.confidence}%</div>
                                        <p className="text-cyan-300/80 text-sm">Confianza General</p>
                                    </div>
                                    <div className="text-center">
                                        <div className="text-4xl font-black gradient-text mb-2">{results.processingTime}</div>
                                        <p className="text-cyan-300/80 text-sm">Tiempo de Análisis</p>
                                    </div>
                                </div>
                            </div>

                            <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-cyan-500/50 rounded-xl p-8">
                                <h3 className="text-lg font-bold text-cyan-100 mb-6">Logos Identificados</h3>
                                <div className="space-y-3">
                                    {results.detectedLogos && results.detectedLogos.map((logo, idx) => (
                                        <div key={idx} className="flex items-center justify-between bg-slate-900/50 border border-cyan-500/30 rounded-lg p-4 hover:border-cyan-500/60 transition">
                                            <div className="flex items-center gap-4">
                                                <div className="text-3xl">{logo.icon}</div>
                                                <div>
                                                    <p className="font-bold text-cyan-100">{logo.name}</p>
                                                    <p className="text-cyan-300/60 text-sm">Marca detectada</p>
                                                </div>
                                            </div>
                                            <div className="text-right">
                                                <div className="text-2xl font-black gradient-text">{logo.confidence}%</div>
                                                <p className="text-cyan-300/60 text-xs">Confianza</p>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Resultados Cámara */}
                    {cameraActive && realtimeResults && (
                        <div className="mb-10 space-y-8">
                            <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-cyan-500/50 rounded-xl p-8">
                                <h3 className="text-lg font-bold text-cyan-100 mb-6">Detección en Tiempo Real</h3>
                                <div className="space-y-3">
                                    {realtimeResults.detectedLogos && realtimeResults.detectedLogos.map((logo, idx) => (
                                        <div key={idx} className="flex items-center justify-between bg-slate-900/50 border border-cyan-500/30 rounded-lg p-4">
                                            <div className="flex items-center gap-4">
                                                <div className="text-3xl">{logo.icon}</div>
                                                <div>
                                                    <p className="font-bold text-cyan-100">{logo.name}</p>
                                                    <p className="text-cyan-300/60 text-sm">Detectado en vivo</p>
                                                </div>
                                            </div>
                                            <div className="text-right">
                                                <div className="text-2xl font-black gradient-text">{realtimeResults.confidence}%</div>
                                                <p className="text-cyan-300/60 text-xs">Confianza</p>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </section>
    )
}
