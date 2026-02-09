import React from 'react'

export default function Footer() {
    const currentYear = new Date().getFullYear()

    return (
        <footer className="bg-gradient-to-b from-slate-900 to-black border-t border-cyan-500/20 text-cyan-200/80 py-12 px-4">
            <div className="container mx-auto">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-12 mb-12">
                    <div>
                        <h4 className="text-2xl font-black gradient-text mb-4 flex items-center gap-2">
                            👁️ KUMO VISION
                        </h4>
                        <p className="text-sm leading-relaxed">
                            Sistema avanzado de detección de logos basado en IA. Proporcionamos soluciones de visión artificial de próxima generación.
                        </p>
                    </div>
                    <div>
                        <h4 className="text-cyan-100 font-bold mb-4">Enlaces Rápidos</h4>
                        <ul className="text-sm space-y-2">
                            <li><a href="#inicio" className="hover:text-cyan-300 transition">Inicio</a></li>
                            <li><a href="#features" className="hover:text-cyan-300 transition">Características</a></li>
                            <li><a href="#demo" className="hover:text-cyan-300 transition">Demo</a></li>
                            <li><a href="#" className="hover:text-cyan-300 transition">API</a></li>
                        </ul>
                    </div>
                    <div>
                        <h4 className="text-cyan-100 font-bold mb-4">Contacto</h4>
                        <p className="text-sm">📧 info@kumovision.ai</p>
                        <p className="text-sm">🌐 www.kumovision.ai</p>
                        <p className="text-sm mt-4">Bootcamp IA - Grupo 2</p>
                    </div>
                </div>
                <div className="border-t border-cyan-500/20 pt-8 text-center text-sm">
                    <p>&copy; {currentYear} KUMO VISION. Todos los derechos reservados. Hecho con ❤️ por el Equipo de Desarrollo</p>
                </div>
            </div>
        </footer>
    )
}
