
import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import tempfile

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_analysis_agent import DataAnalysisAgent, DataIngestion
from core import ScaleDownEngine
from agents import ProfilingAgent, VisualizationAgent


class TestDataIngestion(unittest.TestCase):
    
    def setUp(self):
        self.test_df = pd.DataFrame({
            'age': [25, 30, 35, 40, 45],
            'salary': [50000, 60000, 70000, 80000, 90000],
            'category': ['A', 'B', 'A', 'C', 'B']
        })
    
    def test_validate_data(self):
        validation = DataIngestion.validate_data(self.test_df)
        self.assertTrue(validation['valid'])
        self.assertEqual(validation['rows'], 5)
        self.assertEqual(validation['columns'], 3)
    
    def test_csv_ingestion(self):
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            self.test_df.to_csv(f.name, index=False)
            df = DataIngestion.load_csv(f.name)
            self.assertEqual(df.shape, self.test_df.shape)
            Path(f.name).unlink()


class TestScaleDownEngine(unittest.TestCase):
    
    def setUp(self):
        self.test_df = pd.DataFrame({
            'numeric': np.random.rand(100),
            'category': np.random.choice(['A', 'B', 'C'], 100),
            'integer': np.arange(100)
        })
        self.engine = ScaleDownEngine()
    
    def test_profile_creation(self):
        profile = self.engine.profile_dataset(self.test_df, name="test")
        self.assertEqual(profile.row_count, 100)
        self.assertEqual(profile.column_count, 3)
        self.assertGreater(profile.compression_ratio, 0.5)
    
    def test_column_profiling(self):
        profile = self.engine.profile_dataset(self.test_df)
        
        # Check numeric column
        numeric_col = next(c for c in profile.columns if c.name == 'numeric')
        self.assertTrue(numeric_col.is_numeric)
        self.assertIsNotNone(numeric_col.mean_value)
        
        # Check categorical column
        cat_col = next(c for c in profile.columns if c.name == 'category')
        self.assertTrue(cat_col.is_categorical)
        self.assertIsNotNone(cat_col.top_categories)


class TestAgents(unittest.TestCase):
    
    def setUp(self):
        self.test_df = pd.DataFrame({
            'feature1': np.random.rand(50),
            'feature2': np.random.rand(50),
            'target': np.random.choice([0, 1], 50)
        })
        
        self.profiling_agent = ProfilingAgent()
        self.viz_agent = VisualizationAgent()
    
    def test_profiling_agent(self):
        result = self.profiling_agent.execute(self.test_df)
        self.assertTrue(result.success)
        self.assertIn('dataset_profile', result.output)
        self.assertGreater(result.execution_time, 0)
    
    def test_visualization_agent(self):
        result = self.viz_agent.execute(self.test_df)
        self.assertTrue(result.success)
        self.assertIn('recommended_visualizations', result.output)


class TestMainOrchestrator(unittest.TestCase):
    
    def setUp(self):
        self.test_data_path = Path(tempfile.gettempdir()) / "test_data.csv"
        test_df = pd.DataFrame({
            'x': np.random.rand(100),
            'y': np.random.rand(100),
            'category': np.random.choice(['A', 'B'], 100)
        })
        test_df.to_csv(self.test_data_path, index=False)
        
        self.agent = DataAnalysisAgent(output_dir=tempfile.gettempdir())
    
    def tearDown(self):
        if self.test_data_path.exists():
            self.test_data_path.unlink()
    
    def test_full_analysis(self):
        results = self.agent.analyze(
            data_source=str(self.test_data_path),
            dataset_name="test",
            generate_reports=False  # Skip report generation in test
        )
        
        self.assertTrue(results['success'])
        self.assertGreater(len(results['agent_results']), 0)


if __name__ == '__main__':
    unittest.main()
