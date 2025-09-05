"""
Setup script for bird sound dataset project
Installs FFmpeg if needed and sets up the environment
"""

import subprocess
import sys
import os

def check_ffmpeg():
    """Check if FFmpeg is installed and accessible."""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg is already installed!")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ FFmpeg not found in system PATH")
    return False

def check_chocolatey():
    """Check if Chocolatey is installed."""
    try:
        result = subprocess.run(['choco', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Chocolatey is installed!")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ Chocolatey not found")
    return False

def install_ffmpeg_with_choco():
    """Install FFmpeg using Chocolatey."""
    print("📦 Installing FFmpeg with Chocolatey...")
    try:
        # Run as administrator is required for choco install
        result = subprocess.run(['powershell', '-Command', 
                               'Start-Process', 'choco', 
                               '-ArgumentList', '"install", "ffmpeg", "-y"',
                               '-Verb', 'RunAs', '-Wait'],
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ FFmpeg installation completed!")
            return True
        else:
            print(f"❌ Installation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error during installation: {str(e)}")
        return False

def setup_environment():
    """Set up the complete environment for the bird sound project."""
    
    print("🔧 BIRD SOUND DATASET PROJECT SETUP")
    print("=" * 50)
    
    # Check Python packages
    print("\n1. Checking Python dependencies...")
    required_packages = ['requests', 'pydub']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"📦 Installing missing packages: {', '.join(missing_packages)}")
        subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing_packages)
    
    # Check FFmpeg
    print("\n2. Checking FFmpeg...")
    if not check_ffmpeg():
        print("\n3. Attempting to install FFmpeg...")
        
        if check_chocolatey():
            user_input = input("\nWould you like to install FFmpeg using Chocolatey? (y/n): ")
            if user_input.lower() in ['y', 'yes']:
                if install_ffmpeg_with_choco():
                    print("✅ Setup complete! FFmpeg has been installed.")
                else:
                    print("❌ FFmpeg installation failed. Please install manually.")
                    show_manual_instructions()
            else:
                show_manual_instructions()
        else:
            print("\n💡 Installing Chocolatey first would make this easier...")
            user_input = input("Would you like to see manual installation instructions? (y/n): ")
            if user_input.lower() in ['y', 'yes']:
                show_manual_instructions()
    
    print("\n🎉 Environment setup complete!")
    print("\nNext steps:")
    print("1. Run: python dataset_collector.py")
    print("2. Run: python convert_to_wav.py")
    print("3. Run: python dataset_summary.py")

def show_manual_instructions():
    """Show manual installation instructions for FFmpeg."""
    print("\n📋 MANUAL FFMPEG INSTALLATION INSTRUCTIONS")
    print("=" * 50)
    print("Option 1 - Using Chocolatey (Recommended):")
    print("  1. Install Chocolatey: https://chocolatey.org/install")
    print("  2. Open PowerShell as Administrator")
    print("  3. Run: choco install ffmpeg")
    print("")
    print("Option 2 - Manual Download:")
    print("  1. Download FFmpeg from: https://ffmpeg.org/download.html")
    print("  2. Extract to a folder (e.g., C:\\ffmpeg)")
    print("  3. Add C:\\ffmpeg\\bin to your system PATH")
    print("  4. Restart your terminal/IDE")
    print("")
    print("Option 3 - Using winget (Windows 10+):")
    print("  1. Open PowerShell")
    print("  2. Run: winget install ffmpeg")

if __name__ == "__main__":
    setup_environment()
