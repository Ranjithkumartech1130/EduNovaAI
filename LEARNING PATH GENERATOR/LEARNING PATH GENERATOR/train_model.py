"""
train_model.py  —  Laptop-Safe Training Script
Optimized for low-spec machines (4–8 GB RAM, CPU-only)
"""
import os
import gc
import torch
import pandas as pd
from torch.optim import AdamW
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from torch.utils.data import Dataset, DataLoader

# ─────────────────────────────────────────────────────────────
# LAPTOP-SAFE CONFIGURATION
# ─────────────────────────────────────────────────────────────
MODEL_NAME    = "google/flan-t5-small"   # Smallest Flan-T5 — ~300 MB on disk
EPOCHS        = 6          # Was 3 -> 6 for better accuracy on logic flips
LEARNING_RATE = 1e-4
BATCH_SIZE    = 1          # Was 4 → 1 is safest for <4 GB RAM (no OOM crashes)
MAX_LENGTH    = 64         # Was 128 → 64 is plenty for short pseudocode; 2× faster

# Force CPU — GPU mode can overheat a laptop with no active cooling
DEVICE = torch.device("cpu")

# Limit PyTorch to 2 CPU threads → prevents 100% CPU usage on all cores
torch.set_num_threads(2)
torch.set_num_interop_threads(1)

print("=" * 50)
print("  🖥️  Laptop-Safe Training Mode")
print(f"  Batch Size : {BATCH_SIZE}")
print(f"  Max Length : {MAX_LENGTH}")
print(f"  Epochs     : {EPOCHS}")
print(f"  Device     : {DEVICE}")
print(f"  CPU Threads: {torch.get_num_threads()}")
print("=" * 50)

# ─────────────────────────────────────────────────────────────
# LOAD DATA  (fast — no iterrows loop)
# ─────────────────────────────────────────────────────────────
print("\n📂 Loading dataset...")
df         = pd.read_csv("dataset.csv", usecols=["input", "output"])
train_data = df.to_dict("records")   # 10× faster than iterrows()
print(f"✅ Loaded {len(train_data)} examples.")

# ─────────────────────────────────────────────────────────────
# LOAD MODEL & TOKENIZER
# ─────────────────────────────────────────────────────────────
print(f"\n📥 Loading model '{MODEL_NAME}' ...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model     = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    low_cpu_mem_usage=True    # Loads weights progressively → less RAM spike
)
model.to(DEVICE)

# Enable gradient checkpointing → trades compute for ~40% VRAM/RAM savings
model.gradient_checkpointing_enable()

print(f"✅ Model loaded on {DEVICE}.")
print(f"   Parameters: {sum(p.numel() for p in model.parameters()):,}")

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

        enc_in  = self.tokenizer(
            str(item["input"]),
            padding="max_length",
            truncation=True,
            max_length=self.max_len,
            return_tensors="pt"
        )
        enc_out = self.tokenizer(
            str(item["output"]),
            padding="max_length",
            truncation=True,
            max_length=self.max_len,
            return_tensors="pt"
        )

        labels = enc_out.input_ids[0].clone()
        labels[labels == self.tokenizer.pad_token_id] = -100  # Ignore padding in loss

        return {
            "input_ids":      enc_in.input_ids[0],
            "attention_mask": enc_in.attention_mask[0],
            "labels":         labels
        }

dataset = AlgorithmDataset(train_data, tokenizer)
loader  = DataLoader(
    dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0,    # MUST be 0 on Windows (avoids multiprocessing issues)
    pin_memory=False  # CPU training — pin_memory has no benefit here
)

# ─────────────────────────────────────────────────────────────
# TRAINING LOOP  (CPU-optimised)
# ─────────────────────────────────────────────────────────────
optimizer = AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=0.01)

model.train()
print(f"\n🚀 Starting training...")
print("   Press Ctrl+C at any time to stop safely.\n")

best_loss = float("inf")

for epoch in range(EPOCHS):
    total_loss = 0.0
    num_batches = 0

    for i, batch in enumerate(loader):
        optimizer.zero_grad(set_to_none=True)   # Faster than zero_grad()

        input_ids      = batch["input_ids"].to(DEVICE)
        attention_mask = batch["attention_mask"].to(DEVICE)
        labels         = batch["labels"].to(DEVICE)

        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )
        loss = outputs.loss
        loss.backward()

        # Gradient clipping → prevents unstable training on CPU
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

        optimizer.step()

        total_loss  += loss.item()
        num_batches += 1

        # Progress every 10 batches
        if (i + 1) % 10 == 0:
            print(f"   Epoch {epoch+1}/{EPOCHS} | Batch {i+1}/{len(loader)} | Loss: {loss.item():.4f}")

    avg_loss = total_loss / max(num_batches, 1)
    print(f"\n✅ Epoch {epoch+1}/{EPOCHS} complete — Avg Loss: {avg_loss:.4f}")

    # Save best model checkpoint
    if avg_loss < best_loss:
        best_loss = avg_loss
        model.save_pretrained("trained_algorithm_model")
        tokenizer.save_pretrained("trained_algorithm_model")
        print(f"   💾 Model saved (best loss so far: {best_loss:.4f})")

    # Free memory between epochs
    gc.collect()
    print()

# ─────────────────────────────────────────────────────────────
# DONE
# ─────────────────────────────────────────────────────────────
print("=" * 50)
print(f"🎉 Training complete! Best Loss: {best_loss:.4f}")
print("   Model saved to: trained_algorithm_model/")
print("   Now restart app.py to use the updated model.")
print("=" * 50)