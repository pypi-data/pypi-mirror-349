import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def get_device():
    """Return available device (cuda or cpu)."""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_tokenizer(model_path):
    """
    Load tokenizer from checkpoint.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True)
    return tokenizer

def load_model(model_path, device=None):
    """
    Load causal language model from checkpoint.
    """
    if device is None:
        device = get_device()
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        use_flash_attention_2=True
    )
    return model.to(device).eval()

