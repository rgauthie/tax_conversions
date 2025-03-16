import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required")
        sys.exit(1)

def install_requirements():
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "-r", "requirements.txt"])
        print("Packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        print("\nAlternative installation methods:")
        print("1. Run the command manually with administrator privileges:")
        print("   pip install -r requirements.txt")
        print("2. Or use a virtual environment:")
        print("   python -m venv venv")
        print("   .\\venv\\Scripts\\activate")
        print("   pip install -r requirements.txt")
        sys.exit(1)

def create_directories():
    print("Creating necessary directories...")
    directories = ["input_data", "OUTPUTS", "exchange_rates"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def check_icon():
    """Check if icon exists and is in the correct format"""
    icon_path = os.path.abspath("logo.ico")
    if not os.path.exists(icon_path):
        print("Warning: logo.ico not found in project directory!")
        return None
    return icon_path

def modify_spec_file(spec_file, icon_path):
    """Modify the spec file to ensure icon is included in both build and dist"""
    if not os.path.exists(spec_file):
        return False
        
    with open(spec_file, 'r') as f:
        spec_content = f.read()
    
    # Add icon to the EXE configuration
    if 'icon=' not in spec_content and icon_path:
        spec_content = spec_content.replace(
            'exe = EXE(',
            f'exe = EXE(\n    icon="{icon_path}",'
        )
        
        with open(spec_file, 'w') as f:
            f.write(spec_content)
        return True
    return False

def build_executable():
    print("Building executable...")
    try:
        # Check for icon
        icon_path = check_icon()
        if not icon_path:
            print("Proceeding without custom icon...")
        
        # Create spec file for PyInstaller
        spec_file = "Tax_Conversions.spec"
        
        # Remove existing spec file to ensure clean build
        if os.path.exists(spec_file):
            os.remove(spec_file)
            
        pyinstaller_args = [
            sys.executable,
            "-m",
            "PyInstaller",
            "--name=Tax_Conversions",
            "--onedir",
            "--windowed",
            "--add-data=input_data;input_data",
            "--add-data=OUTPUTS;OUTPUTS",
            "--add-data=exchange_rates;exchange_rates",
            "--hidden-import=convert",
            "--hidden-import=ntpath",
            "--hidden-import=csv",
            "--hidden-import=datetime",
            "--hidden-import=time",
            "--collect-all=tkinter",
            "--collect-all=tkinter.filedialog",
            "--collect-all=tkinter.ttk",
            "--noconfirm"
        ]

        # Add icon if available
        if icon_path:
            pyinstaller_args.extend(["--icon", icon_path])
            print(f"Using icon from: {icon_path}")

        # Add main script
        pyinstaller_args.append("gui.py")

        # Create initial spec file
        subprocess.check_call(pyinstaller_args)
        
        # Modify spec file to ensure icon is included
        if icon_path:
            if modify_spec_file(spec_file, icon_path):
                print("Successfully modified spec file to include icon")
        
        # Build the executable using modified spec
        subprocess.check_call([sys.executable, "-m", "PyInstaller", spec_file])
        
        # Copy necessary directories to dist folder
        dist_dir = os.path.join("dist", "Tax_Conversions")
        if not os.path.exists(dist_dir):
            os.makedirs(dist_dir)
            
        # Copy directories with their contents
        for dir_name in ["input_data", "OUTPUTS", "exchange_rates"]:
            src_dir = os.path.abspath(dir_name)
            dst_dir = os.path.join(dist_dir, dir_name)
            if os.path.exists(src_dir):
                if os.path.exists(dst_dir):
                    shutil.rmtree(dst_dir)
                shutil.copytree(src_dir, dst_dir)
        
        print("\nBuild completed successfully!")
        print("\nYour application can be found in the 'dist/Tax_Conversions' directory.")
        print("To run the application:")
        print("1. Copy the entire 'Tax_Conversions' folder to your desired location")
        print("2. Run 'Tax_Conversions.exe' from within that folder")
    except subprocess.CalledProcessError as e:
        print(f"Error building executable: {e}")
        print("\nAlternative build method:")
        cmd = "pyinstaller --onedir --windowed"
        if icon_path:
            cmd += f" --icon={icon_path}"
        cmd += " --add-data=input_data;input_data --add-data=OUTPUTS;OUTPUTS --add-data=exchange_rates;exchange_rates"
        cmd += " --hidden-import=convert --hidden-import=ntpath --hidden-import=csv --hidden-import=datetime --hidden-import=time"
        cmd += " --collect-all=tkinter --collect-all=tkinter.filedialog --collect-all=tkinter.ttk gui.py"
        print(f"1. Run the command manually with administrator privileges:\n   {cmd}")
        sys.exit(1)

def main():
    print("=== Tax Conversions Build Script ===")
    print("This script will help you package the Tax Conversions application.")
    
    check_python_version()
    install_requirements()
    create_directories()
    build_executable()

if __name__ == "__main__":
    main() 