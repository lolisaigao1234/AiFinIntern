import sys
import importlib

def test_library_import():
    # Dictionary mapping library names to their import module names
    library_mapping = {
        "torch": "torch",
        "transformers": "transformers",
        "pandas": "pandas",
        "numpy": "numpy",
        "yfinance": "yfinance",
        "requests": "requests",
        "beautifulsoup4": "bs4",
        "feedparser": "feedparser",
        "pytest": "pytest",
        "matplotlib": "matplotlib",
    }

    results = {}
    overall_success = True

    print("Testing library imports...\n")

    for lib_name, module_name in library_mapping.items():
        try:
            importlib.import_module(module_name)
            results[lib_name] = "SUCCESS"
        except ImportError as e:
            results[lib_name] = f"FAILURE: {e}"
            overall_success = False
        except Exception as e:
            results[lib_name] = f"ERROR: {e}"
            overall_success = False

    # Print Summary Table
    print(f"{'Library':<20} | {'Status':<10}")
    print("-" * 35)
    for lib_name, status in results.items():
        # Truncate status if it's too long for the table, but keep the full error in the dict if needed
        display_status = status if len(status) < 50 else status[:47] + "..."
        print(f"{lib_name:<20} | {display_status:<10}")

    return overall_success

if __name__ == "__main__":
    success = test_library_import()
    if success:
        print("\nOverall Status: SUCCESS")
        sys.exit(0)
    else:
        print("\nOverall Status: FAILURE")
        sys.exit(1)
