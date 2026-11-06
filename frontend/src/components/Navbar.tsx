import React from 'react';
import { 
  Sparkles, 
  RotateCcw, 
  ShieldAlert, 
  PiggyBank, 
  Scale, 
  Award, 
  LayoutDashboard 
} from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  onResetDemo: () => void;
  isResetting?: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  onResetDemo,
  isResetting = false,
}) => {
  const navItems = [
    { id: 'dashboard', label: 'Boshqaruv Paneli', icon: LayoutDashboard },
    { id: 'smart-pause', label: 'Smart Pause', icon: ShieldAlert, badge: 'Flagman' },
    { id: 'savings', label: 'Invisible Savings', icon: PiggyBank },
    { id: 'debt-coach', label: 'Debt Coach', icon: Scale },
    { id: 'score', label: 'Xulq-atvor Bali', icon: Award },
  ];

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200 bg-white/90 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 text-white shadow-md shadow-emerald-500/20">
            <Sparkles className="h-5 w-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl font-extrabold tracking-tight text-slate-900">
                Fin<span className="text-emerald-600">Bridge</span>
              </span>
              <span className="rounded-full bg-emerald-50 px-2 py-0.5 text-[10px] font-bold text-emerald-700 border border-emerald-200">
                UZS
              </span>
            </div>
            <p className="text-xs text-slate-500 font-medium">Behavioral Finance Platform</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="hidden md:flex items-center gap-1 rounded-2xl bg-slate-100/80 p-1 border border-slate-200/60">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`relative flex items-center gap-2 rounded-xl px-3.5 py-2 text-xs font-semibold transition-all ${
                  isActive
                    ? 'bg-white text-emerald-800 shadow-sm border border-slate-200/50'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
                }`}
              >
                <Icon className={`h-4 w-4 ${isActive ? 'text-emerald-600' : 'text-slate-400'}`} />
                <span>{item.label}</span>
                {item.badge && (
                  <span className="rounded bg-emerald-100 px-1.5 py-0.2 text-[9px] font-bold text-emerald-700">
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Demo reset action */}
        <div className="flex items-center gap-2">
          <button
            onClick={onResetDemo}
            disabled={isResetting}
            title="Barcha ma'lumotlarni boshlang'ich demo holatiga qaytarish"
            className="flex items-center gap-1.5 rounded-xl border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-600 shadow-sm transition hover:bg-slate-50 hover:text-slate-900 active:scale-95 disabled:opacity-50"
          >
            <RotateCcw className={`h-3.5 w-3.5 ${isResetting ? 'animate-spin text-emerald-600' : ''}`} />
            <span className="hidden sm:inline">Demoni tiklash</span>
          </button>
        </div>
      </div>

      {/* Mobile nav */}
      <div className="flex md:hidden border-t border-slate-100 overflow-x-auto px-4 py-2 gap-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex items-center gap-1.5 whitespace-nowrap rounded-lg px-3 py-1.5 text-xs font-semibold ${
                isActive ? 'bg-emerald-600 text-white' : 'bg-slate-100 text-slate-600'
              }`}
            >
              <Icon className="h-3.5 w-3.5" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>
    </header>
  );
};
