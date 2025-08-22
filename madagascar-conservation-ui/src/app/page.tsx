'use client'

import { useState, useEffect } from 'react'
import { 
  ChartBarIcon, 
  GlobeAltIcon, 
  EyeIcon, 
  ShieldCheckIcon,
  MapIcon,
  BeakerIcon,
  CpuChipIcon,
  ArrowRightIcon
} from '@heroicons/react/24/outline'

export default function HomePage() {
  const [isLoaded, setIsLoaded] = useState(false)

  useEffect(() => {
    setIsLoaded(true)
  }, [])

  const features = [
    {
      icon: <GlobeAltIcon className="w-8 h-8" />,
      title: "Real-time Ecosystem Monitoring",
      description: "AI-powered satellite analysis tracking deforestation, habitat changes, and biodiversity patterns across Madagascar's unique landscapes.",
      gradient: "from-emerald-500 to-teal-600"
    },
    {
      icon: <EyeIcon className="w-8 h-8" />,
      title: "Species Detection & Tracking",
      description: "Advanced computer vision models identifying and monitoring endemic species including lemurs, fossas, and rare birds through camera trap networks.",
      gradient: "from-blue-500 to-cyan-600"
    },
    {
      icon: <ChartBarIcon className="w-8 h-8" />,
      title: "Predictive Conservation Analytics",
      description: "Machine learning algorithms predicting habitat loss, species migration patterns, and optimal conservation intervention strategies.",
      gradient: "from-purple-500 to-violet-600"
    },
    {
      icon: <ShieldCheckIcon className="w-8 h-8" />,
      title: "Anti-Poaching Intelligence",
      description: "Real-time threat detection system using acoustic monitoring and movement pattern analysis to prevent illegal hunting activities.",
      gradient: "from-orange-500 to-red-600"
    },
    {
      icon: <MapIcon className="w-8 h-8" />,
      title: "Interactive Conservation Maps",
      description: "Dynamic geospatial visualizations showing protected areas, species distributions, and conservation priority zones for stakeholder decision-making.",
      gradient: "from-green-500 to-emerald-600"
    },
    {
      icon: <BeakerIcon className="w-8 h-8" />,
      title: "Research Collaboration Hub",
      description: "Integrated platform connecting local researchers, international scientists, and conservation organizations for data sharing and collaborative studies.",
      gradient: "from-indigo-500 to-blue-600"
    }
  ]

  const stats = [
    { label: "Protected Areas Monitored", value: "47", unit: "National Parks" },
    { label: "Species Under AI Surveillance", value: "200+", unit: "Endemic Species" },
    { label: "Real-time Data Streams", value: "1,200", unit: "IoT Sensors" },
    { label: "Conservation Success Rate", value: "94%", unit: "Improvement" }
  ]

  return (
    <div className="min-h-screen">
      {/* Header Navigation */}
      <header className="relative z-50 glass-effect border-b border-white/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-emerald-600 to-blue-600 rounded-lg flex items-center justify-center">
                <GlobeAltIcon className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gradient">Madagascar Conservation AI</h1>
                <p className="text-xs text-gray-600">Protecting Biodiversity with Technology</p>
              </div>
            </div>
            <nav className="hidden md:flex space-x-8">
              <a href="#monitoring" className="text-gray-700 hover:text-emerald-600 transition-colors">Monitoring</a>
              <a href="#analytics" className="text-gray-700 hover:text-emerald-600 transition-colors">Analytics</a>
              <a href="#research" className="text-gray-700 hover:text-emerald-600 transition-colors">Research</a>
              <a href="#about" className="text-gray-700 hover:text-emerald-600 transition-colors">About</a>
            </nav>
            <button className="bg-gradient-to-r from-emerald-600 to-blue-600 text-white px-6 py-2 rounded-lg hover:shadow-lg transition-all">
              Dashboard
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-blue-50 to-purple-50"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className={`text-center transform transition-all duration-1000 ${isLoaded ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
            <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-6">
              Protecting
              <span className="text-gradient block">Madagascar's</span>
              Biodiversity
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-4xl mx-auto">
              Advanced AI technology safeguarding the world's 4th largest island and its unique ecosystems 
              through real-time monitoring, predictive analytics, and intelligent conservation strategies.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-gradient-to-r from-emerald-600 to-blue-600 text-white px-8 py-4 rounded-xl text-lg font-semibold hover:shadow-xl transition-all flex items-center justify-center space-x-2">
                <span>Explore Live Data</span>
                <ArrowRightIcon className="w-5 h-5" />
              </button>
              <button className="border-2 border-emerald-600 text-emerald-600 px-8 py-4 rounded-xl text-lg font-semibold hover:bg-emerald-50 transition-all">
                View Research
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className={`text-center transform transition-all duration-500 delay-${index * 100}`}>
                <div className="text-4xl md:text-5xl font-bold text-gradient mb-2">{stat.value}</div>
                <div className="text-sm font-medium text-gray-600 mb-1">{stat.label}</div>
                <div className="text-xs text-gray-500">{stat.unit}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-24 bg-gradient-to-b from-white to-gray-50" id="monitoring">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              AI-Powered Conservation
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Comprehensive technology platform combining satellite imagery, IoT sensors, 
              machine learning, and local expertise to protect Madagascar's irreplaceable biodiversity.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div 
                key={index} 
                className={`card p-8 group hover:scale-105 transition-all duration-300 animate-fade-in`}
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className={`w-16 h-16 bg-gradient-to-br ${feature.gradient} rounded-xl flex items-center justify-center text-white mb-6 group-hover:scale-110 transition-transform`}>
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technology Stack */}
      <section className="py-24 bg-gradient-to-br from-emerald-900 to-blue-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <CpuChipIcon className="w-16 h-16 mx-auto mb-6 text-emerald-300" />
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Cutting-Edge Technology
            </h2>
            <p className="text-xl text-emerald-100 max-w-3xl mx-auto">
              Built on robust, scalable infrastructure designed for Madagascar's unique environmental challenges.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-8 rounded-xl bg-white/10 backdrop-blur">
              <div className="text-3xl font-bold text-emerald-300 mb-2">9</div>
              <div className="text-lg font-semibold mb-2">Microservices</div>
              <div className="text-emerald-100 text-sm">Scalable, resilient architecture</div>
            </div>
            <div className="text-center p-8 rounded-xl bg-white/10 backdrop-blur">
              <div className="text-3xl font-bold text-blue-300 mb-2">100%</div>
              <div className="text-lg font-semibold mb-2">Deployment Ready</div>
              <div className="text-blue-100 text-sm">Validated production pipeline</div>
            </div>
            <div className="text-center p-8 rounded-xl bg-white/10 backdrop-blur">
              <div className="text-3xl font-bold text-purple-300 mb-2">24/7</div>
              <div className="text-lg font-semibold mb-2">Monitoring</div>
              <div className="text-purple-100 text-sm">Real-time ecosystem surveillance</div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-24 bg-gradient-to-r from-emerald-600 to-blue-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Join the Conservation Revolution
          </h2>
          <p className="text-xl text-emerald-100 mb-8">
            Experience how artificial intelligence can transform wildlife protection 
            and ecosystem preservation for Madagascar's future.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-white text-emerald-600 px-8 py-4 rounded-xl text-lg font-semibold hover:shadow-xl transition-all">
              Request Demo
            </button>
            <button className="border-2 border-white text-white px-8 py-4 rounded-xl text-lg font-semibold hover:bg-white/10 transition-all">
              View Documentation
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="col-span-2">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-emerald-600 to-blue-600 rounded-lg flex items-center justify-center">
                  <GlobeAltIcon className="w-6 h-6 text-white" />
                </div>
                <span className="text-xl font-bold">Madagascar Conservation AI</span>
              </div>
              <p className="text-gray-400 mb-4 max-w-md">
                Leveraging artificial intelligence to protect and preserve Madagascar's unique biodiversity 
                for current and future generations.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Platform</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Live Monitoring</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Analytics Dashboard</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Research Tools</a></li>
                <li><a href="#" className="hover:text-white transition-colors">API Access</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Resources</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Research Papers</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Case Studies</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Support</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-12 pt-8 text-center text-gray-400">
            <p>&copy; 2024 Madagascar Conservation AI. Protecting biodiversity through technology.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
