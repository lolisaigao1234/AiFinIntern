import sys

def test_cuda_setup():
    overall_success = True
    
    print("Testing CUDA setup...")
    try:
        import torch
        print("[PASS] torch imported successfully")
    except ImportError as e:
        print(f"[FAIL] Failed to import torch: {e}")
        return False

    # Check CUDA availability
    try:
        if torch.cuda.is_available():
            print("[PASS] CUDA is available")
        else:
            print("[FAIL] CUDA is not available")
            overall_success = False
    except Exception as e:
        print(f"[FAIL] Error checking CUDA availability: {e}")
        overall_success = False

    # Check Device Count
    try:
        device_count = torch.cuda.device_count()
        if device_count > 0:
            print(f"[PASS] Number of CUDA devices: {device_count}")
        else:
            print(f"[FAIL] No CUDA devices found (count is {device_count})")
            overall_success = False
    except Exception as e:
        print(f"[FAIL] Error checking device count: {e}")
        overall_success = False

    # Check Device Name
    try:
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            print(f"[PASS] CUDA Device Name: {device_name}")
        else:
            print("[SKIP] Skipping device name check (CUDA unavailable)")
    except Exception as e:
        print(f"[FAIL] Error getting device name: {e}")
        overall_success = False

    # Check CUDA Version
    try:
        cuda_version = torch.version.cuda
        if cuda_version:
            print(f"[PASS] CUDA Version: {cuda_version}")
        else:
            print("[FAIL] CUDA Version not found")
            overall_success = False
    except Exception as e:
        print(f"[FAIL] Error checking CUDA version: {e}")
        overall_success = False

    # Check Memory Availability
    try:
        if torch.cuda.is_available():
            # Use mem_get_info instead of memory_info
            free, total = torch.cuda.mem_get_info(0)
            print(f"[PASS] Total Memory: {total / 1e9:.2f} GB")
            print(f"[PASS] Available Memory: {free / 1e9:.2f} GB")
        else:
            print("[SKIP] Skipping memory check (CUDA unavailable)")
    except AttributeError:
        print("[FAIL] torch.cuda.mem_get_info() not found (Check PyTorch version)")
        overall_success = False
    except Exception as e:
        print(f"[FAIL] Error checking memory availability: {e}")
        overall_success = False

    return overall_success

if __name__ == "__main__":
    success = test_cuda_setup()
    if success:
        print("\nOverall Status: SUCCESS")
        sys.exit(0)
    else:
        print("\nOverall Status: FAILURE")
        sys.exit(1)
