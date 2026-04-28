# ⚽ Brazil vs Germany 2014 — Match Simulator
 
<p align="center">

  <img width="1919" height="1025" alt="image" src="https://github.com/user-attachments/assets/769945a9-8bf0-4bf4-b194-ac8604c6277b" />
</p>
<p align="center">
  Interactive desktop app that simulates the historic first half of <strong>Brazil 0 – 5 Germany</strong><br/>
  using stochastic simulation with Weibull distribution and Monte Carlo methods.
</p>
---
 
## Overview
 
This project is based on the statistical analysis of the **Brazil vs Germany** first half at the 2014 FIFA World Cup semifinal. From **41 discrete events** recorded in the real match, a full graphical simulator was built that allows you to:
 
- Replay real match events on an **animated pitch**
- Generate simulated matches with **controllable seeds**
- Run up to **50,000 Monte Carlo replicas** in the background
- Compare real vs simulated goal progression in real time
---
 
## Features
 
| Feature | Description |
|---------|-------------|
| Live pitch | Every event appears animated at its real field position |
| Goal flash | Golden full-pitch flash on every goal |
| Speed control | From 0.5× (slow) to maximum speed |
| Seed control | Fix a seed to reproduce the exact same match |
| Events table | Real-time log with minute, type, and team |
| Goal chart | Real (gold) vs simulated (blue dashed) progression |
| Monte Carlo | Up to 50,000 replicas with progress bar and histogram |
 
---
 
## Requirements
 
| Package | Version |
|---------|---------|
| Python  | 3.10+   |
| PyQt6   | 6.4.0+  |
| NumPy   | 1.24.0+ |
| SciPy   | 1.10.0+ |
 
---
 
## Installation & Run
 
**1. Clone the repository**
```bash
git clone https://github.com/your-username/brazil-germany-2014-match-simulator.git
cd brazil-germany-2014-match-simulator
```
 
**2. Create a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate
 
# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```
 
**3. Install dependencies**
```bash
pip install -r requirements.txt
```
 
**4. Run the app**
```bash
python simulacion_partido.py
```
 
---
 
## Methodology
 
**41 discrete events** were recorded across 9 types: goals, shots, turnovers, recoveries, fouls, throw-ins, corners, goal kicks, and offsides.
 
Four distributions were tested for inter-event times using the Kolmogorov-Smirnov test and AIC criterion:
 
| Distribution | AIC  | KS p-value | Status |
|-------------|------|-----------|--------|
| Exponential  | 89.4 | 0.031     | —      |
| **Weibull**  | **86.1** | **0.089** | ✓ Selected |
| Gamma        | 87.3 | 0.054     | ✓      |
| Lognormal    | 91.2 | 0.018     | —      |
 
**Weibull parameters:** shape = 1.20, scale = 1.05
 
With 10,000 replicas, the probability of reproducing the exact scoreline **Brazil 0 – Germany 5** is approximately **1.14%**.
 
---
 
## Project Structure
 
```
brazil-germany-2014-match-simulator/
├── simulacion_partido.py         # Main PyQt6 application
├── simulacionPartidoFinal.ipynb  # Statistical analysis notebook
├── requirements.txt              # Python dependencies
└── README.md
```
 
---
 
**Author: Camilo Andrés Coronado León**
