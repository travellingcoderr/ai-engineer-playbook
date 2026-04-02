import torch

# 1. 📂 Data Creation (The Truth)
# We want to teach the model that y = 2x + 1
X = torch.tensor([[1.0], [2.0], [3.0], [4.0]]) # Inputs
print(f"X = {X}")
y_true = 2 * X + 1 # True Targets: [3, 5, 7, 9]
print(f"y_true = {y_true}")

# 2. 🏛️ The Model (Initial Random Guesses)
# We start with random values for 'weight' and 'bias'
# We set 'requires_grad=True' so we can optimize them.
w = torch.randn(1, requires_grad=True)
b = torch.randn(1, requires_grad=True)

print(f"Starting weights: w={w.item():.2f}, b={b.item():.2f}")

# 3. ⚙️ Hyperparameters
learning_rate = 0.01

# 4. 🔄 The Training Loop
for epoch in range(2):
    # --- Forward Pass ---
    # Prediction: y = w*x + b
    print(f"Forward Pass: y_pred = {w.item()} * {X} + {b.item()}")
    y_pred = w * X + b
    
    # --- Calculate Loss (Mean Squared Error) ---
    # How far is our guess from the truth?
    loss = torch.mean((y_pred - y_true)**2)
    
    # --- Backward Pass ---
    # Find the slopes (gradients)
    loss.backward()
    
    # --- Step: Simple Gradient Descent ---
    # "torch.no_grad()" tells PyTorch to stop recording for this simple update
    with torch.no_grad():
        w -= learning_rate * w.grad
        b -= learning_rate * b.grad
        
        # Manually zero the gradients for the next round
        w.grad.zero_()
        b.grad.zero_()
        
    if (epoch + 1) % 40 == 0:
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}, w: {w.item():.2f}, b: {b.item():.2f}")

print("\n--- Final Results ---")
print(f"Goal: y = 2x + 1")
print(f"Predicted: y = {w.item():.2f}x + {b.item():.2f}")
print("Status: LEARNED!" if round(w.item()) == 2 and round(b.item()) == 1 else "Status: PERSISTING...")
