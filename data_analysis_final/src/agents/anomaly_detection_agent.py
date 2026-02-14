import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime
import time

from .base_agent import BaseAgent, AgentResult


class AnomalyDetectionAgent(BaseAgent):
    
    def __init__(self):
        super().__init__(
            name="Anomaly Detection Agent",
            description="Identifies outliers and anomalies in data"
        )
    
    def execute(self, df: pd.DataFrame, **kwargs) -> AgentResult:
        start_time = time.time()
        
        try:
            threshold = kwargs.get('threshold', 1.5)
            
            output = {
                'univariate_anomalies': self._detect_univariate_anomalies(df, threshold),
                'multivariate_anomalies': self._detect_multivariate_anomalies(df),
                'anomaly_summary': self._summarize_anomalies(df, threshold),
                'quality_issues': self._identify_quality_issues(df),
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
    
    def _detect_univariate_anomalies(self, df: pd.DataFrame, threshold: float = 1.5) -> Dict[str, Any]:
        numeric_df = df.select_dtypes(include=[np.number])
        
        anomalies = {}
        
        for col in numeric_df.columns:
            Q1 = numeric_df[col].quantile(0.25)
            Q3 = numeric_df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            outliers_mask = ((numeric_df[col] < lower_bound) | 
                            (numeric_df[col] > upper_bound))
            
            outlier_count = outliers_mask.sum()
            
            if outlier_count > 0:
                anomalies[col] = {
                    'outlier_count': int(outlier_count),
                    'outlier_percentage': float(outlier_count / len(df) * 100),
                    'lower_bound': float(lower_bound),
                    'upper_bound': float(upper_bound),
                    'values': numeric_df[col][outliers_mask].tolist()[:10]
                }
        
        return anomalies
    
    def _detect_multivariate_anomalies(self, df: pd.DataFrame) -> Dict[str, Any]:
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.shape[1] < 2:
            return {'message': 'Not enough numeric columns for multivariate analysis'}
        
        try:
            from scipy.spatial.distance import mahalanobis
            from scipy.stats import chi2
            
            mean = numeric_df.mean()
            cov = numeric_df.cov()
            
            distances = []
            for idx, row in numeric_df.iterrows():
                z_scores = (row - mean) / numeric_df.std()
                distance = np.sqrt((z_scores ** 2).sum())
                distances.append(distance)
            
            threshold_dist = np.percentile(distances, 95)
            anomalies = sum(1 for d in distances if d > threshold_dist)
            
            return {
                'method': 'Simplified Mahalanobis Distance',
                'anomalies_detected': int(anomalies),
                'anomaly_percentage': float(anomalies / len(df) * 100),
                'average_distance': float(np.mean(distances)),
            }
        except:
            return {'message': 'Multivariate analysis not available'}
    
    def _summarize_anomalies(self, df: pd.DataFrame, threshold: float = 1.5) -> Dict[str, Any]:
        numeric_df = df.select_dtypes(include=[np.number])
        
        total_anomalies = 0
        affected_columns = 0
        
        for col in numeric_df.columns:
            Q1 = numeric_df[col].quantile(0.25)
            Q3 = numeric_df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            outliers = ((numeric_df[col] < (Q1 - threshold * IQR)) | 
                       (numeric_df[col] > (Q3 + threshold * IQR))).sum()
            
            if outliers > 0:
                total_anomalies += outliers
                affected_columns += 1
        
        return {
            'total_anomalies': int(total_anomalies),
            'affected_columns': int(affected_columns),
            'anomaly_percentage': float(total_anomalies / len(df) * 100) if len(df) > 0 else 0,
            'severity': 'High' if total_anomalies / len(df) > 0.05 else 'Low',
        }
    
    def _identify_quality_issues(self, df: pd.DataFrame) -> List[str]:
        issues = []
        
        missing_cols = df.columns[df.isnull().sum() > 0].tolist()
        if missing_cols:
            issues.append(f"Columns with missing values: {', '.join(missing_cols[:5])}")
        
        if df.duplicated().sum() > 0:
            issues.append(f"Found {df.duplicated().sum()} duplicate rows")
        
        for col in df.columns:
            if df[col].nunique() <= 1:
                issues.append(f"Column '{col}' has only one unique value")
        
        object_cols = df.select_dtypes(include=['object']).columns
        for col in object_cols:
            try:
                mixed_types = df[col].apply(lambda x: type(x).__name__).nunique() > 1
                if mixed_types:
                    issues.append(f"Column '{col}' has mixed data types")
            except:
                pass
        
        return issues if issues else ["No major quality issues detected"]
