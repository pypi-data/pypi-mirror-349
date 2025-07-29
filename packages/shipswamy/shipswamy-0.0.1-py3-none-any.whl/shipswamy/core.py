def print_ml_programs():
    return """
Program 6a

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.datasets import fetch_california_housing

housing = fetch_california_housing()
X = housing.data[:700]
y = housing.target[:700]

# Convert to DataFrame for better readability
housing_df = pd.DataFrame(X, columns=housing.feature_names)
print(f"number of attributes = {len(housing_df.columns)}")
housing_df['Price'] = y

# Split the data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a linear regression model
model = LinearRegression()

# Train the model using the training data
model.fit(X_train, y_train)
print("Intercept - beta value:", model.intercept_)
print("Coefficients - beta value:", model.coef_)

# Predict on the test data
y_pred = model.predict(X_test)

# Plotting the true vs predicted values
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
plt.title("True vs Predicted Prices")
plt.xlabel("True Prices")
plt.ylabel("Predicted Prices")
plt.show()

# Calculate performance metrics
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Print the results
print(f"Mean Squared Error: {mse}")
print(f"Root Mean Squared Error: {rmse}")
print(f"R2 Score: {r2}")

Program 6b
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Read dataset
df = pd.read_csv("6b. auto-mpg.csv")
print("before data preprocessing - Number of rows:", df.shape[0])

# Convert "?" to NaN and drop missing values
df.replace("?", np.nan, inplace=True)
df.dropna(inplace=True)
print("after data preprocessing - Number of rows:", df.shape[0])

# Convert 'horsepower' column to numeric
df["horsepower"] = df["horsepower"].astype(float)

# Selecting Features and Target
X = df[["displacement", "horsepower", "weight", "acceleration"]]
y = df["mpg"]

# Splitting Data (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply Polynomial Transformation (Degree = 2)
poly = PolynomialFeatures(degree=2)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# Standardize the Data (Polynomial Features Can Grow Large)
scaler = StandardScaler()
X_train_poly = scaler.fit_transform(X_train_poly)
X_test_poly = scaler.transform(X_test_poly)

# Train the Linear Regression Model
model = LinearRegression()
model.fit(X_train_poly, y_train)

# Predict MPG Values
y_pred = model.predict(X_test_poly)

# Evaluate the Model using mse, rmse, r2 Score
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"Root Mean Squared Error: {rmse}")
print("Polynomial Regression R² Score:", r2)

# Scatter Plot: Actual vs. Predicted MPG
plt.scatter(y_test, y_pred, color='blue', label="Predicted vs Actual")
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', label="Perfect Fit")
plt.xlabel("Actual MPG")
plt.ylabel("Predicted MPG")
plt.legend()
plt.title("Polynomial Regression: Actual vs Predicted MPG")
plt.show()


Program 7
# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns

# Load Titanic dataset from seaborn
df = sns.load_dataset('titanic')

# Drop rows with missing target or key features
df = df.dropna(subset=['age', 'embarked', 'sex', 'fare', 'pclass', 'survived'])

# Encode categorical variables
df['sex'] = df['sex'].map({'male': 0, 'female': 1})
df['embarked'] = df['embarked'].map({'S': 0, 'C': 1, 'Q': 2})
# Select features and target
features = ['pclass', 'sex', 'age', 'fare', 'embarked']
X = df[features]
y = df['survived']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
random_state=42)

# Train a Decision Tree Classifier
clf = DecisionTreeClassifier(
criterion='entropy',
max_depth=3,
min_samples_split=5,
min_samples_leaf=5,
random_state=42
)
#clf = DecisionTreeClassifier(max_depth=3,random_state=42)
clf.fit(X_train, y_train)

# Visualize the decision tree
plt.figure(figsize=(30,40))
plot_tree(clf, feature_names=features, class_names=["Not Survived",
"Survived"], filled=True)
plt.title("Decision Tree using CART - gini/entropy index - Titanic")
plt.show()

# Predict on the test set
y_pred = clf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Print evaluation metrics
print("Model Evaluation Metrics:")
print(f"Accuracy : {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall : {recall:.2f}")
print(f"F1-Score : {f1:.2f}")
print("\nClassification Report:\n", classification_report(y_test, y_pred))

Program 8a
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

class GaussianNBCustom:
    def fit(self, X, y):
        self.classes = np.unique(y)
        self.mean = {}
        self.var = {}
        self.priors = {}

        for c in self.classes:
            X_c = X[y == c]
            self.mean[c] = np.mean(X_c, axis=0)
            self.var[c] = np.var(X_c, axis=0)
            self.priors[c] = X_c.shape[0] / X.shape[0]

    def predict(self, X):
        return [self._predict(x) for x in X]

    def _predict(self, x):
        posteriors = []
        for c in self.classes:
            prior = np.log(self.priors[c])
            class_conditional = np.sum(self._log_gaussian_density(c, x))
            posterior = prior + class_conditional
            posteriors.append(posterior)
        return self.classes[np.argmax(posteriors)]

    def _log_gaussian_density(self, class_idx, x):
        mean = self.mean[class_idx]
        var = self.var[class_idx]
        numerator = -0.5 * ((x - mean) ** 2) / (var + 1e-9)
        denominator = -0.5 * np.log(2 * np.pi * var + 1e-9)
        return numerator + denominator

# Load data
iris = load_iris()
X = iris.data
y = iris.target

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# Train custom model
model = GaussianNBCustom()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy and evaluation
accuracy = accuracy_score(y_test, y_pred)
print("Custom GaussianNB Accuracy: {:.2f}%".format(accuracy * 100))
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=iris.target_names))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

Program 8b
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load the dataset
iris = load_iris()
X = iris.data  # Features
y = iris.target  # Labels

# Split the dataset into training and test data (60% train, 40% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# Initialize and train the Naive Bayes classifier
model = GaussianNB()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Naive Bayes Classifier Accuracy: {:.2f}%".format(accuracy * 100))
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=iris.target_names))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

Program 9

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Load dataset from sklearn
data = load_breast_cancer()

# Get features and labels
X = data.data
y = data.target

# Show the shape of the data
print("Data Shape:", X.shape)
print("Target Shape:", y.shape)

# ====== Standardize the Data ======
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ====== Apply K-Means Clustering ======
kmeans = KMeans(n_clusters=2, random_state=42)  # 2 clusters for malignant and benign
kmeans.fit(X_scaled)

# Get cluster labels
y_kmeans = kmeans.labels_

# Plotting using the first two features
plt.figure(figsize=(8, 6))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=y_kmeans, cmap='viridis', marker='o')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
            c='blue', marker='x', s=100, label='Centroids')
plt.title('K-Means Clustering on Breast Cancer Dataset')
plt.xlabel('Feature 1 (scaled)')
plt.ylabel('Feature 2 (scaled)')
plt.legend()
plt.show()

# Evaluate clustering performance
print("Confusion Matrix:\n", confusion_matrix(y, y_kmeans))
print("\nClassification Report:\n", classification_report(y, y_kmeans))
"""

def print_genai_programs():
    return """8th
 pip install langchain langchain-community cohere google-auth google-auth-oauthlib google-auth-httplib2 googleapiclient


import os
from cohere import Client
from langchain.prompts import PromptTemplate

os.environ["COHERE_API_KEY"] = "RI01YSU6DETF3yEF0MTwwbOOjIsVWRedqTpN627v"
co = Client(os.getenv("COHERE_API_KEY"))
file_path = "/content/a.txt"

with open(file_path, "r") as file:
    text_document = file.read() 

template = '''
You are an expert summarizer. Summarize the following text in a concise manner:
Text: {text}
Summary:
'''
prompt_template = PromptTemplate(input_variables=["text"], template=template)
formatted_prompt = prompt_template.format(text=text_document)

response = co.generate(
model="command",
prompt=formatted_prompt,
max_tokens=100
)

print("Summary:")
print(response.generations[0].text.strip())




9
pip install langchain pydantic wikipedia
from typing import Optional
from pydantic import BaseModel, Field, ValidationError
import wikipedia

class InstitutionDetails(BaseModel):
    name: str = Field(description="Name of the institution")
    founder: Optional[str] = Field(default=None, description="Founder of the institution")
    founding_year: Optional[int] = Field(default=None, description="Year the institution was founded")
    branches: Optional[int] = Field(default=None, description="Number of branches of the institution")
    employees: Optional[int] = Field(default=None, description="Number of employees in the institution")
    summary: Optional[str] = Field(default=None, description="Summary of the institution")

def fetch(institution_name: str) -> InstitutionDetails:
    try:
        page = wikipedia.page(institution_name)
        summary = wikipedia.summary(institution_name, sentences=3)
        
        details = {
            "name": institution_name,
            "founder": None,        
            "founding_year": None, 
            "branches": None,     
            "employees": None, 
            "summary": summary,
        }
        
        return InstitutionDetails(**details)

    except wikipedia.exceptions.PageError:
        return InstitutionDetails(name=institution_name, summary="No Wikipedia page found.")
    except wikipedia.exceptions.DisambiguationError:
        return InstitutionDetails(name=institution_name, summary="Multiple matches found. Please specify.")
    except ValidationError as e:
        print(f"Validation Error: {e}")
        return InstitutionDetails(name=institution_name, summary="Error parsing details.")

if __name__ == "__main__":
    institution_name = input("Enter the institution name: ")
    details = fetch(institution_name)
    print(details)



7

from transformers import pipeline
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")
passage = (
    "Machine learning is a subset of artificial intelligence that focuses on training algorithms "
    "to make predictions. It is widely used in industries like healthcare, finance, and retail."
)
summary = summarizer(passage, max_length=30, min_length=10, do_sample=False)
print("Summary:")
print(summary[0]['summary_text'])



6


from transformers import pipeline
sentiment_pipeline = pipeline("sentiment-analysis")
sentences = [
    "I love this product! It works perfectly.",
    "This is the worst experience I've ever had.",
    "The weather is nice today.",
    "I feel so frustrated with this service."
]
results = sentiment_pipeline(sentences)
for sentence, result in zip(sentences, results):
    print(f"Sentence: {sentence}")
    print(f"Sentiment: {result['label']}, Confidence: {result['score']:.4f}")
    print()








10

First install ollama from the ollama website

Then run that exe file and install it

Then in command prompt run the following commands:

ollama serve

ollama pull deepseek-r1:1.5b

ollama run deepseek-r1:1.5b


Then keep this command prompt window open and execute the program



import pdfplumber
import ollama

# Load and extract text from PDF
with pdfplumber.open("R&D_visit_report.pdf") as pdf:
    full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)

# Chat loop
print("IPC Chatbot Ready. Ask anything about the Indian Penal Code.")
while True:
    query = input("\nYou: ")
    if query.lower() in ["exit", "quit"]:
        print("Chatbot: Goodbye!")
        break

    prompt = f'''You are a helpful assistant.
{full_text[:6000]}  # limit text to avoid going over context length

Question: {query}
Answer:'''

    response = ollama.chat(model="deepseek-r1:1.5b", messages=[{"role": "user", "content": prompt}])
    print(f"Chatbot: {response['message']['content']}")

"""