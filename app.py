import os
import json
from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
from data_engine import generate_ideas_engine, generate_blueprint_engine, generate_scaffold_zip_bytes, generate_synthetic_csv, generate_ieee_paper_html
from mentor_engine import get_mentor_advice, evaluate_viva_answer

app = Flask(__name__)
CORS(app)


@app.route('/api/download-dataset', methods=['POST'])
def download_dataset_api():
    try:
        blueprint = request.json or {}
        csv_content, filename = generate_synthetic_csv(blueprint)
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export-ieee-paper', methods=['POST'])
def export_ieee_paper_api():
    try:
        blueprint = request.json or {}
        paper_html = generate_ieee_paper_html(blueprint)
        return jsonify({'success': True, 'html': paper_html})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/viva-grade', methods=['POST'])
def viva_grade_api():
    try:
        data = request.json or {}
        question = data.get('question', '')
        user_answer = data.get('user_answer', '')
        project_title = data.get('project_title', '')
        skills = data.get('skills', [])

        result = evaluate_viva_answer(question, user_answer, project_title, skills)
        return jsonify({'success': True, 'evaluation': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download-scaffold', methods=['POST'])
def download_scaffold_api():
    try:
        blueprint = request.json or {}
        zip_bytes, filename = generate_scaffold_zip_bytes(blueprint)
        return Response(
            zip_bytes,
            mimetype='application/zip',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

SAVED_FILE = os.path.join(os.path.dirname(__file__), 'saved_projects.json')


def load_saved_projects():
    if not os.path.exists(SAVED_FILE):
        return []
    try:
        with open(SAVED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def save_projects_to_file(projects):
    with open(SAVED_FILE, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate-ideas', methods=['POST'])
def generate_ideas_api():
    try:
        data = request.json or {}
        domain = data.get('domain', 'Healthcare')
        skills = data.get('skills', 'Python, React, Machine Learning')
        category = data.get('category', 'AI/ML Model & Web App')
        difficulty = data.get('difficulty', 'Intermediate')
        goal = data.get('goal', 'Job Portfolio & Resumes')
        api_key = data.get('api_key', '')

        ideas = generate_ideas_engine(domain, skills, category, difficulty, goal, api_key)
        return jsonify({'success': True, 'ideas': ideas})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/generate-blueprint', methods=['POST'])
def generate_blueprint_api():
    try:
        data = request.json or {}
        idea_data = data.get('idea', {})
        api_key = data.get('api_key', '')

        blueprint = generate_blueprint_engine(idea_data, api_key)
        return jsonify({'success': True, 'blueprint': blueprint})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mentor-advise', methods=['POST'])
def mentor_advise_api():
    try:
        data = request.json or {}
        prompt_type = data.get('prompt_type', 'viva_prep')
        project_title = data.get('project_title', '')
        domain = data.get('domain', 'Healthcare')
        skills = data.get('skills', [])
        custom_question = data.get('custom_question', '')

        advice = get_mentor_advice(prompt_type, project_title, domain, skills, custom_question)
        return jsonify({'success': True, 'advice': advice})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/saved-projects', methods=['GET'])
def get_saved_projects_api():
    projects = load_saved_projects()
    return jsonify({'success': True, 'projects': projects})

@app.route('/api/save-project', methods=['POST'])
def save_project_api():
    try:
        blueprint = request.json or {}
        if not blueprint.get('title'):
            return jsonify({'success': False, 'error': 'Invalid blueprint structure'}), 400

        projects = load_saved_projects()
        # Prevent duplicate entries by title
        existing_titles = [p.get('title') for p in projects]
        if blueprint.get('title') not in existing_titles:
            projects.append(blueprint)
            save_projects_to_file(projects)
            return jsonify({'success': True, 'message': 'Project saved successfully!', 'saved_count': len(projects)})
        else:
            return jsonify({'success': True, 'message': 'Project already in saved list!', 'saved_count': len(projects)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/delete-project', methods=['POST'])
@app.route('/api/saved-projects/<path:title>', methods=['DELETE'])
def delete_saved_project_api(title=None):
    try:
        if not title and request.is_json:
            title = request.json.get('title', '')
        
        if not title:
            return jsonify({'success': False, 'error': 'No title provided'}), 400

        projects = load_saved_projects()
        target_title = title.strip().lower()
        updated = [p for p in projects if p.get('title', '').strip().lower() != target_title]
        save_projects_to_file(updated)
        return jsonify({'success': True, 'message': 'Project removed', 'saved_count': len(updated)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export-readme', methods=['POST'])
def export_readme_api():
    try:
        bp = request.json or {}
        title = bp.get('title', 'Final Year Project')
        tagline = bp.get('tagline', '')
        problem = bp.get('problem_statement', '')
        tech = bp.get('tech_stack', {})
        features = bp.get('features', {})
        roadmap = bp.get('roadmap_8_weeks', [])

        readme_content = f"""# {title}
> **{tagline}**

## 📌 Problem Statement
{problem}

---

## 🛠️ Technology Stack
- **Frontend:** {tech.get('Frontend', 'N/A') if isinstance(tech, dict) else 'N/A'}
- **Backend:** {tech.get('Backend', 'N/A') if isinstance(tech, dict) else 'N/A'}
- **AI / ML Engine:** {tech.get('AI_ML', 'N/A') if isinstance(tech, dict) else 'N/A'}
- **Database:** {tech.get('Database', 'N/A') if isinstance(tech, dict) else 'N/A'}
- **Deployment:** {tech.get('DevOps_Deployment', 'N/A') if isinstance(tech, dict) else 'N/A'}

---

## ✨ Key Features

### MVP Features (Phase 1)
"""
        if isinstance(features, dict):
            mvp_feats = features.get('mvp', [])
            adv_feats = features.get('advanced', [])
        elif isinstance(features, list):
            mvp_feats = features
            adv_feats = []
        else:
            mvp_feats = []
            adv_feats = []

        for feat in mvp_feats:
            readme_content += f"- [ ] {feat}\n"

        readme_content += "\n### Advanced Features (Phase 2)\n"
        for feat in adv_feats:
            readme_content += f"- [ ] {feat}\n"

        readme_content += "\n---\n\n## 🚀 8-Week Execution Roadmap\n"
        if isinstance(roadmap, list):
            for phase in roadmap:
                if isinstance(phase, dict):
                    readme_content += f"### {phase.get('week', '')}: {phase.get('title', '')}\n"
                    for t in phase.get('tasks', []):
                        readme_content += f"- [ ] {t}\n"
                    readme_content += "\n"

        readme_content += """---
## 💻 Setup & Installation
```bash
# Clone the repository
git clone https://github.com/your-username/your-project-name.git
cd your-project-name

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

---
*Generated using ProjectCraft AI - Final-Year Project Studio*
"""
        return jsonify({'success': True, 'readme': readme_content})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting ProjectCraft AI Server on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)

