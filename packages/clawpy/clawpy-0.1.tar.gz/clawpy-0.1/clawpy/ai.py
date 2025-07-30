# MIT License © 2025 Anish Chaudhuri
# See full license at the bottom of this file.

import numpy as np

class AI:
    def __init__(self):
        pass

    # 🔥 MACHINE LEARNING MATH
    def mean_squared_error(self, y_true, y_pred):
        """Calculates Mean Squared Error (MSE)."""
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        return np.mean((y_true - y_pred) ** 2)

    def cross_entropy_loss(self, y_true, y_pred):
        """Calculates Cross Entropy Loss (for classification)."""
        y_true, y_pred = np.array(y_true), np.array(y_pred)  # Convert lists to NumPy arrays
        y_pred = np.clip(y_pred, 1e-15, 1 - 1e-15)  # Avoid log(0)
        return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

    # 🔥 ACTIVATION FUNCTIONS
    def sigmoid(self, x):
        """Sigmoid activation function."""
        return 1 / (1 + np.exp(-x))

    def relu(self, x):
        """ReLU activation function."""
        return np.maximum(0, x)

    def softmax(self, x):
        """Softmax activation function (for multi-class classification)."""
        exp_x = np.exp(x - np.max(x))  # For numerical stability
        return exp_x / np.sum(exp_x)

    # 🔥 NEURAL NETWORK BASICS
    def forward_propagation(self, X, W, b):
        """Computes forward pass in a simple neural network (XW + b)."""
        return np.dot(X, W) + b

    def backward_propagation(self, X, y, W, b, lr=0.01):
        """Performs basic backpropagation for a single-layer neural network."""
        m = X.shape[0]
        A = self.sigmoid(self.forward_propagation(X, W, b))
        dW = (1 / m) * np.dot(X.T, (A - y))
        db = (1 / m) * np.sum(A - y)
        W -= lr * dW
        b -= lr * db
        return W, b

    # 🔥 LINEAR REGRESSION
    def linear_regression(self, X, y):
        """Fits a simple linear regression model using least squares."""
        X = np.c_[np.ones(X.shape[0]), X]  # Add bias term
        return np.linalg.lstsq(X, y, rcond=None)[0]

    def polynomial_regression(self, X, y, degree=2):
        """Fits a polynomial regression model."""
        X_poly = np.vander(X, degree + 1)
        return np.linalg.lstsq(X_poly, y, rcond=None)[0]

    # 🔥 K-MEANS CLUSTERING (BASIC)
    def k_means(self, X, k, max_iters=100):
        """Performs K-Means clustering."""
        centroids = X[np.random.choice(X.shape[0], k, replace=False)]
        for _ in range(max_iters):
            labels = np.argmin(np.linalg.norm(X[:, None] - centroids, axis=2), axis=1)
            new_centroids = np.array([X[labels == j].mean(axis=0) for j in range(k)])
            if np.all(centroids == new_centroids):
                break
            centroids = new_centroids
        return centroids, labels

# MIT License
#
# Copyright (c) 2025 Anish Chaudhuri
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
