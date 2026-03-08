#  EduNova — Intelligent Inclusive Learning Ecosystem&Adaptive AI Education for Every Ability



![Project Status](https://img.shields.io/badge/status-active-brightgreen)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![NodeJS](https://img.shields.io/badge/NodeJS-18%2B-green)
![React](https://img.shields.io/badge/React-19-61dafb)

A professional, modular learning platform that leverages AI to generate personalized educational journeys. Features a modern React SPA with Voice Navigation, AI-powered Resume Builder, a multi-language IDE, and a **deeply integrated AI Mock Interview** system.

---

## ✨ Features

-  **AI Learning Paths** — Personalized roadmaps generated with Google Gemini.
-  **Multi-Language IDE** — 17 languages with real code execution and professional terminal.
-  **AI Algorithm Instructor (v3.2)** — **NEW!** Sophisticated logic checking that identifies mistakes and provides **instant fix suggestions** with reference code.
-  **Voice Assistant** — Multilingual voice navigation for hands-free learning.
-  **AI Resume Builder** — Auto-generate professional resumes tailored to your learning profile.
-  **Progress Dashboards** — Visual tracking of your skills and accomplishments.
-  **AI Mock Interview** — Native React assessment system with aptitude tests and coding challenges.

---

## 🏗 Architecture

```
SkillGPS/
├── client/                    # Frontend (React + Vite) → port 5173
├── backend/                   # Main API (Node.js + Express) → port 5001
├── ai/                        # Task AI Service (Python + FastAPI) → port 8002
├── LEARNING PATH GENERATOR/   # AI Algorithm Instructor (Python + Flask) → port 5005
└── Ai-Interview-Tester/
    └── backend/               # Interview Engine (Express + SQLite) → port 5000
```

```
┌──────────────────────────────────────────────────┐
│           SkillGPS Client (React + Vite)          │
│                  port 5173                        │
│                                                   │
│  ┌─────────┐ ┌──────────┐ ┌────────────────────┐ │
│  │Dashboard │ │  Algo  │ │   Mock Interview │ │
│  │ Overview │ │ Helper   │ │  (Native React)    │ │
│  └────┬─────┘ └───┬──┬───┘ └────────┬───────────┘ │
│       │           │  │               │             │
│       │           └──┼───────────────┤             │
└───────┼──────────────┼───────────────┼─────────────┘
        │              │               │
   ┌────▼─────┐   ┌────▼─────┐   ┌─────▼──────┐
   │ SkillGPS │   │ Logic AI │   │ Interview  │
   │ Backend  │   │  :5005   │   │  Backend   │
   │  :5001   │   └────┬─────┘   │   :5000    │
   └──────────┘        │         └────────────┘
                ┌──────▼─────┐
                │  Gemini /  │
                │  Torch AI  │
                └────────────┘
```

---

##  How to Run

### Step 1: Install Dependencies

```bash
# Frontend
cd client && npm install

# Main Backend
cd ../backend && npm install

# Interview Engine
cd ../Ai-Interview-Tester/backend && npm install
```

### Step 2: Start All Services (Required)

You need **4 terminals** running concurrently:

1. **AI Algorithm Instructor** *(Essential for the IDE)*
   ```bash
   cd "LEARNING PATH GENERATOR/LEARNING PATH GENERATOR"
   python app.py
   ```
   >  Running on **http://localhost:5005**

2. **Interview Engine**
   ```bash
   cd Ai-Interview-Tester/backend
   npm start
   ```
   >  Running on **http://localhost:5000**

3. **SkillGPS Backend**
   ```bash
   cd backend
   node index.js
   ```
   >  Running on **http://localhost:5001**

4. **SkillGPS Frontend**
   ```bash
   cd client
   npm run dev
   ```
   >  Running on **http://localhost:5173**

---

##  AI Algorithm Instructor (v3.2 Update)

The integrated AI Instructor is now more powerful than ever. Located inside the IDE under the **"AI Algorithm"** button, it provides:

- **Mistake Analysis**: Detects logic flaws like infinite loops, off-by-one errors, and swapped comparison operators.
- **Fix Suggestions**: For every mistake, it provides a green "How to Fix" card with the corrected code pattern.
- **Reference Code**: Automatically provides the "Perfect Implementation" from a database of 25+ standard algorithms.
- **Complexity Analysis**: Instant Big-O notation for time and space complexity.

---

## 📁 Project Structure

| Component | Responsibility | Tech Stack |
|-----------|----------------|------------|
| `client/` | Modern UI & IDE interface | React 19, Vite, GSAP |
| `backend/` | Logic orchestration & Code Execution | Node.js, Express, WebSocket |
| `LEARNING PATH GENERATOR/`| **AI Algorithm Instructor** | Python, Flask, Gemini Flash |
| `Ai-Interview-Tester/` | Mock Interview assessment engine | Node.js, SQLite, JWT |
| `ai/` | Learning Path & Task Generation | Python, FastAPI, Gemini |

---

## 🔧 Maintenance & Safety

- **Port Conflict?** If a port is busy, run: `netstat -ano | findstr :<PORT>` then `taskkill /PID <PID> /F`
- **Environment**: Ensure your `.env` files in `backend`, `ai`, and `LEARNING PATH GENERATOR` contain a valid `GEMINI_API_KEY`.
- **Offline?**: The Algorithm Helper includes a local fallback database of 25+ algorithms that works even without internet.

---

## 📝 Changelog

### v3.2 (Mar 2026)
- ✅ **Mistake Fix Suggestions** — AI now tells you *how* to fix your code with actionable steps.
- ✅ **Redesigned Mistake UI** — Clean red/green cards for better readability.
- ✅ **Expanded Algorithm DB** — Support for 25+ standard algorithms out-of-the-box.
- ✅ **Safety Checks** — Detects division by zero, infinite loops, and array index errors.

### v3.1 (Feb 2026)
- ✅ **Single Sign-On** — Mock Interview now syncs natively with SkillGPS accounts.
- ✅ **CORS Fixes** — Seamless communication between all localhost service ports.
- ✅ **Performance** — Removed heavy iframes; added native React components.

---

