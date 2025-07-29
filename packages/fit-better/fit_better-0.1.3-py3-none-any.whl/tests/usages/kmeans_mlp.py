import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.cluster import KMeans
from datetime import datetime
import os
from collections import defaultdict
import joblib
import argparse
import warnings
from joblib import Parallel, delayed

# Try to import tqdm for progress bars, but continue if not available
try:
    from tqdm import tqdm

    tqdm_available = True
except ImportError:
    tqdm_available = False
    print(
        "Warning: tqdm not available. Install with 'pip install tqdm' for progress bars."
    )

# Suppress sklearn feature name warnings
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message="X does not have valid feature names, but .* was fitted with feature names",
)


def load_and_match_data(features_file, target_file):
    """
    Load features and target from separate CSV files
    and match by identifier in first column.
    Only keeps rows that exist in both files.

    Parameters:
    features_file (str): Path to CSV file containing features
    target_file (str): Path to CSV file containing target values

    Returns:
    tuple: (X, y, ids, target_col_name, original_features_df)
    """
    # Load data files
    features_df = pd.read_csv(features_file)
    target_df = pd.read_csv(target_file)

    # Store original features dataframe for later use
    original_features_df = features_df.copy()

    # Get column names for IDs
    id_col = features_df.columns[0]  # First column is identifier
    target_id_col = target_df.columns[0]  # First column in target file

    # Print information about the original datasets
    print(
        f"Features dataset: {features_df.shape[0]} rows, {features_df.shape[1]} columns"
    )
    print(f"Target dataset: {target_df.shape[0]} rows, {target_df.shape[1]} columns")

    # Ensure the ID columns have the same name for merging
    if target_id_col != id_col:
        print(f"Renaming ID column in target from '{target_id_col}' to '{id_col}'")
        target_df = target_df.rename(columns={target_id_col: id_col})

    # Merge dataframes on identifier column (inner join keeps only matching rows)
    merged_df = pd.merge(features_df, target_df, on=id_col, how="inner")

    # Calculate and print information about matching
    only_in_features = set(features_df[id_col]) - set(merged_df[id_col])
    only_in_target = set(target_df[id_col]) - set(merged_df[id_col])

    print(f"\nMatching complete:")
    print(f"  - IDs only in features file: {len(only_in_features)}")
    print(f"  - IDs only in target file: {len(only_in_target)}")
    print(f"  - Total matched rows: {merged_df.shape[0]}")

    # Check if there are any matched rows
    if merged_df.shape[0] == 0:
        raise ValueError("No matching rows found between feature and target files!")

    # Extract feature columns (all columns from features_df except the ID column)
    feature_columns = [col for col in features_df.columns if col != id_col]
    X = merged_df[feature_columns]

    # Extract target column(s)
    # Assuming the first column after ID in target_df is the target
    target_col_name = target_df.columns[1]
    y = merged_df[target_col_name]

    # Save the IDs of matched rows
    ids = merged_df[id_col]

    return X, y, ids, target_col_name, original_features_df


def load_comparison_data(additional_file, ids, id_col):
    """
    Load comparison data and match against existing IDs.

    Parameters:
    additional_file (str): Path to CSV file containing comparison values
    ids (Series): IDs from matched data
    id_col (str): Name of the ID column

    Returns:
    tuple: (comparison_values, comparison_col_name)
    """
    # Load additional data
    additional_df = pd.read_csv(additional_file)
    print(
        f"Additional dataset: {additional_df.shape[0]} rows, {additional_df.shape[1]} columns"
    )

    # Ensure the ID column has the same name
    additional_id_col = additional_df.columns[0]
    if additional_id_col != id_col:
        print(
            f"Renaming ID column in additional file from '{additional_id_col}' to '{id_col}'"
        )
        additional_df = additional_df.rename(columns={additional_id_col: id_col})

    # Create a dataframe with the matched IDs
    ids_df = pd.DataFrame({id_col: ids})

    # Merge with additional data
    merged_df = pd.merge(ids_df, additional_df, on=id_col, how="left")

    # Calculate matching statistics
    matched_ids = set(ids) & set(additional_df[id_col])
    only_in_additional = set(additional_df[id_col]) - set(ids)
    missing_in_additional = set(ids) - set(additional_df[id_col])

    print(f"\nAdditional data matching:")
    print(f"  - IDs matched with additional file: {len(matched_ids)}")
    print(f"  - IDs only in additional file: {len(only_in_additional)}")
    print(f"  - IDs missing from additional file: {len(missing_in_additional)}")

    # Extract comparison column (assuming the first column after ID)
    comparison_col_name = additional_df.columns[1]
    comparison_values = merged_df[comparison_col_name]

    # If additional_df has more than 2 columns, print a warning
    if len(additional_df.columns) > 2:
        print(
            f"Warning: Additional file has multiple columns. Using '{comparison_col_name}' for comparison."
        )

    return comparison_values, comparison_col_name


def perform_kmeans_clustering(X, n_clusters=3, random_state=42):
    """
    Perform k-means++ clustering on the feature data.

    Parameters:
    X (DataFrame): Features
    n_clusters (int): Number of clusters
    random_state (int): Random seed for reproducibility

    Returns:
    tuple: (kmeans_model, cluster_labels, scaled_data, scaler)
    """
    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Perform k-means++ clustering
    kmeans = KMeans(
        n_clusters=n_clusters,
        init="k-means++",  # Use k-means++ initialization
        n_init=10,
        max_iter=300,
        random_state=random_state,
    )

    # Fit the model and get cluster labels
    cluster_labels = kmeans.fit_predict(X_scaled)

    # Print cluster sizes
    unique_labels, counts = np.unique(cluster_labels, return_counts=True)
    print("\nCluster sizes:")
    for label, count in zip(unique_labels, counts):
        print(
            f"  - Cluster {label}: {count} samples ({count/len(cluster_labels)*100:.1f}%)"
        )

    return kmeans, cluster_labels, X_scaled, scaler


def train_mlp_regressor(X, y, test_size=0.2, random_state=42):
    """
    Train MLPRegressor model on the given data.

    Parameters:
    X (DataFrame or array): Features
    y (Series or array): Target values
    test_size (float): Proportion of data to use for testing
    random_state (int): Random seed for reproducibility

    Returns:
    tuple: (model, X_train, X_test, y_train, y_test, scaler, train_indices, test_indices)
    """
    # If X is already scaled, don't scale again
    is_already_scaled = isinstance(X, np.ndarray)

    # For very small datasets, use the entire dataset for training
    if len(X) < 10:
        test_size = 0.0

    # Split data into training and testing sets
    if test_size > 0:
        X_train, X_test, y_train, y_test, train_indices, test_indices = (
            train_test_split(
                X, y, np.arange(len(X)), test_size=test_size, random_state=random_state
            )
        )
    else:
        # Use all data for training
        X_train, y_train = X, y
        X_test, y_test = np.empty((0, X.shape[1])), np.empty(0)
        train_indices, test_indices = np.arange(len(X)), np.empty(0, dtype=int)

    if is_already_scaled:
        X_train_scaled = X_train
        X_test_scaled = X_test if test_size > 0 else np.empty((0, X_train.shape[1]))
        scaler = None
    else:
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = (
            scaler.transform(X_test)
            if test_size > 0
            else np.empty((0, X_train.shape[1]))
        )

    # Create and train MLPRegressor with smaller hidden layers for small datasets
    if len(X) < 10:
        # For very small datasets, use simpler model
        mlp = MLPRegressor(
            hidden_layer_sizes=(3,),  # Single small hidden layer
            activation="relu",
            solver="adam",
            alpha=0.01,  # Increase regularization
            batch_size="auto",
            learning_rate="adaptive",
            max_iter=2000,
            random_state=random_state,
            verbose=False,
        )
    else:
        # For larger datasets, use default complexity
        mlp = MLPRegressor(
            hidden_layer_sizes=(100, 50),  # Two hidden layers with 100 and 50 neurons
            activation="relu",
            solver="adam",
            alpha=0.0001,
            batch_size="auto",
            learning_rate="adaptive",
            max_iter=1000,
            random_state=random_state,
            verbose=False,
        )

    # Train the model
    mlp.fit(X_train_scaled, y_train)

    return (
        mlp,
        X_train_scaled,
        X_test_scaled,
        y_train,
        y_test,
        scaler,
        train_indices,
        test_indices,
    )


def evaluate_model(model, X_test, y_test, prefix=""):
    """
    Evaluate model performance.

    Parameters:
    model: Trained model
    X_test: Test features
    y_test: True target values
    prefix: Optional prefix for printing (e.g., cluster name)

    Returns:
    dict: Performance metrics and predictions
    """
    if len(y_test) == 0:
        print(f"{prefix}No test samples available for evaluation")
        return {"mse": np.nan, "rmse": np.nan, "r2": np.nan, "y_test": [], "y_pred": []}

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred) if len(np.unique(y_test)) > 1 else np.nan

    # Print metrics
    print(f"{prefix}Model Performance:")
    print(f"{prefix}  Mean Squared Error: {mse:.4f}")
    print(f"{prefix}  Root Mean Squared Error: {rmse:.4f}")
    print(f"{prefix}  R² Score: {r2:.4f}")

    return {"mse": mse, "rmse": rmse, "r2": r2, "y_test": y_test, "y_pred": y_pred}


def predict_on_original_features(
    original_features_df, kmeans, kmeans_scaler, cluster_models, id_col, target_col_name
):
    """
    Make predictions on the original feature dataset using the trained models.

    Parameters:
    original_features_df (DataFrame): Original features dataframe
    kmeans (KMeans): Trained KMeans model
    kmeans_scaler (StandardScaler): Scaler used for clustering
    cluster_models (dict): Dictionary of trained MLPRegressor models for each cluster
    id_col (str): Name of the ID column
    target_col_name (str): Name of the target column to predict

    Returns:
    DataFrame: Original features with predictions added
    """
    print("\nMaking predictions on original feature dataset...")

    # Create a copy of the original features DataFrame
    result_df = original_features_df.copy()

    # Extract features (all columns except ID)
    feature_cols = [col for col in original_features_df.columns if col != id_col]
    X_orig = original_features_df[feature_cols].values

    # Scale the features using the same scaler used for clustering
    X_orig_scaled = kmeans_scaler.transform(X_orig)

    # Predict clusters for each data point
    clusters = kmeans.predict(X_orig_scaled)

    # Add cluster assignments to the result DataFrame
    result_df["Cluster"] = clusters

    # Initialize prediction column
    result_df[f"Predicted_{target_col_name}"] = np.nan

    # Make predictions for each cluster
    for cluster_idx, model in cluster_models.items():
        # Select data points in this cluster
        cluster_mask = clusters == cluster_idx
        if sum(cluster_mask) == 0:
            continue

        # Get features for this cluster
        X_cluster = X_orig_scaled[cluster_mask]

        # Make predictions
        y_pred_cluster = model.predict(X_cluster)

        # Store predictions in result DataFrame
        result_df.loc[cluster_mask, f"Predicted_{target_col_name}"] = y_pred_cluster

    # Count predictions made
    n_predicted = result_df[f"Predicted_{target_col_name}"].notna().sum()
    print(f"Made predictions for {n_predicted} out of {len(result_df)} samples")

    # Check for any missing predictions (could happen if a cluster had no model)
    n_missing = result_df[f"Predicted_{target_col_name}"].isna().sum()
    if n_missing > 0:
        print(
            f"Warning: {n_missing} samples have no predictions (possibly in clusters with too few training samples)"
        )

    return result_df


def plot_cluster_predictions(cluster_results, output_dir="cluster_plots"):
    """
    Create scatter plots of actual vs predicted values for each cluster.

    Parameters:
    cluster_results (dict): Dictionary of cluster results
    output_dir (str): Directory to save plots
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create plot for each cluster
    for cluster_idx, results in cluster_results.items():
        if len(results["test"]["y_test"]) == 0:
            continue

        plt.figure(figsize=(10, 6))
        plt.scatter(results["test"]["y_test"], results["test"]["y_pred"], alpha=0.7)

        # Plot perfect prediction line
        min_val = min(min(results["test"]["y_test"]), min(results["test"]["y_pred"]))
        max_val = max(max(results["test"]["y_test"]), max(results["test"]["y_pred"]))
        plt.plot([min_val, max_val], [min_val, max_val], "r--")

        plt.xlabel("Actual Values")
        plt.ylabel("Predicted Values")
        plt.title(f"Cluster {cluster_idx}: Model Predictions vs Actual")
        plt.grid(True)

        # Add R² to the plot
        r2 = results["test"]["r2"]
        plt.text(
            0.05,
            0.95,
            f"R² = {r2:.4f}",
            transform=plt.gca().transAxes,
            fontsize=12,
            verticalalignment="top",
        )

        plt.tight_layout()
        plt.savefig(f"{output_dir}/cluster_{cluster_idx}_predictions.png")
        plt.close()

    # Create overall plot combining all clusters
    all_y_test = []
    all_y_pred = []
    colors = ["b", "g", "r", "c", "m", "y", "k"]

    plt.figure(figsize=(12, 8))

    for i, (cluster_idx, results) in enumerate(cluster_results.items()):
        if len(results["test"]["y_test"]) == 0:
            continue

        color_idx = i % len(colors)
        plt.scatter(
            results["test"]["y_test"],
            results["test"]["y_pred"],
            alpha=0.7,
            color=colors[color_idx],
            label=f"Cluster {cluster_idx}",
        )

        all_y_test.extend(results["test"]["y_test"])
        all_y_pred.extend(results["test"]["y_pred"])

    # Plot perfect prediction line
    if all_y_test and all_y_pred:
        min_val = min(min(all_y_test), min(all_y_pred))
        max_val = max(max(all_y_test), max(all_y_pred))
        plt.plot([min_val, max_val], [min_val, max_val], "r--")

        # Calculate overall R²
        overall_r2 = r2_score(all_y_test, all_y_pred)
        plt.text(
            0.05,
            0.95,
            f"Overall R² = {overall_r2:.4f}",
            transform=plt.gca().transAxes,
            fontsize=12,
            verticalalignment="top",
        )

    plt.xlabel("Actual Values")
    plt.ylabel("Predicted Values")
    plt.title("All Clusters: Model Predictions vs Actual")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{output_dir}/all_clusters_predictions.png")
    plt.close()


def make_cluster_predictions_and_compare(
    cluster_models,
    cluster_data,
    comparison_values,
    ids,
    target_col_name,
    comparison_col_name,
):
    """
    Make predictions for each cluster and compare with values from additional file.

    Parameters:
    cluster_models (dict): Dictionary of trained models for each cluster
    cluster_data (dict): Dictionary of data for each cluster
    comparison_values (Series): Values from additional file to compare with
    ids (Series): IDs for all data
    target_col_name (str): Name of the target column
    comparison_col_name (str): Name of the comparison column

    Returns:
    DataFrame: Results with predictions and comparisons
    """
    # Create dataframe to store results
    results_df = pd.DataFrame(
        {
            ids.name: ids,
            f"Actual_{target_col_name}": cluster_data["all"]["y"],
            f"Cluster": cluster_data["all"]["cluster_labels"],
        }
    )

    # Add comparison values if available
    if comparison_values is not None:
        results_df[f"Compare_{comparison_col_name}"] = comparison_values

    # Make predictions for each cluster
    for cluster_idx, model in cluster_models.items():
        # Get data for this cluster
        cluster_mask = cluster_data["all"]["cluster_labels"] == cluster_idx
        if sum(cluster_mask) == 0:
            continue

        # Get features for this cluster
        X_cluster = cluster_data["all"]["X_scaled"][cluster_mask]

        # Make predictions
        y_pred_cluster = model.predict(X_cluster)

        # Store predictions in results dataframe
        results_df.loc[cluster_mask, f"Predicted_{target_col_name}"] = y_pred_cluster

    # Calculate model error metrics
    results_df["Model_Absolute_Error"] = np.abs(
        results_df[f"Actual_{target_col_name}"]
        - results_df[f"Predicted_{target_col_name}"]
    )

    # Calculate percentage errors (handling zero values)
    with np.errstate(divide="ignore", invalid="ignore"):
        model_pct = (
            results_df["Model_Absolute_Error"] / results_df[f"Actual_{target_col_name}"]
        ) * 100

        # Replace infinities and NaNs
        results_df["Model_Percent_Error"] = np.where(
            np.isfinite(model_pct), model_pct, np.nan
        )

    # If comparison values are available, calculate comparison metrics
    if comparison_values is not None:
        results_df["Comparison_Absolute_Error"] = np.abs(
            results_df[f"Actual_{target_col_name}"]
            - results_df[f"Compare_{comparison_col_name}"]
        )

        with np.errstate(divide="ignore", invalid="ignore"):
            comp_pct = (
                results_df["Comparison_Absolute_Error"]
                / results_df[f"Actual_{target_col_name}"]
            ) * 100

            # Replace infinities and NaNs
            results_df["Comparison_Percent_Error"] = np.where(
                np.isfinite(comp_pct), comp_pct, np.nan
            )

        # Calculate performance metrics by cluster with comparison
        print("\nPerformance by Cluster:")
        print(
            f"{'Cluster':10} {'Model MSE':15} {'Comparison MSE':15} {'Model R²':15} {'Comparison R²':15}"
        )
        print(f"{'-'*70}")

        for cluster_idx in sorted(cluster_data["clusters"].keys()):
            cluster_mask = results_df[f"Cluster"] == cluster_idx
            if sum(cluster_mask) == 0:
                continue

            actual = results_df.loc[cluster_mask, f"Actual_{target_col_name}"]
            predicted = results_df.loc[cluster_mask, f"Predicted_{target_col_name}"]
            comparison = results_df.loc[cluster_mask, f"Compare_{comparison_col_name}"]

            model_mse = mean_squared_error(actual, predicted)
            comp_mse = mean_squared_error(actual, comparison)

            model_r2 = (
                r2_score(actual, predicted) if len(np.unique(actual)) > 1 else np.nan
            )
            comp_r2 = (
                r2_score(actual, comparison) if len(np.unique(actual)) > 1 else np.nan
            )

            print(
                f"{cluster_idx:10} {model_mse:15.4f} {comp_mse:15.4f} "
                f"{model_r2:15.4f} {comp_r2:15.4f}"
            )

        # Calculate overall metrics with comparison
        actual_all = results_df[f"Actual_{target_col_name}"]
        predicted_all = results_df[f"Predicted_{target_col_name}"]
        comparison_all = results_df[f"Compare_{comparison_col_name}"]

        model_mse_all = mean_squared_error(actual_all, predicted_all)
        comp_mse_all = mean_squared_error(actual_all, comparison_all)

        model_rmse_all = np.sqrt(model_mse_all)
        comp_rmse_all = np.sqrt(comp_mse_all)

        model_r2_all = r2_score(actual_all, predicted_all)
        comp_r2_all = r2_score(actual_all, comparison_all)

        print(f"\nOverall Performance:")
        print(f"{'':20} {'Model':15} {'Comparison Values':15} {'Difference':15}")
        print(f"{'-'*70}")
        print(
            f"{'MSE':20} {model_mse_all:.4f}{' '*(15-len(f'{model_mse_all:.4f}'))} "
            f"{comp_mse_all:.4f}{' '*(15-len(f'{comp_mse_all:.4f}'))} "
            f"{model_mse_all - comp_mse_all:.4f}"
        )

        print(
            f"{'RMSE':20} {model_rmse_all:.4f}{' '*(15-len(f'{model_rmse_all:.4f}'))} "
            f"{comp_rmse_all:.4f}{' '*(15-len(f'{comp_rmse_all:.4f}'))} "
            f"{model_rmse_all - comp_rmse_all:.4f}"
        )

        print(
            f"{'R²':20} {model_r2_all:.4f}{' '*(15-len(f'{model_r2_all:.4f}'))} "
            f"{comp_r2_all:.4f}{' '*(15-len(f'{comp_r2_all:.4f}'))} "
            f"{model_r2_all - comp_r2_all:.4f}"
        )

        metrics = {
            "model": {"mse": model_mse_all, "rmse": model_rmse_all, "r2": model_r2_all},
            "comparison": {
                "mse": comp_mse_all,
                "rmse": comp_rmse_all,
                "r2": comp_r2_all,
            },
        }
    else:
        # Calculate performance metrics by cluster without comparison
        print("\nPerformance by Cluster:")
        print(f"{'Cluster':10} {'Model MSE':15} {'Model R²':15}")
        print(f"{'-'*40}")

        for cluster_idx in sorted(cluster_data["clusters"].keys()):
            cluster_mask = results_df[f"Cluster"] == cluster_idx
            if sum(cluster_mask) == 0:
                continue

            actual = results_df.loc[cluster_mask, f"Actual_{target_col_name}"]
            predicted = results_df.loc[cluster_mask, f"Predicted_{target_col_name}"]

            model_mse = mean_squared_error(actual, predicted)
            model_r2 = (
                r2_score(actual, predicted) if len(np.unique(actual)) > 1 else np.nan
            )

            print(f"{cluster_idx:10} {model_mse:15.4f} {model_r2:15.4f}")

        # Calculate overall metrics without comparison
        actual_all = results_df[f"Actual_{target_col_name}"]
        predicted_all = results_df[f"Predicted_{target_col_name}"]

        model_mse_all = mean_squared_error(actual_all, predicted_all)
        model_rmse_all = np.sqrt(model_mse_all)
        model_r2_all = r2_score(actual_all, predicted_all)

        print(f"\nOverall Performance:")
        print(f"{'':20} {'Model':15}")
        print(f"{'-'*35}")
        print(f"{'MSE':20} {model_mse_all:.4f}")
        print(f"{'RMSE':20} {model_rmse_all:.4f}")
        print(f"{'R²':20} {model_r2_all:.4f}")

        metrics = {
            "model": {"mse": model_mse_all, "rmse": model_rmse_all, "r2": model_r2_all},
            "comparison": None,
        }

    # Save to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"clustered_prediction_results_{timestamp}.csv"
    results_df.to_csv(output_file, index=False)
    print(f"\nPrediction results saved to {output_file}")

    return results_df, metrics


def plot_comparison_by_cluster(
    results_df, target_col_name, comparison_col_name=None, output_dir="cluster_plots"
):
    """
    Create comparison plots for each cluster.

    Parameters:
    results_df (DataFrame): Results including predictions and comparison values
    target_col_name (str): Name of target column
    comparison_col_name (str, optional): Name of comparison column
    output_dir (str): Directory to save plots
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get unique clusters
    clusters = sorted(results_df["Cluster"].unique())

    has_comparison = (
        comparison_col_name is not None
        and f"Compare_{comparison_col_name}" in results_df.columns
    )

    for cluster_idx in clusters:
        cluster_data = results_df[results_df["Cluster"] == cluster_idx]
        if len(cluster_data) == 0:
            continue

        actual = cluster_data[f"Actual_{target_col_name}"]
        predicted = cluster_data[f"Predicted_{target_col_name}"]

        # Determine how many plots to create
        n_plots = 3 if has_comparison else 1

        fig, axes = plt.subplots(1, n_plots, figsize=(n_plots * 6, 6))

        if n_plots == 1:
            # Single plot: Model vs Actual
            axes.scatter(actual, predicted, alpha=0.7, color="blue")
            min_val = min(min(actual), min(predicted))
            max_val = max(max(actual), max(predicted))
            axes.plot([min_val, max_val], [min_val, max_val], "r--")
            axes.set_xlabel("Actual Values")
            axes.set_ylabel("Model Predictions")
            axes.set_title(f"Cluster {cluster_idx}: Model vs Actual")
            axes.grid(True)
            r2_model = r2_score(actual, predicted)
            axes.text(
                0.05,
                0.95,
                f"R² = {r2_model:.4f}",
                transform=axes.transAxes,
                fontsize=12,
                verticalalignment="top",
            )
        else:
            # Three plots if comparison values are available
            comparison = cluster_data[f"Compare_{comparison_col_name}"]

            # Plot 1: Model vs Actual
            axes[0].scatter(actual, predicted, alpha=0.7, color="blue")
            min_val = min(min(actual), min(predicted))
            max_val = max(max(actual), max(predicted))
            axes[0].plot([min_val, max_val], [min_val, max_val], "r--")
            axes[0].set_xlabel("Actual Values")
            axes[0].set_ylabel("Model Predictions")
            axes[0].set_title(f"Cluster {cluster_idx}: Model vs Actual")
            axes[0].grid(True)
            r2_model = r2_score(actual, predicted)
            axes[0].text(
                0.05,
                0.95,
                f"R² = {r2_model:.4f}",
                transform=axes[0].transAxes,
                fontsize=12,
                verticalalignment="top",
            )

            # Plot 2: Comparison vs Actual
            axes[1].scatter(actual, comparison, alpha=0.7, color="green")
            min_val = min(min(actual), min(comparison))
            max_val = max(max(actual), max(comparison))
            axes[1].plot([min_val, max_val], [min_val, max_val], "r--")
            axes[1].set_xlabel("Actual Values")
            axes[1].set_ylabel(f"{comparison_col_name}")
            axes[1].set_title(f"Cluster {cluster_idx}: {comparison_col_name} vs Actual")
            axes[1].grid(True)
            r2_comp = r2_score(actual, comparison)
            axes[1].text(
                0.05,
                0.95,
                f"R² = {r2_comp:.4f}",
                transform=axes[1].transAxes,
                fontsize=12,
                verticalalignment="top",
            )

            # Plot 3: Model vs Comparison
            axes[2].scatter(comparison, predicted, alpha=0.7, color="purple")
            min_val = min(min(comparison), min(predicted))
            max_val = max(max(comparison), max(predicted))
            axes[2].plot([min_val, max_val], [min_val, max_val], "r--")
            axes[2].set_xlabel(f"{comparison_col_name}")
            axes[2].set_ylabel("Model Predictions")
            axes[2].set_title(f"Cluster {cluster_idx}: Model vs {comparison_col_name}")
            axes[2].grid(True)
            r2_model_comp = r2_score(comparison, predicted)
            axes[2].text(
                0.05,
                0.95,
                f"R² = {r2_model_comp:.4f}",
                transform=axes[2].transAxes,
                fontsize=12,
                verticalalignment="top",
            )

        fig.tight_layout()
        fig.savefig(f"{output_dir}/cluster_{cluster_idx}_comparisons.png")
        plt.close(fig)


def save_models(models, output_dir):
    """
    Save trained models to files.

    Parameters:
    models (dict): Dictionary of models to save
    output_dir (str): Directory to save models
    """
    os.makedirs(output_dir, exist_ok=True)

    # Save KMeans model
    joblib.dump(models["kmeans"], f"{output_dir}/kmeans_model.joblib")

    # Save KMeans scaler
    joblib.dump(models["kmeans_scaler"], f"{output_dir}/kmeans_scaler.joblib")

    # Save MLPRegressor models for each cluster
    cluster_models_dir = f"{output_dir}/cluster_models"
    os.makedirs(cluster_models_dir, exist_ok=True)

    for cluster_idx, model in models["cluster_models"].items():
        joblib.dump(model, f"{cluster_models_dir}/mlp_cluster_{cluster_idx}.joblib")

    # Save cluster indices
    with open(f"{output_dir}/cluster_indices.txt", "w") as f:
        f.write(",".join(str(idx) for idx in models["cluster_models"].keys()))

    print(f"Models saved to {output_dir}")


def load_models(model_dir):
    """
    Load trained models from files.

    Parameters:
    model_dir (str): Directory containing saved models

    Returns:
    dict: Dictionary of loaded models
    """
    print(f"Loading KMeans model and scaler from {model_dir}")

    # Load KMeans model
    kmeans = joblib.load(f"{model_dir}/kmeans_model.joblib")

    # Load KMeans scaler
    kmeans_scaler = joblib.load(f"{model_dir}/kmeans_scaler.joblib")

    # Load cluster indices
    with open(f"{model_dir}/cluster_indices.txt", "r") as f:
        content = f.read().strip()
        if content:
            cluster_indices = [int(idx) for idx in content.split(",")]
        else:
            # No cluster models were saved
            cluster_indices = []

    print(f"Found {len(cluster_indices)} cluster models")

    # Load MLPRegressor models for each cluster
    cluster_models = {}
    for cluster_idx in cluster_indices:
        model_path = f"{model_dir}/cluster_models/mlp_cluster_{cluster_idx}.joblib"
        if os.path.exists(model_path):
            print(f"  Loading model for cluster {cluster_idx}")
            try:
                cluster_models[cluster_idx] = joblib.load(model_path)
            except Exception as e:
                print(f"  Error loading model for cluster {cluster_idx}: {str(e)}")

    print(f"Successfully loaded {len(cluster_models)} cluster models")

    return {
        "kmeans": kmeans,
        "kmeans_scaler": kmeans_scaler,
        "cluster_models": cluster_models,
    }


def process_batch(batch_df, feature_cols, kmeans, kmeans_scaler, cluster_models):
    """
    Process a batch of samples for prediction.

    Parameters:
    batch_df (DataFrame): Batch of data to process
    feature_cols (list): List of feature column names
    kmeans (KMeans): Trained KMeans model
    kmeans_scaler (StandardScaler): Scaler used for clustering
    cluster_models (dict): Dictionary of trained MLPRegressor models for each cluster

    Returns:
    numpy.ndarray: Array of predictions
    """
    try:
        # Extract features for the batch
        X_batch = batch_df[feature_cols].values

        # Scale the features
        X_batch_scaled = kmeans_scaler.transform(X_batch)

        # Predict clusters for all samples in batch
        clusters = kmeans.predict(X_batch_scaled)

        # Initialize predictions array
        batch_predictions = np.full(len(batch_df), np.nan)

        # Get unique clusters in this batch for more efficient processing
        unique_clusters = np.unique(clusters)

        # Process each cluster in the batch
        for cluster_idx in unique_clusters:
            if cluster_idx not in cluster_models:
                continue

            # Create mask for this cluster
            cluster_mask = clusters == cluster_idx

            # Skip if no samples in this cluster
            if not np.any(cluster_mask):
                continue

            # Get the model for this cluster
            model = cluster_models[cluster_idx]

            # Get samples for this cluster
            X_cluster = X_batch_scaled[cluster_mask]

            # Make predictions for this cluster (in one batch operation)
            cluster_preds = model.predict(X_cluster)

            # Assign predictions to the correct positions in the batch
            batch_predictions[cluster_mask] = cluster_preds

        return batch_predictions

    except Exception as e:
        print(f"Error processing batch: {str(e)}")
        return np.full(len(batch_df), np.nan)


def make_predictions(
    features_df,
    kmeans,
    kmeans_scaler,
    cluster_models,
    id_col,
    batch_size=5000,
    n_jobs=None,
):
    """
    Make predictions on features using saved models.
    Process data in parallel batches to maximize speed.

    Parameters:
    features_df (DataFrame): Features dataframe
    kmeans (KMeans): Trained KMeans model
    kmeans_scaler (StandardScaler): Scaler used for clustering
    cluster_models (dict): Dictionary of trained MLPRegressor models for each cluster
    id_col (str): Name of the ID column
    batch_size (int): Number of samples to process in each batch
    n_jobs (int): Number of parallel jobs to use (None for auto-detect)

    Returns:
    DataFrame: Predictions with IDs in the same format as the input
    """
    print("\nMaking predictions using loaded models...")

    # Extract features (all columns except ID)
    feature_cols = [col for col in features_df.columns if col != id_col]

    # Initialize an empty dataframe for results with the same ID column
    result_df = pd.DataFrame({id_col: features_df[id_col].copy(), "y_pred": np.nan})

    # Check if we have any trained models
    if not cluster_models:
        print(
            "Warning: No trained cluster models available. All predictions will be NaN."
        )
        return result_df

    # Get total samples
    n_samples = len(features_df)

    # Determine optimal batch size and number of jobs
    # For very large datasets, use smaller batches
    if n_samples > 100000:
        batch_size = min(batch_size, 2000)

    # Calculate number of batches
    num_batches = (n_samples + batch_size - 1) // batch_size

    print(
        f"Processing {n_samples} samples in {num_batches} batches of size {batch_size}"
    )

    # Determine the number of jobs for parallel processing if not specified
    if n_jobs is None:
        # Use fewer jobs for very large datasets to avoid memory issues
        n_jobs = min(
            joblib.cpu_count(), 4 if n_samples > 100000 else joblib.cpu_count()
        )

    print(f"Using {n_jobs} parallel jobs")

    start_time = datetime.now()

    # Process batches in parallel
    predictions = np.full(n_samples, np.nan)

    try:
        # Split data into batches
        batches = [
            features_df.iloc[i : i + batch_size]
            for i in range(0, n_samples, batch_size)
        ]

        # Process batches in parallel
        batch_results = Parallel(n_jobs=n_jobs, verbose=10)(
            delayed(process_batch)(
                batch, feature_cols, kmeans, kmeans_scaler, cluster_models
            )
            for batch in batches
        )

        # Combine batch results
        for i, batch_pred in enumerate(batch_results):
            start_idx = i * batch_size
            end_idx = min(start_idx + batch_size, n_samples)
            predictions[start_idx:end_idx] = batch_pred

    except Exception as e:
        print(f"Error in parallel processing: {str(e)}")
        print("Falling back to sequential processing...")

        # Fallback to sequential processing if parallel fails
        for i in range(0, n_samples, batch_size):
            if i % (batch_size * 10) == 0:
                elapsed = datetime.now() - start_time
                progress = i / n_samples
                if progress > 0:
                    total_time = elapsed.total_seconds() / progress
                    remaining = total_time - elapsed.total_seconds()
                    print(
                        f"  Processing batch {i//batch_size + 1}/{num_batches} - "
                        f"{progress*100:.1f}% complete, "
                        f"est. remaining: {remaining//60:.0f}m {remaining%60:.0f}s"
                    )

            end_idx = min(i + batch_size, n_samples)
            batch_df = features_df.iloc[i:end_idx]
            batch_predictions = process_batch(
                batch_df, feature_cols, kmeans, kmeans_scaler, cluster_models
            )
            predictions[i:end_idx] = batch_predictions

    # Transfer predictions to the result dataframe
    result_df["y_pred"] = predictions

    end_time = datetime.now()
    total_time = (end_time - start_time).total_seconds()
    print(
        f"Prediction completed in {total_time:.1f} seconds "
        f"({n_samples/total_time:.1f} samples/second)"
    )

    # Count predictions made
    n_predicted = np.sum(~np.isnan(predictions))
    print(f"Made predictions for {n_predicted} out of {len(result_df)} samples")

    # Check for any missing predictions
    n_missing = np.sum(np.isnan(predictions))
    if n_missing > 0:
        print(
            f"Warning: {n_missing} samples have no predictions (possibly in clusters with no model)"
        )

    return result_df


def evaluate_predictions(y_pred_df, y_true_df):
    """
    Evaluate predictions against true values.

    Parameters:
    y_pred_df (DataFrame): Predictions dataframe with IDs
    y_true_df (DataFrame): True values dataframe with IDs

    Returns:
    tuple: (metrics, merged_df)
    """
    # Get ID column names - we'll use the first column of each dataframe
    pred_id_col = y_pred_df.columns[0]
    true_id_col = y_true_df.columns[0]

    print(f"  - Predictions ID column: '{pred_id_col}'")
    print(f"  - True values ID column: '{true_id_col}'")

    # Only merge if the column names are different
    if true_id_col != pred_id_col:
        print(f"  - ID columns have different names, merging on values")
        # Create a copy with renamed column to avoid modifying the original
        y_true_df_copy = y_true_df.copy()
        y_true_df_copy.rename(columns={true_id_col: pred_id_col}, inplace=True)
        merged_df = pd.merge(y_pred_df, y_true_df_copy, on=pred_id_col, how="inner")
    else:
        # Directly merge if column names are the same
        merged_df = pd.merge(y_pred_df, y_true_df, on=pred_id_col, how="inner")

    print(f"\nEvaluation metrics:")
    print(f"  - Total predictions: {len(y_pred_df)}")
    print(f"  - Total true values: {len(y_true_df)}")
    print(f"  - Matched for evaluation: {len(merged_df)}")

    if len(merged_df) == 0:
        print("  - No matching IDs found for evaluation")
        return None, merged_df

    # Get true values column name (assuming it's the second column in y_true_df)
    y_true_col = y_true_df.columns[1]
    print(f"  - Using '{y_true_col}' as ground truth values")

    # Check for NaN values in predictions
    nan_mask = merged_df["y_pred"].isna()
    if nan_mask.any():
        print(
            f"  - Warning: {nan_mask.sum()} predictions are NaN and will be excluded from evaluation"
        )
        if nan_mask.all():
            print("  - All predictions are NaN, cannot calculate metrics")
            return None, merged_df

        # Filter out NaN predictions for evaluation
        eval_df = merged_df[~nan_mask].copy()
    else:
        eval_df = merged_df

    # Calculate metrics
    mse = mean_squared_error(eval_df[y_true_col], eval_df["y_pred"])
    rmse = np.sqrt(mse)
    r2 = r2_score(eval_df[y_true_col], eval_df["y_pred"])

    print(f"  - Mean Squared Error: {mse:.4f}")
    print(f"  - Root Mean Squared Error: {rmse:.4f}")
    print(f"  - R² Score: {r2:.4f}")

    return {"mse": mse, "rmse": rmse, "r2": r2}, merged_df


def train_cluster_model(cluster_idx, data):
    """
    Train an MLPRegressor model for a single cluster.

    Parameters:
    cluster_idx (int): Cluster index
    data (dict): Cluster data including X and y values

    Returns:
    tuple: (cluster_idx, model, results_dict)
    """
    print(f"\nTraining model for Cluster {cluster_idx} ({len(data['X'])} samples):")

    # For very small datasets, train anyway
    if len(data["X"]) < 10:
        print(
            f"  Small cluster detected ({len(data['X'])} samples), using all data for training"
        )

    # Train model for this cluster
    model, X_train, X_test, y_train, y_test, scaler, train_indices, test_indices = (
        train_mlp_regressor(data["X"], data["y"])
    )

    # Evaluate model if there are test samples
    results = {}
    if len(y_test) > 0:
        results = evaluate_model(
            model, X_test, y_test, prefix=f"  Cluster {cluster_idx}: "
        )
    else:
        print(
            f"  Cluster {cluster_idx}: Using all samples for training, no test evaluation"
        )

    return cluster_idx, model, results


def train_models(features_file, target_file, output_dir):
    """
    Train KMeans and MLPRegressor models and save them.

    Parameters:
    features_file (str): Path to features CSV file
    target_file (str): Path to target CSV file
    output_dir (str): Directory to save models and results
    """
    print(f"Training models using {features_file} and {target_file}")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Load and match data from features and target files
    X, y, ids, target_col_name, original_features_df = load_and_match_data(
        features_file, target_file
    )

    # Determine number of clusters based on data size
    # Rule of thumb: sqrt(n/2) but capped at reasonable limits
    n_samples = len(X)
    n_clusters = min(max(2, int(np.sqrt(n_samples / 2))), 10)
    print(f"\nDetermining optimal number of clusters based on data size: {n_clusters}")

    # For very small datasets, use fewer clusters
    if n_samples < 10:
        n_clusters = min(n_clusters, n_samples // 2 + 1)
        print(f"Small dataset detected, reducing to {n_clusters} clusters")

    # Perform k-means++ clustering
    print("\nPerforming k-means++ clustering...")
    kmeans, cluster_labels, X_scaled, kmeans_scaler = perform_kmeans_clustering(
        X, n_clusters=n_clusters
    )

    # Organize data by cluster
    cluster_data = {
        "all": {"X": X, "X_scaled": X_scaled, "y": y, "cluster_labels": cluster_labels},
        "clusters": {},
    }

    for cluster_idx in range(n_clusters):
        # Get indices for this cluster
        cluster_mask = cluster_labels == cluster_idx

        # Store data for this cluster
        cluster_data["clusters"][cluster_idx] = {
            "X": X_scaled[cluster_mask],
            "y": y.iloc[cluster_mask] if hasattr(y, "iloc") else y[cluster_mask],
            "ids": (
                ids.iloc[cluster_mask] if hasattr(ids, "iloc") else ids[cluster_mask]
            ),
        }

    # Train models for each cluster in parallel
    print("\nTraining MLPRegressor models for each cluster...")

    # Determine the number of jobs for parallel training
    # Use fewer jobs for many clusters or if each cluster has a large number of samples
    n_jobs = min(
        joblib.cpu_count(),
        (
            2
            if any(len(data["X"]) > 50000 for data in cluster_data["clusters"].values())
            else joblib.cpu_count()
        ),
    )

    print(f"Training cluster models in parallel using {n_jobs} jobs")

    # Only parallelize if we have multiple clusters
    if len(cluster_data["clusters"]) > 1 and n_jobs > 1:
        # Prepare arguments for parallel processing
        parallel_args = [
            (cluster_idx, data)
            for cluster_idx, data in cluster_data["clusters"].items()
        ]

        # Train models in parallel
        try:
            results = Parallel(n_jobs=n_jobs, verbose=10)(
                delayed(train_cluster_model)(cluster_idx, data)
                for cluster_idx, data in parallel_args
            )

            # Collect results
            cluster_models = {cluster_idx: model for cluster_idx, model, _ in results}

        except Exception as e:
            print(f"Error in parallel training: {str(e)}")
            print("Falling back to sequential training...")

            # Fallback to sequential training
            cluster_models = {}
            for cluster_idx, data in cluster_data["clusters"].items():
                cluster_idx, model, _ = train_cluster_model(cluster_idx, data)
                cluster_models[cluster_idx] = model

    else:
        # Sequential training for single cluster or when parallelization is not beneficial
        print("Using sequential training for clusters")
        cluster_models = {}
        for cluster_idx, data in cluster_data["clusters"].items():
            cluster_idx, model, _ = train_cluster_model(cluster_idx, data)
            cluster_models[cluster_idx] = model

    # Save models
    models = {
        "kmeans": kmeans,
        "kmeans_scaler": kmeans_scaler,
        "cluster_models": cluster_models,
    }

    save_models(models, output_dir)

    # Save model info
    with open(f"{output_dir}/model_info.txt", "w") as f:
        f.write(f"KMeans++ with MLPRegressor Models\n")
        f.write(f"===============================\n\n")
        f.write(f"Training date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Features file: {features_file}\n")
        f.write(f"Target file: {target_file}\n")
        f.write(f"Number of samples: {n_samples}\n")
        f.write(f"Number of features: {X.shape[1]}\n")
        f.write(f"Number of clusters: {n_clusters}\n\n")

        f.write("Cluster sizes:\n")
        for cluster_idx in range(n_clusters):
            cluster_size = sum(cluster_data["all"]["cluster_labels"] == cluster_idx)
            f.write(
                f"  - Cluster {cluster_idx}: {cluster_size} samples "
                f"({cluster_size/len(cluster_data['all']['X'])*100:.1f}%)\n"
            )

        f.write("\nTrained models:\n")
        for cluster_idx in cluster_models:
            f.write(f"  - MLPRegressor for Cluster {cluster_idx}\n")

    print(f"\nTraining complete. Models saved to {output_dir}")


def predict_and_evaluate(
    features_file,
    target_file,
    model_dir,
    output_file="y_pred.csv",
    batch_size=5000,
    n_jobs=0,
):
    """
    Load models, make predictions on features file, and optionally evaluate against target file.

    Parameters:
    features_file (str): Path to features CSV file
    target_file (str): Path to target CSV file to evaluate against (optional)
    model_dir (str): Directory containing saved models
    output_file (str): Path to save predictions
    batch_size (int): Number of samples to process in each batch
    n_jobs (int): Number of parallel jobs (0 for auto-detect)
    """
    print(f"Loading models from {model_dir}")

    # Load models
    models = load_models(model_dir)

    # Get information about features without loading everything
    sample_df = pd.read_csv(features_file, nrows=5)
    feature_cols = [col for col in sample_df.columns if col != sample_df.columns[0]]
    id_col = sample_df.columns[0]

    # Count total rows
    total_rows = sum(1 for _ in open(features_file)) - 1  # subtract header

    print(f"Features file: {features_file}")
    print(f"  - Total rows: {total_rows}")
    print(f"  - ID column: '{id_col}'")
    print(f"  - Feature columns: {len(feature_cols)}")

    # Set optimal parameters for large datasets
    # Use larger chunks for reading
    chunk_size = min(batch_size * 4, 50000)

    # Override jobs if specified
    if n_jobs <= 0:
        # Auto-detect: use fewer jobs for very large datasets
        n_jobs = min(
            joblib.cpu_count(), 4 if total_rows > 100000 else joblib.cpu_count()
        )

    print(f"Using {n_jobs} parallel jobs for prediction")
    print(f"Reading and processing data in chunks of {chunk_size} rows")
    print(f"Using batch size of {batch_size} for prediction")

    # Initialize results dataframe with the same ID column as input
    result_df = pd.DataFrame(columns=[id_col, "y_pred"])

    # Process in chunks
    chunk_reader = pd.read_csv(features_file, chunksize=chunk_size)

    # Calculate total number of chunks for progress reporting
    total_chunks = (total_rows + chunk_size - 1) // chunk_size

    print(f"Processing data in {total_chunks} chunks...")
    start_time = datetime.now()

    for chunk_idx, chunk in enumerate(chunk_reader):
        chunk_start = datetime.now()
        print(f"Processing chunk {chunk_idx+1}/{total_chunks}: {len(chunk)} rows")

        # Make predictions on this chunk
        chunk_results = make_predictions(
            chunk,
            models["kmeans"],
            models["kmeans_scaler"],
            models["cluster_models"],
            id_col,
            batch_size=batch_size,
            n_jobs=n_jobs,
        )

        # Append to results, keeping the exact same ID column
        result_df = pd.concat([result_df, chunk_results], ignore_index=True)

        # Free memory
        del chunk, chunk_results

        # Force garbage collection
        import gc

        gc.collect()

        # Report progress
        chunk_time = datetime.now() - chunk_start
        elapsed = datetime.now() - start_time
        estimated_total = (elapsed.total_seconds() / (chunk_idx + 1)) * total_chunks
        remaining = estimated_total - elapsed.total_seconds()

        print(f"  Chunk {chunk_idx+1} completed in {chunk_time.total_seconds():.1f}s")
        print(f"  Progress: {(chunk_idx+1)/total_chunks*100:.1f}% complete")
        print(
            f"  Elapsed: {elapsed.total_seconds()//60:.0f}m {elapsed.total_seconds()%60:.0f}s"
        )
        print(f"  Estimated remaining: {remaining//60:.0f}m {remaining%60:.0f}s")

    # Save predictions using the exact same ID column from the input file
    print(f"Saving predictions to {output_file}...")
    result_df.to_csv(output_file, index=False)
    print(f"Predictions saved with {len(result_df)} rows to {output_file}")

    # If target file exists, evaluate predictions
    if target_file and os.path.exists(target_file):
        print(f"Evaluating predictions against {target_file}")
        y_true_df = pd.read_csv(target_file)
        print(
            f"Loaded true values: {y_true_df.shape[0]} rows, {y_true_df.shape[1]} columns"
        )

        # Evaluate predictions
        metrics, _ = evaluate_predictions(result_df, y_true_df)


def generate_summary_report(
    cluster_data,
    metrics,
    n_clusters,
    output_dir,
    comparison_available=False,
    comparison_col_name=None,
):
    """
    Generate a summary report with key metrics.

    Parameters:
    cluster_data (dict): Dictionary containing cluster information
    metrics (dict): Performance metrics
    n_clusters (int): Number of clusters
    output_dir (str): Directory to save the report
    comparison_available (bool): Whether comparison values are available
    comparison_col_name (str, optional): Name of comparison column
    """
    with open(f"{output_dir}/summary_report.txt", "w") as f:
        f.write(f"KMeans++ Clustering with MLPRegressor Models\n")
        f.write(f"=========================================\n\n")
        f.write(f"Analysis run on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write(f"Dataset Summary:\n")
        f.write(f"- Total matched samples: {len(cluster_data['all']['X'])}\n")
        f.write(f"- Number of features: {cluster_data['all']['X'].shape[1]}\n")
        f.write(f"- Number of clusters: {n_clusters}\n\n")

        f.write(f"Cluster Sizes:\n")
        for cluster_idx in range(n_clusters):
            cluster_size = sum(cluster_data["all"]["cluster_labels"] == cluster_idx)
            f.write(
                f"- Cluster {cluster_idx}: {cluster_size} samples "
                f"({cluster_size/len(cluster_data['all']['X'])*100:.1f}%)\n"
            )
        f.write("\n")

        f.write(f"Overall Performance:\n")
        f.write(f"- Model MSE: {metrics['model']['mse']:.4f}\n")
        f.write(f"- Model RMSE: {metrics['model']['rmse']:.4f}\n")
        f.write(f"- Model R²: {metrics['model']['r2']:.4f}\n")

        if comparison_available and metrics["comparison"] is not None:
            f.write(f"- Comparison MSE: {metrics['comparison']['mse']:.4f}\n")
            f.write(f"- Comparison RMSE: {metrics['comparison']['rmse']:.4f}\n")
            f.write(f"- Comparison R²: {metrics['comparison']['r2']:.4f}\n")
        f.write("\n")

        # Can add additional sections for more detailed analysis if needed


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="KMeans++ clustering with MLPRegressor models"
    )

    subparsers = parser.add_subparsers(dest="mode", help="Mode of operation")

    # Train mode
    train_parser = subparsers.add_parser("train", help="Train models")
    train_parser.add_argument(
        "--features", required=True, help="Path to features CSV file"
    )
    train_parser.add_argument("--target", required=True, help="Path to target CSV file")
    train_parser.add_argument(
        "--output-dir", default="model", help="Directory to save models"
    )

    # Predict mode
    predict_parser = subparsers.add_parser("predict", help="Make predictions")
    predict_parser.add_argument(
        "--features", required=True, help="Path to features CSV file"
    )
    predict_parser.add_argument(
        "--target",
        required=False,
        help="Optional path to target CSV file for evaluation",
    )
    predict_parser.add_argument(
        "--model-dir", required=True, help="Directory containing saved models"
    )
    predict_parser.add_argument(
        "--output", default="y_pred.csv", help="Path to save predictions"
    )
    predict_parser.add_argument(
        "--batch-size",
        type=int,
        default=5000,
        help="Batch size for processing large datasets",
    )
    predict_parser.add_argument(
        "--jobs",
        type=int,
        default=0,
        help="Number of parallel jobs (0 for auto-detect, default is auto-detect)",
    )

    args = parser.parse_args()

    # Run appropriate mode
    if args.mode == "train":
        train_models(args.features, args.target, args.output_dir)
    elif args.mode == "predict":
        predict_and_evaluate(
            args.features,
            args.target,
            args.model_dir,
            args.output,
            args.batch_size,
            args.jobs,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
