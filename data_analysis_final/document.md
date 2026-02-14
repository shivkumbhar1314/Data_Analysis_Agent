# Data-Analysis-Agent Installation & Setup Guide

## Prerequisites

- Python 3.7+
- pip or conda

## Installation Steps

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- pandas >= 1.3.0
- numpy >= 1.20.0
- scikit-learn >= 1.0.0
- sqlalchemy >= 1.4.0
- openpyxl >= 3.6.0
- pyarrow >= 5.0.0
- scipy >= 1.7.0

### 2. Verify Installation

```bash
python -c "
import sys
sys.path.insert(0, 'src')
from data_analysis_agent import DataAnalysisAgent
print('✓ Installation successful!')
"
```

## Quick Start (30 seconds)

### Option 1: Run Sample Analysis

```bash
python quickstart.py
```

This will:
1. Load sample dataset (`data/sample_data.csv`)
2. Run all analysis agents
3. Generate HTML and JSON reports
4. Display results summary

### Option 2: Analyze Your Own Data

```python
import sys
sys.path.insert(0, 'src')
from data_analysis_agent import DataAnalysisAgent

agent = DataAnalysisAgent()
results = agent.analyze('your_data.csv', dataset_name='MyAnalysis')
agent.print_summary()
```

### Option 3: Run from Command Line

```bash
python main.py --data your_data.csv --name MyDataset
```

## Common Use Cases

### 1. Basic EDA on CSV File

```python
from src.data_analysis_agent import DataAnalysisAgent

agent = DataAnalysisAgent()
agent.analyze('data/sales.csv', dataset_name='sales_eda')
agent.print_summary()
```

### 2. Prepare Data for Classification

```python
results = agent.analyze(
    data_source='data/customer_churn.csv',
    target_column='churn',           # Classification target
    dataset_name='churn_prediction'
)
```

### 3. Regression Analysis

```python
results = agent.analyze(
    data_source='data/house_prices.csv',
    target_column='price',            # Regression target
    dataset_name='price_prediction'
)
```

### 4. Run Specific Agents Only

```python
# Run only profiling and anomaly detection
results = agent.analyze(
    data_source='data/data.csv',
    run_agents=['profiling', 'anomalies'],
    generate_reports=True
)
```

### 5. Disable Report Generation (Speed Up)

```python
results = agent.analyze(
    data_source='data/data.csv',
    generate_reports=False
)
```

## Data Format Support

### CSV Files
```python
agent.analyze('data/file.csv')
```

### Parquet Files
```python
agent.analyze('data/file.parquet')
```

### Excel Files
```python
agent.analyze('data/file.xlsx')
```

### SQL Database
```python
from src.core import DataIngestion

df = DataIngestion.load_sql(
    connection_string='postgresql://user:pass@localhost/db',
    query='SELECT * FROM table'
)
```

## Understanding Output

### Generated Reports

**HTML Report** (`outputs/report_*.html`)
- Interactive, styled analysis report
- All agent results visualized
- Easy to share and present

**JSON Report** (`outputs/report_*.json`)
- Machine-readable format
- Programmatic access to all metrics
- Integration with other tools

### Console Output

```
Profiling Agent: SUCCESS (2.34s)
Visualization Agent: SUCCESS (1.12s)
Insight Generator: SUCCESS (0.89s)
Anomaly Detection Agent: SUCCESS (1.56s)
AutoML Agent: SUCCESS (2.78s)
```

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution:** Add src to Python path
```python
import sys
sys.path.insert(0, 'src')
```

### Issue: Memory Error on Large Files

**Solution:** ScaleDown automatically compresses metadata, but for very large files:
1. Use Parquet format (more efficient)
2. Run agents individually
3. Load data in chunks

### Issue: Missing Values Causing Errors

**Solution:** Check validation output and review agent results
```python
from src.core import DataIngestion
validation = DataIngestion.validate_data(df)
print(validation['issues'])
```

### Issue: Slow Analysis

**Solution:** Skip report generation
```python
agent.analyze('data.csv', generate_reports=False)
```

## Configuration

Create custom configuration:

```python
from src.config import create_custom_config

config = create_custom_config(
    output_directory='my_reports',
    verbose=True,
    generate_html_report=True,
    generate_json_report=True
)
```

## Testing

Run test suite:
```bash
python -m pytest tests/
```

Or:
```bash
python -m unittest tests.test_agent
```

## File Structure

```
Data-Analysis-Agent-Intel-HK/
├── src/                     # Source code
│   ├── agents/             # Analysis agents
│   ├── core/               # Core components
│   ├── utils/              # Utilities
│   └── data_analysis_agent.py  # Main orchestrator
├── data/                   # Data directory (input)
├── outputs/                # Reports directory (output)
├── tests/                  # Test suite
├── quickstart.py           # Quick start example
├── main.py                 # CLI entry point
└── requirements.txt        # Dependencies
```

## Next Steps

1. **Try the sample:** `python quickstart.py`
2. **Load your data:** `agent.analyze('your_file.csv')`
3. **Check reports:** Open `outputs/report_*.html`
4. **Explore code:** Review agent implementations in `src/agents/`
5. **Customize:** Modify configuration in `src/config.py`

## Support & Documentation

- See [README.md](README.md) for project overview
- See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed architecture
- Code docstrings contain detailed documentation
- [tests/test_agent.py](tests/test_agent.py) has usage examples

## Advanced Usage

### Custom Agent

```python
from src.agents import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__('MyAgent', 'My custom analysis')
    
    def execute(self, df, **kwargs):
        # Your analysis code
        pass

agent.agents['custom'] = MyAgent()
```

### Access Agent Results

```python
result = agent.get_agent_result('Profiling Agent')
print(result.output)  # Get detailed output
```

---

**Happy analyzing! 📊**
