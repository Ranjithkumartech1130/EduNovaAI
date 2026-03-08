import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load trained model
model = AutoModelForSeq2SeqLM.from_pretrained("trained_algorithm_model")
tokenizer = AutoTokenizer.from_pretrained("trained_algorithm_model")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if device.type == "cpu":
    torch.set_num_threads(2)
    torch.set_num_interop_threads(1)
    print(f"✅ CPU Threads limited to: {torch.get_num_threads()}")

model.to(device)

# ⭐ GIVE YOUR TEST ALGORITHM HERE
test_input = """Check algorithm:
Start
Input marks
If marks >= 90 then
   Print "Excellent"
Else if marks >= 50 then
   Print "Pass"
Else
   Print "Fail"
Stop
"""

# Tokenize
inputs = tokenizer(test_input, return_tensors="pt").to(device)

# Generate output
outputs = model.generate(
    **inputs,
    max_length=100,
    num_beams=5,
    early_stopping=True
)

# Print result
result = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("\nModel Result:")
print(result)