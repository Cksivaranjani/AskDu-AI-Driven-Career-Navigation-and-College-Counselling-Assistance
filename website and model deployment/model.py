# import pandas as pd
# from sklearn.preprocessing import LabelEncoder
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score
# import pickle

# df = pd.read_excel("C:/Users/sivar/OneDrive/Desktop/Mini Project Chatbot/model_deployment/dataset_chatbot.xlsx")

# df=df.drop(columns=['ALLOTTED\nCATEGORY'])
# df=df.drop(columns=['RANK'])

# df=df.dropna()
# df['COMMUNI\nTY'].unique()

# word_to_delete = 'COMMUNI\nTY'
# df['COMMUNI\nTY'] = df['COMMUNI\nTY'].str.replace(word_to_delete, '')
# df['COMMUNI\nTY'].unique()

# df.replace('', pd.NA, inplace=True)
# df['COMMUNI\nTY'].unique()

# df=df.dropna()
# df['COMMUNI\nTY'].unique()

# print(df.head())

# le = LabelEncoder()
# df['COMMUNI\nTY'] = le.fit_transform(df['COMMUNI\nTY'])
# community_encoder = le

# X = df[['AGGR\nMARK', 'COMMUNI\nTY']]
# y = df[['COLLEGE\nCODE', 'BRANCH\nCODE']]

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# rf_classifier.fit(X_train, y_train)

# y_pred = rf_classifier.predict(X_test)

# # Compute accuracy for 'COLLEGE CODE'
# accuracy_college_code = accuracy_score(y_test['COLLEGE\nCODE'], y_pred[:, 0])

# # Compute accuracy for 'BRANCH CODE'
# accuracy_branch_code = accuracy_score(y_test['BRANCH\nCODE'], y_pred[:, 1])

# print("Accuracy for College Code:", accuracy_college_code)
# print("Accuracy for Branch Code:", accuracy_branch_code)

# # Example of printing the input features (X) and predicted output (y_pred) for the first data point in the test set
# # Assuming X_test contains the input features and y_pred contains the predicted output for the test data

# # Selecting the first data point from X_test and the corresponding predicted output from y_pred
# single_data_point_X = X_test.iloc[0]
# single_data_point_y_pred = y_pred[0]

# print("Input Features (X):")
# print(single_data_point_X)

# print("\nPredicted Output (y_pred):")
# print(single_data_point_y_pred)

# pickle.dump(rf_classifier, open("model.pkl","wb"))


import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# Load the dataset
df = pd.read_excel("C:/Users/sivar/OneDrive/Desktop/Mini Project Chatbot/model_deployment/dataset_chatbot.xlsx")

# Drop unnecessary columns and rows with missing values
df = df.drop(columns=['ALLOTTED CATEGORY', 'RANK']).dropna()

# Check if the 'COMMUNITY' column exists in the DataFrame
if 'COMMUNITY' in df.columns:
    # Preprocess 'COMMUNITY' column
    df['COMMUNITY'] = df['COMMUNITY'].str.replace('COMMUNITY', '').str.strip()
else:
    print("No 'COMMUNITY' column found in the DataFrame.")

# Encode categorical variables
le = LabelEncoder()
df['COMMUNITY'] = le.fit_transform(df['COMMUNITY'])
community_encoder = le

# Define features (X) and labels (y)
X = df[['AGGR MARK', 'COMMUNITY']]
y = df[['COLLEGE CODE', 'BRANCH CODE']]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the random forest classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = rf_classifier.predict(X_test)

# Compute accuracy for 'COLLEGE CODE' and 'BRANCH CODE'
accuracy_college_code = accuracy_score(y_test['COLLEGE CODE'], y_pred[:, 0])
accuracy_branch_code = accuracy_score(y_test['BRANCH CODE'], y_pred[:, 1])

print("Accuracy for College Code:", accuracy_college_code)
print("Accuracy for Branch Code:", accuracy_branch_code)

# Example of printing the input features (X) and predicted output (y_pred) for the first data point in the test set
single_data_point_X = X_test.iloc[0]
single_data_point_y_pred = y_pred[0]

print("\nInput Features (X):")
print(single_data_point_X)

print("\nPredicted Output (y_pred):")
print(single_data_point_y_pred)

# Save the trained model to a file using pickle
with open("model.pkl", "wb") as model_file:
    pickle.dump(rf_classifier, model_file)
