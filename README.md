# 🧬 Causal Insight Engine

**Production-Grade Causal Reasoning — WAD Constitutional Mathematics**

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-Humanity%20%26%20Education-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production_ready-brightgreen.svg)]()
[![WAD](https://img.shields.io/badge/WAD-1e18_precision-purple.svg)]()

---

## 📋 What Is This?

**Causal Insight Engine** is the first production implementation of **Constitutional Axiomatic Intelligence (CAI)** mathematics applied to pharmaceutical causal reasoning. It simulates clinical trials, optimizes dosing, and answers "why" questions — all with **1e18 fixed-point precision (WAD arithmetic)**. No floating-point errors. No black boxes. Complete auditability.

**Built for the regulated economy. Ready for the future.**

---

## ⚡ Quick Start

```bash
# Install
pip install causal-insight-engine

# Run the API
causal-api

# Or run with uvicorn directly
uvicorn src.causal_insight.api.server:app --reload
```

Visit `http://localhost:8000/docs` for interactive API documentation.

---

## 🎯 What It Does

| Feature | Description |
|---------|-------------|
| **Clinical Trial Simulation** | Simulate trials before you run them — save $500M+ per failure |
| **Dosing Optimization** | Find the optimal dose balancing efficacy and safety |
| **Counterfactual Reasoning** | Answer "why" questions about outcomes |
| **Causal Graph** | Full DAG with WAD-scaled causal strengths |
| **Audit Trail** | Complete traceability of every inference |
| **REST API** | Production-ready FastAPI with Swagger docs |

---

## 🏛️ Constitutional Mathematics

This engine is built on **WAD Constitutional Mathematics** — the fixed-point arithmetic foundation of the **Constitutional Axiomatic Intelligence (CAI)** system class.

```
WAD = 1,000,000,000,000,000,000 (1e18 — the unit "one")

All probabilities, strengths, confidences live in [0, WAD].
All arithmetic is integer-only — no float obfuscation.

Examples:
  0.85 → 850,000,000,000,000,000
  0.70 × 0.85 → wmul(700e15, 850e15) = 595,000,000,000,000,000
```

**Why WAD Matters:**

| Feature | Benefit |
|---------|---------|
| **Deterministic** | Same inputs → same outputs, every time |
| **Auditable** | Every calculation is traceable |
| **Regulatory-grade** | 1e18 precision for FDA submissions |
| **No floating-point errors** | Integer arithmetic only |
| **Cross-platform** | Byte-identical across all systems |

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/simulate_trial` | POST | Simulate a clinical trial |
| `/optimize_dosing` | POST | Find optimal dosing regimen |
| `/counterfactual` | POST | Answer "why" questions |
| `/predict` | POST | Predict outcome under intervention |
| `/graph` | GET | Get causal graph structure |
| `/wad_info` | GET | Get WAD arithmetic information |

**Example Request:**
```bash
curl -X POST https://causal-insight-engine.onrender.com/simulate_trial \
  -H "Content-Type: application/json" \
  -d '{"dosing": 1.0, "n_patients": 1000}'
```

---

## 🧬 Pharmaceutical Causal Graph

The engine includes a complete pharmaceutical causal graph with **20+ variables** and **40+ causal relationships**:

```
Dosing → Absorption → Exposure → Target Engagement → Biomarker → Efficacy
Age → Clearance → Exposure
Disease Severity → Efficacy
Comorbidities → Adverse Events
Biomarker → Survival
Efficacy → QoL
Adverse Events → QoL
```

All edges are WAD-scaled with confidence intervals.

---

## 📁 Project Structure

```
causal-insight-engine/
├── src/causal_insight/
│   ├── core/           # WAD arithmetic, causal graph, SCM, inference, counterfactual
│   ├── domains/        # Pharmaceutical domain, clinical trial simulator
│   └── api/            # FastAPI server
├── docs/               # Technical white paper, API reference
├── app.py              # Render entry point
├── requirements.txt
├── setup.py
├── Dockerfile
├── docker-compose.yml
├── LICENSE
├── COMMERCIAL-LICENSE.md
└── README.md
```

---

## 📜 Licensing

| License | For | Price |
|---------|-----|-------|
| **Humanity License** | Individuals, non-profits, humanitarian | **FREE** |
| **Education License** | Students, teachers, researchers | **FREE** |
| **Commerce License** | For-profit companies | **PAID** |

**Commerce License Pricing:**

| Tier | Price | Features |
|------|-------|----------|
| **Starter** | $5,000/mo | 100 API calls/mo, email support |
| **Professional** | $15,000/mo | 500 API calls/mo, priority support |
| **Enterprise** | $50,000/mo | Unlimited API calls, 24/7 support |
| **Global License** | $2,000,000 | Perpetual, full source code, custom features |

**For commercial licensing: Michael@usaxioms.com**

---

## 🐳 Deployment

```bash
# Docker
docker build -t causal-insight-engine .
docker run -p 8000:8000 causal-insight-engine

# Docker Compose
docker-compose up -d

# Render
# 1. Push to GitHub
# 2. Go to render.com → New Web Service
# 3. Build Command: pip install -r requirements.txt
# 4. Start Command: python app.py
```

---

## 🛠️ Development

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Verify WAD constitution
python -c "from causal_insight import verify; verify()"
```

---

## 📄 Documentation

- [Technical White Paper](docs/technical-white-paper.md)
- [API Reference](docs/api-reference.md)
- [Architecture Overview](docs/architecture.md)

---

## 🙏 Acknowledgments

- **WAD Constitutional Mathematics** — Foundation for Aligned Intelligence Truth and Humanity
- **Russell Three-Layer CAI Architecture** — Universal Standard Axiom Corporation
- **R³ Operator** — Russell Recursive Refinement (Banach fixed-point convergence)

---

## 📧 Contact

**Michael Aaron Russell**  
Founder — USAXimCorp  
Email: **Michael@usaxioms.com**  
Website: https://usaxioms.com

**For licensing inquiries:** Michael@usaxioms.com  
**For support:** Michael@usaxioms.com  
**For partnerships:** Michael@usaxioms.com

---

## 🏛️ Constitutional Axiomatic Intelligence

This engine is a production implementation of the **Constitutional Axiomatic Intelligence (CAI)** system class, as defined by the Foundation for Aligned Intelligence Truth and Humanity.

**Priority Date: June 26, 2025**  
**System Class: Constitutional Axiomatic Intelligence**  
**Standards Body: Foundation for Aligned Intelligence Truth and Humanity**

---

**Made with WAD Constitutional Mathematics.**  
**Built for the regulated economy.**  
**Free for humanity. Paid for commerce.**  
**Ready for the future.**

---

## 🔗 Links

- [GitHub Repository](https://github.com/USAXimCorp/causal-insight-engine)
- [API Documentation](https://causal-insight-engine.onrender.com/docs)
- [Contact: Michael@usaxioms.com](mailto:Michael@usaxioms.com)

---

**Now go simulate some trials.** 🧬🚀
