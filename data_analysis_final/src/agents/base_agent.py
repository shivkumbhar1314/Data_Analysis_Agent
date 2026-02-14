from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import pandas as pd
from datetime import datetime


@dataclass
class AgentResult:
    agent_name: str
    timestamp: str
    success: bool
    output: Dict[str, Any]
    error: Optional[str] = None
    execution_time: float = 0.0


class BaseAgent(ABC):
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, df: pd.DataFrame, **kwargs) -> AgentResult:
        pass
    
    def log_execution(self, result: AgentResult):
        status = "SUCCESS" if result.success else "FAILED"
        print(f"[{result.timestamp}] {self.name}: {status}")
        if result.error:
            print(f"  Error: {result.error}")
