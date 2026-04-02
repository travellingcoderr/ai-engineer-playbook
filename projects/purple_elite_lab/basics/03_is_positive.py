import torch
import torch.nn as nn
import torch.optim as optim

# 1. 📂 Data Creation
# Numbers from -10 to 10
X = torch.tensor([[-5.0], [-2.0], [1.0], [3.0], [-1.0], [10.0]])
# Targets: 1 if positive, 0 if negative
y_true = (X > 0).float() 

# 2. 🏛️ The Simple Model
# This is how we organize components in PyTorch
class SimpleClassifier(nn.Module):
    def __init__(self):
        super(SimpleClassifier, self).__init__()
        # One linear layer (weights + bias)
        self.fc = nn.Linear(1, 1)
        # Sigmoid: Squashess output to [0, 1] for probability
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # The chain: Linear -> Sigmoid
        return self.sigmoid(self.fc(x))

# 3. ⚙️ Hyperparameters & Training Setup
model = SimpleClassifier()
criterion = nn.BCELoss() # Binary Cross Entropy (For 0 vs 1)
optimizer = optim.SGD(model.parameters(), lr=0.1)

# print(f"Initial Predicted: {model(X)}")

# 4. 🔄 The Training Loop
for epoch in range(100):
    # Standard steps:
    optimizer.zero_grad()
    predictions = model(X)
    loss = criterion(predictions, y_true)
    loss.backward()
    optimizer.step()
    
    if (epoch + 1) % 20 == 0:
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

# 5. 🔍 Final Predictions
print("\n--- Final Tests ---")
test_cases = torch.tensor([[-8.0], [5.0], [0.5], [-2.0]])
results = model(test_cases)

for i, test in enumerate(test_cases):
    prob = results[i].item()
    status = "POSITIVE" if prob > 0.5 else "NEGATIVE"
    print(f"Input: {test.item():.1f} -> Prob: {prob:.4f} -> Result: {status}")

print("\n💡 Interview Tip: Mention that 'Non-linearity' (Sigmoid)")
print("allows neural networks to make complex decisions (like 0 vs 1).")
