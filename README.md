# EDA_GENAI_PRACTICE - Automated EDA (Exploratory Data Analysis)

A practice/demo project showcasing automated exploratory data analysis using sample sales data. This toolkit generates comprehensive EDA reports using industry-standard profiling tools—perfect for learning data analysis workflows and understanding EDA best practices.

## 📊 Features

- **Automated Report Generation**: Generate professional EDA reports with a single command
- **Multiple Analysis Methods**: 
  - **Sweetviz**: Interactive HTML reports with data quality insights
  - **YData Profiling**: Comprehensive statistical analysis and data profiling
  - **D-Tale**: Interactive data exploration dashboard
- **Sales Data Generation**: Synthetic sales dataset generator for practice and testing
- **Version Verification**: Automatic checking of required library versions

## 🛠️ Tech Stack

- **Python 3.10+**
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **YData Profiling** - Automated statistical data analysis
- **Sweetviz** - Automated exploratory data analysis visualization
- **D-Tale** - Interactive data explorer dashboard

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/EDA_GENAI_PRACTICE.git
cd EDA_GENAI_PRACTICE
```

### 2. Create Virtual Environment
```bash
python -m venv eda_env
```

**Windows:**
```bash
eda_env\Scripts\activate
```

**macOS/Linux:**
```bash
source eda_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Generate Sample Sales Data
```bash
python generate_sales_data.py
```

This creates a **sample dataset** with 100,000 transactions (includes duplicate data for practice):
- Product names (Laptop, Phone, Tablet, Monitor, Keyboard, Mouse, Printer)
- Transaction amounts and dates
- Customer information
- Regional data
- **Note**: This is demo/sample data with intentional duplicates for learning EDA techniques

### Run Automated EDA Analysis
```bash
python automated_eda.py
```

This generates three comprehensive reports:
1. **sweetviz_report.html** - Interactive Sweetviz report
2. **ydata_report.html** - Detailed YData Profiling report
3. Can also launch D-Tale dashboard

### Run the Streamlit Dashboard
```bash
streamlit run app.py
```

This launches a Streamlit dashboard that embeds the generated EDA reports and provides an interactive dataset overview.

### Launch D-Tale Dashboard
```bash
python launch_dtale.py
```

Opens an interactive web-based data explorer for dynamic analysis.

## 📂 Project Structure

```_PRACTICE/
├── app.py                     # Streamlit dashboard app
├── automated_eda.py           # Main EDA report generator
├── generate_sales_data.py     # Sample synthetic data generator
├── launch_dtale.py            # Interactive dashboard launcher
├── requirements.txt           # Python dependencies
├── sales_data.csv             # Generated sample dataset
├── sweetviz_report.html       # Sweetviz analysis output
├── ydata_report.html          # YData Profiling output
└── README.md                  # This file
```

## 📈 What You'll Learn

This practice project demonstrates:
- Automated data profiling and quality assessment techniques
- Statistical analysis workflows and best practices
- Data visualization and interactive exploration
- Handling and identifying duplicates in datasets
- Python data science tooling and automation
- How to generate EDA reports for stakeholder communication
- Real-world data quality issues (duplicates, missing values, etc.)

## 🔍 Report Contents

### Sweetviz Report
- Data overview and summary statistics
- Missing data analysis
- Correlation analysis
- Variable distributions
- Data type information
- Interactive filtering and exploration

### YData Profiling Report
- Detailed variable analysis
- Statistical profiles
- Missing data patterns
- Duplicate records detection
- Correlation matrices
- Variable inte (Learning & Practice)

- **Data Quality Assessment**: Learn to identify duplicates, missing values, and anomalies
- **Stakeholder Communication**: Practice generating professional reports
- **Data Preprocessing**: Understand data exploration before ML projects
- **Educational**: Master data analysis best practices and EDA techniques
- **Hands-on Practice**: Work with real-world data quality scenarios
- **Portfolio Project**: Demonstrate data analysis skills to employerng ML models
- **Educational**: Learn data analysis best practices
- **Testing**: Validate data pipelines and ETL processes

## 📝 Requirements

See [requirements.txt](requirements.txt) for the complete list of dependencies.

- pandas ≥ 2.0.0
- numpy ≥ 1.24.0
- ydata-profiling ≥ 4.6.0
- sweetviz ≥ 2.3.0
- dtale ≥ 3.10.0

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## 📄 License
🎓 Disclaimer

This is a **practice/demo project** with sample data containing intentional duplicates and patterns for educational purposes. It's designed for learning EDA techniques, not for production use.

## 📧 Contact

For questions or suggestions, reach out via LinkedIn or open an issue on GitHub.

---

**Happy Learning &
---

**Happy Analyzing! 📊**
