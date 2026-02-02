import React from 'react'

export default function Header() {
    return (
        <header className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border-b border-cyan-500/30 sticky top-0 z-50 glow-sm">
            <div className="container mx-auto px-4 py-4">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="text-4xl">👁️</div>
                        <div>
                            <h1 className="text-3xl font-black gradient-text">KUMO VISION</h1>
                            <p className="text-cyan-300 text-xs tracking-widest">Detección Inteligente de Logos</p>
                        </div>
                    </div>
                    <nav className="flex gap-8 text-sm font-semibold">
                        <a href="#inicio" className="text-cyan-300 hover:text-cyan-100 transition">Inicio</a>
                        <a href="#features" className="text-cyan-300 hover:text-cyan-100 transition">Características</a>
                        <a href="#demo" className="text-cyan-300 hover:text-cyan-100 transition">Demo</a>
                    </nav>
                </div>
            </div>
        </header>
    )
}
