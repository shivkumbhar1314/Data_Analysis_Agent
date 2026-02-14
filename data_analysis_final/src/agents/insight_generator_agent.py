import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime
import time

from .base_agent import BaseAgent, AgentResult


class InsightGeneratorAgent(BaseAgent):
    
    def __init__(self):
        super().__init__(
            name="Insight Generator",
            description="Discovers and articulates key insights from data"
        )
    
    def execute(self, df: pd.DataFrame, **kwargs) -> AgentResult:
        start_time = time.time()
        
        try:
            output = {
                'statistical_insights': self._generate_statistical_insights(df),
                'distribution_insights': self._analyze_distributions(df),
                'relationship_insights': self._discover_relationships(df),
                'anomaly_indicators': self._identify_anomaly_indicators(df),
                'data_readiness': self._assess_data_readiness(df),
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
    
    def _generate_statistical_insights(self, df: pd.DataFrame) -> List[str]:
        insights = []
        
        numeric_df = df.select_dtypes(include=[np.number])
        
        if not numeric_df.empty:
            high_var = numeric_df.var().nlargest(3)
            insights.append(f"Highest variance columns: {', '.join(high_var.index.tolist())}")
            
            for col in numeric_df.columns:
                skew = numeric_df[col].skew()
                if abs(skew) > 1:
                    insights.append(f"Column '{col}' is highly skewed (skewness={skew:.2f})")
        
        insights.append(f"Dataset contains {len(df):,} rows and {len(df.columns)} columns")
        
        return insights
    
    def _analyze_distributions(self, df: pd.DataFrame) -> Dict[str, Any]:
        numeric_df = df.select_dtypes(include=[np.number])
        categorical_df = df.select_dtypes(include=['object'])
        
        return {
            'numeric_distribution': {
                'count': len(numeric_df.columns),
                'columns': numeric_df.columns.tolist(),
            },
            'categorical_distribution': {
                'count': len(categorical_df.columns),
                'columns': categorical_df.columns.tolist(),
                'cardinality': {col: int(df[col].nunique()) for col in categorical_df.columns[:5]}
            }
        }
    
    def _discover_relationships(self, df: pd.DataFrame) -> Dict[str, Any]:
        numeric_df = df.select_dtypes(include=[np.number])
        
        relationships = {
            'strong_correlations': [],
            'moderate_correlations': [],
        }
        
        if numeric_df.shape[1] >= 2:
            corr_matrix = numeric_df.corr()
            
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    col1 = corr_matrix.columns[i]
                    col2 = corr_matrix.columns[j]
                    
                    if abs(corr_value) > 0.7:
                        relationships['strong_correlations'].append({
                            'variables': f"{col1} - {col2}",
                            'correlation': float(corr_value)
                        })
                    elif abs(corr_value) > 0.3:
                        relationships['moderate_correlations'].append({
                            'variables': f"{col1} - {col2}",
                            'correlation': float(corr_value)
                        })
        
        return relationships
    
    def _identify_anomaly_indicators(self, df: pd.DataFrame) -> List[str]:
        indicators = []
        
        numeric_df = df.select_dtypes(include=[np.number])
        
        for col in numeric_df.columns:
            Q1 = numeric_df[col].quantile(0.25)
            Q3 = numeric_df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            outliers = ((numeric_df[col] < (Q1 - 1.5 * IQR)) | 
                       (numeric_df[col] > (Q3 + 1.5 * IQR))).sum()
            
            if outliers > 0:
                outlier_pct = (outliers / len(df) * 100)
                indicators.append(f"Column '{col}' has {outliers} outliers ({outlier_pct:.1f}%)")
        
        return indicators
    
    def _assess_data_readiness(self, df: pd.DataFrame) -> Dict[str, Any]:
        numeric_df = df.select_dtypes(include=[np.number])
        
        completeness = 100 - (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
        
        return {
            'completeness_score': float(completeness),
            'numeric_features': len(numeric_df.columns),
            'categorical_features': len(df.select_dtypes(include=['object']).columns),
            'recommendation': 'Data appears ready for modeling' if completeness > 80 else 'Consider data cleaning'
        }
