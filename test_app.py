"""
ProjectCraft AI — Automated Test Suite
Unit tests for Flask endpoints, Data Engine, and Mentor Engine.
"""

import unittest
import json
from app import app

class ProjectCraftTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test client before each test."""
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_home_page_accessibility_and_status(self):
        """Test home page loads with 200 OK."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ProjectCraft', response.data)
        self.assertIn(b'lang="en"', response.data)

    def test_generate_ideas_success(self):
        """Test /api/generate-ideas endpoint with valid payload."""
        payload = {
            "domain": "Healthcare",
            "category": "AI/ML Model & Web App",
            "skills": "Python, React, PyTorch"
        }
        response = self.client.post(
            '/api/generate-ideas',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIsInstance(data.get('ideas'), list)
        self.assertGreater(len(data['ideas']), 0)

    def test_generate_ideas_empty_payload(self):
        """Test /api/generate-ideas endpoint fallback handling."""
        response = self.client.post(
            '/api/generate-ideas',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))

    def test_generate_blueprint(self):
        """Test /api/generate-blueprint endpoint."""
        idea = {
            "title": "MediVision AI Diagnostic Engine",
            "domain": "Healthcare",
            "problem": "Diagnostic delays in primary healthcare",
            "tagline": "AI assistant for screening"
        }
        response = self.client.post(
            '/api/generate-blueprint',
            data=json.dumps({"idea": idea}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('blueprint', data)
        self.assertIn('architecture_diagram', data['blueprint'])

    def test_export_readme(self):
        """Test /api/export-readme endpoint."""
        blueprint = {
            "title": "Test Capstone Project",
            "tagline": "AI Diagnostic Engine",
            "problem_statement": "Diagnostic delay problem",
            "tech_stack": {
                "Frontend": "React",
                "Backend": "Python Flask",
                "AI_ML": "PyTorch",
                "Database": "JSON Storage",
                "DevOps_Deployment": "Vercel"
            },
            "features": {
                "mvp": ["Feature A", "Feature B"],
                "advanced": ["Feature C"]
            },
            "roadmap_8_weeks": [
                {"week": "Weeks 1-2", "title": "Setup", "tasks": ["Task 1"]}
            ]
        }
        response = self.client.post(
            '/api/export-readme',
            data=json.dumps(blueprint),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('readme', data)
        self.assertIn('# Test Capstone Project', data['readme'])

    def test_save_and_delete_project(self):
        """Test saving and deleting a project blueprint."""
        blueprint = {
            "title": "Test Automation Deletion Project",
            "domain": "Cybersecurity",
            "tagline": "Temporary Test Project"
        }
        # 1. Save project
        save_res = self.client.post(
            '/api/save-project',
            data=json.dumps(blueprint),
            content_type='application/json'
        )
        self.assertEqual(save_res.status_code, 200)

        # 2. Get saved projects
        get_res = self.client.get('/api/saved-projects')
        self.assertEqual(get_res.status_code, 200)

        # 3. Delete project via POST
        del_res = self.client.post(
            '/api/delete-project',
            data=json.dumps({"title": "Test Automation Deletion Project"}),
            content_type='application/json'
        )
        self.assertEqual(del_res.status_code, 200)
        del_data = json.loads(del_res.data)
        self.assertTrue(del_data.get('success'))

    def test_viva_grade_evaluation(self):
        """Test /api/viva-grade endpoint."""
        payload = {
            "question": "Why Python?",
            "answer": "We chose Python for rapid prototyping and deep learning libraries.",
            "target_keywords": "Python libraries rapid ML"
        }
        response = self.client.post(
            '/api/viva-grade',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('evaluation', data)
        self.assertIn('score', data['evaluation'])

    def test_mentor_advise(self):
        """Test /api/mentor-advise endpoint."""
        payload = {
            "prompt_type": "viva_prep",
            "project_title": "MediVision AI",
            "domain": "Healthcare"
        }
        response = self.client.post(
            '/api/mentor-advise',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('advice', data)

    def test_download_dataset(self):
        """Test /api/download-dataset endpoint."""
        payload = {"title": "Test Project", "domain": "Healthcare"}
        response = self.client.post(
            '/api/download-dataset',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/csv', response.content_type)

    def test_download_scaffold(self):
        """Test /api/download-scaffold ZIP endpoint."""
        payload = {"title": "Test Scaffold Project", "domain": "Healthcare"}
        response = self.client.post(
            '/api/download-scaffold',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/zip', response.content_type)

    def test_export_ieee_paper(self):
        """Test /api/export-ieee-paper endpoint."""
        payload = {"title": "Test IEEE Paper", "domain": "Healthcare"}
        response = self.client.post(
            '/api/export-ieee-paper',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('html', data)

if __name__ == '__main__':
    unittest.main()
