import torch
from transformers import BertTokenizer, BertForSequenceClassification
import torch.nn.functional as F

# Load model and tokenizer
MODEL_DIR = "bert_sentiment_model"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = BertTokenizer.from_pretrained(MODEL_DIR)
model = BertForSequenceClassification.from_pretrained(MODEL_DIR)
model.to(device)
model.eval()

def predict_sentiment_with_score(texts):
    """
    Predict sentiment and provide confidence score for each review.

    Args:
    texts: List of input text strings.

    Returns:
    List of tuples containing sentiment label and confidence score for each input.
    """
    # Tokenize input texts
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt", max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        # Get model outputs
        outputs = model(**inputs)
        
        # Apply softmax to get probabilities for each class
        probs = F.softmax(outputs.logits, dim=1)
        
        # Get confidence score and predicted class
        scores, preds = torch.max(probs, dim=1)
        
    # Convert class predictions and confidence scores
    results = []
    for label, score in zip(preds, scores):
        label_text = "Positive" if label == 1 else "Negative"
        confidence = float(score)
        results.append((label_text, confidence))
    
    return results
