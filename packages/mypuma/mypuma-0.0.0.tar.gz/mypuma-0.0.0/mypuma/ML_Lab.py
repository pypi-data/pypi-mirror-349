# ML_Lab
def get_ml_code():
    ml_code = """
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from xgboost import XGBClassifier
    from catboost import CatBoostClassifier
    from sklearn.decomposition import PCA, TruncatedSVD
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

    # 1. Load Dataset
    def load_dataset(file_path):
        #Load dataset from a file path.
        data = pd.read_csv(file_path)
        print(f"Dataset Shape: {data.shape}")
        return data

    # 2. Perform EDA
    def perform_eda(data):
        #Perform Exploratory Data Analysis on the dataset.
        print("\n--- Dataset Info ---")
        print(data.info())
        print("\n--- Dataset Description ---")
        print(data.describe())
        print("\n--- Missing Values ---")
        print(data.isnull().sum())

        # Visualizations
        print("\n--- Visualizing Dataset ---")
        plt.figure(figsize=(12, 6))
        sns.heatmap(data.corr(), annot=True, cmap="coolwarm")
        plt.title("Correlation Heatmap")
        plt.show()

        plt.figure(figsize=(8, 6))
        sns.countplot(data=data, x=data.columns[-1])
        plt.title("Target Variable Distribution")
        plt.show()

        for col in data.select_dtypes(include=["float64", "int64"]).columns[:-1]:
            plt.figure(figsize=(6, 4))
            sns.histplot(data[col], kde=True, bins=30)
            plt.title(f"Distribution of {col}")
            plt.show()

        for col in data.select_dtypes(include=["object"]).columns:
            plt.figure(figsize=(6, 4))
            sns.countplot(data=data, x=col)
            plt.title(f"Count of {col}")
            plt.show()

    # 3. Preprocessing and PCA/SVD
    def preprocess_and_reduce(data, target_col):
        #Preprocess the dataset and apply PCA and SVD.
        X = data.drop(columns=[target_col])
        y = data[target_col]
        
        # One-hot encode categorical variables if any
        X = pd.get_dummies(X, drop_first=True)
        
        # PCA
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X)
        print("\nPCA Explained Variance Ratio:", pca.explained_variance_ratio_)
        
        plt.figure(figsize=(8, 6))
        plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap="viridis")
        plt.title("PCA: First Two Components")
        plt.colorbar(label="Target")
        plt.show()

        # SVD
        svd = TruncatedSVD(n_components=2)
        X_svd = svd.fit_transform(X)
        print("\nSVD Explained Variance Ratio:", svd.explained_variance_ratio_)
        
        plt.figure(figsize=(8, 6))
        plt.scatter(X_svd[:, 0], X_svd[:, 1], c=y, cmap="plasma")
        plt.title("SVD: First Two Components")
        plt.colorbar(label="Target")
        plt.show()

        return X, y

    # 4. Train Models
    def train_models(X, y):
        #Train multiple models and evaluate them.
        models = {
            "Random Forest": RandomForestClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(),
            "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric="logloss"),
            "CatBoost": CatBoostClassifier(verbose=0)
        }
        
        results = {}
        for name, model in models.items():
            print(f"\n--- Training {name} ---")
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            results[name] = acc
            
            print(f"{name} Accuracy: {acc:.4f}")
            print("Classification Report:\n", classification_report(y_test, y_pred))
            
            # Confusion Matrix
            cm = confusion_matrix(y_test, y_pred)
            plt.figure(figsize=(6, 5))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
            plt.title(f"Confusion Matrix - {name}")
            plt.xlabel("Predicted")
            plt.ylabel("Actual")
            plt.show()
            
        return results

    # 5. Display Results
    def display_results(results):
        #Display and visualize results.
        print("\n--- Model Performance ---")
        for model, accuracy in results.items():
            print(f"{model}: {accuracy:.4f}")
        
        # Bar Plot for Model Performance
        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(results.keys()), y=list(results.values()), palette="viridis")
        plt.title("Model Performance")
        plt.xlabel("Models")
        plt.ylabel("Accuracy")
        plt.ylim(0, 1)
        plt.show()

    # Main Execution
    if __name__ == "__main__":
        # Path to your dataset
        file_path = "path_to_your_dataset.csv"  # Replace with your dataset file path
        
        # Load Dataset
        data = load_dataset(file_path)
        
        # Perform EDA
        perform_eda(data)
        
        # Preprocess and Apply PCA/SVD
        target_col = data.columns[-1]  # Assuming the last column is the target
        X, y = preprocess_and_reduce(data, target_col)
        
        # Train Models
        results = train_models(X, y)
        
        # Display Results
        display_results(results)
    """
    return ml_code