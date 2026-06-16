# 💻 LaptopLens — ML Laptop Price Predictor

> An end-to-end machine learning web app that estimates laptop market prices from hardware specifications, built with Scikit-learn and Streamlit.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.x-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat)

---

## Overview

LaptopLens takes 13 hardware and software specifications as input and outputs a predicted price in Indian Rupees (₹). The model is trained on a cleaned dataset of 1,300+ real-world laptop listings and wrapped in a polished, minimal dark-mode UI.

**Live demo:** [laptop-price-predictor.streamlit.app](https://laptop-price-predictor-gikdrfpnjknikxqxefpand.streamlit.app/)

---

## Features

- **Instant price estimates** — input specs, get a prediction in one click
- **Live configuration card** — spec summary updates in real time as you fill the form
- **13 input features** — brand, type, RAM, SSD, HDD, CPU, GPU, display, OS, and more
- **Log-transformed target** — model predicts `log(price)`, output is exponentiated for accuracy
- **Minimal dark UI** — Space Grotesk + Inter typography, navy/blue palette

---

## Tech Stack

| Layer | Tools |
|---|---|
| Data processing | Pandas, NumPy |
| ML pipeline | Scikit-learn (`Pipeline`, `ColumnTransformer`, `RandomForestRegressor`) |
| Web app | Streamlit |
| Serialization | Pickle |
| Fonts | Google Fonts (Space Grotesk, Inter) |

---

## Project Structure

```
laptop-price-predictor/
├── app.py                  # Streamlit UI
├── pipe.pkl                # Trained ML pipeline (serialized)
├── laptop_data.csv         # Raw dataset
├── model_training.ipynb    # EDA, feature engineering & model training notebook
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Dakshhhhh-ops/laptop-price-predictor.git
cd laptop-price-predictor
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

> **Note:** `pipe.pkl` must be present in the root directory. If you want to retrain the model, run all cells in `model_training.ipynb` — it will generate a fresh `pipe.pkl`.

---

## Model Details

### Dataset
- **Source:** Kaggle Laptop Price Dataset
- **Size:** 1,302 listings after cleaning
- **Target:** `log(Price_in_INR)` — log-transform reduces skew and improves regression performance

### Feature Engineering

| Feature | Transformation |
|---|---|
| Screen resolution + size | Derived `PPI` (pixels per inch) |
| Touchscreen / IPS | Binary encoded (0 / 1) |
| CPU brand | Extracted from raw CPU string |
| GPU brand | Extracted from raw GPU string |
| OS | Grouped into 5 categories |
| Company, TypeName | One-hot encoded |

### Pipeline

```
Input (13 features)
    └── ColumnTransformer
            ├── OneHotEncoder  →  categorical columns
            └── Passthrough    →  numerical columns
                    └── RandomForestRegressor
                            └── np.exp(prediction)  →  ₹ Price
```

### Performance

| Metric | Score |
|---|---|
| R² (test set) | ~0.89 |
| MAE | ~₹8,500 |

---

## Input Features

| Feature | Type | Example |
|---|---|---|
| Company | Categorical | Dell, Apple, Lenovo |
| Type | Categorical | Ultrabook, Gaming, Notebook |
| RAM | Numeric (GB) | 8, 16, 32 |
| Weight | Numeric (kg) | 1.8 |
| Touchscreen | Binary | Yes / No |
| IPS Display | Binary | Yes / No |
| Screen Size | Numeric (inches) | 15.6 |
| Resolution | Categorical | 1920x1080 |
| CPU Brand | Categorical | Intel Core i7 |
| CPU Speed | Numeric (GHz) | 2.5 |
| HDD | Numeric (GB) | 0, 512, 1000 |
| SSD | Numeric (GB) | 256, 512 |
| GPU Brand | Categorical | Nvidia, Intel, AMD |
| OS | Categorical | Windows, Mac, Linux |

---

## Screenshots

> *(Add screenshots of the running app here)*

```
app_screenshot.png
```

---

## Deployment

The app can be deployed to Streamlit Community Cloud in minutes:

1. Push the repository to GitHub (including `pipe.pkl`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo, set `app.py` as the entry point
4. Click **Deploy**

---

## Requirements

```
streamlit
scikit-learn
pandas
numpy
```

Generate a full `requirements.txt` with:

```bash
pip freeze > requirements.txt
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**Daksh** — [@Dakshhhhh-ops](https://github.com/Dakshhhhh-ops)

*Built as a machine learning end-to-end project covering data cleaning, feature engineering, model training, and production UI deployment.*
