import sys
sys.path.insert(0, "./")  
from ai import AI  # Import the AI class
import numpy as np

# Create an instance of AI
ai_math = AI()

print("\n **AI Math Tests**")

# 🔥 MACHINE LEARNING MATH TESTS
y_true = [1, 0, 1, 1]
y_pred = [0.9, 0.1, 0.8, 0.6]

print("\n **Machine Learning Loss Functions**")
print("Mean Squared Error:", ai_math.mean_squared_error(y_true, y_pred))
print("Cross Entropy Loss:", ai_math.cross_entropy_loss(y_true, y_pred))

# 🔥 ACTIVATION FUNCTIONS TESTS
x_values = np.array([-2, 0, 2])

print("\n **Activation Functions**")
print("Sigmoid:", ai_math.sigmoid(x_values))
print("ReLU:", ai_math.relu(x_values))
print("Softmax:", ai_math.softmax(x_values))

# 🔥 NEURAL NETWORK BASICS TESTS
X = np.array([[0.5, 1.2], [1.1, -0.3]])
W = np.array([[0.4], [0.7]])
b = np.array([0.1])

print("\n **Neural Network Basics**")
print("Forward Propagation Output:", ai_math.forward_propagation(X, W, b))

W_updated, b_updated = ai_math.backward_propagation(X, np.array([[1], [0]]), W, b, lr=0.01)
print("Updated Weights After Backpropagation:", W_updated)
print("Updated Bias After Backpropagation:", b_updated)

# 🔥 LINEAR & POLYNOMIAL REGRESSION TESTS
X_train = np.array([1, 2, 3, 4, 5])
y_train = np.array([2, 4, 6, 8, 10])  # Perfectly linear

print("\n **Regression Models**")
print("Linear Regression Coefficients:", ai_math.linear_regression(X_train, y_train))

print("Polynomial Regression Coefficients (Degree=2):", ai_math.polynomial_regression(X_train, y_train, degree=2))

# 🔥 K-MEANS CLUSTERING TEST
X_clusters = np.array([[1, 2], [1, 3], [5, 8], [8, 8], [1, 2.5], [7, 8]])

print("\n **K-Means Clustering**")
centroids, labels = ai_math.k_means(X_clusters, k=2)
print("Cluster Centroids:\n", centroids)
print("Cluster Labels:", labels)
