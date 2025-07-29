# 🔥 firecast_pipeline

This repository provides a unified training and prediction pipeline for **fire risk regression tasks** using the following models:

- **OLS** (Ordinary Least Squares)
- **Lasso**
- **MLP** (Multi-layer Perceptron)
- **CNN** (with Optuna hyperparameter tuning)
- **XGBoost**

The pipeline is designed for `.xlsx` Excel datasets with flexible feature columns.

👉 **The last column must always be the response (target) variable** (e.g., Time to Flashover).

---

## 📁 Expected Excel Format

- **File type:** `.xlsx`
- **Structure:**
  - ✅ First row = column headers
  - ✅ All columns except the **last** = input features
  - ✅ Last column = fire risk target (e.g., TTF)
  - ❌ Unnecessary columns must be **removed**, not just hidden

### ✅ Example

| Thermal Inertia | HRRPUA | Ignition Temp | Time to Flashover |
|-----------------|--------|----------------|--------------------|
| 136500          | 725    | 400            | 42.5               |
| ...             | ...    | ...            | ...                |

---

## 📦 Installation

Install all required dependencies:

```bash
pip install -r requirements.txt
```

> Or manually:

```bash
pip install pandas numpy scikit-learn statsmodels xgboost torch optuna openpyxl joblib plotly
```

---

## 🚀 Training

Train any supported model on your dataset:

```bash
python -m regressorpipeline.train --model_name cnn --data_path examples/example_data_train.xlsx
python -m regressorpipeline.train --model_name ols --data_path examples/example_data_train.xlsx
python -m regressorpipeline.train --model_name lasso --data_path examples/example_data_train.xlsx
python -m regressorpipeline.train --model_name mlp --data_path examples/example_data_train.xlsx
python -m regressorpipeline.train --model_name xgboost --data_path examples/example_data_train.xlsx
```

Models are saved to the `examples/` folder as `best_<model_name>_model.joblib`.

---

## 🔍 Prediction

Run inference on a test `.xlsx` file:

```bash
python -m regressorpipeline.predict \
  --predict_path examples/example_data_test.xlsx \
  --model_path examples/best_cnn_model.joblib
```

To save predictions to CSV:

```bash
python -m regressorpipeline.predict \
  --predict_path examples/example_data_test.xlsx \
  --model_path examples/best_cnn_model.joblib \
  --output_path examples/predict_results.csv
```

---

## 📊 Visualization (CNN only)

Generate a 3D surface plot for CNN predictions over any two features:

```bash
python -m regressorpipeline.visualize \
  --feat1 ThermalInertia \
  --feat2 FuelLoadDensity \
  --model_path examples/best_cnn_model.joblib \
  --save_path examples/cnn_surface.html
```

> Output will be saved as an interactive HTML file.

---

## 📂 Folder Structure

```text
firecast_pipeline/
│
├── regressorpipeline/
│   ├── train.py                # Training logic
│   ├── predict.py              # Prediction logic
│   ├── visualize.py            # 3D surface visualization
│   ├── cnn_module.py           # CNN model definition
│   ├── models.py               # Traditional model trainers
│   └── data_utils.py           # Data loaders and scalers
│
├── examples/
│   ├── example_data_train.xlsx
│   ├── example_data_test.xlsx
│   └── best_cnn_model.joblib
│
├── requirements.txt
└── README.md
```

---

## 📜 License

MIT License – use freely for research or fire safety AI applications. For commercial use, please contact the authors.
