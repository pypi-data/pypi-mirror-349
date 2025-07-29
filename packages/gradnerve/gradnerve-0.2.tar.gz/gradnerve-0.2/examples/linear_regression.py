import numpy as np
from gradnerve import tensor as gn

# Generate some sample data
X = np.array([[1, 2], [2, 3], [3, 4]], dtype=np.float64)
y = np.array([6, 8, 10], dtype=np.float64)

# Define the model
class LinearRegression:
    def __init__(self, n_features):
        self.weights = gn.Tensor(np.zeros((n_features, 1), dtype=np.float64), requires_grad=True)
        self.bias = gn.Tensor(np.zeros(1, dtype=np.float64), requires_grad=True)

    def forward(self, X):
        X = gn.Tensor(X)
        return X @ self.weights + self.bias

# Initialize the model
model = LinearRegression(n_features=2)

# Define the loss function
def mse_loss(y_pred, y_true):
    return ((y_pred - y_true)**2).mean()

# Train the model
learning_rate = 0.01
num_epochs = 100

for epoch in range(num_epochs):
    # Forward pass
    y_pred = model.forward(X)
    y_true = gn.Tensor(y, requires_grad=False)

    # Calculate the loss
    loss = mse_loss(y_pred, y_true)

    # Backward pass
    loss.backward()

    # Update the parameters
    model.weights.data -= learning_rate * model.weights.grad
    model.bias.data -= learning_rate * model.bias.grad

    # Zero the gradients
    model.weights.grad = np.zeros_like(model.weights.data)
    model.bias.grad = np.zeros_like(model.bias.data)

    if (epoch+1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.data:.4f}')

# Print the learned parameters
print(f'Learned weights: {model.weights.data}')
print(f'Learned bias: {model.bias.data}')