import torch

def test_cuda_setup():
    print("Testing CUDA setup...")
    if torch.cuda.is_available():
        print("CUDA is available")
    else:
        print("CUDA is not available")
    
    print("Testing Device Count...")
    device_count = torch.cuda.device_count()
    print(f"Number of CUDA devices: {device_count}")

    print("Testing Device Name...")
    device_name = torch.cuda.get_device_name(0)
    print(f"CUDA Device Name: {device_name}") 

    print("Testing CUDA Version...")
    cuda_version = torch.version.cuda
    print(f"CUDA Version: {cuda_version}")

    print("Testing Memory Availability...")
    memory_info = torch.cuda.memory_info(0)
    print(f"Total Memory: {memory_info.total / 1e9:.2f} GB")
    print(f"Available Memory: {memory_info.free / 1e9:.2f} GB")   

if __name__ == "__main__":
    test_cuda_setup()
