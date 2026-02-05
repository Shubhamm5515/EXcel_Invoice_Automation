"""
Hill Drive Invoice API - Simple Installer
Handles Python 3.13 compatibility issues
"""
import subprocess
import sys
import os

def print_step(step, message):
    """Print formatted step"""
    print(f"\n{'='*60}")
    print(f"Step {step}: {message}")
    print('='*60)

def run_command(command, description):
    """Run command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} - Failed")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    """Main installation process"""
    print("\n" + "="*60)
    print("Hill Drive Invoice API - Installer")
    print("="*60)
    
    # Check Python version
    print(f"\nPython version: {sys.version}")
    
    # Step 1: Upgrade pip
    print_step(1, "Upgrading pip")
    run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Upgrading pip"
    )
    
    # Step 2: Install packages one by one
    print_step(2, "Installing packages")
    
    packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn[standard]", "Uvicorn"),
        ("python-multipart", "Python Multipart"),
        ("pydantic", "Pydantic"),
        ("pydantic-settings", "Pydantic Settings"),
        ("requests", "Requests"),
        ("openpyxl", "OpenPyXL"),
        ("python-dotenv", "Python Dotenv"),
        ("Pillow", "Pillow"),
    ]
    
    failed = []
    for package, name in packages:
        if not run_command(f"{sys.executable} -m pip install {package}", f"Installing {name}"):
            failed.append(name)
    
    # Step 3: Create .env file
    print_step(3, "Creating configuration file")
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            try:
                with open('.env.example', 'r') as src:
                    with open('.env', 'w') as dst:
                        dst.write(src.read())
                print("✓ Created .env file")
                print("⚠ IMPORTANT: Edit .env and add your OCR_SPACE_API_KEY")
            except Exception as e:
                print(f"✗ Failed to create .env: {e}")
        else:
            print("✗ .env.example not found")
    else:
        print("✓ .env file already exists")
    
    # Step 4: Create output directory
    print_step(4, "Creating output directory")
    if not os.path.exists('generated_invoices'):
        try:
            os.makedirs('generated_invoices')
            print("✓ Created generated_invoices directory")
        except Exception as e:
            print(f"✗ Failed to create directory: {e}")
    else:
        print("✓ generated_invoices directory already exists")
    
    # Step 5: Verify template
    print_step(5, "Verifying template file")
    if os.path.exists('inn sample.xlsx'):
        print("✓ Template file found")
    else:
        print("✗ Template file 'inn sample.xlsx' not found!")
        print("  Please ensure the template is in the project directory")
    
    # Summary
    print("\n" + "="*60)
    print("Installation Summary")
    print("="*60)
    
    if failed:
        print(f"\n⚠ Some packages failed to install: {', '.join(failed)}")
        print("You may need to install them manually:")
        for name in failed:
            print(f"  pip install {name}")
    else:
        print("\n✓ All packages installed successfully!")
    
    print("\n" + "="*60)
    print("Next Steps:")
    print("="*60)
    print("\n1. Edit .env file and add your OCR_SPACE_API_KEY")
    print("   Get free API key from: https://ocr.space/ocrapi")
    print("\n2. Start the server:")
    print("   uvicorn main:app --reload")
    print("\n3. Open browser:")
    print("   http://localhost:8000")
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
