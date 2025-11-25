import sys


def test_library_import():
    overall_success = True
    
    print("Testing library imports...")
    try:
        import torch
        print("[PASS] torch imported successfully")
    except ImportError as e:
        print(f"[FAIL] Failed to import torch: {e}")
        overall_success = False

    try:
        import transformers
        print("[PASS] transformers imported successfully")

        version = transformers.__version__
        if version >= "4.40.0":
            print(f"[PASS] transformers version: {version}")
        else:
            print(f"[FAIL] transformers version: {version}")
            overall_success = False
    except ImportError as e:
        print(f"[FAIL] Failed to import transformers: {e}")
        overall_success = False
    
    try:
        import pandas
        print("[PASS] pandas imported successfully")

        version = pandas.__version__
        if version >= "2.2.0":
            print(f"[PASS] pandas version: {version}")
        else:
            print(f"[FAIL] pandas version: {version}")
            overall_success = False
    except ImportError as e:
        print(f"[FAIL] Failed to import pandas: {e}")
        overall_success = False
    
    try:
        import numpy
        print("[PASS] numpy imported successfully")
    except ImportError as e:
        print(f"[FAIL] Failed to import numpy: {e}")
        overall_success = False
    
    try:
        import yfinance
        print("[PASS] yfinance imported successfully")
    except ImportError as e:
        print(f"[FAIL] Failed to import yfinance: {e}")
        overall_success = False
    
    try:
        import requests
        print("[PASS] requests imported successfully")
    except ImportError as e:
        print(f"[FAIL] Failed to import requests: {e}")
        overall_success = False
    
    try:
        import beautifulsoup4
        print("[PASS] beautifulsoup4 imported successfully")
    except ImportError as e:
        print(f"[FAIL] Failed to import beautifulsoup4: {e}")
        overall_success = False
    
    try:
        import feedparser
        print("[PASS] feedparser imported successfully")
    except ImportError as e:
        print(f"[FAIL] Failed to import feedparser: {e}")
        overall_success = False
    
    try:
        import pytest
        print("[PASS] pytest imported successfully")
    except ImportError as e:
        print(f"[FAIL] Failed to import pytest: {e}")
        overall_success = False
    
    try:
        import matplotlib
        print("[PASS] matplotlib imported successfully")
    except ImportError as e:
        print(f"[FAIL] Failed to import matplotlib: {e}")
        overall_success = False

    return overall_success

if __name__ == "__main__":
    success = test_library_import()
    if success:
        print("\nOverall Status: SUCCESS")
        sys.exit(0)
    else:
        print("\nOverall Status: FAILURE")
        sys.exit(1)
