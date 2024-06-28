import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to load tyre sales data from a CSV file
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        messagebox.showerror("Error", f"The file at {file_path} was not found.")
        return None
    except PermissionError:
        messagebox.showerror("Error", f"Permission denied for file at {file_path}.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        return None

# Function to clean the data
def clean_data(df):
    # Check for missing values
    missing_values_before = df.isnull().sum()
    
    # Drop duplicates
    duplicate_count_before = df.duplicated().sum()
    df = df.drop_duplicates()
    
    # Check again for missing values and duplicates after cleaning
    missing_values_after = df.isnull().sum()
    duplicate_count_after = df.duplicated().sum()
    
    # Display reports
    missing_values_report = f"Missing Values Report:\nBefore Cleaning:\n{missing_values_before}\nAfter Cleaning:\n{missing_values_after}\n"
    duplicate_rows_report = f"Duplicate Rows Report:\nNumber of Duplicate Rows Found: {duplicate_count_before}\nAction Taken: Duplicates Removed. Remaining Rows: {len(df)}"
    return missing_values_report, duplicate_rows_report

# Function to perform EDA
def perform_eda(df):
    # Descriptive Statistics
    descriptive_stats = df.describe().to_string()
    
    # Visualizations
    plt.figure(figsize=(20, 15))
    for i, col in enumerate(['Sales', 'Price'], start=1):
        plt.subplot(2, 2, i)
        plt.hist(df[col], bins=30, color='skyblue', edgecolor='black')
        plt.title(f'Histogram of {col}', fontsize=16, color='purple')
        plt.xlabel(col, fontsize=14, color='purple')
        plt.ylabel('Frequency', fontsize=14, color='purple')
    
    plt.suptitle('Histograms of Numerical Features', fontsize=20, color='purple')
    plt.tight_layout()
    plt.show()
    
    # Correlation Matrix and Heatmap
    corr_matrix = df[['Sales', 'Price']].corr()
    plt.figure(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5, cbar_kws={'label': 'Correlation Coefficient'})
    plt.title('Correlation Matrix', fontsize=16, color='darkred')
    plt.show()
    
    # Sales distribution by season
    plt.figure(figsize=(12, 6))
    sns.barplot(x='season', y='Sales', data=df, ci=None, palette='viridis')
    plt.title('Sales Distribution by Season', fontsize=16, color='darkgreen')
    plt.xlabel('Season', fontsize=14, color='darkgreen')
    plt.ylabel('Sales', fontsize=14, color='darkgreen')
    plt.xticks(color='darkgreen')
    plt.yticks(color='darkgreen')
    plt.show()
    
    # Price distribution by vehicle type
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Vehicle Type', y='Price', data=df, palette='coolwarm')
    plt.title('Price Distribution by Vehicle Type', fontsize=16, color='darkblue')
    plt.xlabel('Vehicle Type', fontsize=14, color='darkblue')
    plt.ylabel('Price', fontsize=14, color='darkblue')
    plt.xticks(color='darkblue')
    plt.yticks(color='darkblue')
    plt.show()
    
    # Sales and average price by company
    plt.figure(figsize=(14, 7))
    plt.subplot(1, 2, 1)
    sns.barplot(x='Company', y='Sales', data=df, ci=None, palette='cubehelix')
    plt.title('Sales by Company', fontsize=16, color='darkcyan')
    plt.xlabel('Company', fontsize=14, color='darkcyan')
    plt.ylabel('Sales', fontsize=14, color='darkcyan')
    plt.xticks(color='darkcyan')
    plt.yticks(color='darkcyan')
    
    plt.subplot(1, 2, 2)
    sns.barplot(x='Company', y='Price', data=df, ci=None, palette='magma')
    plt.title('Average Price by Company', fontsize=16, color='darkmagenta')
    plt.xlabel('Company', fontsize=14, color='darkmagenta')
    plt.ylabel('Average Price', fontsize=14, color='darkmagenta')
    plt.xticks(color='darkmagenta')
    plt.yticks(color='darkmagenta')
    
    plt.tight_layout()
    plt.show()
    
    return descriptive_stats

# Main function to handle GUI and data operations
def main():
    # Create the main application window
    root = tk.Tk()
    root.title("Data Cleaning and EDA")
    
    # Function to handle loading and cleaning data
    def start_data_cleaning():
        nonlocal df
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            df = load_data(file_path)
            if df is not None:
                messagebox.showinfo("Success", "Data loaded successfully.")
                missing_values_report, duplicate_rows_report = clean_data(df)
                messagebox.showinfo("Data Cleaning Proof", f"{missing_values_report}\n{duplicate_rows_report}")
                btn_start_eda.config(state=tk.NORMAL)
    
    # Function to handle starting EDA
    def start_eda():
        if df is not None:
            perform_eda(df)
        else:
            messagebox.showwarning("Warning", "Please load data and clean it first.")
    
    # Button to start data cleaning
    btn_start_cleaning = tk.Button(root, text="Start Data Cleaning", command=start_data_cleaning)
    btn_start_cleaning.pack(pady=20)
    
    # Button to start EDA
    btn_start_eda = tk.Button(root, text="Start EDA", command=start_eda, state=tk.DISABLED)
    btn_start_eda.pack(pady=20)
    
    # Run the main application loop
    root.mainloop()

# Run the main function
if __name__ == "__main__":
    main()
