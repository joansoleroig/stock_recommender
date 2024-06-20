# Stock Recommender System

This repository contains the code for a Stock Recommender System built using Streamlit. The system recommends stocks based on sector and risk similarity for users with predefined portfolios.
### You can find the app up and running here: https://stock-recommender.streamlit.app/


## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Data](#data)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Stock Recommender System leverages user portfolio data and S&P 500 companies' data to suggest stocks based on sector and risk similarities. The recommendations are generated using precomputed similarity matrices.

## Features

- Display user portfolios with sector diversification.
- Recommend stocks based on sector similarity.
- Recommend stocks based on risk similarity.

## Data

- **User Portfolios:** `user_portfolios.csv` contains user IDs, names, stocks, sectors, and portfolio weights.
- **S&P 500 Companies:** `constituents.csv` and `constituents_with_changes.csv` contain details of S&P 500 companies including sectors and last month's percentage changes.
- **Similarity Matrices:** `sector_similarity_matrix.csv` and `risk_similarity_matrix.csv` contain precomputed similarity data.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/stock-recommender-system.git
    cd stock-recommender-system
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure you have the necessary CSV files in the `data_generation` folder:
    - `user_portfolios.csv`
    - `constituents.csv`
    - `constituents_with_changes.csv`
    - `sector_similarity_matrix.csv`
    - `risk_similarity_matrix.csv`

## Usage

1. To generate the user portfolio data, run:
    ```bash
    python data_generation/generate_Data.py
    ```

2. To fetch stock data, run:
    ```bash
    python data_generation/fetch_stock_data.py
    ```

3. To start the Streamlit application, run:
    ```bash
    streamlit run app.py
    ```

4. Open your browser and navigate to `http://localhost:8501` to interact with the application.

## Directory Structure

.
├── app.py
├── data_generation
│ ├── generate_Data.py
│ ├── fetch_stock_data.py
│ ├── recommendations.py
│ ├── user_portfolios.csv
│ ├── constituents.csv
│ ├── constituents_with_changes.csv
│ ├── sector_similarity_matrix.csv
│ ├── risk_similarity_matrix.csv
├── finance.webp
└── requirements.txt


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
