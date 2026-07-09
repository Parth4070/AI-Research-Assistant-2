from numpy.ma import outerproduct
import os
import matplotlib.pyplot as plt
import seaborn as sns

def generate_correlation_map(df, output_path):
    numeric_df = df.select_dtypes(include = ["number"])

    if numeric_df.empty:
        return False

    plt.figure(figsize=(10, 8))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Map")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return output_path