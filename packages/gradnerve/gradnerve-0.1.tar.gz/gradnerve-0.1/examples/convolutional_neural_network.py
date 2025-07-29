import sys
sys.path.append("/Users/siddharthshah/Documents/MatrixLand/Gradnerve-p")
import numpy as np
from gradnerve import tensor as gn

# Generate some dummy image data (batch_size, height, width, channels)
batch_size = 4
height = 28
width = 28
channels = 1
X = np.random.rand(batch_size, height, width, channels)
y = np.random.randint(0, 10, batch_size)

# Define a very simple CNN model
class SimpleCNN:
    def __init__(self):
        # Convolutional layer (1 filter, 3x3 kernel)
        self.conv_weight = gn.Tensor(np.random.randn(3, 3, channels, 1), requires_grad=True)
        # Max pooling layer (2x2 pool size, stride=2)
        self.pool_size = 2
        self.pool_stride = 2
        # Fully connected layer
        pooled_height = height // self.pool_stride
        pooled_width = width // self.pool_stride
        self.fc_weight = gn.Tensor(np.random.randn(pooled_height * pooled_width * 1, 10), requires_grad=True)
        self.fc_bias = gn.Tensor(np.zeros(10), requires_grad=True)

    def forward(self, X):
        # Convolution
        # This is a simplified convolution for demonstration.  A proper implementation would be more complex.
        conv_out = gn.Tensor(np.zeros((X.shape[0], X.shape[1] - 2, X.shape[2] - 2, 1))) # Simplified shape calculation
        for b in range(X.shape[0]):
            for i in range(X.shape[1] - 2):
                for j in range(X.shape[2] - 2):
                    conv_out.data[b, i, j, 0] = np.sum(X[b, i:i+3, j:j+3, :] * self.conv_weight.data)

        # Max Pooling
        pooled_height = conv_out.data.shape[1] // self.pool_stride
        pooled_width = conv_out.data.shape[2] // self.pool_stride
        pooled_out = gn.Tensor(np.zeros((X.shape[0], pooled_height, pooled_width, 1)))
        for b in range(conv_out.shape[0]):
            for i in range(pooled_height):
                for j in range(pooled_width):
                    pooled_out.data[b, i, j, 0] = np.max(conv_out.data[b, i*self.pool_stride:(i+1)*self.pool_stride, j*self.pool_stride:(j+1)*self.pool_stride, 0])

        # Flatten
        flattened = pooled_out.reshape((X.shape[0], -1))

        # Fully connected layer
        logits = flattened @ self.fc_weight + self.fc_bias
        return logits

# Initialize the model
model = SimpleCNN()

# Loss function (Cross-entropy)
def cross_entropy_loss(logits, labels):
    # This is a simplified cross-entropy for demonstration.  A proper implementation would be more complex.
    one_hot = np.zeros_like(logits.data)
    one_hot[np.arange(len(labels)), labels] = 1
    probabilities = gn.Tensor(np.exp(logits.data) / np.sum(np.exp(logits.data), axis=1, keepdims=True))
    loss = -np.sum(one_hot * np.log(probabilities.data)) / len(labels)
    return gn.Tensor(np.array([loss]))

# Training loop (very simplified)
learning_rate = 0.001
num_epochs = 10

for epoch in range(num_epochs):
    logits = model.forward(X)
    loss = cross_entropy_loss(logits, y)

    loss.backward()

    model.conv_weight.data -= learning_rate * model.conv_weight.grad
    model.fc_weight.data -= learning_rate * model.fc_weight.grad
    model.fc_bias.data -= learning_rate * model.fc_bias.grad

    model.conv_weight.grad = np.zeros_like(model.conv_weight.data)
    model.fc_weight.grad = np.zeros_like(model.fc_weight.data)
    model.fc_bias.grad = np.zeros_like(model.fc_bias.data)

    print(f"Epoch {epoch+1}, Loss: {loss.data[0]:.4f}")
