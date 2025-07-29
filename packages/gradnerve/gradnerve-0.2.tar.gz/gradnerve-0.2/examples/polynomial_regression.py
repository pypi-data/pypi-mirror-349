import numpy as np
from gradnerve import tensor as gn
from gradnerve import ops

# Generate some sample data
X = np.linspace(-5, 5, 100)
y = 2*X**3 + 3*X**2 - 5*X + 1 + np.random.normal(0, 10, 100)

X = X.reshape(-1, 1)
y = y.reshape(-1, 1)

# Define the model
class PolynomialRegression:
    def __init__(self, degree):
        self.weights = [gn.Tensor(np.random.randn(1, 1), requires_grad=True) for _ in range(degree + 1)]

    def forward(self, X):
        X = gn.Tensor(X)
        y_pred = gn.Tensor(np.zeros_like(X.data), requires_grad=True)
        for i, w in enumerate(self.weights):
            y_pred = y_pred + w * (X ** i)
        return y_pred

# Initialize the model
degree = 3
model = PolynomialRegression(degree)

# Define the loss function
def mse_loss(y_pred, y_true):
    return ops.mean((y_pred - y_true)**2)

# Train the model
learning_rate = 0.0001
num_epochs = 1000

for epoch in range(num_epochs):
    # Forward pass
    y_pred = model.forward(X)
    y_true = gn.Tensor(y, requires_grad=False)

    # Calculate the loss
    loss = mse_loss(y_pred, y_true)

    # Backward pass
    loss.backward()

    # Update the parameters
    for w in model.weights:
        w.data -= learning_rate * w.grad
        w.grad = np.zeros_like(w.data)

    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.data:.4f}')

# Print the learned parameters
for i, w in enumerate(model.weights):
    print(f'Weight {i}: {w.data}')