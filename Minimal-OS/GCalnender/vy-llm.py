import sqlite3
import torch
import torch.nn as nn
import numpy as np
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

# Define model parameters
vocab_size = 5000
hidden_size = 256
num_layers = 2
num_heads = 8

class SimpleTransformer(nn.Module):
    def __init__(self, vocab_size, hidden_size, num_layers, num_heads):
        super(SimpleTransformer, self).__init__()
        
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        
        encoder_layers = nn.TransformerEncoderLayer(d_model=hidden_size, nhead=num_heads)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layers, num_layers=num_layers)
        
        decoder_layers = nn.TransformerDecoderLayer(d_model=hidden_size, nhead=num_heads)
        self.transformer_decoder = nn.TransformerDecoder(decoder_layers, num_layers=num_layers)
        
        self.fc_out = nn.Linear(hidden_size, vocab_size)
        self.hidden_size = hidden_size

    def forward(self, src, tgt):
        src = self.embedding(src) * np.sqrt(self.hidden_size)
        tgt = self.embedding(tgt) * np.sqrt(self.hidden_size)
        
        src = self.transformer_encoder(src)
        output = self.transformer_decoder(tgt, src)
        
        output = self.fc_out(output)
        return output

# Function to create database and table for training data
def create_database():
    conn = sqlite3.connect('llm_training_data.db')
    cursor = conn.cursor()
    
    # Create a table for storing LLM training data
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS training_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

# Function to load data from database
def load_data_from_db():
    conn = sqlite3.connect('llm_training_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT text FROM training_data')
    rows = cursor.fetchall()
    
    conn.close()
    
    # Extract and return text data
    texts = [row[0] for row in rows]
    return texts

# Dummy tokenizer
class DummyTokenizer:
    def encode(self, text, return_tensors='pt'):
        return torch.tensor([ord(c) for c in text], dtype=torch.long)

# Dataset class for PyTorch
class TextDataset(Dataset):
    def __init__(self, texts, tokenizer):
        self.texts = texts
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        encodings = self.tokenizer.encode(text, return_tensors='pt').squeeze()
        return encodings

# Create the database and insert some example data
create_database()
# Insert example data into the database
def insert_training_data(texts):
    conn = sqlite3.connect('llm_training_data.db')
    cursor = conn.cursor()
    
    cursor.executemany('INSERT INTO training_data (text) VALUES (?)', [(text,) for text in texts])
    
    conn.commit()
    conn.close()

# Example data to insert
example_texts = ["Example text for training", "Another training text"]
insert_training_data(example_texts)

# Load data from the database
texts = load_data_from_db()
tokenizer = DummyTokenizer()
dataset = TextDataset(texts, tokenizer)
dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

# Initialize model
model = SimpleTransformer(vocab_size, hidden_size, num_layers, num_heads)

# Training setup
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
optimizer = optim.Adam(model.parameters(), lr=5e-5)
criterion = nn.CrossEntropyLoss()

def train(model, dataloader, optimizer, criterion, device):
    model.train()
    total_loss = 0
    for batch in dataloader:
        src, tgt = batch, batch  # In a real use case, `src` and `tgt` should be different
        optimizer.zero_grad()
        outputs = model(src.to(device), tgt.to(device))
        loss = criterion(outputs.view(-1, vocab_size), tgt.view(-1).to(device))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(dataloader)

# Train the model
num_epochs = 1
for epoch in range(num_epochs):
    loss = train(model, dataloader, optimizer, criterion, device)
    print(f"Epoch {epoch + 1}, Loss: {loss}")

# Save model to .ggml format
def save_to_ggml(model, filename):
    state_dict = model.state_dict()
    with open(filename, 'wb') as f:
        for key, param in state_dict.items():
            param_data = param.cpu().numpy()
            param_data.tofile(f)

save_to_ggml(model, 'vy_words_0.5.ggml')

# Load model from .ggml format
def load_from_ggml(filename, model):
    state_dict = model.state_dict()
    with open(filename, 'rb') as f:
        for key in state_dict.keys():
            param = torch.from_numpy(np.fromfile(f, dtype=np.float32, count=state_dict[key].numel()))
            state_dict[key].copy_(param.view_as(state_dict[key]))

model = SimpleTransformer(vocab_size, hidden_size, num_layers, num_heads)
load_from_ggml('vy_words_0.5.ggml', model)
