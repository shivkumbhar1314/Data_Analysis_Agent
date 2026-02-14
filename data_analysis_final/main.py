
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_analysis_agent import DataAnalysisAgent


def main():
    
    # Initialize agent
    agent = DataAnalysisAgent(output_dir="outputs")
    
    # Example: Analyze a CSV file
    print("Data-Analysis-Agent: Automated EDA & AutoML Pipeline\n")
    
    # Check if there's sample data
    sample_data_path = Path("data/sample_data.csv")
    
    if not sample_data_path.exists():
        print("To run the agent, provide a data file:")
        print(f"  Place your data file at: {sample_data_path}")
        print("\nSupported formats: CSV, Parquet, Excel")
        print("\nExample usage:")
        print("  agent.analyze('data/your_dataset.csv', dataset_name='MyDataset')")
        print("\nOr use command line:")
        print("  python main.py --data data/your_file.csv --name MyDataset")
        return
    
    # Run analysis
    print(f"Analyzing data from {sample_data_path}\n")
    
    results = agent.analyze(
        data_source=str(sample_data_path),
        dataset_name="sample_data",
        target_column=None,  # Set to column name for supervised learning
        generate_reports=True
    )
    
    # Print summary
    agent.print_summary()
    
    if results.get('success'):
        print("\nSUCCESS: Analysis completed successfully!")
        print("Check 'outputs/' directory for detailed reports")
    else:
        print(f"\nFAILED: Analysis failed: {results.get('error')}")


if __name__ == "__main__":
    main()
