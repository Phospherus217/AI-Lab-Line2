def check_environment():
    import torch
    print(f"Torch version: {torch.__version__}")
    return "CUDA available" if torch.cuda.is_available() else "CPU only"

print(check_environment())
