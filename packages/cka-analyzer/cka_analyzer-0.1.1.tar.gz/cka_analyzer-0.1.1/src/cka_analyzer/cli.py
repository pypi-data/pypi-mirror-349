# src/cka_analyzer/cli.py

import argparse
from cka_analyzer.interface import run_cka_analysis

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_reference_path', type=str, required=True)
    parser.add_argument('--model_path', type=str, required=True)
    parser.add_argument('--data_path', type=str, required=True)
    parser.add_argument('--output_path', type=str, required=True)
    parser.add_argument('--batch_size', type=int, default=4)
    parser.add_argument('--num_batches', type=int, default=10)
    parser.add_argument('--max_length', type=int, default=128)
    return parser.parse_args()

def load_texts(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    args = get_args()
    texts = load_texts(args.data_path)

    run_cka_analysis(
        model_reference_path=args.model_reference_path,
        model_path=args.model_path,
        texts=texts,
        output_path=args.output_path,
        batch_size=args.batch_size,
        num_batches=args.num_batches,
        max_length=args.max_length
    )

if __name__ == "__main__":
    main()
