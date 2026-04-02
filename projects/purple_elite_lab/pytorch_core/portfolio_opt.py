import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# 1. 📈 Data Setup (Market Data)
def generate_portfolio_data(n_samples=500, n_assets=4):
    # Features: [Interest Rate, Inflation, Market Volatility, S&P Index]
    X = torch.randn(n_samples, 4)
    # Returns: Randomly distributed returns for 4 different stocks
    y = torch.randn(n_samples, n_assets) * 0.05 + 0.01 
    return X, y

# 2. 🏛️ The Portfolio Model
class PortfolioNet(nn.Module):
    def __init__(self, n_assets=4):
        super(PortfolioNet, self).__init__()
        # Shared layer: Learns market dependencies
        self.fc1 = nn.Linear(4, 32)
        self.relu = nn.ReLU()
        # Head 1: Predicts individual asset returns (Regression)
        self.return_head = nn.Linear(32, n_assets)
        # Head 2: Recommends weights (Allocation)
        self.weight_head = nn.Linear(32, n_assets)
        self.softmax = nn.Softmax(dim=1) # Ensures weights sum to 1.0 (100%)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        returns = self.return_head(x)
        weights = self.softmax(self.weight_head(x))
        return returns, weights

# 3. 🎯 Custom Loss: The Sharpe Ratio (Simplified)
# Business Objective: Maximize Return per unit of Risk
def sharpe_loss(returns, weights):
    # Predicted Portfolio Return = Sum(Predicted Asset Return * Allocated Weight)
    portfolio_return = torch.sum(returns * weights, dim=1)
    
    # We want to MAXIMIZE return, so we MINIMIZE negative return
    mean_return = torch.mean(portfolio_return)
    std_return = torch.std(portfolio_return) + 1e-6 # Stability
    
    # Negative Sharpe Ratio (Optimization usually minimizes)
    return -(mean_return / std_return)

# 4. 🏋️ Training
model = PortfolioNet()
optimizer = optim.Adam(model.parameters(), lr=0.001)

X_data, y_true_returns = generate_portfolio_data()

print("Optimizing Portfolio...")
for epoch in range(150):
    optimizer.zero_grad()
    
    # Forward Pass
    pred_returns, weights = model(X_data)
    
    # Composite Loss: Predict returns accurately AND Maximize Sharpe Ratio
    mse_loss = nn.MSELoss()(pred_returns, y_true_returns)
    optimization_loss = sharpe_loss(pred_returns, weights)
    
    # Total loss = (Accuracy Loss) + (Efficiency Loss)
    total_loss = mse_loss + optimization_loss
    
    total_loss.backward()
    optimizer.step()
    
    if (epoch + 1) % 20 == 0:
        print(f"Epoch {epoch+1}, Loss: {total_loss.item():.4f} (Sharpe component: {optimization_loss.item():.4f})")

# 5. 🔍 Final Recommendation
test_market_state = torch.tensor([[0.5, -0.2, 1.2, 0.1]]) # Current Economy
_, final_weights = model(test_market_state)

print(f"\nRecommended Portfolio Weights for current Economy:")
assets = ["Tech", "Energy", "Healthcare", "Finance"]
for i, asset in enumerate(assets):
    print(f"{asset}: {final_weights[0, i].item()*100:.2f}%")
