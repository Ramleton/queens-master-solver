# Queens Master Solver

Queens Master Solver is a full-stack project that solves and visualizes any board state from the mobile game "Queens Master" — a take on the classic N-Queens combinatorial puzzle that removes the NxN board restriction and adds additional placement constraints. The project combines an algorithmic backend solver with an interactive web frontend.

---

## Features

- 🧩 **Flexible Solver:** Computes valid queen placements for any board size using backtracking with constraint-based pruning.
- 🖥️ **Interactive Web Interface:** Visualizes the board state, displays the solution, and provides step-through playback of the algorithm's execution.
- ⚙️ **Full-Stack Architecture:** React/Vite frontend backed by a Django REST API, separating solving logic from the UI.
- 📊 **Educational Tool:** Demonstrates combinatorial algorithms and backtracking strategies in action.

---

## Tech Stack

- **Backend:** Python, Django, Django Ninja
- **Frontend:** TypeScript, React, Vite, TanStack Query, CSS
- **Deployment:** Vercel (frontend), Render (backend)

---

## Live Demo

The project is live at **https://queens.ishaansaini.dev**. No installation required to try it.

---

## Local Development

### Prerequisites

- Python 3.x
- Node.js + pnpm

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Ramleton/queens-master-solver.git
   cd queens-master-solver
   ```

2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   cd frontend
   pnpm install
   ```

### Running Locally

1. Start the backend (from the `backend` folder):
   ```bash
   python manage.py runserver
   ```

2. Start the frontend in a separate terminal (from the `frontend` folder):
   ```bash
   pnpm run dev
   ```

3. Open your browser and navigate to `http://localhost:5173`.

---

## Deployment

The frontend is deployed on **Vercel** and the backend on **Render**. The frontend reads the backend URL from a `VITE_API_URL` environment variable, defaulting to `http://localhost:8000` for local development.
