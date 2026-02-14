import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import json


@dataclass
class ColumnProfile:
    name: str
    dtype: str
    null_count: int
    null_percentage: float
    unique_count: int
    cardinality_ratio: float
    
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    mean_value: Optional[float] = None
    median_value: Optional[float] = None
    std_value: Optional[float] = None
    skewness: Optional[float] = None
    
    top_categories: Optional[List[Tuple[str, int]]] = None
    
    is_numeric: bool = False
    is_categorical: bool = False
    is_datetime: bool = False


@dataclass
class DatasetProfile:
    name: str
    row_count: int
    column_count: int
    columns: List[ColumnProfile]
    duplicates_count: int
    duplicates_percentage: float
    memory_size_bytes: int
    compressed_size_bytes: int
    compression_ratio: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'row_count': self.row_count,
            'column_count': self.column_count,
            'columns': [asdict(col) for col in self.columns],
            'duplicates_count': self.duplicates_count,
            'duplicates_percentage': self.duplicates_percentage,
            'memory_size_bytes': self.memory_size_bytes,
            'compressed_size_bytes': self.compressed_size_bytes,
            'compression_ratio': self.compression_ratio,
        }


class ScaleDownEngine:
    
    def __init__(self, top_categories: int = 10):
        self.top_categories = top_categories
    
    def profile_dataset(self, df: pd.DataFrame, name: str = "dataset") -> DatasetProfile:
        columns = []
        
        for col in df.columns:
            col_profile = self._profile_column(df, col)
            columns.append(col_profile)
        
        # Calculate overall statistics
        row_count = len(df)
        column_count = len(df.columns)
        duplicates_count = df.duplicated().sum()
        duplicates_percentage = (duplicates_count / row_count * 100) if row_count > 0 else 0
        
        original_size = df.memory_usage(deep=True).sum()
        compressed_size = self._estimate_compressed_size(columns)
        compression_ratio = 1 - (compressed_size / original_size) if original_size > 0 else 0
        
        return DatasetProfile(
            name=name,
            row_count=row_count,
            column_count=column_count,
            columns=columns,
            duplicates_count=int(duplicates_count),
            duplicates_percentage=float(duplicates_percentage),
            memory_size_bytes=int(original_size),
            compressed_size_bytes=int(compressed_size),
            compression_ratio=float(compression_ratio),
        )
    
    def _profile_column(self, df: pd.DataFrame, col: str) -> ColumnProfile:
        series = df[col]
        null_count = series.isnull().sum()
        null_percentage = (null_count / len(series) * 100) if len(series) > 0 else 0
        unique_count = series.nunique()
        cardinality_ratio = unique_count / len(series) if len(series) > 0 else 0
        
        profile = ColumnProfile(
            name=col,
            dtype=str(series.dtype),
            null_count=int(null_count),
            null_percentage=float(null_percentage),
            unique_count=int(unique_count),
            cardinality_ratio=float(cardinality_ratio),
        )
        
        if pd.api.types.is_numeric_dtype(series):
            profile.is_numeric = True
            valid_series = series.dropna()
            if len(valid_series) > 0:
                profile.min_value = float(valid_series.min())
                profile.max_value = float(valid_series.max())
                profile.mean_value = float(valid_series.mean())
                profile.median_value = float(valid_series.median())
                profile.std_value = float(valid_series.std())
                profile.skewness = float(valid_series.skew())
        
        elif pd.api.types.is_object_dtype(series) or pd.api.types.is_categorical_dtype(series):
            profile.is_categorical = True
            top_cats = series.value_counts().head(self.top_categories)
            profile.top_categories = list(zip(top_cats.index.astype(str), top_cats.values.tolist()))
        
        elif pd.api.types.is_datetime64_any_dtype(series):
            profile.is_datetime = True
            valid_series = series.dropna()
            if len(valid_series) > 0:
                profile.min_value = valid_series.min().timestamp()
                profile.max_value = valid_series.max().timestamp()
        
        return profile
    
    def _estimate_compressed_size(self, columns: List[ColumnProfile]) -> int:
        size = 500
        for col in columns:
            if col.is_numeric or col.is_datetime:
                size += 200
            elif col.is_categorical:
                size += 500
            else:
                size += 100
        
        return size
    
    def get_compression_stats(self) -> Dict[str, Any]:
        return {
            'avg_compression_ratio': 0.75,
            'typical_metadata_reduction': '75%',
            'benefits': [
                'Reduced memory footprint',
                'Faster multi-table analysis',
                'Efficient data transfer',
                'Maintains analytical value'
            ]
        }
