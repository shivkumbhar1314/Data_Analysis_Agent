# Data-Analysis-Agent

## Project Structure

```
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── main.py                            # Example usage and CLI entry point
├── src/
│   ├── __init__.py                   # Package initialization
│   ├── config.py                     # Configuration settings
│   ├── data_analysis_agent.py        # Main orchestrator
│   ├── core/                         # Core components
│   │   ├── __init__.py
│   │   ├── scaledown_engine.py       # Data compression engine (~75% reduction)
│   │   └── data_ingestion.py         # Multi-format data loading (CSV, SQL, Parquet)
│   ├── agents/                       # Specialized analysis agents
│   │   ├── __init__.py
│   │   ├── base_agent.py            # Abstract base class for agents
│   │   ├── profiling_agent.py       # Dataset profiling (structure, quality)
│   │   ├── visualization_agent.py   # Visualization recommendations
│   │   ├── insight_generator_agent.py  # Insight discovery
│   │   ├── anomaly_detection_agent.py  # Outlier & anomaly detection
│   │   └── automl_agent.py          # Model recommendations and AutoML
│   └── utils/                        # Utilities
│       ├── __init__.py
│       └── report_generator.py       # HTML/JSON report generation
├── data/                             # Data directory (input files)
├── outputs/                          # Generated reports
└── tests/
    └── test_agent.py                # Unit tests
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Python path (if running directly):
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

## Quick Start

### Basic Usage (Python)

```python
from src.data_analysis_agent import DataAnalysisAgent

# Initialize agent
agent = DataAnalysisAgent(output_dir="outputs")

# Run analysis
results = agent.analyze(
    data_source="data/your_dataset.csv",
    dataset_name="MyAnalysis",
    target_column=None,
    generate_reports=True
)

# Print summary
agent.print_summary()
```

### Command Line Usage

```bash
python main.py --data data/sample.csv --name MyDataset
```

### With Target Variable (Supervised Learning)

```python
results = agent.analyze(
    data_source="data/data.csv",
    dataset_name="Classification",
    target_column="target_variable"
)
```

## Core Components

### 1. ScaleDown Engine
- Compresses dataset metadata by ~75%
- Maintains analytical value
- Enables efficient multi-table analysis
- Reduces memory footprint

**Key Benefits:**
- 75% compression of schema and statistics
- Faster analysis on compressed profiles
- Efficient data transfer
- Maintains all analytical insights

### 2. Data Ingestion Layer
Supports multiple data sources:
- **CSV files** - With configurable parsing
- **Parquet** - Columnar format for big data
- **Excel** - XLSX and XLS support
- **SQL databases** - Via SQLAlchemy connection strings

**Auto-detection** of file format and **validation** of loaded data.

### 3. Analysis Agents

#### Profiling Agent
- Dataset structure and shape analysis
- Column-level statistics
- Data quality assessment
- Missing data patterns
- Duplicate detection

**Output:**
- Compressed column profiles
- Data quality metrics
- Missing data analysis
- Memory usage statistics

#### Visualization Agent
- Smart chart recommendations
- Visualization metadata
- Univariate analysis suggestions
- Bivariate relationships
- Correlation recommendations

**Output:**
- Recommended chart types
- Column applicability
- Visualization metadata

#### Insight Generator
- Statistical discoveries
- Distribution analysis
- Relationship identification
- Anomaly indicators
- Data readiness assessment

**Output:**
- Key statistical insights
- Distribution summaries
- Correlation findings
- Anomaly indicators
- Readiness scores

#### Anomaly Detection Agent
- Univariate outlier detection (IQR method)
- Multivariate anomaly detection
- Data quality issue identification
- Statistical anomalies

**Output:**
- Outlier lists with bounds
- Anomaly percentages
- Quality issues
- Severity assessment

#### AutoML Agent
- Problem type inference
- Feature recommendations
- Model suggestions
- Preprocessing guidance
- Pipeline recommendations

**Output:**
- Problem classification
- Feature importance
- Model recommendations with scores
- Preprocessing steps
- AutoML pipeline guidance

## Report Generation

Automatically generates:
- **HTML Report** - Interactive, styled analysis report
- **JSON Report** - Machine-readable results format
- **Text Summary** - Console summary of findings

Reports include:
- Dataset profile and statistics
- Results from all agents
- Visualizations metadata
- Recommendations
- Data quality assessment

## Configuration

Edit `src/config.py` to customize:

```python
from src.config import create_custom_config

config = create_custom_config(
    verbose=True,
    output_directory="custom_outputs",
    generate_html_report=True,
    generate_json_report=True
)
```

## Testing

Run the test suite:

```bash
python -m pytest tests/
# or
python -m unittest tests.test_agent
```

## Examples

### 1. Basic EDA on CSV

```python
from src.data_analysis_agent import DataAnalysisAgent

agent = DataAnalysisAgent()
results = agent.analyze("data/sales.csv", dataset_name="sales_eda")
```

### 2. Classification Analysis with Target

```python
results = agent.analyze(
    data_source="data/customer_churn.csv",
    target_column="churn",
    dataset_name="churn_prediction"
)
```

### 3. Run Specific Agents Only

```python
results = agent.analyze(
    data_source="data/data.csv",
    run_agents=['profiling', 'insights', 'anomalies']
)
```

### 4. SQL Data Analysis

```python
from src.core import DataIngestion

df = DataIngestion.load_sql(
    "postgresql://user:password@localhost/db",
    "SELECT * FROM table"
)
```

## Workflow

```
┌─────────────────────────────────┐
│  Load Data (CSV/SQL/Parquet)   │
└────────────┬────────────────────┘
             │
┌────────────v────────────────────┐
│  Create ScaleDown Profile       │
│  (75% compression)              │
└────────────┬────────────────────┘
             │
    ┌────────v────────┐
    │                 │
    v                 v
┌──────────┐     ┌───────────────┐
│ Profil.  │     │ Visualiz.     │
│ Agent    │     │ Agent         │
└────┬─────┘     └────┬──────────┘
     │                │
     │     ┌──────────┤
     │     │          │
     v     v          v
┌──────────────────────────────────┐
│ Insight Generator Anomaly Detect │
│ AutoML Agent                      │
└────────────┬─────────────────────┘
             │
┌────────────v────────────────────┐
│  Generate Reports               │
│  (HTML, JSON, Summary)          │
└────────────┬────────────────────┘
             │
    ┌────────v────────┐
    │ Results Ready   │
    └─────────────────┘
```

## Performance

- **Speed:** Typically completes EDA in 30-60 seconds for datasets < 10MB
- **Memory:** Uses ~75% less memory via ScaleDown compression
- **Scalability:** ScaleDown enables analysis of larger datasets

## Customization

### Add Custom Agent

```python
from src.agents import BaseAgent, AgentResult
import pandas as pd

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__("Custom", "My custom analysis")
    
    def execute(self, df: pd.DataFrame, **kwargs):
        # Your analysis logic
        return AgentResult(...)

# Add to orchestrator
agent.agents['custom'] = CustomAgent()
```

## Troubleshooting

**Memory errors on large datasets:**
- Use ScaleDown compression (automatic)
- Load data in chunks
- Use Parquet format for better compression

**Slow analysis:**
- Profile only key columns
- Skip report generation temporarily
- Run specific agents only

**Missing values causing issues:**
- Check validation output
- Use imputation in preprocessing

## Tech Stack

- **Data Processing:** Pandas, NumPy
- **ML/Stats:** Scikit-learn, SciPy
- **Database:** SQLAlchemy
- **Visualization:** Matplotlib, Seaborn (metadata only)
- **Reporting:** HTML, JSON

## License

MIT

## Contributing

Contributions welcome! Submit issues and PRs.

## Support

For issues, questions, or suggestions:
- Create a GitHub issue
- Check documentation in code docstrings
- Review test cases for usage examples

---

**Data-Analysis-Agent** - Automated EDA & AutoML with ScaleDown Compression
