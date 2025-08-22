"""
Command Line Interface for RHD Bearings Catalog Generator.
"""

import argparse
import sys
from pathlib import Path

from .generators.json_generator import BearingJSONGenerator
from .core.config import Config


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="RHD Bearings Product Catalog Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  rhd-bearings generate                    # Generate complete catalog
  rhd-bearings generate --output custom/  # Generate to custom directory
  rhd-bearings --version                   # Show version
        """
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version="RHD Bearings Catalog Generator 1.0.0"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Generate command
    generate_parser = subparsers.add_parser(
        "generate", 
        help="Generate bearing catalog JSON files"
    )
    generate_parser.add_argument(
        "--output", 
        type=str, 
        help="Output directory for generated files",
        default=None
    )
    generate_parser.add_argument(
        "--bearings-only",
        action="store_true",
        help="Generate only the bearings catalog (skip series pages)"
    )
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Show project information")
    
    args = parser.parse_args()
    
    if args.command == "generate":
        generate_catalog(args)
    elif args.command == "info":
        show_info()
    else:
        parser.print_help()


def generate_catalog(args):
    """Generate the bearing catalog."""
    try:
        print("🏭 RHD Bearings Catalog Generator")
        print("=" * 40)
        
        generator = BearingJSONGenerator()
        
        # Set custom output path if provided
        output_path = None
        if args.output:
            output_path = Path(args.output) / "generated_bearings_complete.json"
        
        generator.save_catalog(output_path)
        
        print("\n✅ Catalog generation completed successfully!")
        print("\n📊 Generated files:")
        print(f"   • Bearings catalog: {output_path or Config.OUTPUT_FILES['bearings_catalog']}")
        
        if not args.bearings_only:
            print(f"   • Series pages: {Config.OUTPUT_FILES['series_pages']}")
        
        print("\n🚀 Ready for website deployment!")
        
    except Exception as e:
        print(f"\n❌ Error generating catalog: {e}")
        sys.exit(1)


def show_info():
    """Show project information."""
    print("🏭 RHD Bearings Product Catalog Generator")
    print("=" * 50)
    print()
    print("📋 Project Information:")
    print(f"   • Version: 1.0.0")
    print(f"   • Company: {Config.COMPANY['name']}")
    print(f"   • Website: {Config.COMPANY['website']}")
    print(f"   • Email: {Config.COMPANY['email']}")
    print(f"   • Phone: {Config.COMPANY['phone']}")
    print()
    print("📁 Project Structure:")
    print(f"   • Data directory: {Config.DATA_DIR}")
    print(f"   • Output directory: {Config.OUTPUT_DIR}")
    print(f"   • Documentation: {Config.DOCS_DIR}")
    print()
    print("🎯 Features:")
    print("   • 194 bearing models with complete specifications")
    print("   • SEO-optimized metadata and URLs")
    print("   • LLM-friendly content for AI recommendations")
    print("   • Technical drawings and detailed applications")
    print("   • Comprehensive FAQs and cross-references")
    print()
    print("📞 Contact Information:")
    print(f"   • Sales: {Config.COMPANY['email']}")
    print(f"   • OEM Sales: {Config.COMPANY['oem_email']}")
    print(f"   • Phone: {Config.COMPANY['phone']}")


if __name__ == "__main__":
    main()
