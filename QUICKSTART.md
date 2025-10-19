# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Run Setup
```bash
cd /Users/ethanwhite/Desktop/AI-Staffing
./setup.sh
```

This will:
- Create a virtual environment
- Install all required dependencies (Streamlit, Pandas, Plotly)

### Step 2: Launch the Application
```bash
./run.sh
```

Or manually:
```bash
source venv/bin/activate
streamlit run app.py
```

### Step 3: Open Your Browser
The app will automatically open at: **http://localhost:8501**

---

## 📋 What You Can Do

### 1. **Employee Directory** 👥
Find employees by:
- Skills (Python, CV, SQL, etc.)
- Role (Director, Engineer, etc.)
- Location (Austin, Dallas, Houston)
- Job Title

**Example**: Find all Python engineers in Texas
- Go to "Employee Directory"
- Select Skills: Python
- Select Location: Texas
- View results with full profiles

### 2. **Projects Dashboard** 📊
View projects by:
- Client (TX Sheriff's Dept, NYC Police, Federal DHS)
- Industry (Law Enforcement, Government)
- Technology (Python, OpenCV, PyTorch)
- Dollar Amount

**Example**: See all Federal projects over $200K
- Go to "Projects"
- Select Client: Federal DHS
- Set Min Dollar Amount: 200000
- View project details and team

### 3. **Billing & Time Tracking** ⏰
Track hours:
- By Employee: See all projects an employee worked on
- By Project: See all team members on a project
- By Year: Analyze trends over time

**Example**: How many hours did Alice Ward bill in 2025?
- Go to "Billing & Time Tracking"
- Tab: "By Employee"
- Select: 10001 - Alice Ward
- View breakdown by project

### 4. **Resume & Skills Matrix** 📄
View:
- Individual employee resumes with education, certifications, experience
- Skills distribution across the organization
- Project history for each employee

**Example**: View Carol Singh's complete profile
- Go to "Resume & Skills Matrix"
- Select: 10003 - Carol Singh
- See education (PhD AI), certifications (AWS DevOps), and project history

### 5. **Deliverables Tracker** 📦
Monitor:
- All deliverables by project
- Completion dates
- Topic areas (Computer Vision, Surveillance, Identification)
- Technologies and codebases

**Example**: Find all Computer Vision deliverables
- Go to "Deliverables"
- Select Topic Area: Computer Vision
- View Facial Rec API and other CV deliverables

### 6. **Analytics & Reports** 📈
Analyze:
- Hours and revenue by industry/client
- Staff distribution by skill
- Employee count by role

**Example**: Which industry generates the most revenue?
- Go to "Analytics & Reports"
- Tab: "Industry Analysis"
- View charts showing Law Enforcement projects

### 7. **Complex Search** 🔍
Advanced queries combining multiple criteria:

**Example 1**: Senior Python engineers in Texas who worked on law enforcement
- Go to "Complex Search"
- Skills: Python
- Role: Senior Engineer
- Location: Texas
- Industry Experience: Law Enforcement
- Click "Search"

**Example 2**: Computer vision experts with Federal experience
- Skills: CV, OpenCV
- Client Experience: Federal
- Click "Search"

**Example 3**: Use quick search buttons for common queries

---

## 🎯 Sample Queries to Try

1. **Find Python experts in Houston**
   - Employee Directory → Skills: Python, Location: Houston

2. **Show all projects for NYC Police**
   - Projects → Client: NYC Police

3. **How many hours on TX Facial Rec project?**
   - Billing → By Project → PC-001

4. **Who has AWS certifications?**
   - Resume & Skills Matrix → Search for "AWS" in certifications

5. **All deliverables completed in 2025**
   - Deliverables → View all, sort by Date_Completed

6. **Which skills are most common?**
   - Analytics & Reports → Skills Analysis

7. **Find all Division Directors**
   - Employee Directory → Role: Division Director

8. **Projects using PyTorch**
   - Projects → Technology: PyTorch

---

## 💡 Tips

- **Export Results**: Use the download button in Complex Search to export results as CSV
- **Multiple Filters**: Combine filters for more specific results
- **Visual Analytics**: Check the charts and graphs for quick insights
- **Employee Details**: Click on any employee to see their full profile and project history
- **Project Teams**: Select a project to see all team members and their roles

---

## 🔧 Troubleshooting

**App won't start?**
```bash
# Make sure you're in the right directory
cd /Users/ethanwhite/Desktop/AI-Staffing

# Activate virtual environment
source venv/bin/activate

# Try running directly
streamlit run app.py
```

**Missing dependencies?**
```bash
pip install -r requirements.txt
```

**Port already in use?**
```bash
streamlit run app.py --server.port 8502
```

---

## 📚 Learn More

- Full documentation: See `README.md`
- Code details: Check `database.py` for all query methods
- Customize: Edit `app.py` to add new features

---

## 🎉 You're Ready!

Start exploring your workforce data with powerful analytics and insights!
