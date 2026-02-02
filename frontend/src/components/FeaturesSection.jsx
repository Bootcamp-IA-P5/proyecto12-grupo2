import React from 'react'

const features = [
    {
        icon: '🤖',
        title: 'IA Avanzada',
        description: 'YOLOv8 última generación para detección en tiempo real'
    },
    {
        icon: '⚡',
        title: 'Rendimiento',
        description: 'Procesamiento ultrarrápido sin comprometer precisión'
    },
    {
        icon: '🎯',
        title: 'Precisión',
        description: 'Detección de logos con exactitud de 98.5%'
    },
    {
        icon: '🔐',
        title: 'Seguridad',
        description: 'Procesamiento encriptado de datos sensibles'
    }
]

export default function FeaturesSection() {
    return (
        <section id="features" className="py-24 px-4 bg-gradient-to-b from-slate-900 to-blue-900">
            <div className="container mx-auto">
                <h2 className="text-5xl font-black text-center mb-4 gradient-text">
                    Características Principales
                </h2>
                <p className="text-center text-cyan-300 text-lg mb-16">
                    Tecnología de vanguardia para detección inteligente
                </p>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {features.map((feature, idx) => (
                        <div
                            key={idx}
                            className="group relative bg-gradient-to-br from-slate-800 to-slate-900 border border-cyan-500/30 rounded-2xl p-8 hover:border-cyan-500/60 transition duration-300 hover-scale glow-sm"
                        >
                            <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 to-blue-500/10 opacity-0 group-hover:opacity-100 transition rounded-2xl"></div>
                            <div className="relative z-10">
                                <div className="text-5xl mb-4 block">{feature.icon}</div>
                                <h3 className="text-xl font-bold text-cyan-100 mb-2">
                                    {feature.title}
                                </h3>
                                <p className="text-cyan-300/80 text-sm leading-relaxed">
                                    {feature.description}
                                </p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    )
}
