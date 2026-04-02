import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# 1. 📂 Data Preparation (Synthetic)
# Imagine this comes from a SQL DB (User age, Transaction amount, Time of day, etc.)
def generate_synthetic_data(n_samples=1000):
    # Features: [Amount, Frequency, Age]
    X = torch.randn(n_samples, 3) 
    # Logic: If Amount > 1.5, it's likely Fraud (1)
    y = (X[:, 0] > 1.5).float().view(-1, 1)
    return X, y

# 2. 🏛️ Model Architecture
# In PyTorch, you ALWAYS inherit from nn.Module
class FraudClassifier(nn.Module):
    def __init__(self):
        super(FraudClassifier, self).__init__()
        # Linear layer: In_features=3 (our inputs), Out_features=16
        self.layer1 = nn.Linear(3, 16)
        # Activation: Non-linear magic
        self.relu = nn.ReLU()
        # Output layer: Reduces to 1 final probability
        self.layer2 = nn.Linear(16, 1)
        # Sigmoid: Flattens output to [0, 1] for binary classification
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # The sequence of execution
        x = self.relu(self.layer1(x))
        x = self.sigmoid(self.layer2(x))
        return x

# 3. 🏋️ Setup Training
model = FraudClassifier()
criterion = nn.BCELoss() # Binary Cross Entropy
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Generate data
X_train, y_train = generate_synthetic_data(2000)

# 4. 🔄 The Training Loop
print("Starting Training...")
for epoch in range(100):
    # 1. Zero the gradients (clear the previous step)
    optimizer.zero_grad()
    
    # 2. Forward pass: Process data through model
    outputs = model(X_train)
    
    # 3. Calculate Loss: How wrong are we?
    loss = criterion(outputs, y_train)
    
    # 4. Backward pass: Calculate gradients (the magic)
    loss.backward()
    
    # 5. Step: Update weights
    optimizer.step()
    
    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch+1}/100], Loss: {loss.item():.4f}')

# 5. 🧪 Testing
test_transaction = torch.tensor([[2.0, 0.5, -1.0]]) # Large amount transaction
prediction = model(test_transaction)
print(f"\nPrediction for sample transaction: {prediction.item():.4f}")
print("Status: FRAUD" if prediction.item() > 0.5 else "Status: NORMAL")
