import pandas as pd
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

from .core import ScaleDownEngine, DataIngestion
from .agents import (
    ProfilingAgent,
    VisualizationAgent,
    InsightGeneratorAgent,
    AnomalyDetectionAgent,
    AutoMLAgent,
    AgentResult
)
from .utils import ReportGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataAnalysisAgent:
    
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        
        self.scaledown = ScaleDownEngine()
        self.report_generator = ReportGenerator(output_dir)
        self.agents = {
            'profiling': ProfilingAgent(),
            'visualization': VisualizationAgent(),
            'insights': InsightGeneratorAgent(),
            'anomalies': AnomalyDetectionAgent(),
            'automl': AutoMLAgent(),
        }
        
        # Results storage
        self.data = None
        self.dataset_profile = None
        self.agent_results = {}
    
    def analyze(self, data_source: str, source_type: Optional[str] = None,
               target_column: Optional[str] = None, 
               dataset_name: Optional[str] = None,
               run_agents: Optional[List[str]] = None,
               generate_reports: bool = True) -> Dict[str, Any]:
        
        logger.info("=" * 60)
        logger.info("Starting Data Analysis Agent")
        logger.info("=" * 60)
        
        # Step 1: Load data
        logger.info(f"Loading data from {data_source}")
        try:
            self.data = DataIngestion.load_data(data_source, source_type=source_type)
            logger.info(f"Data loaded: {self.data.shape[0]} rows, {self.data.shape[1]} columns")
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            return {'error': str(e), 'success': False}
        
        validation = DataIngestion.validate_data(self.data)
        if not validation['valid']:
            logger.warning(f"Data validation issues: {validation['issues']}")
        
        logger.info("Creating compressed dataset profile")
        if dataset_name is None:
            dataset_name = "dataset"
        
        self.dataset_profile = self.scaledown.profile_dataset(self.data, name=dataset_name)
        logger.info(f"SUCCESS Profile created - Compression ratio: {self.dataset_profile.compression_ratio:.1%}")
        
        if run_agents is None:
            agents_to_run = list(self.agents.keys())
        else:
            agents_to_run = run_agents
        
        for agent_name in agents_to_run:
            if agent_name not in self.agents:
                logger.warning(f"Unknown agent: {agent_name}")
                continue
            
            logger.info(f"Executing {agent_name} agent...")
            agent = self.agents[agent_name]
            
            agent_kwargs = {}
            if agent_name == 'profiling':
                agent_kwargs['dataset_name'] = dataset_name
            elif agent_name == 'automl':
                agent_kwargs['target_column'] = target_column
                agent_kwargs['task_type'] = 'infer'
            
            try:
                result = agent.execute(self.data, **agent_kwargs)
                self.agent_results[agent.name] = result
                
                if result.success:
                    logger.info(f"{agent.name} completed in {result.execution_time:.2f}s")
                else:
                    logger.error(f"{agent.name} failed: {result.error}")
            except Exception as e:
                logger.error(f"Error running {agent_name}: {e}")
        
        if generate_reports:
            logger.info("Generating reports...")
            
            report_data = {
                agent_result.agent_name: agent_result.output 
                for agent_result in self.agent_results.values()
            }
            
            report_data['ScaleDown Profile'] = self.dataset_profile.to_dict()
            
            try:
                html_report = self.report_generator.generate_html_report(
                    report_data, dataset_name
                )
                logger.info(f"HTML report generated: {html_report}")
                
                json_report = self.report_generator.generate_json_report(
                    report_data, dataset_name
                )
                logger.info(f"JSON report generated: {json_report}")
                
            except Exception as e:
                logger.error(f"Error generating reports: {e}")
        
        logger.info("=" * 60)
        logger.info("Analysis Complete!")
        logger.info("=" * 60)
        
        return self._compile_results()
    
    def _compile_results(self) -> Dict[str, Any]:
        results = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'dataset_profile': self.dataset_profile.to_dict() if self.dataset_profile else None,
            'agent_results': {
                name: {
                    'success': result.success,
                    'execution_time': result.execution_time,
                    'output': result.output,
                    'error': result.error
                }
                for name, result in self.agent_results.items()
            },
            'summary': self._generate_summary()
        }
        return results
    
    def _generate_summary(self) -> str:
        summary = []
        summary.append("")
        
        if self.dataset_profile:
            profile = self.dataset_profile
            summary.append(f"Dataset: {profile.name}")
            summary.append(f"Rows: {profile.row_count:,}")
            summary.append(f"Columns: {profile.column_count}")
            summary.append(f"Duplicates: {profile.duplicates_count} ({profile.duplicates_percentage:.1f}%)")
            summary.append(f"Compression Ratio: {profile.compression_ratio:.1%}")
        
        summary.append(f"\nAgents Executed: {len(self.agent_results)}")
        for agent_name, result in self.agent_results.items():
            status = "Success" if result.success else "Failed"
            summary.append(f"  - {agent_name}: {status} ({result.execution_time:.2f}s)")
        
        return "\n".join(summary)
    
    def get_agent_result(self, agent_name: str) -> Optional:
        return self.agent_results.get(agent_name)
    
    def print_summary(self):
        if self.agent_results:
            print("\n" + "=" * 60)
            print("DATA ANALYSIS RESULTS")
            print("=" * 60)
            
            for agent_name, result in self.agent_results.items():
                print(f"\n{agent_name}:")
                print(f"  Status: {'Success' if result.success else 'Failed'}")
                print(f"  Time: {result.execution_time:.2f}s")
                if result.error:
                    print(f"  Error: {result.error}")
