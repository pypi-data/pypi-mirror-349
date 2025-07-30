import torch
from torch.utils.data import Dataset, DataLoader

class TextDataset(Dataset):
    def __init__(self, texts, tokenizer, model, max_length=128):
        enc = tokenizer(
            texts,
            return_tensors="pt",
            truncation=True,
            padding="max_length",
            max_length=max_length
        ).to(model.device)
        self.input_ids = enc["input_ids"]
        self.attention_mask = enc["attention_mask"]
        self.labels = enc["input_ids"]  # Same as input_ids for language modeling

    def __len__(self):
        return self.input_ids.size(0)

    def __getitem__(self, idx):
        return {
            "input_ids": self.input_ids[idx],
            "attention_mask": self.attention_mask[idx],
            "labels": self.labels[idx],
        }
    

def build_dataloader(texts, tokenizer, model, batch_size=4, max_length=128, shuffle=False):
    """
    Utility function to create the dataset and dataloader
    """
    dataset = TextDataset(texts, tokenizer, model, max_length=max_length)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)

