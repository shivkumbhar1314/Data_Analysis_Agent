import pandas as pd
import numpy as np
from typing import Dict, Optional, Any, List
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class DataIngestion:
    
    SUPPORTED_FORMATS = {'csv', 'parquet', 'excel', 'sql'}
    
    @staticmethod
    def load_csv(filepath: str, **kwargs) -> pd.DataFrame:
        logger.info(f"Loading CSV from {filepath}")
        try:
            df = pd.read_csv(filepath, **kwargs)
            logger.info(f"Loaded CSV with shape {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Failed to load CSV: {e}")
            raise
    
    @staticmethod
    def load_parquet(filepath: str, **kwargs) -> pd.DataFrame:
        logger.info(f"Loading Parquet from {filepath}")
        try:
            df = pd.read_parquet(filepath, **kwargs)
            logger.info(f"Loaded Parquet with shape {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Failed to load Parquet: {e}")
            raise
    
    @staticmethod
    def load_excel(filepath: str, **kwargs) -> pd.DataFrame:
        logger.info(f"Loading Excel from {filepath}")
        try:
            df = pd.read_excel(filepath, **kwargs)
            logger.info(f"Loaded Excel with shape {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Failed to load Excel: {e}")
            raise
    
    @staticmethod
    def load_sql(connection_string: str, query: str) -> pd.DataFrame:
        logger.info(f"Loading data from SQL query")
        try:
            from sqlalchemy import create_engine
            engine = create_engine(connection_string)
            df = pd.read_sql(query, engine)
            logger.info(f"Loaded SQL data with shape {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Failed to load SQL data: {e}")
            raise
    
    @staticmethod
    def load_data(filepath: str, source_type: Optional[str] = None, **kwargs) -> pd.DataFrame:
        if source_type is None:
            source_type = DataIngestion._detect_source_type(filepath)
        
        source_type = source_type.lower()
        
        if source_type == 'csv':
            return DataIngestion.load_csv(filepath, **kwargs)
        elif source_type == 'parquet':
            return DataIngestion.load_parquet(filepath, **kwargs)
        elif source_type == 'excel':
            return DataIngestion.load_excel(filepath, **kwargs)
        elif source_type == 'sql':
            raise ValueError("SQL requires connection_string and query parameters")
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
    
    @staticmethod
    def _detect_source_type(filepath: str) -> str:
        path = Path(filepath)
        extension = path.suffix.lower()
        
        extension_map = {
            '.csv': 'csv',
            '.parquet': 'parquet',
            '.xlsx': 'excel',
            '.xls': 'excel',
        }
        
        if extension in extension_map:
            return extension_map[extension]
        else:
            raise ValueError(f"Unknown file extension: {extension}")
    
    @staticmethod
    def validate_data(df: pd.DataFrame) -> Dict[str, Any]:
        report = {
            'valid': True,
            'shape': df.shape,
            'columns': len(df.columns),
            'rows': len(df),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'duplicates': df.duplicated().sum(),
            'issues': []
        }
        
        if df.empty:
            report['valid'] = False
            report['issues'].append('DataFrame is empty')
        
        if df.isnull().all().any():
            report['valid'] = False
            report['issues'].append('Some columns are entirely null')
        
        return report
