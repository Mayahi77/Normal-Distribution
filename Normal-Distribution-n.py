import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_normal_distribution(data, column_name, file_name):
    """
    Plots the normal distribution of a given data column.
    """
    # Calculate mean and standard deviation
    mean = np.mean(data)
    std_dev = np.std(data)

    # Generate normal distribution values
    x = np.linspace(mean - 4 * std_dev, mean + 4 * std_dev, 1000)  # Standard deviation range
    y = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)  # Normal distribution formula

    # Create a figure
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(data, bins=30, density=True, alpha=0.6, color='skyblue', label="Data Histogram")
    ax.plot(x, y, color='red', label=f"Normal Distribution\nμ={mean:.4f}, σ={std_dev:.4f}")
    ax.set_title(f"Normal Distribution of ({file_name})")
    ax.set_xlabel(column_name)
    ax.set_ylabel("Density")
    ax.legend()
    ax.grid(True)
    
    # Set x-ticks and limits
    xticks = np.arange(-1.75, 1.1, 0.25)
    ax.set_xticks(xticks)
    ax.set_xlim(-1.75, 1.0)

    return fig

def main():
    st.title("Normal Distribution for Rotating Wedge")
    st.write("Upload files and choose a sample size")

    # File upload section
    uploaded_files = st.file_uploader(
        "Upload CSV files",
        type=["csv"],
        accept_multiple_files=True,
        help="You can upload multiple CSV files containing torque data.",
    )

    # Column name for the torque
    torque_col = st.text_input(
        "Enter the column name for torque data:",
        value="Actual Torque [of nominal]",
        help="Specify the column name containing the torque data in your CSV files."
    )

    # User input for sample size
    sample_size = st.number_input(
        "Enter sample size (n):",
        min_value=1,
        value=10,
        step=1,
        help="Choose the number of random data points to sample from the torque column."
    )

    if uploaded_files and torque_col:
        combined_fig, ax = plt.subplots(figsize=(10, 6))  # Combined plot initialization

        for uploaded_file in uploaded_files:
            try:
                # Read the CSV file
                df = pd.read_csv(uploaded_file, delimiter='\t')
                df = df.drop(columns=['Unnamed: 3'], errors='ignore')

                # Check if the required column exists
                if torque_col not in df.columns:
                    st.error(f"File {uploaded_file.name} does not contain the required column: '{torque_col}'")
                    continue

                # Extract the column data and take a random chunk of size n
                data = df[torque_col].dropna()
                if len(data) >= sample_size:
                    sampled_data = data.sample(n=sample_size, random_state=42)
                else:
                    st.warning(f"File {uploaded_file.name} has fewer than {sample_size} data points. Taking all available data.")
                    sampled_data = data

                # Generate individual plot for the sampled data
                fig = plot_normal_distribution(sampled_data, torque_col, uploaded_file.name)
                st.pyplot(fig)

                # Add to combined plot
                mean = np.mean(sampled_data)
                std_dev = np.std(sampled_data)
                x = np.linspace(mean - 4 * std_dev, mean + 4 * std_dev, 1000)
                y = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)
                ax.plot(x, y, label=f"{uploaded_file.name}\nμ={mean:.4f}, σ={std_dev:.4f}")

            except Exception as e:
                st.error(f"An error occurred while processing {uploaded_file.name}: {e}")

        # Finalize combined plot
        ax.set_title("Combined Normal Distribution of All Files")
        ax.set_xlabel("Torque")
        ax.set_ylabel("Density")
        ax.legend()
        ax.grid(True)

        # Set x-ticks and limits for the combined plot
        xticks_combined = np.arange(-1.75, 1.1, 0.25)
        ax.set_xticks(xticks_combined)
        ax.set_xlim(-1.75, 1.0)
        ax.set_ylim(0, 6)  # Set y-axis limit

        # Show the combined plot once
        st.pyplot(combined_fig)

if __name__ == "__main__":
    main()
