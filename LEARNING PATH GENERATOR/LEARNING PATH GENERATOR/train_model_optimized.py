"""
train_model.py  —  Optimized Training Script
"""
import os
import gc
import torch
import pandas as pd
from torch.optim import AdamW
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, get_linear_schedule_with_warmup
from torch.utils.data import Dataset, DataLoader

# ─────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────
MODEL_NAME    = "google/flan-t5-small"
EPOCHS        = 10
LEARNING_RATE = 2e-4
BATCH_SIZE    = 4
GRADIENT_ACCUMULATION_STEPS = 4
MAX_LENGTH    = 128
SAVE_PATH     = "trained_algorithm_model"

# Device detection
if torch.cuda.is_available():
    DEVICE = torch.device("cuda")
    print("Using CUDA (GPU)")
else:
    DEVICE = torch.device("cpu")
    print("Using CPU")

torch.set_num_threads(4)

# ─────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────
print("\nLoading dataset...")
df = pd.read_csv("dataset.csv", usecols=["input", "output"])
train_data = df.to_dict("records")
print(f"Loaded {len(train_data)} examples.")

# ─────────────────────────────────────────────────────────────
# LOAD MODEL & TOKENIZER
# ─────────────────────────────────────────────────────────────
print(f"\nLoading model '{MODEL_NAME}' ...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, low_cpu_mem_usage=True)
model.to(DEVICE)
model.gradient_checkpointing_enable()

# ─────────────────────────────────────────────────────────────
# DATASET
# ─────────────────────────────────────────────────────────────
class AlgorithmDataset(Dataset):
    def __init__(self, data, tokenizer, max_len=MAX_LENGTH):
        self.data      = data
        self.tokenizer = tokenizer
        self.max_len   = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        enc_in = self.tokenizer(str(item["input"]), padding="max_length", truncation=True, max_length=self.max_len, return_tensors="pt")
        enc_out = self.tokenizer(str(item["output"]), padding="max_length", truncation=True, max_length=self.max_len, return_tensors="pt")
        labels = enc_out.input_ids[0].clone()
        labels[labels == self.tokenizer.pad_token_id] = -100
        return {"input_ids": enc_in.input_ids[0], "attention_mask": enc_in.attention_mask[0], "labels": labels}

dataset = AlgorithmDataset(train_data, tokenizer)
loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)

# ─────────────────────────────────────────────────────────────
# TRAINING SETUP
# ─────────────────────────────────────────────────────────────
optimizer = AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=0.01)
total_steps = (len(loader) // GRADIENT_ACCUMULATION_STEPS) * EPOCHS
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=int(0.1 * total_steps), num_training_steps=total_steps)

model.train()
print(f"\nStarting optimized training...")

best_loss = float("inf")

for epoch in range(EPOCHS):
    total_loss = 0.0
    optimizer.zero_grad()
    
    for i, batch in enumerate(loader):
        input_ids = batch["input_ids"].to(DEVICE)
        attention_mask = batch["attention_mask"].to(DEVICE)
        labels = batch["labels"].to(DEVICE)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss / GRADIENT_ACCUMULATION_STEPS
        loss.backward()

        if (i + 1) % GRADIENT_ACCUMULATION_STEPS == 0:
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()

        total_loss += loss.item() * GRADIENT_ACCUMULATION_STEPS
        
        if (i + 1) % 5 == 0:
            print(f"   Epoch {epoch+1}/{EPOCHS} | Batch {i+1}/{len(loader)} | Loss: {loss.item()*GRADIENT_ACCUMULATION_STEPS:.4f}")

    avg_loss = total_loss / len(loader)
    print(f"\nEpoch {epoch+1}/{EPOCHS} complete — Avg Loss: {avg_loss:.4f}")

    if avg_loss < best_loss:
        best_loss = avg_loss
        model.save_pretrained(SAVE_PATH)
        tokenizer.save_pretrained(SAVE_PATH)
        print(f"   Model saved (best loss: {best_loss:.4f})")

    gc.collect()

print("\nTraining complete!")
