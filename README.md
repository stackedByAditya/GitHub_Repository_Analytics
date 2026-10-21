# 📊 GitHub Repository Analytics

An interactive data analytics dashboard for exploring GitHub repositories, analyzing repository popularity, comparing development activity, and discovering patterns across open-source projects.

Built using **Python, Streamlit, Pandas, and Plotly**, this project transforms repository data into interactive visualizations and insights through a web-based dashboard.

## 📸 Project Preview

![GitHub Repository Analytics Dashboard](Screenshot%202026-10-21%20152211.png)

![GitHub Repository Analytics Dashboard - Additional View](Screenshot%202026-10-21%20152233.png)

*Screenshot of the GitHub Repository Analytics dashboard will be added here.*

## 🎯 Project Objectives

The main objective of this project is to analyze GitHub repository data and present meaningful information through an interactive and user-friendly dashboard.

The project aims to:

- Analyze repository popularity using stars and forks.
- Explore repository activity through open issue counts.
- Identify popular repositories and programming language trends.
- Visualize relationships between repository metrics.
- Enable users to filter and explore repository data interactively.
- Present data-driven insights in an accessible visual format.

## ✨ Key Features

### 1. Interactive Analytics Dashboard
Displays key performance indicators (KPIs), including:

- Total number of repositories
- Total stars across repositories
- Total forks across repositories
- Total open issues

### 2. Repository Popularity Analysis
Visualizes repository popularity and helps users explore repositories with high star counts.

### 3. Programming Language Analysis
Provides visual insights into the distribution of programming languages represented in the dataset.

### 4. Repository Explorer
Allows users to explore repository records and apply available filters to narrow down the displayed data.

### 5. Correlation and Insights
Provides visual analysis of relationships between repository metrics, helping users investigate patterns in stars, forks, and other numerical attributes.

### 6. Interactive Visualizations
Uses Plotly charts to provide interactive data exploration through visual elements such as bar charts and pie charts.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web dashboard |
| Pandas | Data loading, manipulation, and analysis |
| Plotly | Interactive data visualization |
| CSV | Dataset storage and processing |
| Git and GitHub | Version control and project hosting |
| Streamlit Community Cloud | Web application deployment |

## 📂 Project Structure

```text
GitHub_Repository_Analytics/
│
├── processed_data/
│   ├── github_repositories_enhanced.csv
│   └── github_repositories_cleaned.csv
│
├── app_light_fixed.py
├── requirements.txt
└── README.md
```

### File Description

- **`app_light_fixed.py`** — Main Streamlit application containing the dashboard and visualization logic.
- **`processed_data/github_repositories_enhanced.csv`** — Enhanced repository dataset used by the dashboard when available.
- **`processed_data/github_repositories_cleaned.csv`** — Cleaned repository dataset available as a fallback.
- **`requirements.txt`** — Lists the Python packages required to run the application.
- **`README.md`** — Project documentation and setup instructions.

## 📊 Dataset Overview

The dashboard currently loads **2,000 GitHub repository records** from the enhanced dataset.

The application displays repository-related metrics, including stars, forks, and open issues, and supports visual exploration of the available repository attributes.

The dataset files are stored in the `processed_data/` directory.

## ⚙️ Installation and Setup

Follow these steps to run the project locally.

### Prerequisites

- Python 3.9 or a compatible Python version
- pip package manager
- Git (optional, for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/stackedByAditya/GitHub_Repository_Analytics.git
```

### Step 2: Open the Project Directory

```bash
cd GitHub_Repository_Analytics
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
streamlit run app_light_fixed.py
```

### Step 5: Open the Dashboard

Streamlit will provide a local URL in the terminal, usually:

```text
http://localhost:8501
```

Open this URL in your browser to interact with the dashboard.

## 🌐 Live Demo

The application is deployed using Streamlit Community Cloud.

**Live Dashboard:** [GitHub Repository Analytics](https://share.streamlit.io/)

*Replace this link with the direct URL of your deployed dashboard.*

## 🔍 Potential Applications

This project demonstrates how repository data can be used to:

- Explore open-source software projects.
- Compare repository popularity and engagement.
- Investigate programming language distributions.
- Understand relationships between repository metrics.
- Practice exploratory data analysis and interactive visualization.

## 🚀 Future Enhancements

Possible future improvements include:

- Integration with the GitHub REST API for retrieving live repository information.
- Automated dataset updates.
- Advanced repository ranking and comparison tools.
- Time-based analysis of repository growth.
- Additional filters and more detailed statistical analysis.
- Exporting filtered data and analytical reports.

## 🎓 Learning Outcomes

Through this project, the following concepts are demonstrated:

- Data loading and manipulation using Pandas.
- Exploratory data analysis.
- Interactive dashboard development using Streamlit.
- Data visualization using Plotly.
- Organizing a Python project and managing dependencies.
- Version control and deployment using GitHub and Streamlit Community Cloud.

## 👨‍💻 Author

**Aditya**

GitHub: [@stackedByAditya](https://github.com/stackedByAditya)

## 📄 License

No license has been specified for this repository yet. If you intend to allow others to reuse or modify the project, consider adding an appropriate open-source license.

