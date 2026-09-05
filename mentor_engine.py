import random

def get_mentor_advice(prompt_type, project_title, domain, skills, custom_question=""):
    """
    Provides targeted, actionable AI mentoring advice based on student prompt categories.
    """
    title = project_title if project_title else "Your Project"
    skills_str = ", ".join(skills) if isinstance(skills, list) else str(skills)

    if prompt_type == "research_upgrade":
        return {
            "category": "🎓 IEEE Paper & Research Grade Elevation",
            "headline": f"How to elevate '{title}' to IEEE / Springer publication level:",
            "steps": [
                {
                    "title": "1. Mathematical Formalization & Baseline Benchmarking",
                    "detail": "Do not just report accuracy. Include formal algorithmic pseudo-code, mathematical loss function formulations, and compare your model against at least 2 classic baselines (e.g., Random Forest vs. XGBoost vs. your proposed architecture)."
                },
                {
                    "title": "2. Explainability & Interpretability Integration",
                    "detail": "Add SHAP (SHapley Additive exPlanations) or Grad-CAM visualization maps to explain WHY the model made specific predictions. Evaluators love seeing explainability graphs."
                },
                {
                    "title": "3. Ablation Study",
                    "detail": "Conduct an ablation study showing performance when individual components (e.g., specific feature layers or preprocessing steps) are removed. This proves every part of your architecture has technical justification."
                },
                {
                    "title": "4. Open Science & Reproducibility",
                    "detail": "Publish a clean GitHub repository with a detailed README, DOI badge (via Zenodo), clear requirements.txt, and a 1-click Google Colab demo link."
                }
            ],
            "pro_tip": "💡 Hackathon Pro-Tip: Submit your paper abstract to an IEEE Student Conference before your final university viva presentation. Showing a 'Submitted to IEEE' receipt instantly impresses external project judges!"
        }

    elif prompt_type == "viva_prep":
        return {
            "category": "⚖️ Evaluator Defense & Viva Q&A Masterclass",
            "headline": f"Top defense strategy & answers for '{title}':",
            "steps": [
                {
                    "title": "Q1: 'Did you build this yourself or use pre-made code?'",
                    "detail": f"Answer: 'We engineered the system pipeline, modular API endpoints, and UI dashboard custom for this domain. We leveraged battle-tested open-source frameworks like {skills_str} for baseline primitives while writing the core domain-specific logic and integration handlers ourselves.'"
                },
                {
                    "title": "Q2: 'What is the mathematical limitation of your approach?'",
                    "detail": "Answer: State your model's computational complexity (e.g., O(N log N)) and admit edge cases (e.g., extreme class imbalance or rare outlier noise) along with how you mitigate them using data augmentation."
                },
                {
                    "title": "Q3: 'How do you ensure zero data leakage between train and test sets?'",
                    "detail": "Answer: 'We performed feature engineering, normalization, and missing value imputation strictly AFTER splitting datasets into K-Fold cross-validation splits using pipeline transformers.'"
                },
                {
                    "title": "Q4: 'What would happen if 10,000 concurrent users accessed this right now?'",
                    "detail": "Answer: 'The current prototype is an MVP running on a single instance. In production, we would decouple execution using an asynchronous task queue (Celery/Redis), scale frontend containers via Kubernetes, and cache frequent queries in memory.'"
                }
            ],
            "pro_tip": "💡 Viva Hack: Keep a live demo running on a tablet or laptop during viva, with pre-loaded edge case samples ready to show the judges instantly."
        }

    elif prompt_type == "constraint_solver":
        return {
            "category": "⚡ No-Budget / Hardware & Data Bottleneck Solutions",
            "headline": f"Practical workarounds for compute & dataset constraints in '{title}':",
            "steps": [
                {
                    "title": "1. Dataset Problem? Use Synthetic Data + Augmentation",
                    "detail": "If real data is unavailable or confidential, use Python libraries like `Faker`, `SDV` (Synthetic Data Vault), or LLM prompt generation to construct high-fidelity synthetic benchmark datasets. Document this clearly as a privacy-safe synthetic testbed."
                },
                {
                    "title": "2. Low GPU / Compute Power?",
                    "detail": "Utilize free cloud environments: Google Colab T4 GPUs, Kaggle Code Notebooks (30 hrs/week free P100/T4), or Lightning.ai. Convert heavy PyTorch models to ONNX format or Quantized INT8 representations for fast CPU inference."
                },
                {
                    "title": "3. Cloud Hosting Expenses?",
                    "detail": "Deploy frontend and backend for free using Vercel, Render.com free tier, HuggingFace Spaces (Gradio/Streamlit), or Railway. App startup takes seconds."
                }
            ],
            "pro_tip": "💡 Benchmark Tip: Evaluators value resourcefulness! Explaining how you optimized model inference to run on standard CPU hardware demonstrates high software engineering maturity."
        }

    elif prompt_type == "resume_booster":
        return {
            "category": "🚀 Resume & LinkedIn Impact Bullets",
            "headline": f"High-impact resume statements for '{title}':",
            "steps": [
                {
                    "title": "GitHub README Star Structure",
                    "detail": "Structure your repository with: 1) System Architecture Diagram, 2) 1-Minute Demo GIF, 3) Quickstart Installation Commands, 4) Benchmark Results Table, 5) License & Citation."
                },
                {
                    "title": "Bullet 1 (Action + Tech + Impact)",
                    "detail": f"Architected a full-stack {domain} platform using {skills_str}, delivering automated diagnostic predictions with sub-second latency."
                },
                {
                    "title": "Bullet 2 (Optimization Metric)",
                    "detail": "Optimized machine learning inference pipeline via model quantization and response caching, reducing compute overhead by 40%."
                },
                {
                    "title": "Bullet 3 (Engineering Quality)",
                    "detail": "Designed scalable REST microservices and modular frontend UI featuring live real-time visual metrics and Mermaid architecture rendering."
                }
            ],
            "pro_tip": "💡 Resume Tip: Record a 60-second Loom/YouTube video walking through the live app and pin it at the top of your GitHub README!"
        }

    else: # Custom question or default
        return {
            "category": "💡 Custom AI Mentor Guidance",
            "headline": f"Guidance for '{title}':",
            "steps": [
                {
                    "title": "Key Recommendation",
                    "detail": f"For '{custom_question or 'project enhancement'}', focus on modular code separation between backend data processing and frontend dashboard presentation using {skills_str}."
                },
                {
                    "title": "Next Logical Step",
                    "detail": "Implement clear error boundaries, log tracking, and responsive feedback indicators in the user interface to elevate the user experience."
                }
            ],
            "pro_tip": "💡 Keep your project modular so you can easily swap algorithms or datasets during live testing!"
        }

def evaluate_viva_answer(question, user_answer, project_title, skills):
    """
    Evaluates a student's answer in the Live Viva Voce Simulator.
    Computes a score (0-10), lists key technical terms present vs missing, and provides feedback.
    """
    ans = user_answer.strip().lower()
    
    # Calculate score based on depth and keywords
    word_count = len(ans.split())
    if word_count < 5:
        score = 3
        feedback_tier = "Needs Improvement"
        summary = "Your answer was too brief for an external evaluator. Elaborate on implementation details."
    elif word_count < 15:
        score = 6
        feedback_tier = "Satisfactory"
        summary = "Good start, but missing key technical metrics and architectural rationale."
    else:
        score = 8.5 + (0.5 if "api" in ans or "model" in ans or "pipeline" in ans else 0)
        score = min(10.0, score)
        feedback_tier = "Strong Defense!"
        summary = "Excellent answer! You demonstrated solid architectural understanding."

    # Highlight keyword detection
    technical_keywords = ["pipeline", "architecture", "latency", "accuracy", "quantization", "validation", "rest api", "explainability", "dataset"]
    found_keywords = [k for k in technical_keywords if k in ans]
    missing_keywords = [k for k in technical_keywords if k not in ans][:3]

    model_answer = f"In {project_title or 'our system'}, we isolate core logic into modular services using {skills[0] if skills else 'Python'}, ensuring input validation, sub-second latency, and graceful error fallbacks under evaluator inspection."

    return {
        "score": score,
        "max_score": 10,
        "feedback_tier": feedback_tier,
        "summary": summary,
        "found_keywords": found_keywords,
        "missing_keywords": missing_keywords,
        "model_answer": model_answer
    }

