import argparse
from py2exelite.builder import ensure_engine, build_exe, clean_temp

def main():
    parser = argparse.ArgumentParser(
        prog="py2exelite",
        description="Py2ExeLite – Convert Python scripts to .exe easily.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("file", help="Python file to convert (.py)")
    parser.add_argument("--icon", help="Path to .ico icon file")
    parser.add_argument("--name", help="Output exe name")
    parser.add_argument("--version", help="Add version to output name")
    parser.add_argument("--gui", action="store_true", help="GUI mode (no console)")
    parser.add_argument("--console", action="store_true", help="Force show console")
    parser.add_argument("--clean", action="store_true", help="Clean temp folders after build")
    parser.add_argument("--debug", action="store_true", help="Enable verbose logging")
    parser.add_argument("--output", help="Custom output folder for the .exe")
    parser.add_argument("--encrypt", action="store_true", help="Encrypt the script before build (base64)")
    parser.add_argument("--splash", help="Splash image path")
    parser.add_argument("--no-upx", action="store_true", help="Disable UPX compression")
    parser.add_argument("--hidden-import", help="Hidden import to include")

    args = parser.parse_args()

    ensure_engine()
    build_exe(args)

    if args.clean:
        clean_temp()

    print("✅ Build complete! Your .exe is ready.")

if __name__ == "__main__":
    main()
