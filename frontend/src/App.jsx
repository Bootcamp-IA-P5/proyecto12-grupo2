import './App.css'
import Header from './components/Header'
import HeroSection from './components/HeroSection'
import FeaturesSection from './components/FeaturesSection'
import DemoSection from './components/DemoSection'
import Footer from './components/Footer'

function App() {
  return (
    <div className="w-full min-h-screen flex flex-col">
      <Header />
      <HeroSection />
      <FeaturesSection />
      <DemoSection />
      <Footer />
    </div>
  )
}

export default App
