import numpy as np
from gradnerve import tensor as gn
from gradnerve import ops

# Define a simple sequence
text = "hello world"
chars = list(set(text))
char_to_index = {ch: i for i, ch in enumerate(chars)}
index_to_char = {i: ch for i, ch in enumerate(chars)}

# Create training data
seq_length = 4
X = []
y = []
for i in range(len(text) - seq_length):
    X.append([char_to_index[ch] for ch in text[i:i+seq_length]])
    y.append(char_to_index[text[i+seq_length]])

X = np.array(X)
y = np.array(y)

# RNN Model
class SimpleRNN:
    def __init__(self, input_size, hidden_size, output_size):
        self.hidden_size = hidden_size
        self.weight_ih = gn.Tensor(np.random.randn(input_size, hidden_size) * 0.01, requires_grad=True) # Input to hidden
        self.weight_hh = gn.Tensor(np.random.randn(hidden_size, hidden_size) * 0.01, requires_grad=True) # Hidden to hidden
        self.bias_h = gn.Tensor(np.zeros((1, hidden_size)), requires_grad=True)
        self.weight_ho = gn.Tensor(np.random.randn(hidden_size, output_size) * 0.01, requires_grad=True) # Hidden to output
        self.bias_o = gn.Tensor(np.zeros((1, output_size)), requires_grad=True)

    def forward(self, input_seq):
        input_seq = gn.Tensor(input_seq)
        batch_size = input_seq.shape[0]
        hidden = gn.Tensor(np.zeros((batch_size, self.hidden_size)), requires_grad=False) # Initialize hidden state

        for t in range(seq_length):
            input_t = input_seq[:, t]
            # One-hot encode input_t
            input_one_hot = np.zeros((batch_size, input_size))
            input_one_hot[np.arange(batch_size), input_t.data] = 1
            input_one_hot = gn.Tensor(input_one_hot, requires_grad=False)

            hidden = gn.Tensor(np.tanh((input_one_hot @ self.weight_ih + hidden @ self.weight_hh + self.bias_h))) 

        output = hidden @ self.weight_ho + self.bias_o
        return output

# Initialize model
input_size = len(chars)
hidden_size = 8
output_size = len(chars)
model = SimpleRNN(input_size, hidden_size, output_size)

# Loss function (Cross-entropy)
def cross_entropy_loss(logits, labels):
    # Convert labels to one-hot encoding
    one_hot = np.zeros_like(logits.data)
    one_hot[np.arange(len(labels)), labels] = 1

    # Calculate probabilities using softmax
    probabilities = gn.Tensor(ops.exp(logits.data) / np.sum(ops.exp(logits.data), axis=1, keepdims=True))

    # Calculate cross-entropy loss
    loss = -np.sum(one_hot * ops.log(probabilities.data)) / len(labels)
    return gn.Tensor(np.array([loss]))

# Training loop
learning_rate = 0.01
num_epochs = 500

for epoch in range(num_epochs):
    # Prepare input data
    input_seq = gn.Tensor(X, requires_grad=False)

    # Forward pass
    output = model.forward(input_seq)

    # Calculate loss
    loss = cross_entropy_loss(output, y)

    # Backward pass
    loss.backward()

    # Update parameters
    model.weight_ih.data -= learning_rate * model.weight_ih.grad
    model.weight_hh.data -= learning_rate * model.weight_hh.grad
    model.bias_h.data -= learning_rate * model.bias_h.grad
    model.weight_ho.data -= learning_rate * model.weight_ho.grad
    model.bias_o.data -= learning_rate * model.bias_o.grad

    # Zero gradients
    model.weight_ih.grad = np.zeros_like(model.weight_ih.data)
    model.weight_hh.grad = np.zeros_like(model.weight_hh.data)
    model.bias_h.grad = np.zeros_like(model.bias_h.data)
    model.weight_ho.grad = np.zeros_like(model.weight_ho.data)
    model.bias_o.grad = np.zeros_like(model.bias_o.data)

    if (epoch + 1) % 100 == 0:
        print(f"Epoch {epoch + 1}, Loss: {loss.data[0]:.4f}")

# Example of generating the next character
input_text = "worl"
input_indices = [char_to_index[ch] for ch in input_text]
input_seq = gn.Tensor(np.array([input_indices]), requires_grad=False)
output = model.forward(input_seq)
predicted_index = np.argmax(output.data)
predicted_char = index_to_char[predicted_index]
print(f"Input text: {input_text}")
print(f"Predicted next character: {predicted_char}")