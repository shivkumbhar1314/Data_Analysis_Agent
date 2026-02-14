import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime
import time

from .base_agent import BaseAgent, AgentResult


class VisualizationAgent(BaseAgent):
    
    def __init__(self):
        super().__init__(
            name="Visualization Agent",
            description="Recommends appropriate visualizations for data analysis"
        )
    
    def execute(self, df: pd.DataFrame, **kwargs) -> AgentResult:
        start_time = time.time()
        
        try:
            output = {
                'recommended_visualizations': self._recommend_visualizations(df),
                'univariate_charts': self._generate_univariate_recs(df),
                'bivariate_charts': self._generate_bivariate_recs(df),
                'correlation_analysis': self._recommend_correlation_viz(df),
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
    
    def _recommend_visualizations(self, df: pd.DataFrame) -> List[Dict[str, str]]:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        recommendations = [
            {
                'type': 'Histogram',
                'description': 'Distribution of numerical variables',
                'applicable_columns': numeric_cols[:3] if numeric_cols else []
            },
            {
                'type': 'Box Plot',
                'description': 'Statistical summary of numerical distributions',
                'applicable_columns': numeric_cols[:3] if numeric_cols else []
            },
            {
                'type': 'Bar Chart',
                'description': 'Categorical variable frequencies',
                'applicable_columns': categorical_cols[:3] if categorical_cols else []
            }
        ]
        
        if len(numeric_cols) >= 2:
            recommendations.append({
                'type': 'Scatter Plot',
                'description': 'Relationship between two numerical variables',
                'applicable_columns': numeric_cols[:2]
            })
        
        if numeric_cols and categorical_cols:
            recommendations.append({
                'type': 'Violin Plot',
                'description': 'Distribution of numerical variable grouped by categorical',
                'applicable_columns': f"{numeric_cols[0]} grouped by {categorical_cols[0]}"
            })
        
        return recommendations
    
    def _generate_univariate_recs(self, df: pd.DataFrame) -> Dict[str, Any]:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        univariate = {}
        for col in numeric_cols[:5]:
            skewness = df[col].skew()
            univariate[col] = {
                'recommended_chart': 'Histogram with KDE' if abs(skewness) < 2 else 'Histogram with log scale',
                'skewness': float(skewness),
                'variance': float(df[col].var()),
            }
        
        return univariate
    
    def _generate_bivariate_recs(self, df: pd.DataFrame) -> List[Dict[str, str]]:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        bivariate = []
        if len(numeric_cols) >= 2:
            for i, col1 in enumerate(numeric_cols[:3]):
                for col2 in numeric_cols[i+1:3]:
                    corr = df[col1].corr(df[col2])
                    bivariate.append({
                        'variables': f"{col1} vs {col2}",
                        'chart_type': 'Scatter Plot',
                        'correlation': float(corr),
                    })
        
        return bivariate
    
    def _recommend_correlation_viz(self, df: pd.DataFrame) -> Dict[str, Any]:
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.shape[1] < 2:
            return {'message': 'Not enough numeric columns for correlation analysis'}
        
        return {
            'type': 'Correlation Heatmap',
            'columns': numeric_df.columns.tolist(),
            'recommendation': 'Visualize correlations between all numerical features'
        }
