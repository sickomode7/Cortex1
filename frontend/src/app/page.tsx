import { Button } from "@/components/ui/button";
import { ArrowRight, Brain, Target, LineChart, Sparkles } from "lucide-react";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-slate-50 font-sans selection:bg-indigo-500/30 overflow-x-hidden">
      
      {/* Navigation - Floating Pill Style */}
      <header className="fixed top-3 right-0 left-0 z-50 mx-auto w-full max-w-[1480px] transition-all duration-300">
        <div className="px-4 py-3 bg-black/50 backdrop-blur-md rounded-full border border-white/10 flex items-center justify-between mx-4">
          <Link href="/" className="flex items-center gap-2 px-2">
            <Brain className="w-6 h-6 text-white" />
            <span className="text-xl font-bold tracking-tight text-white">Cortex</span>
          </Link>
          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-400">
            <Link href="#product" className="hover:text-white transition-colors">Product</Link>
            <Link href="#solutions" className="hover:text-white transition-colors">Solutions</Link>
            <Link href="#integrations" className="hover:text-white transition-colors">Integrations</Link>
            <Link href="#pricing" className="hover:text-white transition-colors">Pricing</Link>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/login" className="text-sm font-medium text-slate-300 hover:text-white transition-colors hidden md:block">
              Sign In
            </Link>
            <Button className="bg-white text-black hover:bg-slate-200 rounded-full px-6 h-9 font-semibold">
              Get Started
            </Button>
          </div>
        </div>
      </header>

      <main>
        {/* Hero Section */}
        <section className="relative flex flex-col pt-16 overflow-clip pb-0 min-h-[40rem] sm:min-h-[50rem]">
          {/* Gradients */}
          <div className="absolute inset-x-0 top-0 -bottom-[164px] -z-10 bg-[linear-gradient(180deg,#000_0%,#1a1918_67%)]"></div>
          
          <div className="relative mx-auto w-full max-w-[1512px] flex flex-col items-center px-6 md:px-10 grow justify-end gap-[76px] pt-24 pb-0 z-10">
            <div className="flex flex-col items-center text-center gap-7">
              <div className="flex flex-col items-center text-center gap-5">
                <h1 className="max-w-[1000px] text-5xl md:text-7xl lg:text-[5rem] font-medium tracking-tight text-white leading-[1.1]">
                  <span className="hero-word inline-block" style={{ animationDelay: '0s' }}>The</span>{' '}
                  <span className="hero-word inline-block" style={{ animationDelay: '0.08s' }}>intelligence</span>{' '}
                  <span className="hero-word inline-block" style={{ animationDelay: '0.16s' }}>layer</span>{' '}
                  <span className="hero-word inline-block" style={{ animationDelay: '0.24s' }}>for</span><br />
                  <span className="hero-word inline-block text-slate-400" style={{ animationDelay: '0.32s' }}>personalized</span>{' '}
                  <span className="hero-word inline-block text-slate-400" style={{ animationDelay: '0.40s' }}>learning</span>
                </h1>
                <p className="hero-word max-w-[500px] text-lg text-slate-400 mt-4" style={{ animationDelay: '0.75s' }}>
                  Dynamic curriculum generation, real-time mastery tracking, and an adaptive Socratic tutor—built for the modern learner.
                </p>
                <div className="hero-word mt-4" style={{ animationDelay: '1.05s' }}>
                  <Button className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-full h-12 px-8 text-base font-medium transition-all shadow-[0_0_40px_-10px_rgba(79,70,229,0.4)]">
                    Start Learning Free
                  </Button>
                </div>
              </div>
            </div>

            {/* Dashboard Mockup Placeholder */}
            <div className="relative w-full max-w-5xl mx-auto mt-8 perspective-[2000px]">
              <div className="hero-word w-full h-[400px] md:h-[600px] bg-[#0c0c0e] rounded-t-3xl border border-white/10 shadow-[0_-20px_80px_-20px_rgba(255,255,255,0.05)] overflow-hidden flex flex-col" style={{ animationDelay: '1.2s' }}>
                <div className="h-12 border-b border-white/10 flex items-center px-6 gap-2 bg-[#121214]">
                  <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
                  <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
                  <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
                </div>
                <div className="p-8 flex-1 flex flex-col gap-6 bg-[linear-gradient(180deg,#121214_0%,#000_100%)]">
                  <div className="flex flex-col sm:flex-row gap-6">
                     <div className="w-full sm:w-1/3 h-32 rounded-2xl border border-white/5 bg-white/[0.02] p-6 flex flex-col justify-between">
                       <span className="text-slate-500 text-sm font-medium">Python Mastery</span>
                       <span className="text-4xl font-semibold text-white">72%</span>
                     </div>
                     <div className="w-full sm:w-2/3 h-32 rounded-2xl border border-white/5 bg-white/[0.02] p-6 flex flex-col justify-between">
                       <span className="text-slate-500 text-sm font-medium">Next Recommended Action</span>
                       <div className="flex items-center gap-3">
                         <div className="bg-indigo-500/20 p-2 rounded-lg"><Target className="w-5 h-5 text-indigo-400" /></div>
                         <span className="text-lg sm:text-xl font-medium text-white">Review: Loops & Conditionals</span>
                       </div>
                     </div>
                  </div>
                  <div className="flex-1 rounded-2xl border border-white/5 bg-white/[0.01] p-6">
                    <div className="h-4 w-1/4 bg-white/5 rounded-full mb-6"></div>
                    <div className="space-y-4">
                      <div className="h-16 w-full bg-white/[0.02] rounded-xl border border-white/5"></div>
                      <div className="h-16 w-full bg-white/[0.02] rounded-xl border border-white/5"></div>
                      <div className="h-16 w-full bg-white/[0.02] rounded-xl border border-white/5"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Feature Cards Section */}
        <section className="mx-auto w-full px-6 md:px-10 py-24 max-w-[1512px] border-t border-white/5 bg-black">
          <h2 className="mb-16 text-4xl md:text-5xl font-medium text-white text-center tracking-tight">Accelerate your learning</h2>
          
          <div className="grid gap-6 lg:grid-cols-2">
            
            {/* Card 1 */}
            <div className="flex flex-col justify-between gap-8 p-8 md:p-12 rounded-[2rem] bg-[#0c0c0e] border border-white/5 group hover:bg-[#121214] transition-colors shadow-2xl">
              <div className="flex flex-col gap-4">
                <span className="text-sm font-medium text-indigo-400 uppercase tracking-wider">Core Engine</span>
                <h3 className="text-3xl font-medium text-white">Adaptive Curriculum</h3>
                <p className="text-lg text-slate-400 leading-relaxed max-w-md">
                  Stop following rigid syllabuses. Your learning path rearranges itself dynamically based on your performance, goals, and available time.
                </p>
              </div>
              <div className="mt-4 flex items-center text-white font-medium group-hover:text-indigo-400 transition-colors cursor-pointer w-max">
                Explore feature <ArrowRight className="ml-2 w-5 h-5" />
              </div>
            </div>

            {/* Card 2 */}
            <div className="flex flex-col justify-between gap-8 p-8 md:p-12 rounded-[2rem] bg-[#0c0c0e] border border-white/5 group hover:bg-[#121214] transition-colors shadow-2xl">
              <div className="flex flex-col gap-4">
                <span className="text-sm font-medium text-violet-400 uppercase tracking-wider">AI Assistance</span>
                <h3 className="text-3xl font-medium text-white">Socratic Tutor</h3>
                <p className="text-lg text-slate-400 leading-relaxed max-w-md">
                  Our AI doesn't just give you the answer. It asks guiding questions to help you build the mental models yourself, mimicking a real mentor.
                </p>
              </div>
              <div className="mt-4 flex items-center text-white font-medium group-hover:text-violet-400 transition-colors cursor-pointer w-max">
                Explore feature <ArrowRight className="ml-2 w-5 h-5" />
              </div>
            </div>

          </div>
        </section>
      </main>
    </div>
  );
}
