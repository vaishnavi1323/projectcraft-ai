# 🚀 ProjectCraft AI - Final-Year Project Idea Generator & Mentor

> **Hackathon MVP Submission**: An AI-powered platform for final-year CS & Engineering students to discover, blueprint, and defend top-tier technical projects.

---

## 🌟 Key Features

1. **Intelligent Idea Discovery Engine**: Generates non-generic project concepts based on student domain interests, technical skills, complexity level, and career goals.
2. **Interactive Technical Blueprint & Diagram Studio**:
   - Auto-generates **Mermaid.js** architecture dataflow diagrams.
   - Comprehensive Tech Stack recommendations.
   - 8-Week Phased Milestones with actionable checklists.
   - Evaluator Defense (Viva Voce Q&A) prep cards.
3. **AI Mentor Workshop**:
   - Research Paper / IEEE Elevation strategies (SHAP, Grad-CAM, ablation studies).
   - No-budget hardware and dataset bottleneck solvers (synthetic data generator tips, quantization).
   - 1-Click GitHub `README.md` Exporter.

---

## 🛠️ Tech Stack & Architecture

- **Backend:** Python 3 + Flask + Flask-CORS (`app.py`, `data_engine.py`, `mentor_engine.py`)
- **Frontend:** HTML5, Modern CSS Glassmorphic UX, FontAwesome 6, Google Fonts (`Outfit` & `Inter`)
- **Diagrams:** Mermaid.js CDN integration
- **Storage:** Local JSON file storage (`saved_projects.json`)

---

## 💻 Local Setup Instructions

```bash
# 1. Clone Repository
git clone https://github.com/YOUR_USERNAME/projectcraft-ai.git
cd projectcraft-ai

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Launch Application
python app.py
```
Open `http://127.0.0.1:5000` in your browser!

---

## 🚀 Deployment Instructions

### Deploy on Render (Recommended Free Deployment)
1. Push code to GitHub repository.
2. Go to [Render.com](https://render.com) and click **New -> Web Service**.
3. Connect your GitHub repository.
4. Set Build Command: `pip install -r requirements.txt`
5. Set Start Command: `gunicorn app:app`
6. Click **Create Web Service**!
