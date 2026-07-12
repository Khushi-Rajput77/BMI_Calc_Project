# 💚 BMI Calculator

> Track, analyse & improve your Body Mass Index — built with Python & Streamlit

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=python&logoColor=white)

---

## 📋 Overview

BMI Calculator is a modern, full-featured web application that allows multiple users to **calculate**, **track**, and **analyse** their Body Mass Index over time — with beautiful charts, personalised health tips, and local data persistence.

- ✅ Runs entirely in your **browser**
- ✅ **No database** or server setup required
- ✅ **No internet** needed after install
- ✅ Data saved **locally** to your machine

---

## ✨ Features

### 📊 Tab 1 — Calculator
- Calculate BMI instantly from weight (kg) and height (m)
- Visual colour-coded BMI scale bar with animated marker
- Shows category: Underweight / Normal / Overweight / Obese
- Displays healthy weight range for your exact height
- Shows how many kg you are away from the healthy range
- Multi-user support — create and switch between profiles
- Save records to a local JSON file with one click

### 📈 Tab 2 — History
- View all saved BMI records for any user in a clean table
- Latest snapshot showing date, weight, height, and BMI
- Records sorted chronologically

### 📉 Tab 3 — Statistics
- Summary cards: Average, Min, Max BMI and total record count
- Trend message — tells you if BMI improved or worsened over time
- BMI trend chart with healthy range band highlighted
- Weight progression chart over time
- Requires at least **2 saved records** to unlock charts

### ❤️ Tab 4 — Health Tips
- Personalised tips based on your current BMI category
- General guidelines for Exercise, Nutrition, and Lifestyle
- Tips update automatically when you change BMI input

---

## 📁 File Structure
##

```
bmi_project/
├── bmi_app.py          # Main application (only file you need to run)
├── bmi_data.json       # Auto-created when you save your first record
└── README.md           # This file
```

> **Note:** `bmi_data.json` is created automatically the first time you save a BMI record. You do not need to create it manually.

---

## 📦 Requirements

**Python 3.8 or higher** is required.

| Library | Purpose |
|---|---|
| `streamlit` | Web framework — renders the entire UI in browser |
| `pandas` | DataFrame for history table display |
| `matplotlib` | BMI and weight trend charts |
| `numpy` | Chart axis and array calculations |
| `json` | Built-in — saves user data to local file |
| `os` | Built-in — file path and existence checks |
| `datetime` | Built-in — timestamps for each saved record |

---

## 🚀 Installation & Setup

### Step 1 — Clone the Repository

```bash
git clone https://github.com/your-username/bmi-calculator.git
cd bmi-calculator
```

### Step 2 — Install Dependencies

```bash
pip install streamlit pandas matplotlib numpy
```

### Step 3 — Run the App

```bash
streamlit run bmi_app.py
```

The app opens automatically in your browser at:

```
http://localhost:8501
```

### Step 4 — Stop the App

Press `Ctrl + C` in the terminal to stop the server.

---

## 📖 How to Use

### Creating Your First Record
1. Open the app and go to the **Calculator** tab
2. Enter your username (e.g. `Alex`)
3. Enter your **weight** in kilograms and **height** in metres
4. Your BMI is calculated and displayed instantly on the right
5. Click **Save Record** to store this entry

### Switching Between Users
- Once at least one user exists, a dropdown appears at the top
- Select an existing user or choose **➕ Create New User**
- Each user has their own independent history

### Viewing Trends
- Go to the **Statistics** tab and select your username
- Charts appear automatically if you have **2 or more** saved records
- The trend message tells you if your BMI improved since your first record

---

## 📊 BMI Reference Table

| BMI Range | Category | Status |
|---|---|---|
| Below 18.5 | Underweight | 🔵 |
| 18.5 — 24.9 | Normal Weight | 🟢 |
| 25.0 — 29.9 | Overweight | 🟡 |
| 30.0 and above | Obese | 🔴 |

**Formula:**

```
BMI = Weight (kg) ÷ Height (m)²
```

**Example:**
```
70 kg ÷ (1.75 × 1.75) = 70 ÷ 3.0625 = 22.86  →  Normal Weight ✅
```

---

## 💾 Data Storage & Privacy

All data is stored **locally on your computer** in `bmi_data.json`.  
No data is sent to any server, cloud, or external service.

### Data Format

```json
{
  "Alex": {
    "records": [
      {
        "date": "2025-03-05 10:30",
        "weight": 70.0,
        "height": 1.75,
        "bmi": 22.86,
        "category": "Normal Weight"
      }
    ]
  }
}
```

### Deleting Data
- **Delete all data** — delete the `bmi_data.json` file
- **Delete one user** — open the file in any text editor and remove their block

---

## 🔧 Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: streamlit` | Run `pip install streamlit pandas matplotlib numpy` |
| Port 8501 already in use | Run `streamlit run bmi_app.py --server.port 8502` |
| App opens but shows error | Check Python version — needs 3.8 or higher |
| Charts not showing | Add at least 2 saved records in the Calculator tab first |
| Data not saving | Check write permissions in the folder where `bmi_app.py` is saved |
| Browser does not open | Manually go to `http://localhost:8501` |

---

## 🛠️ Technology Stack

| Technology | Role |
|---|---|
| Python 3.8+ | Core programming language |
| Streamlit | Web UI framework — renders everything in browser |
| Pandas | DataFrame for history table display |
| Matplotlib + NumPy | BMI and weight trend charts |
| JSON | Lightweight local data persistence — no database needed |
| Custom CSS | Dark green theme, animations, card layouts, scale bar |

---



