import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import time

from .base_agent import BaseAgent, AgentResult


class AutoMLAgent(BaseAgent):
    
    def __init__(self):
        super().__init__(
            name="AutoML Agent",
            description="Recommends models and builds AutoML pipeline"
        )
    
    def execute(self, df: pd.DataFrame, **kwargs) -> AgentResult:
        start_time = time.time()
        
        try:
            target_column = kwargs.get('target_column')
            task_type = kwargs.get('task_type', 'infer')
            
            output = {
                'problem_type': self._infer_problem_type(df, target_column, task_type),
                'feature_recommendations': self._recommend_features(df),
                'model_recommendations': self._recommend_models(df, target_column, task_type),
                'preprocessing_steps': self._suggest_preprocessing(df),
                'pipeline_summary': self._generate_pipeline_summary(df, target_column),
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
    
    def _infer_problem_type(self, df: pd.DataFrame, target_column: Optional[str], 
                           task_type: str = 'infer') -> Dict[str, str]:
        if task_type != 'infer' and task_type in ['regression', 'classification', 'clustering']:
            problem_type = task_type
        else:
            problem_type = 'unsupervised'
            
            if target_column and target_column in df.columns:
                target = df[target_column]
                
                if pd.api.types.is_numeric_dtype(target):
                    unique_ratio = target.nunique() / len(target)
                    if unique_ratio > 0.1:
                        problem_type = 'regression'
                    else:
                        problem_type = 'classification'
                else:
                    problem_type = 'classification'
        
        return {
            'type': problem_type,
            'description': self._get_problem_description(problem_type),
            'target_column': target_column or 'Not specified'
        }
    
    def _get_problem_description(self, problem_type: str) -> str:
        descriptions = {
            'regression': 'Predicting continuous numerical values',
            'classification': 'Predicting categorical classes',
            'clustering': 'Grouping data into clusters',
            'unsupervised': 'Unsupervised learning without target variable'
        }
        return descriptions.get(problem_type, 'Unknown problem type')
    
    def _recommend_features(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        numeric_features = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_features = df.select_dtypes(include=['object']).columns.tolist()
        
        low_var_numeric = []
        for col in numeric_features:
            if df[col].std() < df[col].mean() * 0.01:
                low_var_numeric.append(col)
        
        recommended_numeric = [f for f in numeric_features if f not in low_var_numeric]
        
        return {
            'recommended_numeric': recommended_numeric[:10],
            'recommended_categorical': categorical_features[:10],
            'features_to_drop': low_var_numeric,
            'total_features': len(numeric_features) + len(categorical_features),
        }
    
    def _recommend_models(self, df: pd.DataFrame, target_column: Optional[str], 
                         task_type: str = 'infer') -> List[Dict[str, Any]]:
        problem_type = self._infer_problem_type(df, target_column, task_type)['type']
        
        if problem_type == 'regression':
            return self._regression_models()
        elif problem_type == 'classification':
            return self._classification_models(df, target_column)
        elif problem_type == 'clustering':
            return self._clustering_models()
        else:
            return self._general_models()
    
    def _regression_models(self) -> List[Dict[str, Any]]:
        return [
            {
                'model': 'Linear Regression',
                'pros': 'Simple, interpretable, fast',
                'cons': 'Assumes linear relationships',
                'recommendation_score': 0.8
            },
            {
                'model': 'Random Forest Regressor',
                'pros': 'Handles non-linearity, robust',
                'cons': 'Less interpretable, prone to overfitting',
                'recommendation_score': 0.9
            },
            {
                'model': 'Gradient Boosting (XGBoost/LightGBM)',
                'pros': 'High performance, feature importance',
                'cons': 'Requires tuning, longer training time',
                'recommendation_score': 0.95
            },
            {
                'model': 'Support Vector Machine',
                'pros': 'Works with non-linear relationships',
                'cons': 'Slower training, memory intensive',
                'recommendation_score': 0.75
            }
        ]
    
    def _classification_models(self, df: pd.DataFrame, target_column: Optional[str]) -> List[Dict[str, Any]]:
        models = [
            {
                'model': 'Logistic Regression',
                'pros': 'Simple, fast, interpretable',
                'cons': 'Assumes linear relationships',
                'recommendation_score': 0.8
            },
            {
                'model': 'Random Forest Classifier',
                'pros': 'Handles non-linearity, ranks features',
                'cons': 'Less interpretable',
                'recommendation_score': 0.9
            },
            {
                'model': 'Gradient Boosting',
                'pros': 'High performance, feature importance',
                'cons': 'Complex tuning',
                'recommendation_score': 0.95
            },
            {
                'model': 'Support Vector Machine',
                'pros': 'Works well in high dimensions',
                'cons': 'Slower, less interpretable',
                'recommendation_score': 0.75
            }
        ]
        
        if target_column and target_column in df.columns:
            value_counts = df[target_column].value_counts()
            if len(value_counts) > 0:
                imbalance_ratio = value_counts.max() / value_counts.min()
                if imbalance_ratio > 5:
                    models.append({
                        'model': 'Class Weight Adjusted Model',
                        'pros': 'Handles imbalaced classes',
                        'cons': 'May overfit minority class',
                        'recommendation_score': 0.85
                    })
        
        return models
    
    def _clustering_models(self) -> List[Dict[str, Any]]:
        return [
            {
                'model': 'K-Means',
                'pros': 'Fast, scalable',
                'cons': 'Assumes spherical clusters',
                'recommendation_score': 0.8
            },
            {
                'model': 'DBSCAN',
                'pros': 'Finds arbitrary shapes, detects outliers',
                'cons': 'Requires parameter tuning',
                'recommendation_score': 0.8
            },
            {
                'model': 'Hierarchical Clustering',
                'pros': 'Produces dendrogram, interpretable',
                'cons': 'Slow on large datasets',
                'recommendation_score': 0.75
            }
        ]
    
    def _general_models(self) -> List[Dict[str, Any]]:
        return [
            {
                'model': 'Random Forest',
                'pros': 'Versatile, handles many data types',
                'cons': 'Memory intensive',
                'recommendation_score': 0.85
            }
        ]
    
    def _suggest_preprocessing(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        steps = []
        
        if df.isnull().sum().sum() > 0:
            steps.append('Handle missing values (imputation or removal)')
        
        categorical = df.select_dtypes(include=['object']).columns
        if len(categorical) > 0:
            steps.append('Encode categorical variables (one-hot or label encoding)')
        
        numeric = df.select_dtypes(include=[np.number])
        if len(numeric) > 0:
            steps.append('Scale/normalize numerical features')
        
        if df.duplicated().sum() > 0:
            steps.append('Remove duplicate rows')
        
        steps.append('Consider outlier handling or transformation')
        
        steps.append('Consider feature engineering (interactions, polynomials)')
        
        return {
            'preprocessing_steps': steps,
            'priority': ['Handle missing values', 'Handle outliers', 'Scale features', 'Encode categorical']
        }
    
    def _generate_pipeline_summary(self, df: pd.DataFrame, target_column: Optional[str]) -> Dict[str, Any]:
        return {
            'data_shape': {'rows': len(df), 'columns': len(df.columns)},
            'features_count': len(df.select_dtypes(include=[np.number]).columns),
            'categorical_count': len(df.select_dtypes(include=['object']).columns),
            'target_column': target_column or 'Not specified',
            'next_steps': [
                'Run preprocessing pipeline',
                'Split data (train/test)',
                'Train recommended models',
                'Perform cross-validation',
                'Evaluate and compare models',
                'Tune best model',
                'Generate feature importance'
            ]
        }
