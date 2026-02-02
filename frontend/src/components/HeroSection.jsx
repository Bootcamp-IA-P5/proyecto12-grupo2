import React, { useState } from 'react'

export default function HeroSection() {
    const [count, setCount] = useState(0)

    return (
        <section id="inicio" className="relative min-h-screen bg-gradient-to-b from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center overflow-hidden py-20 px-4">
            <div className="absolute inset-0 overflow-hidden">
                <div className="absolute top-20 left-10 w-72 h-72 bg-cyan-500/10 rounded-full blur-3xl animate-pulse"></div>
                <div className="absolute bottom-20 right-10 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
            </div>

            <div className="container mx-auto max-w-4xl relative z-10 text-center">
                <div className="mb-8 inline-block">
                    <div className="text-8xl mb-4">👁️</div>
                    <h1 className="text-6xl font-black mb-4 gradient-text">KUMO VISION</h1>
                    <p className="text-xl text-cyan-300 font-semibold tracking-widest mb-2">Visión Artificial Avanzada</p>
                </div>

                <p className="text-lg text-cyan-200/80 mb-12 leading-relaxed">
                    Detección inteligente de logos con tecnología YOLO v8<br />
                    Precisión extrema + Rendimiento sin precedentes
                </p>

                <div className="bg-slate-800/50 border border-cyan-500/50 rounded-2xl p-8 backdrop-blur-sm glow">
                    <p className="text-cyan-300 font-semibold mb-6">Contador Interactivo</p>
                    <div className="flex items-center justify-center gap-6">
                        <button
                            onClick={() => setCount(count - 1)}
                            className="bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-400 hover:to-blue-400 px-8 py-4 rounded-xl font-bold text-lg transition transform hover:scale-110 active:scale-95"
                        >
                            −
                        </button>
                        <div className="text-5xl font-black gradient-text min-w-24 text-center">
                            {count}
                        </div>
                        <button
                            onClick={() => setCount(count + 1)}
                            className="bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-400 hover:to-blue-400 px-8 py-4 rounded-xl font-bold text-lg transition transform hover:scale-110 active:scale-95"
                        >
                            +
                        </button>
                    </div>
                </div>
            </div>
        </section>
    )
}
