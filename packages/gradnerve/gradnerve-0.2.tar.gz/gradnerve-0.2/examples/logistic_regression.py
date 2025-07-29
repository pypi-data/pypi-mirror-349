import numpy as np
from gradnerve import tensor as gn
from gradnerve import ops

# Generate some sample data
n_samples = 100
n_features = 2

X = np.random.randn(n_samples, n_features)
y = np.random.randint(0, 2, n_samples)

# Define the model
class LogisticRegression:
    def __init__(self, n_features):
        self.weights = gn.Tensor(np.zeros((n_features, 1)), requires_grad=True)
        self.bias = gn.Tensor(np.zeros(1), requires_grad=True)

    def forward(self, X):
        X = gn.Tensor(X)
        linear_model = X @ self.weights + self.bias
        return gn.Tensor([1.0]) / (gn.Tensor([1.0]) + ops.exp( -linear_model))

# Initialize the model
model = LogisticRegression(n_features)

# Define the loss function (Binary Cross-Entropy)
def binary_cross_entropy(y_pred, y_true):
    log_probs = y_true * ops.log(y_pred) + (gn.Tensor([1.0]) - y_true) * ops.log(gn.Tensor([1.0]) - y_pred)
    return ops.mean(log_probs) * gn.Tensor([-1.0])

# Train the model
learning_rate = 0.1
num_epochs = 500

for epoch in range(num_epochs):
    # Forward pass
    y_pred = model.forward(X)
    y_true = gn.Tensor(y.reshape(-1, 1))

    # Calculate the loss
    loss = binary_cross_entropy(y_pred, y_true)

    # Backward pass
    loss.backward()

    # Update the parameters
    model.weights.data -= learning_rate * model.weights.grad
    model.bias.data -= learning_rate * model.bias.grad

    # Zero the gradients
    model.weights.grad = np.zeros_like(model.weights.data)
    model.bias.grad = np.zeros_like(model.bias.data)

    if (epoch+1) % 50 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.data[0]:.4f}')

# Print the learned parameters
print(f'Learned weights: {model.weights.data}')
print(f'Learned bias: {model.bias.data}')