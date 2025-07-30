import os
import subprocess
import sys
import base64

def ensure_engine():
    try:
        import PyInstaller.__main__
    except ImportError:
        print("🔧 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def clean_temp():
    for folder in ["build", "dist", "__pycache__"]:
        if os.path.exists(folder):
            print(f"🧹 Cleaning: {folder}")
            subprocess.call(["rmdir", "/s", "/q", folder] if os.name == "nt" else ["rm", "-rf", folder])

def build_exe(args):
    py_file = args.file

    if args.encrypt:
        print("🔐 Encrypting Python file with base64...")
        with open(py_file, 'r') as f:
            content = f.read()
        encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        py_file = "_encrypted_temp.py"
        with open(py_file, 'w') as f:
            f.write("import base64;exec(base64.b64decode('{}'))".format(encoded))

    command = ["pyinstaller", "--onefile"]

    if args.gui and not args.console:
        command.append("--windowed")
    if args.icon:
        command.append(f"--icon={args.icon}")
    if args.name:
        name = args.name
        if args.version:
            name += f"_v{args.version}"
        command.append(f"--name={name}")
    if args.output:
        command.append(f"--distpath={args.output}")
    if args.no_upx:
        command.append("--noupx")
    if args.splash:
        command.append(f"--splash={args.splash}")
    if args.hidden_import:
        command.append(f"--hidden-import={args.hidden_import}")
    if args.debug:
        command.append("--log-level=DEBUG")

    command.append(py_file)

    print("🚀 Compiling your .exe with FastInstaller...")
    subprocess.call(command)

    if args.encrypt:
        os.remove(py_file)
        print("🗑️ Encrypted temp file removed.")
