# ResearchAI - AI-Powered Research Assistant

ResearchAI is a web-based, automated workspace designed to streamline data preparation, statistical profiling, cleaning, and machine learning pipelines for research and development. 

Built with Django and Scikit-Learn, it features a premium glassmorphic dark-mode interface with a custom CSS design system.

---

## Key Features

1. **User Authentication & Dashboard**
   - Secure registration, login, and session logout.
   - Centralized statistics tracking counts of active projects, uploaded datasets, and trained models.

2. **Project Workspaces**
   - Group related datasets under specific projects.
   - Displays dataset histories, derived files, and direct shortcuts to clean or train.

3. **Statistical Dataset Explorer**
   - Direct parsing of uploaded CSV and Excel formats.
   - Comprehensive metadata profiles: Row/column counts, memory usage, duplicate rows, data type validation, and missing values count per attribute.
   - Features preview tables and summary statistical calculations (`describe`).

4. **Automated Cleaning Pipeline**
   - Deduplicates redundant database rows.
   - Imputes missing columns (Mean for numeric features, Mode/missing values for categorical features).
   - Generates a new derived dataset, automatically linking it back to the project workspace.

5. **AutoML Model Trainer**
   - **Task Detection**: Dynamically infers prediction type (Classification vs. Regression) based on target variables.
   - **Feature Preprocessing**: Imputes remaining column voids, handles categorical fields, and performs one-hot encoding.
   - **Model Selection & Comparison**: Fits and compares multiple estimators side-by-side:
     - *Classification*: Logistic Regression, Decision Tree, Random Forest, KNN, SVM, Naive Bayes, XGBoost.
     - *Regression*: Linear Regression, Decision Tree, Random Forest, SVR, XGBoost.
   - **Model Serialization**: Automatically serializes the best performing estimator to `.pkl` format, allowing easy download from the UI.

---

## Technology Stack

- **Backend**: Python 3.x, Django 6.0
- **Database**: SQLite3
- **Data & ML Libraries**: Pandas, NumPy, Scikit-Learn, XGBoost
- **Frontend Styling**: HTML5, Vanilla CSS3 (Custom Glassmorphism Dark Theme)

---

## Directory Structure

```text
├── backend/
│   ├── research_ai/
│   │   ├── accounts/         # User registration and authentication
│   │   ├── dashboard/        # Central landing page and statistics aggregator
│   │   ├── datasets/         # File uploads, processing services, and profiling
│   │   ├── ml_engine/        # Scikit-learn trainers (classification/regression)
│   │   ├── projects/         # Workspace grouping and detail logs
│   │   ├── templates/        # HTML templates styled with glassmorphism
│   │   ├── static/           # Global styles and static stylesheets
│   │   ├── manage.py
│   │   └── db.sqlite3
├── venv/                     # Python virtual environment
├── requirements.txt          # Python dependencies list
└── README.md
```

---

## Getting Started

### 1. Prerequisites
Make sure Python 3.10+ is installed on your system.

### 2. Setup Virtual Environment & Install Dependencies
Navigate to the root directory and activate the virtual environment:

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

Install packages:
```bash
pip install -r requirements.txt
```

### 3. Run Database Migrations
Create database tables and apply initial schemas:
```bash
python backend/research_ai/manage.py migrate
```

### 4. Create an Admin User (Optional)
To access the Django Admin panel at `/admin/`:
```bash
python backend/research_ai/manage.py createsuperuser
```

### 5. Launch the Server
Start the local development server:
```bash
python backend/research_ai/manage.py runserver
```
Visit the application in your browser at `http://127.0.0.1:8000/`.

---

## Running Tests

Automated tests are available inside the `ml_engine` app to verify classification and regression model pipelines. To run tests, execute:

```bash
cd backend/research_ai
python manage.py test
```
