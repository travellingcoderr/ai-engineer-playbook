import torch

# 1. 📂 Define inputs (Tensors)
# We set 'requires_grad=True' so PyTorch starts "recording" every operation
x = torch.tensor(3.0, requires_grad=True)
y = torch.tensor(5.0, requires_grad=True)
print(f"x = {x}, y = {y}")

# 2. ➕ Perform a simple math operation
# Let's say z = (x + y) * 2
# With x=3, y=5, then (3+5)*2 = 16.0
z = (x + y) * 2
print(f"z = (x + y) * 2")
print(f"Result (z): {z.item()}") # Should be 16.0

# 3. 🔍 The "Magic" Step: backward()
# This command calculates the "slopes" (derivatives) automatically.
# derivative of z w.r.t x is: d/dx (2x + 2y) = 2
print(f"Before backward() - Slope (gradient) of z with respect to x: {x.grad}") # Should be None
print(f"Before backward() - Slope (gradient) of z with respect to y: {y.grad}") # Should be None

z.backward()

# 4. 📈 View the slope
print(f"Slope (gradient) of z with respect to x: {x.grad}") # Should be 2.0
print(f"Slope (gradient) of z with respect to y: {y.grad}") # Should be 2.0

print("\n--- Why does this matter? ---")
print("In Machine Learning, we calculate a 'Loss' (error).")
print("We use .backward() to find the slope of the error.")
print("The Optimizer then 'slides down' the slope to reduce the error.")
