"""
Quick start script - Runs the complete setup and test
"""

import subprocess
import sys
import os


def run_command(description, command):
    """Run a command and display output"""
    print("\n" + "=" * 70)
    print(f"⚡ {description}")
    print("=" * 70)
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    return result.returncode == 0


def main():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        EMAIL PHISHING DETECTION SYSTEM - QUICK START        ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Check Python version
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Step 1: Install dependencies
    print("\n[STEP 1/3] Installing dependencies...")
    success = run_command(
        "Installing required packages",
        f"{sys.executable} -m pip install -r requirements.txt"
    )
    
    if not success:
        print("❌ Failed to install dependencies. Please check the error above.")
        return
    
    # Step 2: Train model
    print("\n[STEP 2/3] Training the phishing detection model...")
    success = run_command(
        "Training machine learning model",
        f"{sys.executable} train_model.py"
    )
    
    if not success:
        print("❌ Failed to train model. Please check the error above.")
        return
    
    # Step 3: Run tests
    print("\n[STEP 3/3] Running tests...")
    success = run_command(
        "Testing the detection system",
        f"{sys.executable} test_detector.py"
    )
    
    print("\n" + "=" * 70)
    print("✅ SETUP COMPLETE!")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Start the API server: python app.py")
    print("  2. Test the API: python test_detector.py")
    print("  3. Read the README.md for more information")
    print("\nThe API will be available at: http://localhost:5000")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    main()
