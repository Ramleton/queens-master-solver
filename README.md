# Queens Master Solver

Queens Master Solver is a full-stack project that solves and visualizes any board state from the mobile game "Queens Master", which is a take on a classic combinatorial puzzle where N queens must be placed on an N×N chessboard so that no two queens threaten each other that removes the restriction of an NxN chessboard and adds a few more. The project combines an algorithmic backend solver with a web-based frontend to explore solutions interactively.

---

## Features

- 🧩 **Flexible N-Queens Solver:** Computes valid queen placements for any board size using efficient backtracking/search algorithms.
- 🖥️ **Interactive Web Interface:** Visualizes solutions on a chessboard and allows users to explore multiple configurations.
- ⚙️ **Full-Stack Architecture:** Separates the solving logic from the UI, making it easy to extend or modify.
- 📊 **Educational Tool:** Demonstrates combinatorial algorithms and backtracking strategies in action.

---

## Tech Stack

- **Backend:** Python, Django, Django Ninja (solver algorithms)
- **Frontend:** TypeScript / JavaScript, React, HTML, CSS, TanStack Query
- **Visualization:** Web-based chessboard display for interactive solution exploration

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Ramleton/queens-master-solver.git
   cd queens-master-solver
   ```

2. Install backend dependencies (Python):
   ```bash
   pip install -r requirements.txt
   ```

3. Install frontend dependencies (if any, e.g., Node.js):
   ```bash
   cd frontend
   pnpm install
   ```

## Usage

1. Start the backend solver:
   ```bash
   python manage.py runserver
   ```

2. Launch the frontend (in a separate terminal):
   ```bash
   pnpm run preview
   ```
3. Open your browser and navigate to http://localhost:4173 to interact with the solver.