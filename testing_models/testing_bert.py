# Too slow

from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax
import torch

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased")

# Example comments
comments = [
    "I love to hate"
]

# Convert comments to tokenized format
tokenized_comments = tokenizer(comments, padding=True, truncation=True, return_tensors="pt")

# Forward pass through the model
with torch.no_grad():
    outputs = model(**tokenized_comments)

# Convert logits to probabilities using softmax
probs = softmax(outputs.logits, dim=1)

# Get predicted labels (0 for negative, 1 for positive)
predicted_labels = torch.argmax(probs, dim=1)

# Map labels to sentiment categories
sentiment_labels = {0: 'Negative', 1: 'Positive'}
predicted_sentiments = [sentiment_labels[label.item()] for label in predicted_labels]

# Print the results
for comment, sentiment in zip(comments, predicted_sentiments):
    print(f"Comment: '{comment}'")
    print(f"Predicted Sentiment: {sentiment}")
    print("\n" + "="*50 + "\n")
