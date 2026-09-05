"""
ProjectCraft AI — Engine Level Unit Tests
Tests for data_engine.py and mentor_engine.py logic modules.
"""

import unittest
from data_engine import (
    generate_ideas_engine,
    generate_blueprint_engine,
    generate_scaffold_zip_bytes,
    generate_synthetic_csv,
    generate_ieee_paper_html
)
from mentor_engine import evaluate_viva_answer, get_mentor_advice

class TestEngines(unittest.TestCase):

    def test_ideas_engine_synthesis(self):
        """Test generate_ideas_engine output structure."""
        ideas = generate_ideas_engine("Healthcare", "AI/ML Model & Web App", "Python, React", "Intermediate", "IEEE Paper")
        self.assertIsInstance(ideas, list)
        self.assertGreater(len(ideas), 0)
        self.assertIn('title', ideas[0])
        self.assertIn('domain', ideas[0])

    def test_blueprint_engine_synthesis(self):
        """Test generate_blueprint_engine diagram generation."""
        idea = {"title": "Test MediVision", "domain": "Healthcare"}
        blueprint = generate_blueprint_engine(idea)
        self.assertIn('architecture_diagram', blueprint)
        self.assertIn('graph TD', blueprint['architecture_diagram'])

    def test_scaffold_zip_builder(self):
        """Test generate_scaffold_zip_bytes byte generation."""
        blueprint = {"title": "Test Scaffold", "domain": "FinTech"}
        zip_bytes, filename = generate_scaffold_zip_bytes(blueprint)
        self.assertIsInstance(zip_bytes, bytes)
        self.assertGreater(len(zip_bytes), 100)
        self.assertTrue(filename.endswith('.zip'))

    def test_synthetic_csv_generator(self):
        """Test generate_synthetic_csv CSV string generation."""
        blueprint = {"title": "Test Dataset", "domain": "FinTech"}
        csv_str, filename = generate_synthetic_csv(blueprint)
        self.assertIsInstance(csv_str, str)
        self.assertIn(',', csv_str)
        self.assertTrue(filename.endswith('.csv'))

    def test_ieee_paper_html_rendering(self):
        """Test generate_ieee_paper_html HTML output."""
        blueprint = {"title": "IEEE Test Paper", "domain": "Healthcare"}
        html = generate_ieee_paper_html(blueprint)
        self.assertIn('<!DOCTYPE html>', html)
        self.assertIn('IEEE Test Paper', html)

    def test_viva_grader_engine(self):
        """Test evaluate_viva_answer scoring logic."""
        res = evaluate_viva_answer("Why Python?", "We chose Python for ML libraries", "Python ML libraries", ["Python"])
        self.assertIn('score', res)
        self.assertGreaterEqual(res['score'], 0)
        self.assertLessEqual(res['score'], 10)

    def test_mentor_advice_engine(self):
        """Test get_mentor_advice categories."""
        advice = get_mentor_advice("viva_prep", "MediVision", "Healthcare", ["Python"])
        self.assertIn('category', advice)
        self.assertIn('steps', advice)

if __name__ == '__main__':
    unittest.main()
