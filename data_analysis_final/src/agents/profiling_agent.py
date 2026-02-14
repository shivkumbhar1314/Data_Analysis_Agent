import pandas as pd
import numpy as np
from typing import Dict, Any
from datetime import datetime
import time

from .base_agent import BaseAgent, AgentResult
from ..core import ScaleDownEngine


class ProfilingAgent(BaseAgent):
    
    def __init__(self):
        super().__init__(
            name="Profiling Agent",
            description="Analyzes dataset structure, types, and distributions"
        )
        self.scaledown = ScaleDownEngine()
    
    def execute(self, df: pd.DataFrame, **kwargs) -> AgentResult:
        start_time = time.time()
        
        try:
            dataset_name = kwargs.get('dataset_name', 'dataset')
            
            # Create compressed profile
            profile = self.scaledown.profile_dataset(df, name=dataset_name)
            
            output = {
                'dataset_profile': profile.to_dict(),
                'column_summaries': self._summarize_columns(df),
                'data_quality': self._assess_data_quality(df),
                'missing_data_analysis': self._analyze_missing_data(df),
            }
            
            execution_time = time.time() - start_time
            
            result = AgentResult(
                agent_name=self.name,
                timestamp=datetime.now().isoformat(),
                success=True,
                output=output,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            result = AgentResult(
                agent_name=self.name,
                timestamp=datetime.now().isoformat(),
                success=False,
                output={},
                error=str(e),
                execution_time=execution_time
            )
        
        self.log_execution(result)
        return result
    
    def _summarize_columns(self, df: pd.DataFrame) -> Dict[str, Any]:
        summaries = {}
        for col in df.columns:
            summaries[col] = {
                'dtype': str(df[col].dtype),
                'unique_count': int(df[col].nunique()),
                'null_count': int(df[col].isnull().sum()),
                'non_null_count': int(df[col].notna().sum()),
            }
        return summaries
    
    def _assess_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        null_percentage = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
        duplicate_percentage = (df.duplicated().sum() / len(df) * 100) if len(df) > 0 else 0
        
        return {
            'total_cells': len(df) * len(df.columns),
            'null_cells': int(df.isnull().sum().sum()),
            'null_percentage': float(null_percentage),
            'duplicate_rows': int(df.duplicated().sum()),
            'duplicate_percentage': float(duplicate_percentage),
            'quality_score': float(100 - null_percentage - (duplicate_percentage * 0.5))
        }
    
    def _analyze_missing_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        missing = df.isnull().sum()
        missing_pct = (missing / len(df) * 100)
        
        return {
            'columns_with_missing': int((missing > 0).sum()),
            'missing_distribution': missing[missing > 0].to_dict(),
            'missing_percentage': missing_pct[missing > 0].to_dict(),
            'completely_missing': list(missing[missing == len(df)].index),
        }
