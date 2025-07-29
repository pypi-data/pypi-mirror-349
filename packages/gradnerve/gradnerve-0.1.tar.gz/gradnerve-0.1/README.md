# GradNerve: A Minimalist Autograd Engine for Deep Learning Education

## Introduction

Automatic differentiation is a fundamental technique in deep learning, enabling the efficient computation of gradients for optimizing model parameters. GradNerve is a lightweight, NumPy-based autograd engine designed for educational purposes. It provides a clear and concise implementation of reverse-mode automatic differentiation, making it suitable for learning and experimentation.

## Key Features

- **Tensor Class:** The core `Tensor` class is the building block of GradNerve. It stores data, gradients, and tracks the operations performed on it.
    - `.data`: A NumPy array storing the tensor's values.
    - `.grad`: A NumPy array storing the accumulated gradient.
    - `.requires_grad`: A boolean flag indicating whether gradients should be tracked for this tensor.
    - `._prev`: A set containing the parent `Tensor` objects in the computation graph.
    - `._backward`: A function that computes the local gradient and propagates it to the parents.
- **Automatic Differentiation:** GradNerve implements reverse-mode automatic differentiation, a technique for efficiently computing gradients of a scalar function with respect to its inputs.
- **Computation Graph:** The computation graph is a directed acyclic graph that represents the sequence of operations performed on the tensors. GradNerve builds this graph dynamically as operations are performed.
- **Operator Overloading:** GradNerve overloads common operators (e.g., `__add__`, `__mul__`, `__matmul__`) to automatically build the computation graph.

## Mathematical Foundations

GradNerve implements reverse-mode automatic differentiation (also known as backpropagation), which is a powerful technique for computing gradients of a scalar function with respect to its inputs. This is essential for training deep learning models using gradient-based optimization algorithms.

Let's consider a simple computation graph where a scalar output $L$ (the loss) is a function of several intermediate variables, which are in turn functions of the input variables. For example:

$L = f(y_1, y_2)$
$y_1 = g_1(x_1, x_2)$
$y_2 = g_2(x_2, x_3)$

where $L$ is the loss, $y_i$ are intermediate variables, and $x_i$ are the input variables (parameters of the model).

The goal is to compute the gradients of $L$ with respect to each $x_i$, i.e., $\frac{\partial L}{\partial x_i}$.

Reverse-mode automatic differentiation computes these gradients in two phases:

1.  **Forward Pass:** The input values $x_i$ are fed forward through the computation graph to compute the values of the intermediate variables $y_i$ and the final loss $L$.
2.  **Backward Pass:** Starting from the output $L$, the gradients are computed recursively using the chain rule. The chain rule states that if $z = f(y)$ and $y = g(x)$, then:

$$\frac{\partial z}{\partial x} = \frac{\partial z}{\partial y} \cdot \frac{\partial y}{\partial x}$$

In our example, the backward pass would proceed as follows:

*   Compute $\frac{\partial L}{\partial y_1}$ and $\frac{\partial L}{\partial y_2}$ (the local gradients at the output).
*   Compute $\frac{\partial L}{\partial x_1} = \frac{\partial L}{\partial y_1} \cdot \frac{\partial y_1}{\partial x_1}$ and $\frac{\partial L}{\partial x_2} = \frac{\partial L}{\partial y_1} \cdot \frac{\partial y_1}{\partial x_2} + \frac{\partial L}{\partial y_2} \cdot \frac{\partial y_2}{\partial x_2}$.
*   Compute $\frac{\partial L}{\partial x_3} = \frac{\partial L}{\partial y_2} \cdot \frac{\partial y_2}{\partial x_3}$.

Each `_backward` function in GradNerve implements the computation of the local gradient (e.g., $\frac{\partial y}{\partial x}$) and multiplies it by the incoming gradient (e.g., $\frac{\partial L}{\partial y}$) to compute the gradient with respect to its inputs.

## Code Examples

```python
import gradnerve.tensor as gn
import numpy as np

# Create two tensors with requires_grad=True
x = gn.Tensor([2.0], requires_grad=True)
y = gn.Tensor([3.0], requires_grad=True)

# Perform an operation
z = x * y

# Compute the gradients
z.backward()

# Print the gradients
print(x.grad)
print(y.grad)
```

### Linear Regression Example

```python
import gradnerve.tensor as gn
import numpy as np

# Generate some sample data
X = np.array([[1, 2], [2, 3], [3, 4]], dtype=np.float64)
y = np.array([6, 8, 10], dtype=np.float64)

# Define the model
class LinearRegression:
    def __init__(self, n_features):
        self.weights = gn.Tensor(np.zeros((n_features, 1), dtype=np.float64), requires_grad=True)
        self.bias = gn.Tensor(np.zeros(1, dtype=np.float64), requires_grad=True)

    def forward(self, X):
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
    X_tensor = gn.Tensor(X, requires_grad=False)
    y_pred = model.forward(X_tensor)
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
```

## Design Choices

GradNerve prioritizes simplicity and clarity over performance and features. This design choice was made to create an engine that is easy to understand, modify, and extend for educational purposes. While this approach leads to a more accessible codebase, it also results in certain trade-offs:

*   **Performance:** GradNerve's performance is not optimized for large-scale computations. Operations are performed using NumPy, which is efficient but not as highly optimized as lower-level libraries or hardware-specific implementations.
*   **Features:** GradNerve implements a limited set of features compared to more comprehensive autograd engines like PyTorch or TensorFlow. This allows for a smaller and more focused codebase, but it also means that some advanced techniques may not be directly supported.
*   **Memory Usage:** The computation graph in GradNerve is stored explicitly, which can lead to higher memory usage compared to techniques like tape-based autograd.

These trade-offs were carefully considered to create an engine that is well-suited for its primary goal: to provide a clear and concise implementation of automatic differentiation for educational purposes.

## Limitations

GradNerve is a work in progress, and the current implementation has several limitations:

*   **Limited Operator Support:** Only a basic set of operators is currently supported. More advanced operations, such as convolutions and recurrent layers, are not yet implemented.
*   **No GPU Support:** GradNerve relies on NumPy, which primarily uses the CPU. GPU acceleration is not currently supported.
*   **Lack of Optimization:** The implementation is not optimized for performance. Operations are performed using NumPy, which is not as efficient as lower-level libraries or hardware-specific implementations.
*   **No Automatic Memory Management:** The user is responsible for managing memory and avoiding memory leaks.
*   **Limited Testing:** The test suite is not yet comprehensive, and there may be undiscovered bugs.

These limitations are known and may be addressed in future versions of GradNerve.

## Comparison to Other Autograd Engines

GradNerve is a minimalist autograd engine, while libraries like PyTorch and TensorFlow offer a wide range of features and optimizations. GradNerve is intended for educational purposes, while PyTorch and TensorFlow are designed for production use.

## Installation Instructions

```bash
pip install numpy
```

## Usage Instructions

```python
import gradnerve.tensor as gn
import numpy as np

# Create a tensor
x = gn.Tensor([1.0, 2.0, 3.0])

# Perform an operation
y = x + 1

# Print the result
print(y.data)
```

## Contribution Guidelines

Contributions to GradNerve are welcome! Please submit bug reports, feature requests, and pull requests through the GitHub repository.

## License

MIT License

## References

- [Automatic Differentiation in Machine Learning: a Survey](https://arxiv.org/abs/1502.05767)
