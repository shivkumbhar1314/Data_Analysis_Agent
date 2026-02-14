
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AgentConfig:
    enabled: bool = True
    timeout: float = 300.0  # seconds
    max_retries: int = 1


@dataclass
class ScaleDownConfig:
    top_categories: int = 10  # Number of categories to track
    compression_target: float = 0.75  # Target compression ratio


@dataclass
class AnalysisConfig:
    
    # Component configurations
    profiling: AgentConfig = None
    visualization: AgentConfig = None
    insights: AgentConfig = None
    anomalies: AgentConfig = None
    automl: AgentConfig = None
    
    scaledown: ScaleDownConfig = None
    
    # Analysis settings
    output_directory: str = "outputs"
    generate_html_report: bool = True
    generate_json_report: bool = True
    verbose: bool = True
    
    # Data validation
    min_rows: int = 10
    max_missing_percentage: float = 90.0
    
    def __post_init__(self):
        if self.profiling is None:
            self.profiling = AgentConfig()
        if self.visualization is None:
            self.visualization = AgentConfig()
        if self.insights is None:
            self.insights = AgentConfig()
        if self.anomalies is None:
            self.anomalies = AgentConfig()
        if self.automl is None:
            self.automl = AgentConfig()
        if self.scaledown is None:
            self.scaledown = ScaleDownConfig()


# Default configuration
DEFAULT_CONFIG = AnalysisConfig()


def get_config() -> AnalysisConfig:
    return DEFAULT_CONFIG


def create_custom_config(**kwargs) -> AnalysisConfig:
    config = AnalysisConfig()
    
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
    
    return config
