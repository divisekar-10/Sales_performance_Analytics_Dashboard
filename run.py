"""
Quick Launcher for Sales Performance Analytics Dashboard
Runs environment checks, dataset validation, and launches Streamlit.
"""

import sys
import subprocess
import os

def main():
    print("=" * 65)
    print("  SALES PERFORMANCE ANALYTICS DASHBOARD - LAUNCHER")
    print("  Academic AI and Data Science Internship Project")
    print("=" * 65)
    
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # 1. Check Python version
    print(f"[✓] Python Version: {sys.version.split()[0]}")
    
    # 2. Check if dataset exists
    data_file = os.path.join(project_dir, "data", "sales_data.csv")
    if not os.path.exists(data_file):
        print("[!] sales_data.csv not found. Generating synthetic dataset...")
        from data.generate_dataset import generate_sales_data
        generate_sales_data(output_path=data_file)
        print("[✓] Dataset generated successfully.")
    else:
        print("[✓] Dataset verified at data/sales_data.csv")
        
    # 3. Launch Streamlit
    print("\n[⚡] Starting Streamlit Dashboard Server...")
    print("[ℹ] The dashboard will open in your default web browser.")
    print("[ℹ] Press Ctrl+C in this terminal to terminate the server.\n")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n[✓] Dashboard stopped by user.")

if __name__ == "__main__":
    main()
