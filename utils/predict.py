import os
import gdown
import torch
import torch.nn.functional as F
from transformers import BertTokenizer, BertForSequenceClassification, BertConfig
from safetensors.torch import load_file

# Set model directory and file paths
MODEL_DIR = "bert_sentiment_model"
MODEL_PATH = os.path.join(MODEL_DIR, "model.safetensors")
GDRIVE_FILE_ID = "1Qki6uC3x9DX_n1OoEZxuD-C8bdGZUM9n"

# Download model if not present
if not os.path.exists(MODEL_PATH):
    print("Downloading model from Google Drive...")
    os.makedirs(MODEL_DIR, exist_ok=True)
    url = f"https://drive.google.com/uc?id={GDRIVE_FILE_ID}"
    gdown.download(url, MODEL_PATH, quiet=False)

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load tokenizer and config
tokenizer = BertTokenizer.from_pretrained(MODEL_DIR)
config = BertConfig.from_pretrained(MODEL_DIR)

# Initialize and load model
model = BertForSequenceClassification(config)
model.load_state_dict(load_file(MODEL_PATH))
model.to(device)
model.eval()

def predict_sentiment_with_score(texts):
    """
    Predict sentiment and provide confidence score for each review.
    """
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt", max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
        scores, preds = torch.max(probs, dim=1)

    results = []
    for label, score in zip(preds, scores):
        label_text = "Positive" if label == 1 else "Negative"
        results.append((label_text, float(score)))

    return results
