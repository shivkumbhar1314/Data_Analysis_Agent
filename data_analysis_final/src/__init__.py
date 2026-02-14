
from .data_analysis_agent import DataAnalysisAgent
from .core import ScaleDownEngine, DataIngestion
from .agents import (
    BaseAgent, AgentResult, ProfilingAgent, VisualizationAgent,
    InsightGeneratorAgent, AnomalyDetectionAgent, AutoMLAgent
)

__version__ = "1.0.0"

__all__ = [
    'DataAnalysisAgent',
    'ScaleDownEngine',
    'DataIngestion',
    'BaseAgent',
    'AgentResult',
    'ProfilingAgent',
    'VisualizationAgent',
    'InsightGeneratorAgent',
    'AnomalyDetectionAgent',
    'AutoMLAgent',
]
