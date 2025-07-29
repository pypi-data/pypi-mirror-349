import sys
sys.path.append("/Users/siddharthshah/Documents/MatrixLand/gradnerve")
from gradnerve import tensor as gn
import numpy as np
from gradnerve import ops

# Generate some sample data
n_samples = 100
n_features = 2

X = np.random.randn(n_samples, n_features)
y = np.random.randint(0, 2, n_samples)

# Define the model
class SimpleNeuralNetwork:
    def __init__(self, n_features, n_hidden):
        self.weights1 = gn.Tensor(np.random.randn(n_features, n_hidden), requires_grad=True)
        self.bias1 = gn.Tensor(np.zeros((1, n_hidden)), requires_grad=True)
        self.weights2 = gn.Tensor(np.random.randn(n_hidden, 1), requires_grad=True)
        self.bias2 = gn.Tensor(np.zeros((1, 1)), requires_grad=True)

    def forward(self, X):
        layer1 = X @ self.weights1 + self.bias1
        activation1 = gn.Tensor([1.0]) / (gn.Tensor([1.0]) + gn.Tensor(np.exp(-layer1.data)))  # Sigmoid activation
        output = activation1 @ self.weights2 + self.bias2
        return gn.Tensor([1.0]) / (gn.Tensor([1.0]) + gn.Tensor(np.exp(-output.data)))  # Sigmoid activation

# Initialize the model
n_hidden = 4
model = SimpleNeuralNetwork(n_features, n_hidden)

# Define the loss function (Binary Cross-Entropy)
def binary_cross_entropy(y_pred, y_true):
    log_probs = y_true * ops.log(y_pred) + (gn.Tensor([1.0]) - y_true) * ops.log(gn.Tensor([1.0]) - y_pred)
    return ops.mean(log_probs) * gn.Tensor([-1.0])

# Train the model
learning_rate = 0.1
num_epochs = 500

for epoch in range(num_epochs):
    # Forward pass
    X_tensor = gn.Tensor(X)
    y_pred = model.forward(X_tensor)
    y_true = gn.Tensor(y.reshape(-1, 1))

    # Calculate the loss
    y_true_tensor = gn.Tensor(y.reshape(-1, 1))
    loss = binary_cross_entropy(y_pred, y_true_tensor)

    # Backward pass
    loss.backward()

    # Update the parameters
    model.weights1.data -= learning_rate * model.weights1.grad
    model.bias1.data -= learning_rate * model.bias1.grad
    model.weights2.data -= learning_rate * model.weights2.grad
    model.bias2.data -= learning_rate * model.bias2.grad

    # Zero the gradients
    model.weights1.grad = np.zeros_like(model.weights1.data)
    model.bias1.grad = np.zeros_like(model.bias1.data)
    model.weights2.grad = np.zeros_like(model.weights2.data)
    model.bias2.grad = np.zeros_like(model.bias2.data)

    if (epoch+1) % 50 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.data[0]:.4f}')

# Print the learned parameters
print(f'Learned weights1: {model.weights1.data}')
print(f'Learned bias1: {model.bias1.data}')
print(f'Learned weights2: {model.weights2.data}')
print(f'Learned bias2: {model.bias2.data}')