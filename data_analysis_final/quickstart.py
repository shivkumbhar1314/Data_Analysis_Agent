
import sys
from pathlib import Path

# Setup path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.data_analysis_agent import DataAnalysisAgent


def main():
    
    print("\n" + "=" * 70)
    print("DATA-ANALYSIS-AGENT: Automated EDA & AutoML")
    print("=" * 70)
    
    # Initialize
    agent = DataAnalysisAgent(output_dir="outputs")
    
    # QUICK START: Run analysis on sample data
    sample_data_path = "data/sample_data.csv"
    
    print(f"\nRunning analysis on: {sample_data_path}")
    print("    This will execute all agents and generate reports...")
    print()
    
    # Run full analysis
    results = agent.analyze(
        data_source=sample_data_path,
        dataset_name="sample_loan_data",
        target_column="approved",           # For supervised learning
        run_agents=None,                     # Run all agents
        generate_reports=True
    )
    
    # Display results
    print("\n" + "=" * 70)
    if results.get('success'):
        print("SUCCESS: ANALYSIS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        
        # Summary
        print("\nANALYSIS SUMMARY:")
        if results.get('summary'):
            print(results['summary'])
        
        # Agent results
        print("\nAGENT RESULTS:")
        for agent_name, agent_result in results.get('agent_results', {}).items():
            status = "SUCCESS" if agent_result.get('success') else "FAILED"
            time = agent_result.get('execution_time', 0)
            print(f"   {status} {agent_name:30s} ({time:.2f}s)")
        
        print("\nREPORTS GENERATED:")
        print("   SUCCESS outputs/report_sample_loan_data_*.html")
        print("   SUCCESS outputs/report_sample_loan_data_*.json")
    
    else:
        print("FAILED: ANALYSIS FAILED")
        print("=" * 70)
        print(f"Error: {results.get('error')}")
    
    print("\n" + "=" * 70)
    print("Check the 'outputs/' directory for detailed analysis reports")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    main()
