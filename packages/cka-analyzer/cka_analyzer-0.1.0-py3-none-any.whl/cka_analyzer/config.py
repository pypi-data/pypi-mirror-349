import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_reference_path', type=str, default="Qwen/Qwen2.5-7B", help="Model reference path")
    parser.add_argument('--model_path', type=str, default="Qwen/Qwen2.5-7B", help="Model path")
    parser.add_argument('--output_path', type=str, default="output", help="output path")
    parser.add_argument('--batch_size', type=int, default=4, help="Batch size for DataLoader")
    parser.add_argument('--num_batches', type=int, default=10, help="Number of batches to estimate CKA")
    parser.add_argument('--max_length', type=int, default=128)
    return parser.parse_args()