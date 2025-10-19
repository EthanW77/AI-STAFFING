# Workforce Intelligence Platform

A comprehensive web-based dashboard for analyzing staff, projects, deliverables, billed time, roles, and skills across multiple organizational units.

## 🎯 Features

### Core Functionalities
- **Employee Directory**: Filter by skills, role, location, and title
- **Projects Dashboard**: View by client, technology, and dollar amount
- **Billing & Time Tracking**: Track hours per employee, per project, per year
- **Resume & Skills Matrix**: View education, certifications, and project experience
- **Deliverables Tracker**: Monitor deliverables by project, topic area, and client
- **Analytics & Reports**: Aggregate insights across the organization
- **Complex Search**: Advanced multi-criteria search (e.g., "Find all senior Python engineers in Texas who worked on law enforcement projects")

### Data Relationships
The system establishes the following relationships using primary and foreign keys:

```
employees.Employee_ID ←→ billing.Employee_ID
employees.Employee_ID ←→ resume_data.Employee_ID
projects.Billing_Code ←→ billing.Billing_Code
projects.Billing_Code ←→ deliverables.Billing_Code
employees.Role_ID ←→ roles.Role_ID
```

## 📁 Project Structure

```
AI-Staffing/
├── Data/                           # CSV data files
│   ├── EmployeeID-Name-Email-RoleID-JobTitle-Location-Skills-LinkedInURL.csv
│   ├── BillingCode-ProjectName-Client-Industry-Technologies-DollarAmount-ProjectScope.csv
│   ├── BillingCode-EmployeeID-Year-HoursBilled-RoleinProject.csv
│   ├── EmployeeID-Education-Experience-Certifications-Summary.csv
│   ├── BillingCode-Deliverable-DateCompleted-TopicArea-Technologies-Client-Codebase.csv
│   └── RoleID-StandardRole-RoleTitleVariants.csv
├── database.py                     # Database module with relationship logic
├── app.py                          # Streamlit web application
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /Users/ethanwhite/Desktop/AI-Staffing
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Mac/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Streamlit server:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser:**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in the terminal

## 📊 Usage Guide

### 1. Dashboard (Home)
- View key metrics: total employees, projects, hours billed, and revenue
- Visualize hours by industry and staff distribution by role
- See recent deliverables

### 2. Employee Directory
- **Filters**: Skills, role, location, job title
- **View**: Detailed employee profiles with resume and project history
- **Example**: Find all employees with "Python" and "CV" skills in "Texas"

### 3. Projects Dashboard
- **Filters**: Client, industry, technology, dollar amount
- **View**: Project details, team members, and deliverables
- **Visualizations**: Revenue charts and project comparisons

### 4. Billing & Time Tracking
- **By Employee**: See all hours billed by each employee across projects
- **By Project**: View team composition and hours for each project
- **By Year**: Analyze billing trends over time

### 5. Resume & Skills Matrix
- **Individual Resumes**: Complete employee profiles with education, certifications, and experience
- **Skills Overview**: Distribution of skills across the organization
- **Project History**: See which projects each employee has worked on

### 6. Deliverables Tracker
- **Filters**: Project, topic area, client, technology
- **View**: All deliverables with completion dates and codebases
- **Visualizations**: Deliverables by topic area and client

### 7. Analytics & Reports
- **Industry Analysis**: Total hours and revenue by industry/client
- **Skills Analysis**: Staff distribution by skill
- **Role Distribution**: Employee count by role

### 8. Complex Search
Advanced multi-criteria search combining:
- Skills (e.g., Python, OpenCV, TensorFlow)
- Location (e.g., Texas, Austin)
- Role (e.g., Senior Engineer, Division Director)
- Client experience (e.g., Federal DHS)
- Industry experience (e.g., Law Enforcement)
- Years of experience

**Example Searches:**
- "Find all senior Python engineers in Texas who worked on law enforcement projects"
- "List employees with computer vision skills and Federal client experience"
- "Show data science leaders with 5+ years experience"

## 🔧 Technical Details

### Database Module (`database.py`)
- Uses SQLite in-memory database for fast operations
- Pandas DataFrames for data manipulation
- Implements proper foreign key relationships
- Provides query methods for all dashboard views

### Key Methods:
- `get_employee_directory()`: Filtered employee search
- `get_projects_dashboard()`: Project filtering and display
- `get_billing_by_employee()`: Employee billing history
- `get_billing_by_project()`: Project billing details
- `get_resume_matrix()`: Employee resume information
- `get_deliverables_tracker()`: Deliverable filtering
- `get_analytics_by_industry()`: Industry-level analytics
- `complex_search()`: Advanced multi-criteria search

### Web Application (`app.py`)
- Built with Streamlit for rapid development
- Interactive filters and visualizations
- Plotly charts for data visualization
- Responsive layout with tabs and columns
- Export functionality for search results

## 🔮 Future Enhancements

### Recommended Features:
1. **Resume Parsing Automation**
   - Integrate with resume parsing APIs (e.g., Affinda, Sovren)
   - Extract skills, education, and experience automatically
   - Update database with parsed information

2. **LinkedIn Enrichment**
   - Use LinkedIn API to fetch updated profile data
   - Sync skills and experience automatically
   - Track endorsements and recommendations

3. **Advanced Analytics**
   - Predictive analytics for resource allocation
   - Skills gap analysis
   - Employee utilization rates
   - Revenue forecasting

4. **Integration Options**
   - Export to Excel/PDF reports
   - API endpoints for external systems
   - Email notifications for milestones
   - Calendar integration for project timelines

5. **Machine Learning**
   - Employee-project matching recommendations
   - Skill development suggestions
   - Project success prediction
   - Anomaly detection in billing

## 📝 Data Schema

### employees.csv
- **Primary Key**: Employee_ID
- **Foreign Key**: Role_ID → roles.Role_ID
- Fields: Name, Email, Job_Title, Location, Skills, LinkedIn_URL

### roles.csv
- **Primary Key**: Role_ID
- Fields: Standard_Role, Role_Title_Variants

### projects.csv
- **Primary Key**: Billing_Code
- Fields: Project_Name, Client, Industry, Technologies, Dollar_Amount, Project_Scope

### billing.csv
- **Foreign Keys**: 
  - Employee_ID → employees.Employee_ID
  - Billing_Code → projects.Billing_Code
- Fields: Year, Hours_Billed, Role_in_Project

### resume_data.csv
- **Foreign Key**: Employee_ID → employees.Employee_ID
- Fields: Education, Experience, Certifications, Summary

### deliverables.csv
- **Foreign Key**: Billing_Code → projects.Billing_Code
- Fields: Deliverable, Date_Completed, Topic_Area, Technologies, Client, Codebase

## 🛠️ Customization

### Adding New Data
1. Update CSV files in the `Data/` folder
2. Ensure proper column names match the schema
3. Restart the Streamlit app to reload data

### Modifying Filters
Edit the filter sections in `app.py` for each page to add/remove filter options.

### Adding New Views
1. Add a new page option in the sidebar navigation
2. Create a new section with `elif page == "Your Page":`
3. Implement filters and display logic

### Styling
Modify the CSS in the `st.markdown()` section at the top of `app.py` to customize colors, fonts, and layout.

## 📄 License

This project is provided as-is for internal company use.

## 🤝 Support

For questions or issues:
1. Check the code comments in `database.py` and `app.py`
2. Review the Streamlit documentation: https://docs.streamlit.io
3. Review the Pandas documentation: https://pandas.pydata.org

## 🎉 Credits

Built with:
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **SQLite**: In-memory relational database
