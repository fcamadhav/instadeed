import re

# Read current landing.html content
with open("landing.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Define the premium Light Theme style block
light_css = """:root {
  --blue: #2563EB;
  --blue-l: #3B82F6;
  --blue-d: #1D4ED8;
  --blue-glow: rgba(59, 130, 246, 0.08);
  --cyan: #06B6D4;
  --cyan-l: #0891B2;
  --emerald: #10B981;
  --purple: #8B5CF6;
  --rose: #F43F5E;
  --amber: #F59E0B;
  
  --bg-dark: #F8FAFC;
  --bg-slate: #FFFFFF;
  --border-light: rgba(15, 23, 42, 0.06);
  --border-glow: rgba(59, 130, 246, 0.25);
  --text-primary: #0F172A;
  --text-secondary: #475569;
  --text-muted: #94A3B8;
  
  --shadow-glow: 0 0 30px rgba(59, 130, 246, 0.06), 0 10px 40px rgba(15, 23, 42, 0.04);
  
  --r: 12px;
  --rl: 16px;
  --rxl: 20px;
  --r2xl: 24px;
  --rf: 9999px;
}

*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
  scroll-padding-top: 76px;
}

body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: var(--bg-dark);
  color: var(--text-primary);
  line-height: 1.6;
  overflow-x: hidden;
  position: relative;
}

a {
  text-decoration: none;
  color: inherit;
}

button {
  font-family: inherit;
  cursor: pointer;
  border: none;
  background: none;
}

img {
  display: block;
  max-width: 100%;
}

/* ═══════════════════════
   AMBIENT GLOW SYSTEM
   ═══════════════════════ */
.glow-blob {
  position: absolute;
  width: 65vw;
  height: 65vw;
  filter: blur(140px);
  pointer-events: none;
  z-index: 0;
  opacity: 0.55;
  border-radius: 50%;
}
.blob1 { top: 0%; left: -20%; }
.blob2 { top: 22%; right: -20%; }
.blob3 { top: 48%; left: -10%; }
.blob4 { top: 70%; right: -15%; }
.blob5 { top: 88%; left: -15%; }

/* ═══════════════════════
   TOP ANNOUNCEMENT BAR
   ═══════════════════════ */
.topbar {
  background: linear-gradient(90deg, #090C15 0%, #1E3A8A 50%, #090C15 100%);
  padding: .55rem 1.5rem;
  text-align: center;
  font-size: .78rem;
  font-weight: 500;
  color: rgba(255, 255, 255, .9);
  letter-spacing: .02em;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  position: relative;
  z-index: 310;
}

/* ═══════════════════════
   NAV — Glassmorphism Light
   ═══════════════════════ */
.nav {
  position: sticky;
  top: 0;
  z-index: 300;
  background: rgba(255, 255, 255, 0.85);
  border-bottom: 1px solid rgba(15, 23, 42, 0.06);
  backdrop-filter: blur(20px) saturate(180%);
  transition: all .25s;
}
.nav-inner {
  max-width: 1240px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: .5rem;
  padding: .8rem 1.5rem;
}
.logo-wrap {
  display: inline-flex;
  align-items: center;
  gap: .65rem;
  cursor: pointer;
  flex-shrink: 0;
  text-decoration: none;
}
.logo-mark {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--blue), #3B82F6);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 15px rgba(37, 99, 235, .25);
  transition: all .3s;
}
.logo-wrap:hover .logo-mark {
  transform: scale(1.04);
  box-shadow: 0 0 20px rgba(37, 99, 235, .4);
}
.logo-mark svg { width: 18px; height: 18px; }
.logo-wordmark {
  font-family: 'Outfit', sans-serif;
  font-weight: 900;
  font-size: 1.45rem;
  letter-spacing: -.04em;
  line-height: 1;
  display: inline-flex;
  align-items: baseline;
  gap: 0;
}
.lw-part1 { color: #0F172A; }
.lw-part2 { color: #2563EB; }
.lw-tld {
  font-family: 'Outfit', sans-serif;
  font-size: .65rem;
  font-weight: 900;
  color: #FFFFFF;
  background: #2563EB;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  margin-left: .25rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(37, 99, 235, .3);
}

.nav-links {
  flex: 1;
  display: flex;
  align-items: stretch;
  justify-content: center;
  gap: .5rem;
}
.nav-link {
  font-size: .85rem;
  font-weight: 600;
  color: var(--text-secondary);
  padding: .4rem .9rem;
  border-radius: var(--rf);
  transition: all .18s;
  cursor: pointer;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: .3rem;
}
.nav-link:hover {
  color: #0F172A;
  background: rgba(15, 23, 42, 0.04);
}
.nav-link i.chevron {
  font-size: .6rem;
  transition: transform .2s;
}
.nav-link:hover i.chevron {
  transform: rotate(180deg);
}

.nav-item { position: relative; }
.nav-dropdown {
  position: absolute;
  top: calc(100% + 12px);
  left: 50%;
  transform: translateX(-50%) translateY(-6px);
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: var(--rl);
  padding: .6rem;
  min-width: 245px;
  box-shadow: 0 20px 40px rgba(15, 23, 42, 0.08);
  opacity: 0;
  visibility: hidden;
  transition: all .2s;
  z-index: 100;
}
.nav-item:hover .nav-dropdown {
  opacity: 1;
  visibility: visible;
  transform: translateX(-50%) translateY(0);
}
.dd-item {
  display: flex;
  align-items: center;
  gap: .75rem;
  padding: .65rem .9rem;
  border-radius: var(--r);
  color: #334155;
  font-size: .84rem;
  font-weight: 600;
  cursor: pointer;
  transition: all .18s;
}
.dd-item:hover {
  background: rgba(15, 23, 42, 0.04);
  color: #0F172A;
}
.dd-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: .82rem;
  flex-shrink: 0;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: .65rem;
  flex-shrink: 0;
}
.nav-phone-pill {
  display: flex;
  align-items: center;
  gap: .4rem;
  font-size: .78rem;
  font-weight: 700;
  color: var(--text-secondary);
  border: 1px solid rgba(15, 23, 42, 0.12);
  border-radius: var(--rf);
  padding: .42rem .95rem;
  transition: all .18s;
}
.nav-phone-pill:hover {
  border-color: #2563EB;
  color: #2563EB;
  background: rgba(37, 99, 235, 0.05);
}
.btn-nav-login {
  font-size: .82rem;
  font-weight: 700;
  color: #0F172A;
  border: 1px solid rgba(15, 23, 42, 0.18);
  border-radius: var(--rf);
  padding: .42rem 1.15rem;
  transition: all .18s;
}
.btn-nav-login:hover {
  background: rgba(15, 23, 42, 0.04);
  border-color: #0f172a;
}
.btn-nav-signup {
  font-size: .82rem;
  font-weight: 800;
  color: #fff;
  background: linear-gradient(135deg, var(--blue), #3B82F6);
  border-radius: var(--rf);
  padding: .45rem 1.25rem;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
  transition: all .2s;
}
.btn-nav-signup:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(37, 99, 235, 0.3);
}

/* User chip integration */
.nav-auth-area {
  display: flex;
  align-items: center;
}
.user-chip {
  display: none;
  align-items: center;
  gap: .5rem;
  padding: .35rem .75rem;
  background: rgba(15, 23, 42, 0.03);
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: var(--rf);
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
}
.user-chip:hover {
  background: rgba(15, 23, 42, 0.06);
  border-color: rgba(15, 23, 42, 0.15);
}
.user-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--blue);
  color: #fff;
  font-weight: 700;
  font-size: .75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.user-name {
  font-size: .8rem;
  font-weight: 600;
  color: #0F172A;
}
.user-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(15, 23, 42, 0.1);
  border-radius: var(--rl);
  width: 200px;
  box-shadow: 0 10px 25px rgba(15, 23, 42, 0.1);
  display: none;
  z-index: 1000;
  padding: .5rem;
  backdrop-filter: blur(15px);
}
.user-menu-header {
  padding: .5rem .75rem;
  border-bottom: 1px solid rgba(15, 23, 42, 0.08);
  margin-bottom: .4rem;
}
.user-menu-email {
  font-size: .72rem;
  color: var(--text-secondary);
  word-break: break-all;
}
.user-menu-item {
  display: flex;
  align-items: center;
  gap: .6rem;
  padding: .5rem .75rem;
  font-size: .8rem;
  font-weight: 600;
  color: #334155;
  border-radius: var(--r);
  transition: all .18s;
}
.user-menu-item:hover {
  background: rgba(15, 23, 42, 0.04);
  color: #0F172A;
}
.nav-auth-signed-in .nav-auth-signed-out {
  display: none !important;
}

/* ═══════════════════════
   HERO — Light Glass
   ═══════════════════════ */
.hero {
  background: transparent;
  position: relative;
  overflow: hidden;
  padding: 6.5rem 1.5rem 5.5rem;
  border-bottom: 1px solid rgba(15, 23, 42, 0.05);
}
.hero-inner {
  max-width: 1240px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 4rem;
  position: relative;
  z-index: 1;
}
.hero-left {
  flex: 1.1;
  min-width: 0;
}
.hero-right {
  flex: 0.9;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: heroFloat 6s ease-in-out infinite alternate;
}
@keyframes heroFloat {
  0% { transform: translateY(0) rotate(0deg) }
  100% { transform: translateY(-15px) rotate(0.5deg) }
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: .5rem;
  background: rgba(15, 23, 42, 0.03);
  border: 1px solid rgba(15, 23, 42, 0.06);
  border-radius: var(--rf);
  padding: .4rem 1.1rem;
  font-size: .73rem;
  font-weight: 700;
  color: var(--text-secondary);
  margin-bottom: 1.8rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.hero-badge .live-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #10B981;
  flex-shrink: 0;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, .25);
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 2px rgba(16, 185, 129, .25) }
  50% { box-shadow: 0 0 0 5px rgba(16, 185, 129, .1) }
}

.hero-h1 {
  font-family: 'Outfit', sans-serif;
  font-size: clamp(2.4rem, 4.8vw, 3.8rem);
  font-weight: 900;
  line-height: 1.1;
  letter-spacing: -.04em;
  color: #0F172A;
  margin-bottom: 1.3rem;
}
.hero-h1 .grad {
  background: linear-gradient(135deg, #2563EB 0%, #06B6D4 50%, #10B981 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-sub {
  font-size: 1.05rem;
  color: var(--text-secondary);
  max-width: 550px;
  margin-bottom: 2.2rem;
  line-height: 1.75;
}

/* ── Search bar ── */
.hero-search-wrap {
  max-width: 560px;
  margin-bottom: 1.3rem;
}
.hero-search {
  display: flex;
  align-items: center;
  gap: .75rem;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: var(--rf);
  padding: .75rem .95rem .75rem 1.4rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 25px rgba(15, 23, 42, 0.03);
  transition: all .25s;
}
.hero-search:focus-within {
  border-color: #2563EB;
  background: #FFFFFF;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1), 0 15px 30px rgba(0,0,0,0.03);
}
.hero-search i {
  color: #94A3B8;
  font-size: 1.1rem;
  flex-shrink: 0;
}
.hero-search input {
  flex: 1;
  border: none;
  outline: none;
  font-size: .98rem;
  color: #0F172A;
  background: transparent;
  font-family: 'Inter', sans-serif;
}
.hero-search input::placeholder { color: #94A3B8 }
.btn-search {
  font-size: .85rem;
  font-weight: 800;
  color: #fff;
  background: linear-gradient(135deg, var(--blue), #3B82F6);
  padding: .55rem 1.45rem;
  border-radius: var(--rf);
  white-space: nowrap;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
  transition: all .18s;
}
.btn-search:hover {
  transform: scale(1.02);
  box-shadow: 0 6px 18px rgba(37, 99, 235, 0.3);
}

.hero-tags {
  display: flex;
  gap: .6rem;
  flex-wrap: wrap;
  margin-bottom: 2.2rem;
}
.hero-tag {
  font-size: .78rem;
  font-weight: 600;
  color: #2563EB;
  cursor: pointer;
  transition: color .18s;
  display: flex;
  align-items: center;
  gap: .25rem;
}
.hero-tag:hover {
  color: #1D4ED8;
  text-decoration: underline;
}
.hero-tag-sep {
  color: #E2E8F0;
  font-size: .75rem;
}

.hero-pills {
  display: flex;
  gap: .8rem;
  flex-wrap: wrap;
}
.hero-pill {
  display: inline-flex;
  align-items: center;
  gap: .55rem;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(15, 23, 42, 0.06);
  border-radius: var(--rf);
  padding: .6rem 1.15rem;
  font-size: .84rem;
  font-weight: 700;
  color: #334155;
  cursor: pointer;
  transition: all .22s;
}
.hero-pill i { font-size: .88rem; }
.hero-pill:hover {
  border-color: #2563EB;
  color: #2563EB;
  background: rgba(37, 99, 235, 0.04);
  transform: translateY(-1px);
}

/* Document Card Mockup */
.hero-visual {
  position: relative;
  width: 100%;
  max-width: 440px;
}
.doc-mockup {
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(15, 23, 42, 0.06);
  border-radius: var(--rxl);
  box-shadow: 0 20px 40px rgba(15, 23, 42, 0.05);
  padding: 1.8rem;
  width: 100%;
  backdrop-filter: blur(12px);
}
.dm-header {
  display: flex;
  align-items: center;
  gap: .85rem;
  margin-bottom: 1.4rem;
}
.dm-icon {
  width: 46px;
  height: 46px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.06), rgba(139, 92, 246, 0.08));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.15rem;
  color: #2563EB;
  flex-shrink: 0;
  border: 1px solid rgba(59, 130, 246, 0.15);
}
.dm-title {
  font-family: 'Outfit', sans-serif;
  font-weight: 800;
  font-size: 1.05rem;
  color: #0F172A;
  transition: opacity 0.4s ease-in-out;
}
.dm-sub {
  font-size: .73rem;
  color: var(--text-secondary);
  margin-top: .12rem;
  transition: opacity 0.4s ease-in-out;
}
.dm-line {
  height: 7px;
  background: rgba(15, 23, 42, 0.04);
  border-radius: 4px;
  margin-bottom: .7rem;
}
.dm-line.w-full { width: 100% }
.dm-line.w-3q { width: 75% }
.dm-line.w-half { width: 50% }
.dm-line.w-2q { width: 65% }
.dm-sig-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 1.4rem;
  padding-top: 1.2rem;
  border-top: 1px dashed rgba(15, 23, 42, 0.08);
}
.dm-sig {
  display: inline-flex;
  align-items: center;
  gap: .5rem;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, .2);
  border-radius: var(--rf);
  padding: .4rem .9rem;
  font-size: .73rem;
  font-weight: 800;
  color: #10B981;
}
.dm-date {
  font-size: .73rem;
  color: var(--text-muted);
}

.float-card {
  position: absolute;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(15, 23, 42, 0.06);
  border-radius: var(--rl);
  padding: .8rem 1rem;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.03);
  display: flex;
  align-items: center;
  gap: .6rem;
  font-size: .8rem;
  font-weight: 700;
  color: #334155;
  animation: cardFloat 6s ease-in-out infinite alternate;
  backdrop-filter: blur(10px);
}
.float-card.fc1 { top: -20px; right: -15px; animation-duration: 7s }
.float-card.fc2 { bottom: 35px; left: -25px; animation-duration: 8s; animation-delay: -3s }
.float-card .fci {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: .82rem;
}
.fci.ic-g {
  background: rgba(16, 185, 129, 0.1);
  color: #10B981;
  border: 1px solid rgba(16, 185, 129, 0.2);
}
.fci.ic-b {
  background: rgba(37, 99, 235, 0.08);
  color: #2563EB;
  border: 1px solid rgba(37, 99, 235, 0.15);
}
.fci.ic-o {
  background: rgba(249, 115, 22, 0.08);
  color: #EA580C;
  border: 1px solid rgba(249, 115, 22, 0.15);
}
.fci.ic-p {
  background: rgba(139, 92, 246, 0.08);
  color: #8B5CF6;
  border: 1px solid rgba(139, 92, 246, 0.15);
}
.fci.ic-a {
  background: rgba(6, 182, 212, 0.08);
  color: #0891B2;
  border: 1px solid rgba(6, 182, 212, 0.15);
}
.fci.ic-s {
  background: rgba(16, 185, 129, 0.1);
  color: #10B981;
  border: 1px solid rgba(16, 185, 129, 0.2);
}
@keyframes cardFloat { 0% { transform: translateY(0) } 100% { transform: translateY(-12px) } }

/* ═══════════════════════
   STATS BAR (Light Glass)
   ═══════════════════════ */
.stats-bar {
  background: rgba(255, 255, 255, 0.7);
  border-bottom: 1px solid rgba(15, 23, 42, 0.05);
  padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
  backdrop-filter: blur(15px);
  position: relative;
  z-index: 10;
}
.stats-inner {
  max-width: 1050px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
}
.stat-item {
  text-align: center;
  padding: .4rem 2.8rem;
}
.stat-num {
  font-family: 'Outfit', sans-serif;
  font-size: 1.85rem;
  font-weight: 900;
  color: #0F172A;
  line-height: 1;
  text-shadow: 0 0 15px rgba(37, 99, 235, 0.1);
}
.stat-label {
  font-size: .75rem;
  color: var(--text-secondary);
  margin-top: .35rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}
.stat-div {
  width: 1px;
  height: 44px;
  background: rgba(15, 23, 42, 0.06);
  flex-shrink: 0;
}

/* Trust logos */
.trust-bar {
  background: rgba(255, 255, 255, 0.35);
  border-bottom: 1px solid rgba(15, 23, 42, 0.04);
  padding: 1rem 1.5rem;
  position: relative;
  z-index: 10;
}
.trust-inner {
  max-width: 1050px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
  justify-content: center;
}
.trust-label {
  font-size: .72rem;
  font-weight: 700;
  color: var(--text-muted);
  letter-spacing: .08em;
  text-transform: uppercase;
  white-space: nowrap;
}
.trust-sep {
  width: 1px;
  height: 20px;
  background: rgba(15, 23, 42, 0.06);
}
.trust-badge {
  display: flex;
  align-items: center;
  gap: .45rem;
  font-size: .76rem;
  font-weight: 700;
  color: #334155;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(15, 23, 42, 0.06);
  border-radius: var(--rf);
  padding: .35rem .95rem;
  box-shadow: var(--shadow-xs);
}
.trust-badge i { font-size: .8rem }
.trust-badge.green {
  color: #069669;
  border-color: rgba(16, 185, 129, .15);
  background: rgba(16, 185, 129, .03);
}
.trust-badge.blue {
  color: #2563EB;
  border-color: rgba(59, 130, 246, .15);
  background: rgba(59, 130, 246, .03);
}

/* ═══════════════════════
   SECTION COMMON
   ═══════════════════════ */
section {
  position: relative;
  z-index: 10;
}
.wrapper {
  max-width: 1240px;
  margin: 0 auto;
  padding: 0 1.5rem;
}
.sp { padding: 5.5rem 0 }
.sec-label {
  display: inline-flex;
  align-items: center;
  gap: .4rem;
  font-size: .72rem;
  font-weight: 800;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: #2563EB;
  background: rgba(59, 130, 246, 0.06);
  border: 1px solid rgba(59, 130, 246, 0.15);
  border-radius: var(--rf);
  padding: .3rem .9rem;
  margin-bottom: 1rem;
}
.sec-title {
  font-family: 'Outfit', sans-serif;
  font-size: clamp(1.7rem, 3.2vw, 2.4rem);
  font-weight: 800;
  letter-spacing: -.035em;
  color: #0F172A;
  line-height: 1.2;
}
.sec-sub {
  color: var(--text-secondary);
  font-size: 1rem;
  margin-top: .85rem;
  line-height: 1.7;
  max-width: 550px;
}
.sec-head {
  text-align: center;
  margin-bottom: 3rem;
}
.sec-head .sec-sub {
  margin-left: auto;
  margin-right: auto;
}

/* ═══════════════════════
   POPULAR DOCS STRIP
   ═══════════════════════ */
.popular-strip {
  background: rgba(255, 255, 255, 0.5);
  border-bottom: 1px solid rgba(15, 23, 42, 0.04);
  padding: 1.4rem;
  position: relative;
  z-index: 10;
}
.pop-inner {
  max-width: 1240px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 1.1rem;
  overflow-x: auto;
  scrollbar-width: none;
}
.pop-inner::-webkit-scrollbar { display: none }
.pop-label {
  font-size: .72rem;
  font-weight: 800;
  color: var(--text-muted);
  letter-spacing: .08em;
  text-transform: uppercase;
  white-space: nowrap;
  flex-shrink: 0;
}
.pop-sep {
  width: 1px;
  height: 20px;
  background: rgba(15, 23, 42, 0.08);
  flex-shrink: 0;
}
.pop-chip {
  display: inline-flex;
  align-items: center;
  gap: .5rem;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(15, 23, 42, 0.06);
  border-radius: var(--rf);
  padding: .42rem 1.05rem;
  font-size: .82rem;
  font-weight: 700;
  color: #475569;
  white-space: nowrap;
  cursor: pointer;
  transition: all .18s;
  flex-shrink: 0;
}
.pop-chip i { font-size: .8rem }
.pop-chip:hover {
  background: rgba(59, 130, 246, 0.05);
  border-color: #2563EB;
  color: #2563EB;
}
.pop-chip.hot {
  background: rgba(249, 115, 22, 0.04);
  border-color: rgba(249, 115, 22, 0.15);
  color: #EA580C;
}

/* ═══════════════════════
   HOW IT WORKS (Light Glass Steps)
   ═══════════════════════ */
.how-section {
  background: transparent;
  border-bottom: 1px solid rgba(15, 23, 42, 0.05);
}
.steps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.8rem;
  position: relative;
}
.steps-grid::after {
  content: '';
  position: absolute;
  top: 48px;
  left: calc(33.3% + 0px);
  right: calc(33.3% + 0px);
  height: 2px;
  background: linear-gradient(90deg, rgba(15, 23, 42, 0.03), rgba(15, 23, 42, 0.12), rgba(15, 23, 42, 0.03));
  z-index: 0;
}
.step-card {
  background: rgba(255, 255, 255, 0.75);
  border: 1px solid rgba(15, 23, 42, 0.05);
  border-radius: var(--rxl);
  padding: 2.2rem 1.8rem;
  text-align: center;
  position: relative;
  z-index: 1;
  box-shadow: 0 10px 25px rgba(15, 23, 42, 0.02);
  transition: all .3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  backdrop-filter: blur(12px);
}
.step-card:hover {
  box-shadow: 0 15px 30px rgba(37, 99, 235, 0.08);
  transform: translateY(-4px);
  border-color: #2563EB;
}
.step-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--blue), #8B5CF6);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform .3s;
}
.step-card:hover::before { transform: scaleX(1) }
.step-bubble {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(37, 99, 235, 0.05);
  border: 2px solid rgba(37, 99, 235, .15);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.4rem;
  transition: all .25s;
}
.step-card:hover .step-bubble {
  background: #2563EB;
  border-color: #2563EB;
}
.step-bubble span {
  font-family: 'Outfit', sans-serif;
  font-weight: 900;
  font-size: .9rem;
  color: #2563EB;
  transition: color .25s;
}
.step-card:hover .step-bubble span { color: #fff }
.step-icon-box {
  width: 46px;
  height: 46px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  margin: 0 auto 1.25rem;
}
.step-title {
  font-family: 'Outfit', sans-serif;
  font-weight: 800;
  font-size: 1.05rem;
  color: #0F172A;
  margin-bottom: .6rem;
}
.step-desc {
  font-size: .85rem;
  color: var(--text-secondary);
  line-height: 1.7;
}
.step-link {
  display: inline-flex;
  align-items: center;
  gap: .35rem;
  font-size: .8rem;
  font-weight: 800;
  color: #2563EB;
  margin-top: 1.1rem;
  cursor: pointer;
  transition: gap .2s;
}
.step-link:hover { gap: .55rem }

/* ═══════════════════════
   DOCUMENT CATALOG (Light Grid)
   ═══════════════════════ */
.catalog-section {
  background: transparent;
  border-bottom: 1px solid rgba(15, 23, 42, 0.05);
}
.search-row {
  max-width: 480px;
  margin: 0 auto 2rem;
  position: relative;
}
.catalog-search {
  width: 100%;
  padding: .75rem 1.2rem .75rem 2.8rem;
  border: 1.5px solid rgba(15, 23, 42, 0.08);
  border-radius: var(--rf);
  font-size: .9rem;
  color: #0F172A;
  background: rgba(255, 255, 255, 0.85);
  font-family: 'Inter', sans-serif;
  outline: none;
  transition: all .2s;
}
.catalog-search:focus {
  border-color: #2563EB;
  background: #FFFFFF;
  box-shadow: 0 0 15px rgba(37, 99, 235, 0.08);
}
.catalog-search-icon {
  position: absolute;
  left: 1.1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #94A3B8;
  font-size: .9rem;
  pointer-events: none;
}

.cat-tabs {
  display: flex;
  gap: .5rem;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 2.2rem;
}
.cat-tab {
  font-size: .82rem;
  font-weight: 700;
  padding: .45rem 1.15rem;
  border-radius: var(--rf);
  border: 1.5px solid rgba(15, 23, 42, 0.06);
  background: rgba(255, 255, 255, 0.7);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all .18s;
  font-family: 'Inter', sans-serif;
}
.cat-tab:hover {
  border-color: #2563EB;
  color: #2563EB;
}
.cat-tab.active {
  background: #2563EB;
  border-color: #2563EB;
  color: #fff;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
}

.docs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}
.adobe-card {
  background: rgba(255, 255, 255, 0.75);
  border: 1.5px solid rgba(15, 23, 42, 0.05);
  border-radius: var(--rl);
  padding: 1.8rem;
  display: flex;
  flex-direction: column;
  position: relative;
  transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  box-shadow: 0 10px 25px rgba(15, 23, 42, 0.02);
  backdrop-filter: blur(12px);
}
.adobe-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(37, 99, 235, 0.08);
  border-color: #2563EB;
}
.adobe-card-icon-wrap {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  margin-bottom: 1.25rem;
}
.adobe-card-title {
  font-family: 'Outfit', sans-serif;
  font-weight: 800;
  font-size: 1.08rem;
  color: #0F172A;
  margin-bottom: 0.6rem;
  line-height: 1.35;
}
.adobe-card-desc {
  font-size: 0.84rem;
  color: var(--text-secondary);
  line-height: 1.65;
  margin-bottom: 1.5rem;
  flex-grow: 1;
}
.adobe-card-action {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: auto;
}
.adobe-card-link {
  font-size: 0.85rem;
  font-weight: 800;
  color: #2563EB;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  transition: gap 0.2s;
}
.adobe-card:hover .adobe-card-link {
  color: #1D4ED8;
  gap: 0.55rem;
}
.adobe-card-badge {
  position: absolute;
  top: 1.2rem;
  right: 1.2rem;
  font-size: 0.65rem;
  font-weight: 800;
  padding: 0.2rem 0.65rem;
  border-radius: var(--rf);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
.badge-new {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  color: #059669;
}
.badge-pop {
  background: rgba(249, 115, 22, 0.1);
  border: 1px solid rgba(249, 115, 22, 0.2);
  color: #EA580C;
}

/* ═══════════════════════
   LOCKED PANEL (Light Theme Grid)
   ═══════════════════════ */
.locked-card-panel {
  grid-column: 1 / -1;
  text-align: center;
  padding: 4.5rem 2rem;
  background: rgba(255, 255, 255, 0.7);
  border: 1px dashed rgba(15, 23, 42, 0.15);
  border-radius: var(--rxl);
  backdrop-filter: blur(12px);
  width: 100%;
  box-shadow: var(--shadow-glow);
}
.locked-icon {
  font-size: 2.8rem;
  margin-bottom: 1.25rem;
  color: #D97706;
  text-shadow: 0 0 20px rgba(217, 119, 6, 0.15);
  display: block;
}
.locked-title {
  font-family: 'Outfit', sans-serif;
  font-weight: 800;
  font-size: 1.2rem;
  color: var(--text-primary);
  margin-bottom: 0.6rem;
}
.locked-desc {
  font-size: 0.88rem;
  color: var(--text-secondary);
  max-width: 380px;
  margin: 0 auto;
  line-height: 1.6;
}

/* ═══════════════════════
   AUDIENCE SECTION
   ═══════════════════════ */
.audience-section {
  background: transparent;
  border-bottom: 1px solid rgba(15, 23, 42, 0.05);
}
.audience-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  border: 1px solid rgba(15, 23, 42, 0.06);
  border-radius: var(--rxl);
  overflow: hidden;
  background: rgba(15, 23, 42, 0.06);
  gap: 1px;
}
.aud-card {
  background: #FFFFFF;
  padding: 1.8rem 1.6rem;
  cursor: pointer;
  transition: all .2s;
  position: relative;
  color: #0F172A;
}
.aud-card:hover { background: rgba(37, 99, 235, 0.04) }
.aud-dot {
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  top: 0;
  left: 0;
  transform: translate(-50%, -50%);
  background: rgba(15, 23, 42, 0.06);
  border: 1px solid rgba(15, 23, 42, 0.12);
  z-index: 1;
}
.aud-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.05rem;
  margin-bottom: 1rem;
}
.aud-title {
  font-family: 'Outfit', sans-serif;
  font-weight: 800;
  font-size: 1rem;
  color: #0F172A;
  margin-bottom: .45rem;
}
.aud-desc {
  font-size: .85rem;
  color: var(--text-secondary);
  line-height: 1.65;
}

/* ═══════════════════════
   FEATURES BENTO
   ═══════════════════════ */
.features-section {
  background: transparent;
  color: #0F172A;
  border-bottom: 1px solid rgba(15, 23, 42, 0.05);
}
.features-section .sec-title { color: #0F172A }
.features-section .sec-sub { color: var(--text-secondary) }
.features-section .sec-label {
  background: rgba(37, 99, 235, 0.05);
  color: #2563EB;
  border-color: rgba(37, 99, 235, 0.15);
}
.bento {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: auto;
  gap: 1.5rem;
}
.bento-card {
  background: rgba(255, 255, 255, 0.75);
  border: 1px solid rgba(15, 23, 42, 0.05);
  border-radius: var(--rxl);
  padding: 2rem;
  box-shadow: 0 10px 25px rgba(15, 23, 42, 0.02);
  transition: all .3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(12px);
}
.bento-card:hover {
  box-shadow: 0 15px 30px rgba(37, 99, 235, 0.08);
  transform: translateY(-3px);
  border-color: #2563EB;
}
.bento-card.hero-card-feat {
  grid-column: span 2;
  background: linear-gradient(135deg, rgba(241, 245, 249, 0.7) 0%, rgba(226, 232, 240, 0.8) 100%);
  border-color: rgba(15, 23, 42, 0.06);
}
.bento-card.hero-card-feat .bento-title { color: #0F172A }
.bento-card.hero-card-feat .bento-desc { color: var(--text-secondary) }
.bfi {
  width: 46px;
  height: 46px;
  border-radius: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  margin-bottom: 1.4rem;
}
.bento-title {
  font-family: 'Outfit', sans-serif;
  font-weight: 800;
  font-size: 1.05rem;
  color: #0F172A;
  margin-bottom: .55rem;
}
.bento-desc {
  font-size: .85rem;
  color: var(--text-secondary);
  line-height: 1.7;
}
.bento-card.hero-card-feat .bfi {
  background: rgba(37, 99, 235, 0.08);
  border: 1px solid rgba(37, 99, 235, 0.18);
}
.bento-card.hero-card-feat .bfi i { color: #2563EB }

/* ═══════════════════════
   TESTIMONIALS
   ═══════════════════════ */
.testi-section {
  background: transparent;
  border-bottom: 1px solid rgba(15, 23, 42, 0.05);
}
.testi-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}
.testi-card {
  background: rgba(255, 255, 255, 0.75);
  border: 1px solid rgba(15, 23, 42, 0.05);
  border-radius: var(--rxl);
  padding: 1.8rem;
  transition: all .25s;
  box-shadow: 0 10px 25px rgba(15, 23, 42, 0.02);
  backdrop-filter: blur(12px);
}
.testi-card:hover {
  box-shadow: 0 15px 30px rgba(37, 99, 235, 0.05);
  transform: translateY(-3px);
  border-color: #2563EB;
}
.t-stars {
  color: #F59E0B;
  font-size: .85rem;
  letter-spacing: .04em;
  margin-bottom: .9rem;
}
.t-text {
  font-size: .9rem;
  color: #334155;
  line-height: 1.75;
  margin-bottom: 1.25rem;
  font-style: italic;
}
.t-author {
  display: flex;
  align-items: center;
  gap: .75rem;
}
.t-av {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Outfit', sans-serif;
  font-weight: 800;
  font-size: .82rem;
  color: #fff;
  flex-shrink: 0;
}
.t-name {
  font-weight: 700;
  font-size: .85rem;
  color: #0F172A;
}
.t-role {
  font-size: .73rem;
  color: var(--text-secondary);
  margin-top: .15rem;
}

/* ═══════════════════════
   PRICING
   ═══════════════════════ */
.pricing-section {
  background: transparent;
  border-bottom: 1px solid rgba(15, 23, 42, 0.05);
}
.pricing-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.8rem;
}
.plan-card {
  background: rgba(255, 255, 255, 0.75);
  border: 1.5px solid rgba(15, 23, 42, 0.05);
  border-radius: var(--rxl);
  padding: 2.2rem 1.8rem;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(15, 23, 42, 0.025);
  backdrop-filter: blur(12px);
}
.plan-card.popular {
  border-color: #2563EB;
  box-shadow: 0 0 35px rgba(37, 99, 235, 0.12), 0 10px 30px rgba(15, 23, 42, 0.03);
}
.plan-card.popular::before {
  content: 'MOST POPULAR';
  position: absolute;
  top: 1.1rem;
  right: 1.1rem;
  background: #2563EB;
  color: #fff;
  font-size: .6rem;
  font-weight: 800;
  letter-spacing: .12em;
  padding: .25rem .75rem;
  border-radius: var(--rf);
  box-shadow: 0 4px 10px rgba(37, 99, 235, 0.25);
}
.plan-name {
  font-family: 'Outfit', sans-serif;
  font-weight: 800;
  font-size: 1.15rem;
  color: #0F172A;
  margin-bottom: .35rem;
}
.plan-price {
  font-family: 'Outfit', sans-serif;
  font-weight: 900;
  font-size: 2.6rem;
  color: #0F172A;
  letter-spacing: -.05em;
  line-height: 1;
  margin: .95rem 0 .35rem;
}
.plan-price sup {
  font-size: 1.2rem;
  vertical-align: .45em;
  font-weight: 800;
}
.plan-price sub {
  font-size: .78rem;
  font-weight: 600;
  color: var(--text-secondary);
  letter-spacing: 0;
}
.plan-sub {
  font-size: .82rem;
  color: var(--text-secondary);
  margin-bottom: 1.6rem;
  line-height: 1.6;
}
.plan-features {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: .75rem;
  margin-bottom: 2rem;
}
.plan-features li {
  display: flex;
  align-items: flex-start;
  gap: .55rem;
  font-size: .84rem;
  color: #334155;
  line-height: 1.55;
}
.plan-features li i {
  font-size: .75rem;
  margin-top: .25rem;
  flex-shrink: 0;
}
.plan-features li i.ok { color: #10B981 }
.plan-features li i.no { color: #94A3B8 }
.btn-plan {
  width: 100%;
  padding: .75rem;
  border-radius: var(--rf);
  font-size: .88rem;
  font-weight: 800;
  font-family: 'Outfit', sans-serif;
  cursor: pointer;
  transition: all .22s;
  border: none;
}
.btn-plan-outline {
  background: transparent;
  color: #2563EB;
  border: 1.5px solid #2563EB;
}
.btn-plan-outline:hover { background: rgba(37, 99, 235, 0.05) }
.btn-plan-filled {
  background: linear-gradient(135deg, var(--blue), #3B82F6);
  color: #fff;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
}
.btn-plan-filled:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(37, 99, 235, 0.35);
}
.btn-plan-dark {
  background: #0F172A;
  color: #fff;
}
.btn-plan-dark:hover { background: #1E293B }
.plan-card:hover:not(.popular) {
  transform: translateY(-3px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.03);
}

/* ═══════════════════════
   COMPARISON TABLE
   ═══════════════════════ */
.compare-section {
  background: transparent;
  border-bottom: 1px solid rgba(15, 23, 42, 0.05);
}
.compare-table {
  width: 100%;
  border-collapse: collapse;
  border-radius: var(--rxl);
  overflow: hidden;
  border: 1px solid rgba(15, 23, 42, 0.06);
  background: rgba(255, 255, 255, 0.4);
}
.compare-table th, .compare-table td {
  padding: 1rem 1.4rem;
  text-align: center;
  font-size: .85rem;
  border-bottom: 1px solid rgba(15, 23, 42, 0.04);
}
.compare-table th:first-child, .compare-table td:first-child {
  text-align: left;
  font-weight: 700;
  color: #0F172A;
}
.compare-table thead th {
  background: rgba(241, 245, 249, 0.8);
  font-weight: 800;
  font-size: .78rem;
  color: #0F172A;
  letter-spacing: .06em;
  text-transform: uppercase;
}
.compare-table thead th.highlight {
  background: rgba(37, 99, 235, 0.05);
  color: #2563EB;
}
.compare-table tbody tr:hover td { background: rgba(15, 23, 42, 0.01) }
.compare-table tbody tr:last-child td { border-bottom: none }
.cmp-yes {
  color: #10B981;
  font-size: .95rem;
}
.cmp-no {
  color: #94A3B8;
  font-size: .95rem;
}
.cmp-partial {
  color: #F59E0B;
  font-size: .78rem;
  font-weight: 700;
}

/* ═══════════════════════
   FAQ
   ═══════════════════════ */
.faq-section {
  background: transparent;
  border-bottom: 1px solid rgba(15, 23, 42, 0.05);
}
.faq-wrap {
  max-width: 780px;
  margin: 0 auto;
}
.faq-item { border-bottom: 1px solid rgba(15, 23, 42, 0.06) }
.faq-q {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.35rem 0;
  cursor: pointer;
  font-weight: 700;
  font-size: .95rem;
  color: #0F172A;
  transition: color .18s;
}
.faq-q:hover { color: #2563EB }
.faq-q i {
  color: #94A3B8;
  font-size: .8rem;
  flex-shrink: 0;
  transition: transform .25s, color .18s;
}
.faq-q:hover i { color: #2563EB }
.faq-item.open .faq-q i {
  transform: rotate(45deg);
  color: #2563EB;
}
.faq-a {
  max-height: 0;
  overflow: hidden;
  font-size: .88rem;
  color: var(--text-secondary);
  line-height: 1.75;
  transition: max-height .35s ease, padding .3s;
  padding: 0;
}
.faq-item.open .faq-a {
  max-height: 300px;
  padding-bottom: 1.35rem;
}

/* ═══════════════════════
   CTA BAND (Modern dark gradient)
   ═══════════════════════ */
.cta-section {
  background: #090C15;
  padding: 6.5rem 1.5rem;
  text-align: center;
  position: relative;
  overflow: hidden;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.cta-section::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 30% 50%, rgba(37, 99, 235, .15) 0%, transparent 60%),
              radial-gradient(circle at 70% 50%, rgba(139, 92, 246, .12) 0%, transparent 60%);
}
.cta-inner {
  max-width: 680px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}
.cta-pill {
  display: inline-flex;
  align-items: center;
  gap: .45rem;
  background: rgba(255, 255, 255, .04);
  border: 1px solid rgba(255, 255, 255, .08);
  color: #FBBF24;
  border-radius: var(--rf);
  padding: .35rem 1rem;
  font-size: .7rem;
  font-weight: 800;
  letter-spacing: .1em;
  text-transform: uppercase;
  margin-bottom: 1.3rem;
  box-shadow: 0 0 15px rgba(251, 191, 36, 0.15);
}
.cta-h {
  font-family: 'Outfit', sans-serif;
  font-size: clamp(1.8rem, 4.2vw, 2.8rem);
  font-weight: 900;
  color: #fff;
  letter-spacing: -.04em;
  line-height: 1.15;
  margin-bottom: 1rem;
}
.cta-sub {
  color: var(--text-secondary);
  font-size: 1.02rem;
  margin-bottom: 2.2rem;
  line-height: 1.75;
}
.cta-btns {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}
.btn-cta-w {
  display: inline-flex;
  align-items: center;
  gap: .5rem;
  font-size: .9rem;
  font-weight: 800;
  color: #070913;
  background: #fff;
  padding: .8rem 1.8rem;
  border-radius: var(--rf);
  box-shadow: 0 8px 24px rgba(0, 0, 0, .4);
  transition: all .22s;
  font-family: 'Outfit', sans-serif;
}
.btn-cta-w:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, .5);
}
.btn-cta-o {
  display: inline-flex;
  align-items: center;
  gap: .5rem;
  font-size: .9rem;
  font-weight: 800;
  color: #fff;
  background: transparent;
  border: 2px solid rgba(255, 255, 255, .25);
  padding: .78rem 1.7rem;
  border-radius: var(--rf);
  transition: all .22s;
  font-family: 'Outfit', sans-serif;
}
.btn-cta-o:hover {
  background: rgba(255, 255, 255, .06);
  border-color: #fff;
}

/* ═══════════════════════
   FOOTER (Dark)
   ═══════════════════════ */
footer {
  background: #090C15;
  color: var(--text-secondary);
  padding: 4rem 1.5rem 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  position: relative;
  z-index: 10;
}
.footer-inner {
  max-width: 1240px;
  margin: 0 auto;
}
.footer-top {
  display: grid;
  grid-template-columns: 2fr 1.1fr 1.1fr 1.1fr;
  gap: 2.5rem;
  margin-bottom: 3rem;
}
.footer-brand .logo-main {
  color: #fff;
  font-size: 1.15rem;
}
.footer-tagline {
  font-size: .82rem;
  color: var(--text-muted);
  margin-top: .7rem;
  line-height: 1.7;
  max-width: 260px;
}
.footer-col-title {
  font-weight: 800;
  font-size: .82rem;
  color: #FFFFFF;
  margin-bottom: 1.1rem;
  letter-spacing: .05em;
  text-transform: uppercase;
}
.footer-col-links {
  display: flex;
  flex-direction: column;
  gap: .65rem;
}
.footer-col-links a {
  font-size: .82rem;
  color: var(--text-secondary);
  transition: color .18s;
  cursor: pointer;
}
.footer-col-links a:hover { color: #FFFFFF }
.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, .06);
  padding-top: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}
.footer-copy {
  font-size: .8rem;
  color: var(--text-muted);
}
.footer-legal {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}
.footer-legal a {
  font-size: .8rem;
  color: var(--text-muted);
  transition: color .18s;
}
.footer-legal a:hover { color: #FFFFFF }

/* MOBILE STICKY */
.mobile-sticky {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(15px);
  border-top: 1px solid rgba(15, 23, 42, 0.08);
  padding: .85rem 1.5rem;
  display: none;
  justify-content: space-between;
  gap: 1rem;
  z-index: 250;
  box-shadow: 0 -10px 25px rgba(0, 0, 0, 0.02);
}
.btn-ms-d {
  flex: 0.9;
  padding: .7rem;
  border-radius: var(--rf);
  background: transparent;
  border: 1px solid rgba(15, 23, 42, 0.18);
  color: #0F172A;
  font-weight: 700;
  font-size: .82rem;
}
.btn-ms-p {
  flex: 1.1;
  padding: .7rem;
  border-radius: var(--rf);
  background: linear-gradient(135deg, var(--blue), #3B82F6);
  color: #fff;
  font-weight: 800;
  font-size: .82rem;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
}
@media(max-width:768px){
  .mobile-sticky { display: flex }
  body { padding-bottom: 70px }
  .hero-inner { flex-direction: column; text-align: center; gap: 3rem }
  .hero-sub { margin-left: auto; margin-right: auto }
  .hero-search-wrap { margin-left: auto; margin-right: auto }
  .hero-tags { justify-content: center }
  .hero-pills { justify-content: center }
  .steps-grid { grid-template-columns: 1fr; gap: 1.5rem }
  .steps-grid::after { display: none }
  .audience-grid { grid-template-columns: 1fr; gap: 1px }
  .bento { grid-template-columns: 1fr }
  .bento-card.hero-card-feat { grid-column: span 1 }
  .testi-grid { grid-template-columns: 1fr }
  .pricing-grid { grid-template-columns: 1fr; gap: 1.5rem }
  .footer-top { grid-template-columns: 1fr 1fr; gap: 2rem }
}
@media(max-width:480px){
  .footer-top { grid-template-columns: 1fr }
}

/* ═══════════════════════
   SMART FORM EDITOR OVERLAY
   ═══════════════════════ */
.editor-overlay {
  position: fixed;
  inset: 0;
  background: var(--bg-dark);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  opacity: 0;
  visibility: hidden;
  transform: scale(0.97);
  transition: all .25s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.editor-overlay.open {
  opacity: 1;
  visibility: visible;
  transform: scale(1);
}
.editor-topbar {
  background: rgba(255, 255, 255, 0.95);
  border-bottom: 1px solid rgba(15, 23, 42, 0.08);
  padding: .75rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  backdrop-filter: blur(10px);
}
.edt-doc-name {
  font-family: 'Outfit', sans-serif;
  font-weight: 800;
  font-size: 1.05rem;
  color: #0F172A;
}
.edt-doc-sub {
  font-size: .72rem;
  color: var(--text-secondary);
}
.edt-actions {
  display: flex;
  align-items: center;
  gap: .65rem;
}
.btn-esign {
  background: linear-gradient(135deg, #10B981, #059669);
  color: #fff;
  padding: .5rem 1.15rem;
  border-radius: var(--rf);
  font-weight: 800;
  font-size: .8rem;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
  display: inline-flex;
  align-items: center;
  gap: .35rem;
  transition: all .2s;
}
.btn-esign:hover {
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.3);
  transform: translateY(-1px);
}
.btn-dl {
  background: rgba(15, 23, 42, 0.03);
  border: 1px solid rgba(15, 23, 42, 0.1);
  color: #0F172A;
  padding: .5rem 1.15rem;
  border-radius: var(--rf);
  font-weight: 700;
  font-size: .8rem;
  display: inline-flex;
  align-items: center;
  gap: .35rem;
  transition: all .18s;
}
.btn-dl:hover {
  background: rgba(15, 23, 42, 0.06);
  border-color: #0F172A;
}
.btn-close-ed {
  color: var(--text-secondary);
  font-size: 1.1rem;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all .18s;
}
.btn-close-ed:hover {
  background: rgba(15, 23, 42, 0.04);
  color: #0F172A;
}
.editor-frame {
  flex: 1;
  width: 100%;
  border: none;
  background: #ffffff;
}

/* ═══════════════════════
   AUTH MODAL & AADHAAR ESIGN (Light Glass)
   ═══════════════════════ */
.m-overlay, .es-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.35);
  backdrop-filter: blur(12px);
  z-index: 1100;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  visibility: hidden;
  transition: all .25s;
}
.m-overlay.open, .es-overlay.open {
  opacity: 1;
  visibility: visible;
}
.m-box {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: var(--r2xl);
  padding: 2.4rem;
  width: 100%;
  max-width: 430px;
  position: relative;
  box-shadow: 0 20px 50px rgba(15, 23, 42, 0.06);
  transform: translateY(15px);
  transition: transform .3s;
}
.m-overlay.open .m-box { transform: translateY(0) }
.m-close {
  position: absolute;
  top: 1.25rem;
  right: 1.25rem;
  color: var(--text-secondary);
  font-size: 1rem;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all .18s;
}
.m-close:hover {
  background: rgba(15, 23, 42, 0.04);
  color: #0F172A;
}
.m-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: .5rem;
  margin-bottom: 1.4rem;
}
.m-h {
  font-family: 'Outfit', sans-serif;
  font-weight: 800;
  font-size: 1.4rem;
  text-align: center;
  color: #0F172A;
  margin-bottom: .45rem;
}
.m-sub {
  font-size: .83rem;
  color: var(--text-secondary);
  text-align: center;
  line-height: 1.6;
  margin-bottom: 1.6rem;
}
.btn-google {
  width: 100%;
  padding: .72rem;
  border-radius: var(--rf);
  border: 1px solid rgba(15, 23, 42, 0.08);
  background: rgba(15, 23, 42, 0.02);
  color: #334155;
  font-size: .86rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: .65rem;
  transition: all 0.2s;
  box-shadow: 0 2px 5px rgba(0, 0, 0, .02);
}
.btn-google:hover {
  background: rgba(15, 23, 42, 0.05);
  border-color: rgba(15, 23, 42, 0.15);
}
.auth-divider {
  display: flex;
  align-items: center;
  text-align: center;
  color: var(--text-muted);
  font-size: .7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .08em;
  margin: 1.4rem 0;
}
.auth-divider::before, .auth-divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid rgba(15, 23, 42, 0.06);
}
.auth-divider span { padding: 0 .75rem; background: #FFFFFF; }

.f-grp {
  display: flex;
  flex-direction: column;
  gap: .45rem;
  margin-bottom: 1.25rem;
  text-align: left;
}
.f-label {
  font-size: .74rem;
  font-weight: 700;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: .04em;
}
.phone-input-wrap {
  display: flex;
  align-items: center;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: var(--r);
  background: rgba(255, 255, 255, 0.8);
  overflow: hidden;
  transition: border-color .2s;
}
.phone-input-wrap:focus-within { border-color: #2563EB }
.phone-flag {
  font-size: .88rem;
  font-weight: 700;
  color: #0F172A;
  background: rgba(15, 23, 42, 0.02);
  padding: .65rem .85rem;
  border-right: 1px solid rgba(15, 23, 42, 0.06);
}
.phone-inp {
  flex: 1;
  padding: .65rem .95rem;
  background: transparent;
  border: none;
  outline: none;
  font-size: .95rem;
  color: #0F172A;
  font-weight: 600;
  letter-spacing: .04em;
}
.phone-inp::placeholder { color: var(--text-muted) }
.btn-fp {
  width: 100%;
  padding: .75rem;
  border-radius: var(--rf);
  background: linear-gradient(135deg, var(--blue), #3B82F6);
  color: #fff;
  font-weight: 800;
  font-family: 'Outfit', sans-serif;
  font-size: .88rem;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
  transition: all .2s;
}
.btn-fp:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(37, 99, 235, 0.3);
}

.auth-back-btn {
  font-size: .75rem;
  font-weight: 700;
  color: var(--blue-l);
  display: inline-flex;
  align-items: center;
  gap: .3rem;
}
.auth-back-btn:hover { color: #0F172A }
.otp-boxes {
  display: flex;
  justify-content: space-between;
  gap: .5rem;
}
.otp-box {
  width: 44px;
  height: 48px;
  border-radius: 8px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  background: rgba(255, 255, 255, 0.8);
  text-align: center;
  font-size: 1.25rem;
  font-weight: 800;
  color: #0F172A;
  outline: none;
  transition: all .2s;
}
.otp-box:focus {
  border-color: #2563EB;
  background: #FFFFFF;
  box-shadow: 0 0 10px rgba(37, 99, 235, 0.1);
}
.otp-box.filled { border-color: #2563EB; background: rgba(37, 99, 235, 0.02); }

/* Aadhaar eSign Layout */
.es-box {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: var(--r2xl);
  width: 100%;
  max-width: 460px;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(15, 23, 42, 0.06);
  transform: translateY(15px);
  transition: transform .3s;
}
.es-overlay.open .es-box { transform: translateY(0) }
.es-head {
  background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%);
  padding: 1.8rem;
  border-bottom: 1px solid rgba(15, 23, 42, 0.06);
}
.es-head-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}
.es-badge {
  display: inline-flex;
  align-items: center;
  gap: .35rem;
  background: rgba(37, 99, 235, 0.08);
  border: 1px solid rgba(37, 99, 235, 0.18);
  color: #2563EB;
  font-size: .62rem;
  font-weight: 800;
  padding: .25rem .7rem;
  border-radius: var(--rf);
  margin-bottom: .7rem;
  letter-spacing: .06em;
}
.es-hclose {
  color: var(--text-secondary);
  font-size: .95rem;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.es-hclose:hover { background: rgba(15, 23, 42, 0.04); color: #0F172A }
.es-prog {
  display: flex;
  align-items: center;
  margin-top: 1.4rem;
}
.ep-d {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: .75rem;
  font-weight: 700;
  z-index: 2;
}
.ep-d.active { background: #2563EB; color: #fff; box-shadow: 0 0 10px rgba(37, 99, 235, .25); }
.ep-d.done { background: #10B981; color: #fff }
.ep-d.pend { background: rgba(15, 23, 42, 0.03); border: 1px solid rgba(15, 23, 42, 0.08); color: var(--text-muted); }
.ep-l {
  flex: 1;
  height: 2px;
  background: rgba(15, 23, 42, 0.06);
  margin: 0 -.15rem;
  z-index: 1;
}
.ep-l.done { background: #10B981 }

.es-body { padding: 1.8rem }
.es-step { display: none }
.es-step.active { display: block }
.es-info {
  display: flex;
  align-items: flex-start;
  gap: .65rem;
  background: rgba(37, 99, 235, 0.04);
  border: 1px solid rgba(37, 99, 235, 0.15);
  border-radius: var(--rl);
  padding: .9rem 1.1rem;
  margin-bottom: 1.25rem;
}
.es-info i { color: #2563EB; font-size: .92rem; margin-top: .15rem }
.es-info p { font-size: .8rem; color: #334155; line-height: 1.55 }
.f-inp {
  padding: .68rem .9rem;
  border-radius: var(--r);
  border: 1px solid rgba(15, 23, 42, 0.08);
  background: rgba(255, 255, 255, 0.8);
  color: #0F172A;
  outline: none;
  font-size: .9rem;
  transition: all .2s;
  font-weight: 600;
}
.f-inp:focus { border-color: #2563EB; box-shadow: 0 0 10px rgba(37, 99, 235, 0.05) }
.es-legal {
  font-size: .68rem;
  color: var(--text-muted);
  line-height: 1.5;
  margin-bottom: 1.4rem;
}
.otp-row {
  display: flex;
  justify-content: space-between;
  gap: .5rem;
  margin-bottom: 1.25rem;
}
.otp-d {
  width: 44px;
  height: 48px;
  border-radius: 8px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  background: rgba(255, 255, 255, 0.8);
  text-align: center;
  font-size: 1.25rem;
  font-weight: 800;
  color: #0F172A;
  outline: none;
}
.otp-d:focus { border-color: #2563EB; background: #FFFFFF; }
.es-success { text-align: center }
.es-s-icon {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  background: rgba(16, 185, 129, 0.1);
  border: 2.5px solid rgba(16, 185, 129, 0.3);
  color: #10B981;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin: 0 auto 1.2rem;
  box-shadow: 0 0 20px rgba(16, 185, 129, 0.1);
}
.es-s-title {
  font-family: 'Outfit', sans-serif;
  font-weight: 800;
  font-size: 1.25rem;
  color: #0F172A;
  margin-bottom: .45rem;
}
.es-s-sub {
  font-size: .83rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 1.4rem;
}
.cert-box {
  display: flex;
  align-items: center;
  gap: .65rem;
  background: rgba(16, 185, 129, 0.04);
  border: 1px solid rgba(16, 185, 129, 0.15);
  border-radius: var(--rl);
  padding: .85rem 1.1rem;
  text-align: left;
  margin-bottom: 1.6rem;
}
.cert-box i { color: #10B981; font-size: 1.35rem }
.cert-title { font-weight: 800; font-size: .8rem; color: #10B981 }
.cert-body { font-size: .72rem; color: #065F46; margin-top: .1rem }
"""

# Let's search for '<style>' and '</style>' in content and replace it
style_start_idx = content.find("<style>")
style_end_idx = content.find("</style>", style_start_idx)

if style_start_idx != -1 and style_end_idx != -1:
    # Replace content between style tags
    new_content = content[:style_start_idx + 7] + "\n" + light_css + "\n" + content[style_end_idx:]
    print("Light Theme CSS applied successfully!")
else:
    new_content = content
    print("Could not find style tags in landing.html")

# 2. Modify ambient glow spots in the body tag
# Let's search for blobs block and replace it
old_blobs = """  <!-- Ambient Glow Blobs -->
  <div class="glow-blob blob1" style="background: radial-gradient(circle, rgba(59,130,246,0.18) 0%, transparent 70%);"></div>
  <div class="glow-blob blob2" style="background: radial-gradient(circle, rgba(139,92,246,0.15) 0%, transparent 70%);"></div>
  <div class="glow-blob blob3" style="background: radial-gradient(circle, rgba(6,182,212,0.15) 0%, transparent 70%);"></div>
  <div class="glow-blob blob4" style="background: radial-gradient(circle, rgba(16,185,129,0.12) 0%, transparent 70%);"></div>
  <div class="glow-blob blob5" style="background: radial-gradient(circle, rgba(244,63,94,0.1) 0%, transparent 70%);"></div>"""

new_blobs = """  <!-- Ambient Glow Blobs -->
  <div class="glow-blob blob1" style="background: radial-gradient(circle, rgba(59,130,246,0.08) 0%, transparent 70%);"></div>
  <div class="glow-blob blob2" style="background: radial-gradient(circle, rgba(139,92,246,0.07) 0%, transparent 70%);"></div>
  <div class="glow-blob blob3" style="background: radial-gradient(circle, rgba(6,182,212,0.07) 0%, transparent 70%);"></div>
  <div class="glow-blob blob4" style="background: radial-gradient(circle, rgba(16,185,129,0.06) 0%, transparent 70%);"></div>
  <div class="glow-blob blob5" style="background: radial-gradient(circle, rgba(244,63,94,0.05) 0%, transparent 70%);"></div>"""

new_content = new_content.replace(old_blobs, new_blobs)
print("Light theme glow blobs replaced!")

# Save modified landing.html
with open("landing.html", "w", encoding="utf-8") as f:
    f.write(new_content)

print("landing.html written successfully!")
