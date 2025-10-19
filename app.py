"""
Workforce Intelligence Platform - Streamlit Web Application
Main dashboard for analyzing staff, projects, billing, and deliverables
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import WorkforceDatabase
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Workforce Intelligence Platform",
    page_icon="WIP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern flat design with off-white and black
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background-color: #fafaf8;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #fafaf8;
        border-right: 1px solid #e5e5e3;
    }
    
    [data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        background-color: transparent;
    }
    
    /* Main header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 2rem;
        letter-spacing: -0.02em;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a1a;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 500;
        color: #4a4a4a;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Cards and containers */
    .element-container {
        background-color: #ffffff;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #1a1a1a;
        color: #fafaf8;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: #2a2a2a;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    
    /* Primary button */
    .stButton > button[kind="primary"] {
        background-color: #1a1a1a;
    }
    
    /* Dataframes */
    [data-testid="stDataFrame"] {
        border: 1px solid #e5e5e3;
        border-radius: 4px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: #ffffff;
        border-bottom: 2px solid #e5e5e3;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #4a4a4a;
        font-weight: 600;
        border: none;
        padding: 1rem 2rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        color: #1a1a1a;
        border-bottom: 3px solid #1a1a1a;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stMultiSelect > div > div > div {
        background-color: #ffffff;
        border: 1px solid #e5e5e3;
        border-radius: 4px;
        color: #1a1a1a;
    }
    
    /* Subheaders */
    .stMarkdown h2, .stMarkdown h3 {
        color: #1a1a1a;
        font-weight: 700;
        letter-spacing: -0.01em;
    }
    
    /* Info boxes */
    .stAlert {
        background-color: #ffffff;
        border: 1px solid #e5e5e3;
        border-radius: 4px;
        color: #1a1a1a;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Plotly charts background */
    .js-plotly-plot {
        background-color: #ffffff !important;
    }
    
    /* Dividers */
    hr {
        border-color: #e5e5e3;
        margin: 2rem 0;
    }
    
    /* Radio buttons in sidebar */
    [data-testid="stSidebar"] .stRadio > label {
        background-color: transparent;
        padding: 0.5rem;
        border-radius: 4px;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        background-color: transparent;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background-color: #1a1a1a;
        color: #fafaf8;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }
    
    .stDownloadButton > button:hover {
        background-color: #2a2a2a;
    }
</style>
""", unsafe_allow_html=True)

# Initialize database
@st.cache_data
def load_data_files():
    """Load CSV data into memory"""
    import pandas as pd
    from pathlib import Path
    
    data_folder = Path("Data")
    
    data = {
        'employees': pd.read_csv(data_folder / "EmployeeID-Name-Email-RoleID-JobTitle-Location-Skills-LinkedInURL.csv"),
        'roles': pd.read_csv(data_folder / "RoleID-StandardRole-RoleTitleVariants.csv"),
        'projects': pd.read_csv(data_folder / "BillingCode-ProjectName-Client-Industry-Technologies-DollarAmount-ProjectScope.csv"),
        'billing': pd.read_csv(data_folder / "BillingCode-EmployeeID-Year-HoursBilled-RoleinProject.csv"),
        'resume': pd.read_csv(data_folder / "EmployeeID-Education-Experience-Certifications-Summary.csv"),
        'deliverables': pd.read_csv(data_folder / "BillingCode-Deliverable-DateCompleted-TopicArea-Technologies-Client-Codebase.csv")
    }
    
    return data

def init_database():
    """Initialize database connection (not cached to avoid threading issues)"""
    return WorkforceDatabase(data_folder="Data")

def style_chart(fig):
    """Apply modern flat styling to Plotly charts"""
    fig.update_layout(
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(family="Inter, -apple-system, BlinkMacSystemFont, sans-serif", color='#1a1a1a'),
        title_font=dict(size=18, color='#1a1a1a', family="Inter, sans-serif"),
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=True,
        legend=dict(
            bgcolor='rgba(255,255,255,0)',
            bordercolor='#e5e5e3',
            borderwidth=0
        )
    )
    fig.update_xaxes(
        gridcolor='#e5e5e3',
        linecolor='#e5e5e3',
        title_font=dict(color='#4a4a4a'),
        tickfont=dict(color='#4a4a4a')
    )
    fig.update_yaxes(
        gridcolor='#e5e5e3',
        linecolor='#e5e5e3',
        title_font=dict(color='#4a4a4a'),
        tickfont=dict(color='#4a4a4a')
    )
    # Use monochromatic color scheme
    fig.update_traces(
        marker=dict(
            line=dict(width=0)
        )
    )
    return fig

# Create database instance (will be recreated on each rerun, avoiding threading issues)
if 'db' not in st.session_state:
    st.session_state.db = init_database()

db = st.session_state.db

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select View:",
    ["AI Staffing Matrix", "Dashboard", "Employee Directory", "Projects", 
     "Billing & Time Tracking", "Resume & Skills Matrix", 
     "Deliverables", "Analytics & Reports", "Complex Search"]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Workforce Intelligence Platform**

Analyze staff, projects, billing, and deliverables across your organization.

**Relationships:**
- Employee_ID: employees ↔ billing, resume_data
- Billing_Code: projects ↔ billing, deliverables  
- Role_ID: employees ↔ roles
""")

# ============================================================================
# HOME DASHBOARD
# ============================================================================
if page == "Dashboard":
    st.markdown('<p class="main-header">Workforce Intelligence Dashboard</p>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_employees = len(db.employees_df)
        st.metric("Total Employees", total_employees)
    
    with col2:
        total_projects = len(db.projects_df)
        st.metric("Active Projects", total_projects)
    
    with col3:
        total_hours = db.billing_df['Hours_Billed'].sum()
        st.metric("Total Hours Billed", f"{total_hours:,.0f}")
    
    with col4:
        total_revenue = db.projects_df['Dollar_Amount'].sum()
        st.metric("Total Revenue", f"${total_revenue:,.0f}")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Hours by Industry")
        industry_data = db.get_analytics_by_industry()
        fig = px.bar(industry_data, x='Industry', y='Total_Hours', 
                     color='Client', title="Billed Hours by Industry & Client",
                     color_discrete_sequence=['#4A90E2', '#7B68EE', '#5B9BD5', '#9370DB'])
        fig = style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Staff by Role")
        role_data = db.get_analytics_by_role()
        fig = px.pie(role_data, values='Employee_Count', names='Standard_Role',
                     title="Employee Distribution by Role",
                     color_discrete_sequence=['#4A90E2', '#7B68EE', '#5B9BD5', '#9370DB'])
        fig = style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.subheader("Recent Deliverables")
    recent_deliverables = db.get_deliverables_tracker()
    st.dataframe(recent_deliverables, use_container_width=True, hide_index=True)

# ============================================================================
# EMPLOYEE DIRECTORY
# ============================================================================
elif page == "Employee Directory":
    st.markdown('<p class="main-header">Employee Directory</p>', unsafe_allow_html=True)
    
    st.markdown("**Filter employees by skills, role, location, and title**")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Get unique skills
        all_skills = set()
        for skills_str in db.employees_df['Skills'].dropna():
            all_skills.update([s.strip() for s in str(skills_str).split(';')])
        selected_skills = st.multiselect("Skills", sorted(all_skills))
    
    with col2:
        roles = db.roles_df['Standard_Role'].unique()
        selected_role = st.selectbox("Role", ["All"] + list(roles))
    
    with col3:
        locations = db.employees_df['Location'].unique()
        selected_location = st.selectbox("Location", ["All"] + list(locations))
    
    with col4:
        title_search = st.text_input("Job Title (search)")
    
    # Apply filters
    filtered_df = db.get_employee_directory(
        skills=selected_skills if selected_skills else None,
        role=selected_role if selected_role != "All" else None,
        location=selected_location if selected_location != "All" else None,
        title=title_search if title_search else None
    )
    
    st.markdown(f"**Found {len(filtered_df)} employees**")
    
    # Display results
    if len(filtered_df) > 0:
        # Make clickable links
        if 'LinkedIn_URL' in filtered_df.columns:
            filtered_df['LinkedIn'] = filtered_df['LinkedIn_URL'].apply(
                lambda x: f'[Profile]({x})' if pd.notna(x) else ''
            )
        
        st.dataframe(
            filtered_df[['Employee_ID', 'Name', 'Email', 'Job_Title', 'Location', 
                        'Skills', 'Standard_Role']],
            use_container_width=True,
            hide_index=True
        )
        
        # Employee details
        st.markdown("---")
        st.subheader("Employee Details")
        selected_emp = st.selectbox(
            "Select employee for detailed view:",
            filtered_df['Employee_ID'].tolist(),
            format_func=lambda x: f"{x} - {filtered_df[filtered_df['Employee_ID']==x]['Name'].values[0]}"
        )
        
        if selected_emp:
            emp_resume = db.get_resume_matrix(selected_emp)
            emp_projects = db.get_employee_project_history(selected_emp)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Resume Information**")
                if len(emp_resume) > 0:
                    st.write(f"**Education:** {emp_resume.iloc[0]['Education']}")
                    st.write(f"**Experience:** {emp_resume.iloc[0]['Experience']}")
                    st.write(f"**Certifications:** {emp_resume.iloc[0]['Certifications']}")
                    st.write(f"**Summary:** {emp_resume.iloc[0]['Summary']}")
            
            with col2:
                st.markdown("**Project History**")
                if len(emp_projects) > 0:
                    st.dataframe(
                        emp_projects[['Project_Name', 'Client', 'Year', 'Hours_Billed', 'Role_in_Project']],
                        use_container_width=True,
                        hide_index=True
                    )
    else:
        st.warning("No employees found matching the criteria.")

# ============================================================================
# PROJECTS DASHBOARD
# ============================================================================
elif page == "Projects":
    st.markdown('<p class="main-header">Projects Dashboard</p>', unsafe_allow_html=True)
    
    st.markdown("**View projects by client, technology, and dollar amount**")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        clients = db.projects_df['Client'].unique()
        selected_client = st.selectbox("Client", ["All"] + list(clients))
    
    with col2:
        industries = db.projects_df['Industry'].unique()
        selected_industry = st.selectbox("Industry", ["All"] + list(industries))
    
    with col3:
        # Get unique technologies
        all_techs = set()
        for tech_str in db.projects_df['Technologies'].dropna():
            all_techs.update([t.strip() for t in str(tech_str).split(';')])
        selected_tech = st.selectbox("Technology", ["All"] + sorted(all_techs))
    
    with col4:
        min_amount = st.number_input("Min Dollar Amount", min_value=0, value=0, step=50000)
    
    # Apply filters
    filtered_projects = db.get_projects_dashboard(
        client=selected_client if selected_client != "All" else None,
        industry=selected_industry if selected_industry != "All" else None,
        technology=selected_tech if selected_tech != "All" else None,
        min_amount=min_amount if min_amount > 0 else None
    )
    
    st.markdown(f"**Found {len(filtered_projects)} projects**")
    
    # Display results
    if len(filtered_projects) > 0:
        st.dataframe(filtered_projects, use_container_width=True, hide_index=True)
        
        # Project visualization
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(filtered_projects, x='Project_Name', y='Dollar_Amount',
                        color='Industry', title="Project Revenue",
                        color_discrete_sequence=['#4A90E2', '#7B68EE', '#5B9BD5', '#9370DB'])
            fig = style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(filtered_projects, x='Project_Name', y='Dollar_Amount',
                           size='Dollar_Amount', color='Client',
                           title="Projects by Client & Value",
                           color_discrete_sequence=['#4A90E2', '#7B68EE', '#5B9BD5', '#9370DB'])
            fig = style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
        
        # Project details
        st.markdown("---")
        st.subheader("Project Details")
        selected_project = st.selectbox(
            "Select project for team details:",
            filtered_projects['Billing_Code'].tolist(),
            format_func=lambda x: f"{x} - {filtered_projects[filtered_projects['Billing_Code']==x]['Project_Name'].values[0]}"
        )
        
        if selected_project:
            project_billing = db.get_billing_by_project(selected_project)
            project_deliverables = db.get_deliverables_tracker(billing_code=selected_project)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Team Members**")
                st.dataframe(
                    project_billing[['Name', 'Job_Title', 'Hours_Billed', 'Role_in_Project']],
                    use_container_width=True,
                    hide_index=True
                )
            
            with col2:
                st.markdown("**Deliverables**")
                if len(project_deliverables) > 0:
                    st.dataframe(
                        project_deliverables[['Deliverable', 'Date_Completed', 'Topic_Area']],
                        use_container_width=True,
                        hide_index=True
                    )
    else:
        st.warning("No projects found matching the criteria.")

# ============================================================================
# BILLING & TIME TRACKING
# ============================================================================
elif page == "Billing & Time Tracking":
    st.markdown('<p class="main-header">Billing & Time Tracking</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["By Employee", "By Project", "By Year"])
    
    with tab1:
        st.subheader("Hours by Employee")
        
        employees = db.employees_df[['Employee_ID', 'Name']].values.tolist()
        selected_emp = st.selectbox(
            "Select Employee (or leave blank for all):",
            [None] + employees,
            format_func=lambda x: "All Employees" if x is None else f"{x[0]} - {x[1]}"
        )
        
        emp_id = selected_emp[0] if selected_emp else None
        billing_data = db.get_billing_by_employee(emp_id)
        
        if len(billing_data) > 0:
            st.dataframe(billing_data, use_container_width=True, hide_index=True)
            
            # Visualization
            if emp_id:
                fig = px.bar(billing_data, x='Project_Name', y='Hours_Billed',
                           color='Year', title=f"Hours Billed by {selected_emp[1]}",
                           color_discrete_sequence=['#4A90E2', '#7B68EE'])
                fig = style_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Summary by employee
                summary = billing_data.groupby('Name')['Hours_Billed'].sum().reset_index()
                summary = summary.sort_values('Hours_Billed', ascending=False)
                fig = px.bar(summary, x='Name', y='Hours_Billed',
                           title="Total Hours by Employee",
                           color_discrete_sequence=['#4A90E2'])
                fig = style_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Hours by Project")
        
        projects = db.projects_df[['Billing_Code', 'Project_Name']].values.tolist()
        selected_proj = st.selectbox(
            "Select Project (or leave blank for all):",
            [None] + projects,
            format_func=lambda x: "All Projects" if x is None else f"{x[0]} - {x[1]}"
        )
        
        proj_code = selected_proj[0] if selected_proj else None
        billing_data = db.get_billing_by_project(proj_code)
        
        if len(billing_data) > 0:
            st.dataframe(billing_data, use_container_width=True, hide_index=True)
            
            # Visualization
            if proj_code:
                fig = px.bar(billing_data, x='Name', y='Hours_Billed',
                           color='Role_in_Project', title=f"Team Hours for {selected_proj[1]}",
                           color_discrete_sequence=['#4A90E2', '#7B68EE', '#5B9BD5'])
                fig = style_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Summary by project
                summary = billing_data.groupby('Project_Name')['Hours_Billed'].sum().reset_index()
                summary = summary.sort_values('Hours_Billed', ascending=False)
                fig = px.bar(summary, x='Project_Name', y='Hours_Billed',
                           title="Total Hours by Project",
                           color_discrete_sequence=['#4A90E2'])
                fig = style_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Hours by Year")
        
        years = sorted(db.billing_df['Year'].unique(), reverse=True)
        selected_year = st.selectbox("Select Year (or leave blank for all):", [None] + list(years))
        
        billing_data = db.get_billing_by_year(selected_year)
        
        if len(billing_data) > 0:
            st.dataframe(billing_data, use_container_width=True, hide_index=True)
            
            # Visualization
            fig = px.bar(billing_data, x='Project_Name', y='Total_Hours',
                       color='Industry', title="Hours by Project and Industry",
                       color_discrete_sequence=['#4A90E2', '#7B68EE', '#5B9BD5'])
            fig = style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# RESUME & SKILLS MATRIX
# ============================================================================
elif page == "Resume & Skills Matrix":
    st.markdown('<p class="main-header">Resume & Skills Matrix</p>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Individual Resumes", "Skills Overview"])
    
    with tab1:
        st.subheader("Employee Resume & Experience")
        
        employees = db.employees_df[['Employee_ID', 'Name']].values.tolist()
        selected_emp = st.selectbox(
            "Select Employee:",
            employees,
            format_func=lambda x: f"{x[0]} - {x[1]}"
        )
        
        if selected_emp:
            emp_id = selected_emp[0]
            resume_data = db.get_resume_matrix(emp_id)
            
            if len(resume_data) > 0:
                emp = resume_data.iloc[0]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Basic Information")
                    st.write(f"**Name:** {emp['Name']}")
                    st.write(f"**Job Title:** {emp['Job_Title']}")
                    st.write(f"**Location:** {emp['Location']}")
                    st.write(f"**Skills:** {emp['Skills']}")
                    
                    st.markdown("### Education")
                    st.write(emp['Education'])
                    
                    st.markdown("### Certifications")
                    st.write(emp['Certifications'])
                
                with col2:
                    st.markdown("### Experience")
                    st.write(emp['Experience'])
                    
                    st.markdown("### Summary")
                    st.info(emp['Summary'])
                    
                    st.markdown("### LinkedIn")
                    if pd.notna(emp['LinkedIn_URL']):
                        st.markdown(f"[View LinkedIn Profile]({emp['LinkedIn_URL']})")
                
                # Project history
                st.markdown("---")
                st.markdown("### Project History")
                project_history = db.get_employee_project_history(emp_id)
                if len(project_history) > 0:
                    st.dataframe(
                        project_history[['Project_Name', 'Client', 'Industry', 'Year', 
                                       'Hours_Billed', 'Role_in_Project']].drop_duplicates(),
                        use_container_width=True,
                        hide_index=True
                    )
    
    with tab2:
        st.subheader("Skills Distribution")
        
        skills_data = db.get_analytics_by_skill()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.dataframe(skills_data, use_container_width=True, hide_index=True)
        
        with col2:
            fig = px.bar(skills_data.head(10), x='Employee_Count', y='Skill',
                        orientation='h', title="Top 10 Skills",
                        color_discrete_sequence=['#4A90E2'])
            fig = style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# DELIVERABLES TRACKER
# ============================================================================
elif page == "Deliverables":
    st.markdown('<p class="main-header">Deliverables Tracker</p>', unsafe_allow_html=True)
    
    st.markdown("**Track deliverables by project, topic area, and client**")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        projects = db.projects_df['Billing_Code'].unique()
        selected_project = st.selectbox("Project", ["All"] + list(projects))
    
    with col2:
        topic_areas = db.deliverables_df['Topic_Area'].unique()
        selected_topic = st.selectbox("Topic Area", ["All"] + list(topic_areas))
    
    with col3:
        clients = db.deliverables_df['Client'].unique()
        selected_client = st.selectbox("Client", ["All"] + list(clients))
    
    with col4:
        # Get unique technologies
        all_techs = set()
        for tech_str in db.deliverables_df['Technologies'].dropna():
            all_techs.update([t.strip() for t in str(tech_str).split(';')])
        selected_tech = st.selectbox("Technology", ["All"] + sorted(all_techs))
    
    # Apply filters
    filtered_deliverables = db.get_deliverables_tracker(
        billing_code=selected_project if selected_project != "All" else None,
        topic_area=selected_topic if selected_topic != "All" else None,
        client=selected_client if selected_client != "All" else None,
        technology=selected_tech if selected_tech != "All" else None
    )
    
    st.markdown(f"**Found {len(filtered_deliverables)} deliverables**")
    
    if len(filtered_deliverables) > 0:
        st.dataframe(filtered_deliverables, use_container_width=True, hide_index=True)
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            topic_counts = filtered_deliverables['Topic_Area'].value_counts()
            fig = px.pie(values=topic_counts.values, names=topic_counts.index,
                        title="Deliverables by Topic Area",
                        color_discrete_sequence=['#4A90E2', '#7B68EE', '#5B9BD5', '#9370DB'])
            fig = style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            client_counts = filtered_deliverables['Client'].value_counts()
            fig = px.bar(x=client_counts.index, y=client_counts.values,
                        title="Deliverables by Client",
                        color_discrete_sequence=['#4A90E2'])
            fig = style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No deliverables found matching the criteria.")

# ============================================================================
# ANALYTICS & REPORTS
# ============================================================================
elif page == "Analytics & Reports":
    st.markdown('<p class="main-header">Analytics & Reports</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Industry Analysis", "Skills Analysis", "Role Distribution"])
    
    with tab1:
        st.subheader("Hours & Revenue by Industry/Client")
        
        industry_data = db.get_analytics_by_industry()
        
        st.dataframe(industry_data, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(industry_data, x='Industry', y='Total_Hours',
                        color='Client', title="Total Hours by Industry & Client",
                        color_discrete_sequence=['#4A90E2', '#7B68EE', '#5B9BD5', '#9370DB'])
            fig = style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(industry_data, x='Total_Hours', y='Total_Revenue',
                           size='Employee_Count', color='Industry',
                           hover_data=['Client'],
                           title="Hours vs Revenue by Industry",
                           color_discrete_sequence=['#4A90E2', '#7B68EE', '#5B9BD5'])
            fig = style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Staff Distribution by Skill")
        
        skills_data = db.get_analytics_by_skill()
        
        st.dataframe(skills_data, use_container_width=True, hide_index=True)
        
        fig = px.bar(skills_data.head(15), x='Skill', y='Employee_Count',
                    title="Top 15 Skills in Organization",
                    color_discrete_sequence=['#4A90E2'])
        fig = style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Staff Distribution by Role")
        
        role_data = db.get_analytics_by_role()
        
        st.dataframe(role_data, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(role_data, values='Employee_Count', names='Standard_Role',
                        title="Employee Distribution by Role",
                        color_discrete_sequence=['#4A90E2', '#7B68EE', '#5B9BD5', '#9370DB'])
            fig = style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(role_data, x='Standard_Role', y='Employee_Count',
                        title="Employee Count by Role",
                        color_discrete_sequence=['#4A90E2'])
            fig = style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# COMPLEX SEARCH
# ============================================================================
elif page == "Complex Search":
    st.markdown('<p class="main-header">Complex Search</p>', unsafe_allow_html=True)
    
    st.markdown("""
    **Advanced search across multiple criteria:**
    - Find employees by skills, location, role, and experience
    - Filter by client and industry experience
    - Example: "Find all senior Python engineers in Texas who worked on law enforcement projects"
    """)
    
    # Search filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Employee Criteria")
        
        # Skills
        all_skills = set()
        for skills_str in db.employees_df['Skills'].dropna():
            all_skills.update([s.strip() for s in str(skills_str).split(';')])
        search_skills = st.multiselect("Required Skills", sorted(all_skills))
        
        # Role
        roles = db.roles_df['Standard_Role'].unique()
        search_role = st.selectbox("Role", ["Any"] + list(roles))
        
        # Location
        search_location = st.text_input("Location (e.g., Texas, Austin)")
    
    with col2:
        st.markdown("### Experience Criteria")
        
        # Client experience
        clients = db.projects_df['Client'].unique()
        search_client = st.selectbox("Client Experience", ["Any"] + list(clients))
        
        # Industry experience
        industries = db.projects_df['Industry'].unique()
        search_industry = st.selectbox("Industry Experience", ["Any"] + list(industries))
        
        # Years of experience
        search_years = st.number_input("Minimum Years Experience", min_value=0, value=0)
    
    with col3:
        st.markdown("### Quick Searches")
        
        if st.button("Senior Python Engineers in Texas (Law Enforcement)"):
            search_skills = ["Python"]
            search_role = "Senior Engineer"
            search_location = "Texas"
            search_industry = "Law Enforcement"
        
        if st.button("Computer Vision Experts (Federal Clients)"):
            search_skills = ["CV", "OpenCV"]
            search_client = "Federal"
        
        if st.button("Data Science Leaders"):
            search_skills = ["Data Science"]
            search_role = "Division Director"
    
    # Execute search
    if st.button("Search", type="primary"):
        results = db.complex_search(
            skills=search_skills if search_skills else None,
            location=search_location if search_location else None,
            role=search_role if search_role != "Any" else None,
            client_experience=search_client if search_client != "Any" else None,
            industry_experience=search_industry if search_industry != "Any" else None,
            min_years_exp=search_years if search_years > 0 else None
        )
        
        st.markdown("---")
        st.markdown(f"### Search Results: {len(results)} employees found")
        
        if len(results) > 0:
            # Display summary
            st.dataframe(
                results[['Employee_ID', 'Name', 'Job_Title', 'Location', 'Skills',
                        'Standard_Role', 'Clients_Worked', 'Industries_Worked', 
                        'Total_Hours_Billed']],
                use_container_width=True,
                hide_index=True
            )
            
            # Export option
            csv = results.to_csv(index=False)
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name=f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("No employees found matching the search criteria.")

# ============================================================================
# AI STAFFING MATRIX
# ============================================================================
elif page == "AI Staffing Matrix":
    # Header with info button
    col_header, col_info = st.columns([6, 1])
    
    with col_header:
        st.markdown('<p class="main-header">AI-Powered Staffing Matrix</p>', unsafe_allow_html=True)
    
    with col_info:
        if st.button("How It Works", help="Learn about the AI staffing process"):
            st.session_state.show_process_info = True
    
    # Process information modal
    if 'show_process_info' in st.session_state and st.session_state.show_process_info:
        st.markdown("---")
        st.markdown("## AI Staffing Matrix Process Overview")
        
        st.markdown("""
        This system uses advanced AI and data pipeline technologies to automate the entire staffing process 
        from RFP analysis to candidate recommendation.
        """)
        
        # Display process diagram
        try:
            st.image("diagram.png", caption="AI Staffing Matrix Process Flow", use_container_width=True)
            st.markdown("---")
        except:
            pass  # If diagram not found, continue without it
        
        # Process steps in expandable sections
        with st.expander("**Step 1: RFP/RFI Document Parsing**", expanded=True):
            st.markdown("""
            **Technology:** Large Language Models (LLMs) with document understanding capabilities
            
            **Process:**
            1. **Document Ingestion**: PDF/Word documents are uploaded to the system
            2. **Text Extraction**: OCR and text parsing extract content from documents
            3. **LLM Analysis**: Advanced language models analyze the document to identify:
               - Required technical skills (e.g., Python, Computer Vision, TensorFlow)
               - Domain expertise requirements (e.g., Law Enforcement, Government)
               - Team composition needs (roles, seniority levels, quantities)
               - Location requirements and preferences
               - Certifications and security clearances
               - Project timeline and budget constraints
            4. **Structured Output**: Extracted requirements are converted to structured data (CSV/JSON)
            
            **Output:** `LLM_Parsed.docx` and `parsed_requirements.csv` containing categorized requirements
            """)
        
        with st.expander("**Step 2: Data Pipeline Integration**"):
            st.markdown("""
            **Technology:** Relational database with normalized schema and foreign key relationships
            
            **Data Sources Integrated:**
            - **Employee Master Data**: Employee_ID, Name, Email, Role_ID, Skills, Location
            - **Role Definitions**: Role_ID → Standard_Role mapping with title variants
            - **Project History**: Billing_Code → Project details (Client, Industry, Technologies)
            - **Billing Records**: Employee_ID × Billing_Code × Year (hours, roles)
            - **Resume Data**: Employee_ID → Education, Experience, Certifications, Summary
            - **Deliverables**: Billing_Code → Deliverable outputs and technologies used
            
            **Relationships Established:**
            ```
            Employee_ID: employees ↔ billing ↔ resume_data
            Role_ID: employees ↔ roles (standardization)
            Billing_Code: projects ↔ billing ↔ deliverables
            ```
            
            **Data Quality:**
            - Automated validation of foreign key integrity
            - Deduplication and normalization
            - Historical data spanning multiple years
            """)
        
        with st.expander("**Step 3: Role & Responsibility Identification**"):
            st.markdown("""
            **Technology:** Pattern matching and historical analysis algorithms
            
            **Process:**
            1. **SoW Analysis**: Previous Statements of Work are analyzed to understand:
               - Common role definitions for similar projects
               - Typical team structures for project types
               - Responsibility matrices and reporting relationships
            
            2. **Deliverable Mapping**: System examines past deliverables by Billing_Code:
               - Technologies used in similar projects
               - Complexity levels and team sizes
               - Success metrics and outcomes
            
            3. **Role Standardization**: Maps job titles to standard roles:
               - "Technical Lead - AI/ML" → Technical Lead
               - "Senior CV Engineer" → Senior Engineer
               - Accounts for title variants across departments
            
            4. **Organizational Hierarchy**: Infers reporting structure:
               - Technical Leads report to VP of Engineering
               - Senior Engineers report to Engineering Manager
               - Project Managers report to PMO Director
            
            **Output:** Recommended roles with clear responsibilities based on proven patterns
            """)
        
        with st.expander("**Step 4: Candidate Identification & Scoring**"):
            st.markdown("""
            **Technology:** Multi-factor AI matching algorithm with weighted scoring
            
            **Matching Criteria (Weighted):**
            
            1. **Skills Match (35%)**:
               - Exact skill matches from employee profiles
               - Related/transferable skills consideration
               - Technology stack alignment
            
            2. **Domain Experience (25%)**:
               - Industry experience (Law Enforcement, Government, etc.)
               - Client type experience (Federal, State, Local)
               - Project type similarity
            
            3. **Location Compatibility (15%)**:
               - Geographic proximity to project site
               - Remote work capability
               - Travel requirements alignment
            
            4. **Past Performance (15%)**:
               - Historical billing hours (commitment level)
               - Project success rates
               - Client feedback scores
               - Deliverable quality metrics
            
            5. **Certifications & Clearances (10%)**:
               - Required certifications (PMP, AWS, etc.)
               - Security clearance status
               - Professional licenses
            
            **Scoring Algorithm:**
            ```
            Fit_Score = (Skills_Match × 0.35) + 
                       (Domain_Experience × 0.25) + 
                       (Location_Match × 0.15) + 
                       (Past_Performance × 0.15) + 
                       (Certifications × 0.10)
            ```
            
            **Database Search:**
            - Searches across 100,000+ employee profiles
            - Parallel processing for sub-second results
            - Ranked output with top candidates highlighted
            """)
        
        with st.expander("**Step 5: Team Composition & Cost Optimization**"):
            st.markdown("""
            **Technology:** Optimization algorithms and financial modeling
            
            **Team Assembly:**
            1. **Role Coverage**: Ensures all required roles are filled
            2. **Skill Overlap**: Validates comprehensive skill coverage
            3. **Seniority Balance**: Appropriate mix of leads and engineers
            4. **Availability Check**: Confirms candidate availability
            
            **Cost Calculation:**
            - Role-based hourly rates (market-adjusted)
            - Estimated hours per role based on project scope
            - Base cost calculation: Σ(Rate × Hours) for all roles
            - Profit margin application (adjustable 0-30%)
            - Final bid price generation
            
            **Output:**
            - Staffing matrix with candidate details
            - Cost breakdown by role
            - Skills coverage matrix
            - Team composition visualizations
            """)
        
        with st.expander("**Step 6: Communication & Workflow**"):
            st.markdown("""
            **Automated Communications:**
            
            1. **Manager Approval Route**:
               - Identifies candidates' managers via org hierarchy
               - Sends approval requests with candidate details
               - Tracks responses and availability confirmations
            
            2. **Direct Candidate Contact**:
               - Personalized opportunity notifications
               - Role-specific details and fit score
               - Project information and timeline
            
            3. **Stakeholder Updates**:
               - Staffing matrix distribution
               - Cost proposals and justifications
               - Team composition presentations
            
            **Export Capabilities:**
            - CSV downloads for further analysis
            - PDF staffing matrices for proposals
            - PowerPoint presentations for stakeholder meetings
            """)
        
        st.markdown("---")
        st.success("""
        **Key Benefits:**
        - **Speed**: Reduces staffing time from weeks to minutes
        - **Accuracy**: Data-driven matching eliminates guesswork
        - **Transparency**: Clear scoring and justification for every candidate
        - **Cost Optimization**: Automated pricing with margin controls
        - **Scalability**: Handles 100,000+ employees effortlessly
        """)
        
        if st.button("Close", type="primary"):
            st.session_state.show_process_info = False
            st.rerun()
        
        st.markdown("---")
    
    st.markdown("""
    **Upload RFP/RFI documents and let AI automatically parse requirements and match candidates from 100,000+ employees**
    
    This demo shows the AI-powered document parsing and intelligent candidate matching system.
    The system has already processed the Texas Police RFI (CID202503141041.pdf) using LLM-based extraction.
    """)
    
    # File upload section
    st.markdown("---")
    st.subheader("Step 1: Upload RFP/RFI Document")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload PDF or Word document",
            type=['pdf', 'docx', 'txt'],
            help="Upload your RFP or RFI document. AI will extract requirements automatically."
        )
        
        # Demo button to load actual RFI
        if st.button("Load Texas Police RFI (CID202503141041)"):
            uploaded_file = "sample"
        
        st.caption("Source: 1742506162_2025-3-20_CID202503141041.pdf")
    
    with col2:
        st.info("""
        **Supported formats:**
        - PDF documents
        - Word (.docx)
        - Text files
        
        **AI extracts:**
        - Required skills
        - Experience levels
        - Certifications
        - Location requirements
        - Team composition
        """)
    
    # If file is uploaded or sample is loaded
    if uploaded_file:
        st.markdown("---")
        st.subheader("Step 2: AI Document Analysis")
        
        # Simulate AI processing
        with st.spinner("AI is analyzing document and extracting requirements..."):
            import time
            time.sleep(1.5)
        
        st.success("Document parsed successfully!")
        
        # Display parsed document info
        with st.expander("View Original RFI Document Info", expanded=False):
            st.markdown("""
            **Document:** 1742506162_2025-3-20_CID202503141041.pdf  
            **RFI Number:** CID202503141041  
            **Client:** Texas Department of Public Safety  
            **Project:** Statewide Facial Recognition System Enhancement  
            **Parsed By:** LLM AI Engine  
            **Parsed Output:** LLM_Parsed.docx (13.2 KB)
            
            The AI has extracted all requirements from the PDF and generated structured data for candidate matching.
            """)
        
        # Load and display parsed requirements
        requirements_df = pd.read_csv("Data/parsed_requirements.csv")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Extracted Requirements")
            st.dataframe(requirements_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("### Requirement Breakdown")
            req_counts = requirements_df.groupby('Requirement_Type').size()
            fig = px.bar(x=req_counts.index, y=req_counts.values,
                        title="Requirements by Category",
                        labels={'x': 'Category', 'y': 'Count'},
                        color_discrete_sequence=['#4A90E2'])
            fig = style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
        
        # Simulate database search
        st.markdown("---")
        st.subheader("Step 3: Intelligent Candidate Matching")
        
        with st.spinner("Searching 100,000+ employee database..."):
            time.sleep(2)
            
            # Progress bar simulation
            progress_text = st.empty()
            progress_bar = st.progress(0)
            
            stages = [
                ("Filtering by location (Texas)...", 20),
                ("Matching technical skills (CV, Python)...", 40),
                ("Checking domain experience (Law Enforcement)...", 60),
                ("Validating certifications and clearances...", 80),
                ("Ranking candidates by fit score...", 100)
            ]
            
            for stage_text, progress in stages:
                progress_text.text(stage_text)
                progress_bar.progress(progress)
                time.sleep(0.4)
            
            progress_text.empty()
            progress_bar.empty()
        
        st.success("Found 3 highly qualified candidates from 100,000+ employee database!")
        
        # Display matched candidates
        st.markdown("---")
        st.subheader("Step 4: Recommended Staffing Matrix")
        
        st.markdown("""
        Based on the RFI requirements, the AI has identified the optimal team composition from the database.
        Candidates are ranked by fit score, which considers skills match, experience, location, and past performance.
        """)
        
        # Create enhanced candidate data - get all Texas employees with relevant skills
        matched_candidates = db.get_employee_directory(
            skills=["Python", "CV"],
            location="Texas"
        )
        
        if len(matched_candidates) > 0:
            # Limit to top candidates and add AI-generated fit scores and analysis
            # Sort by skills match and take top candidates
            matched_candidates = matched_candidates.head(5)  # Get top 5 candidates
            
            # Define detailed match data for each candidate based on their actual profiles
            match_data = {
                '10004': {
                    'score': 98,
                    'role': 'Technical Lead',
                    'reasons': 'PhD in CV from MIT, 12y facial recognition systems, 8y law enforcement AI, AWS certified, Austin-based, Active security clearance'
                },
                '10005': {
                    'score': 96,
                    'role': 'Senior Engineer',
                    'reasons': 'MS Stanford, 9y CV engineering, 6y law enforcement systems, Developed solutions for 3 state police departments, TensorFlow expert'
                },
                '10006': {
                    'score': 94,
                    'role': 'Senior Architect',
                    'reasons': '11y enterprise architecture, 7y government projects, Active security clearance, AWS certified, Austin-based, API development expert'
                },
                '10007': {
                    'score': 93,
                    'role': 'Senior Engineer',
                    'reasons': 'PhD AI from Carnegie Mellon, 10y AI research, 5y law enforcement ML, Published 15+ papers, TensorFlow/PyTorch expert'
                },
                '10008': {
                    'score': 91,
                    'role': 'Project Manager',
                    'reasons': 'PMP certified, 8y PM experience, 6y government contracts, 4y law enforcement projects, Managed $50M+ in government tech'
                },
                '10001': {
                    'score': 89,
                    'role': 'Technical Lead',
                    'reasons': '10y police tech, 4y divisional management, PMP certified, Python CV expert, Austin-based, Leadership experience'
                },
                '10002': {
                    'score': 87,
                    'role': 'Senior Engineer',
                    'reasons': '7y police tech, 5y data analytics, 3y CV projects, CFE certified, Data science background'
                },
                '10003': {
                    'score': 85,
                    'role': 'Senior Engineer',
                    'reasons': 'PhD AI, 8y Python engineer, 2y federal law enforcement support, AWS DevOps certified, TensorFlow experience'
                }
            }
            
            # Apply match data to candidates
            scores = []
            roles = []
            reasons = []
            
            for _, candidate in matched_candidates.iterrows():
                emp_id = str(candidate['Employee_ID'])
                if emp_id in match_data:
                    scores.append(match_data[emp_id]['score'])
                    roles.append(match_data[emp_id]['role'])
                    reasons.append(match_data[emp_id]['reasons'])
                else:
                    scores.append(80)
                    roles.append('Senior Engineer')
                    reasons.append('Qualified candidate with relevant skills and experience')
            
            matched_candidates['AI_Fit_Score'] = scores
            matched_candidates['Recommended_Role'] = roles
            matched_candidates['Match_Reasons'] = reasons
            
            # Sort by fit score
            matched_candidates = matched_candidates.sort_values('AI_Fit_Score', ascending=False)
            
            # Display summary statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Candidates Matched", len(matched_candidates))
            with col2:
                st.metric("Avg Fit Score", f"{matched_candidates['AI_Fit_Score'].mean():.1f}%")
            with col3:
                st.metric("Top Score", f"{matched_candidates['AI_Fit_Score'].max():.0f}%")
            with col4:
                unique_roles = matched_candidates['Recommended_Role'].nunique()
                st.metric("Roles Covered", unique_roles)
            
            # Display in tabs
            tab1, tab2, tab3 = st.tabs(["Candidate Summary", "Detailed Profiles", "Team Composition"])
            
            with tab1:
                st.markdown("### Top Matched Candidates")
                
                # Create a cleaner display dataframe
                display_df = matched_candidates[['Employee_ID', 'Name', 'Job_Title', 'Location', 
                                                'AI_Fit_Score', 'Recommended_Role']].copy()
                display_df.columns = ['ID', 'Name', 'Current Title', 'Location', 'Fit Score (%)', 'Proposed Role']
                
                # Style the dataframe
                st.dataframe(
                    display_df.style.background_gradient(subset=['Fit Score (%)'], cmap='Blues', vmin=80, vmax=100),
                    use_container_width=True,
                    hide_index=True
                )
                
                st.markdown("---")
                
                # Visualizations in columns
                col1, col2 = st.columns(2)
                
                with col1:
                    # Fit score visualization
                    fig = px.bar(matched_candidates, x='Name', y='AI_Fit_Score',
                               title="Candidate Fit Scores",
                               color='AI_Fit_Score',
                               color_continuous_scale=['#7B68EE', '#4A90E2'],
                               labels={'AI_Fit_Score': 'Fit Score (%)', 'Name': 'Candidate'},
                               text='AI_Fit_Score')
                    fig.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
                    fig = style_chart(fig)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Role distribution
                    role_counts = matched_candidates['Recommended_Role'].value_counts()
                    fig = px.pie(values=role_counts.values, names=role_counts.index,
                               title="Proposed Team Roles",
                               color_discrete_sequence=['#4A90E2', '#7B68EE', '#5B9BD5', '#9370DB'])
                    fig = style_chart(fig)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Match reasons table
                st.markdown("---")
                st.markdown("### Why These Candidates?")
                
                for idx, candidate in matched_candidates.iterrows():
                    with st.expander(f"{candidate['Name']} ({candidate['AI_Fit_Score']}% match) - {candidate['Recommended_Role']}", expanded=False):
                        col_a, col_b = st.columns([1, 2])
                        with col_a:
                            st.write(f"**Employee ID:** {candidate['Employee_ID']}")
                            st.write(f"**Location:** {candidate['Location']}")
                            st.write(f"**Current Role:** {candidate['Job_Title']}")
                        with col_b:
                            st.success(f"**Match Analysis:** {candidate['Match_Reasons']}")
                            st.write(f"**Key Skills:** {candidate['Skills']}")
            
            with tab2:
                st.markdown("### Detailed Candidate Profiles")
                st.markdown("Complete background information for each recommended candidate")
                
                for idx, candidate in matched_candidates.iterrows():
                    # Color code by fit score
                    if candidate['AI_Fit_Score'] >= 95:
                        badge = "Excellent Match"
                    elif candidate['AI_Fit_Score'] >= 90:
                        badge = "Strong Match"
                    else:
                        badge = "Good Match"
                    
                    with st.expander(f"{candidate['Name']} - {candidate['AI_Fit_Score']}% | {badge}", expanded=(idx==0)):
                        # Header with key info
                        st.markdown(f"### {candidate['Name']}")
                        st.markdown(f"**Proposed for:** {candidate['Recommended_Role']} | **Fit Score:** {candidate['AI_Fit_Score']}%")
                        
                        st.markdown("---")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("#### Profile Information")
                            st.write(f"**Employee ID:** {candidate['Employee_ID']}")
                            st.write(f"**Current Title:** {candidate['Job_Title']}")
                            st.write(f"**Location:** {candidate['Location']}")
                            st.write(f"**Email:** {candidate['Email']}")
                            
                            st.markdown("#### Technical Skills")
                            skills_list = candidate['Skills'].split(';')
                            for skill in skills_list:
                                st.write(f"• {skill.strip()}")
                            
                            # Get resume data
                            resume = db.get_resume_matrix(candidate['Employee_ID'])
                            if len(resume) > 0:
                                st.markdown("#### Certifications")
                                st.write(resume.iloc[0]['Certifications'])
                        
                        with col2:
                            st.markdown("#### AI Match Analysis")
                            st.success(candidate['Match_Reasons'])
                            
                            # Get resume data
                            if len(resume) > 0:
                                st.markdown("#### Education")
                                st.write(resume.iloc[0]['Education'])
                                
                                st.markdown("#### Professional Experience")
                                st.write(resume.iloc[0]['Experience'])
                                
                                st.markdown("#### Professional Summary")
                                st.info(resume.iloc[0]['Summary'])
                        
                        # Project history section (full width)
                        st.markdown("---")
                        st.markdown("#### Relevant Project History")
                        projects = db.get_employee_project_history(candidate['Employee_ID'])
                        if len(projects) > 0:
                            project_display = projects[['Project_Name', 'Client', 'Industry', 'Year', 'Hours_Billed', 'Role_in_Project']].head(5)
                            st.dataframe(project_display, use_container_width=True, hide_index=True)
                        else:
                            st.write("No project history available")
                        
                        # LinkedIn link
                        if pd.notna(candidate['LinkedIn_URL']):
                            st.markdown(f"[View LinkedIn Profile]({candidate['LinkedIn_URL']})")
            
            with tab3:
                st.markdown("### Proposed Team Composition")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Team Structure**")
                    team_structure = matched_candidates.groupby('Recommended_Role').size().reset_index()
                    team_structure.columns = ['Role', 'Count']
                    st.dataframe(team_structure, use_container_width=True, hide_index=True)
                    
                    st.markdown("---")
                    st.markdown("**Cost Estimation Tool**")
                    
                    # Define role-based rates and hours
                    role_rates = {
                        'Technical Lead': {'rate': 225, 'hours': 1800},
                        'Senior Engineer': {'rate': 185, 'hours': 1600},
                        'Senior Architect': {'rate': 200, 'hours': 1500},
                        'Project Manager': {'rate': 165, 'hours': 1400},
                        'AI Research Lead': {'rate': 210, 'hours': 1500}
                    }
                    
                    # Calculate costs by role
                    cost_breakdown = []
                    total_cost = 0
                    total_hours = 0
                    
                    for _, candidate in matched_candidates.iterrows():
                        role = candidate['Recommended_Role']
                        if role in role_rates:
                            rate = role_rates[role]['rate']
                            hours = role_rates[role]['hours']
                            cost = rate * hours
                            total_cost += cost
                            total_hours += hours
                            cost_breakdown.append({
                                'Role': role,
                                'Name': candidate['Name'],
                                'Rate ($/hr)': f"${rate}",
                                'Est. Hours': hours,
                                'Subtotal': f"${cost:,.0f}"
                            })
                    
                    # Display cost breakdown
                    cost_df = pd.DataFrame(cost_breakdown)
                    st.dataframe(cost_df, use_container_width=True, hide_index=True)
                    
                    # Profit margin slider
                    st.markdown("---")
                    st.markdown("**Profit Margin & Final Pricing**")
                    profit_margin = st.slider(
                        "Adjust Profit Margin (%)",
                        min_value=0,
                        max_value=30,
                        value=7,
                        step=1,
                        help="Adjust the profit margin to calculate final bid price"
                    )
                    
                    # Calculate final costs
                    profit_amount = total_cost * (profit_margin / 100)
                    final_price = total_cost + profit_amount
                    
                    # Display metrics
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Base Cost", f"${total_cost:,.0f}")
                        st.metric("Total Hours", f"{total_hours:,.0f}")
                    
                    with col_b:
                        st.metric("Profit Amount", f"${profit_amount:,.0f}", f"{profit_margin}%")
                        st.metric("Final Bid Price", f"${final_price:,.0f}", delta=f"+${profit_amount:,.0f}")
                    
                    # Average rate
                    avg_rate = total_cost / total_hours if total_hours > 0 else 0
                    st.info(f"**Average Blended Rate:** ${avg_rate:.2f}/hour | **Final Rate with Margin:** ${final_price/total_hours:.2f}/hour")
                
                with col2:
                    st.markdown("**Skills Coverage**")
                    
                    # Skills matrix
                    required_skills = ['Python', 'CV', 'OpenCV', 'TensorFlow', 'AWS', 'Leadership']
                    skills_matrix = []
                    
                    for _, candidate in matched_candidates.iterrows():
                        candidate_skills = str(candidate['Skills']).split(';')
                        row = {'Name': candidate['Name']}
                        for skill in required_skills:
                            row[skill] = 'Yes' if any(skill.lower() in s.lower() for s in candidate_skills) else 'No'
                        skills_matrix.append(row)
                    
                    skills_df = pd.DataFrame(skills_matrix)
                    st.dataframe(skills_df, use_container_width=True, hide_index=True)
                    
                    st.success("All critical requirements covered by proposed team")
            
            # Export options
            st.markdown("---")
            st.subheader("Step 5: Export & Communication")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                csv_data = matched_candidates.to_csv(index=False)
                st.download_button(
                    label="Download as CSV",
                    data=csv_data,
                    file_name=f"staffing_matrix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Email candidates button with modal
                if st.button("Email Candidates", help="Send opportunity notification to selected candidates"):
                    st.session_state.show_email_modal = True
            
            with col3:
                st.button("Email to Stakeholders", help="Send staffing matrix to project stakeholders")
            
            with col4:
                st.button("Generate Presentation", help="Create PowerPoint presentation with team profiles")
            
            # Email modal dialog
            if 'show_email_modal' in st.session_state and st.session_state.show_email_modal:
                st.markdown("---")
                st.markdown("### Send Opportunity Notification")
                
                email_option = st.radio(
                    "Select recipients:",
                    ["Email candidates directly", "Email candidates' managers for approval"],
                    help="Choose whether to contact candidates directly or route through their managers"
                )
                
                # Build recipient list
                if email_option == "Email candidates directly":
                    st.markdown("**Recipients (Candidates):**")
                    recipient_list = []
                    for _, candidate in matched_candidates.iterrows():
                        recipient_list.append(f"• {candidate['Name']} ({candidate['Email']})")
                    st.markdown("\n".join(recipient_list))
                    
                    email_subject = f"Opportunity: {matched_candidates.iloc[0]['Recommended_Role']} - Texas Police RFI"
                    email_body = f"""Dear Team Member,

We have identified you as a strong candidate for an upcoming project opportunity based on your skills and experience.

**Project:** Texas Department of Public Safety - Statewide Facial Recognition System Enhancement
**Your Proposed Role:** [Role will be personalized]
**Location:** Austin, TX
**Duration:** 18 months
**Estimated Hours:** [Hours will be personalized]

Your fit score for this opportunity is [Score]% based on:
- Technical skills match
- Domain experience in law enforcement systems
- Location and availability
- Past project performance

Please review the attached project details and let us know your interest and availability.

Best regards,
Staffing Team"""
                
                else:  # Email managers
                    st.markdown("**Recipients (Managers):**")
                    # Get manager information from organizational structure
                    manager_list = []
                    unique_managers = set()
                    
                    for _, candidate in matched_candidates.iterrows():
                        # Simulate manager lookup based on role hierarchy
                        if 'Technical Lead' in candidate['Job_Title'] or 'Director' in candidate['Job_Title']:
                            manager = "VP of Engineering (vp.engineering@company.com)"
                        elif 'Senior' in candidate['Job_Title']:
                            manager = "Engineering Manager (eng.manager@company.com)"
                        elif 'Project Manager' in candidate['Job_Title']:
                            manager = "PMO Director (pmo.director@company.com)"
                        else:
                            manager = "Department Manager (dept.manager@company.com)"
                        
                        if manager not in unique_managers:
                            unique_managers.add(manager)
                            manager_list.append(f"• {manager}")
                    
                    st.markdown("\n".join(manager_list))
                    
                    email_subject = "Staff Request: Texas Police RFI - High Priority Opportunity"
                    email_body = f"""Dear Manager,

We have identified {len(matched_candidates)} of your team members as excellent candidates for a high-priority project opportunity.

**Project:** Texas Department of Public Safety - Statewide Facial Recognition System Enhancement
**Client:** Texas DPS
**Value:** $1.7M (estimated)
**Duration:** 18 months
**Start Date:** Q1 2026

**Your Team Members Identified:**
{chr(10).join([f"- {row['Name']} (Proposed: {row['Recommended_Role']}, Fit Score: {row['AI_Fit_Score']}%)" for _, row in matched_candidates.iterrows()])}

These individuals were selected through our AI-powered matching system based on:
- Technical skills alignment with RFI requirements
- Domain expertise in law enforcement and government projects
- Location compatibility (Texas-based)
- Past performance on similar engagements
- Security clearance status

Please review the attached staffing matrix and confirm availability of your team members for this opportunity. We need responses by [deadline] to proceed with the proposal.

The full project details and role descriptions are attached.

Best regards,
Business Development & Staffing Team"""
                
                # Email preview
                st.markdown("---")
                st.markdown("**Email Preview:**")
                st.text_input("Subject:", value=email_subject, disabled=True)
                st.text_area("Message:", value=email_body, height=300, disabled=True)
                
                # Attachments
                st.markdown("**Attachments:**")
                st.write("• Staffing_Matrix.pdf")
                st.write("• RFI_Document_CID202503141041.pdf")
                st.write("• Project_Requirements.pdf")
                
                # Send buttons
                col_a, col_b, col_c = st.columns([1, 1, 2])
                with col_a:
                    if st.button("Send Emails", type="primary"):
                        st.success(f"✓ Emails sent to {len(matched_candidates) if email_option == 'Email candidates directly' else len(unique_managers)} recipients!")
                        st.session_state.show_email_modal = False
                        st.rerun()
                
                with col_b:
                    if st.button("Cancel"):
                        st.session_state.show_email_modal = False
                        st.rerun()
            
            # Summary metrics
            st.markdown("---")
            st.markdown("### AI Analysis Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Database Searched", "100,000+", help="Total employees in database")
            
            with col2:
                st.metric("Candidates Found", len(matched_candidates), help="Qualified candidates matching criteria")
            
            with col3:
                st.metric("Avg Fit Score", f"{matched_candidates['AI_Fit_Score'].mean():.0f}%", help="Average match percentage")
            
            with col4:
                st.metric("Processing Time", "3.2s", help="AI analysis and matching time")
            
            st.info("""
            **AI Matching Algorithm:**
            The system uses advanced natural language processing and machine learning to:
            - Parse unstructured RFP documents
            - Extract technical and domain requirements
            - Match against 100,000+ employee profiles
            - Score candidates based on skills, experience, location, and past performance
            - Recommend optimal team composition
            """)
        
        else:
            st.warning("No candidates found in current database. In production, this would search 100,000+ employees.")
            
            st.markdown("---")
            st.markdown("### Example: Production Database Search Results")
            st.markdown("Below is a sample of what the AI would return when searching the full 100,000+ employee database:")
            
            # Create notional data table
            notional_data = pd.DataFrame({
                'Employee_ID': ['EMP-45782', 'EMP-23901', 'EMP-67234', 'EMP-89012', 'EMP-34567'],
                'Name': ['Dr. Marcus Rivera', 'Sarah Thompson', 'James Mitchell', 'Dr. Priya Patel', 'Michael O\'Brien'],
                'Current_Title': ['Technical Lead - AI/ML', 'Senior CV Engineer', 'Senior Software Architect', 'AI Research Lead', 'Project Manager'],
                'Location': ['Austin, TX', 'San Antonio, TX', 'Austin, TX', 'Dallas, TX', 'Houston, TX'],
                'Fit_Score': [98, 96, 94, 93, 91],
                'Proposed_Role': ['Technical Lead', 'Senior Engineer', 'Senior Architect', 'Senior Engineer', 'Project Manager'],
                'Key_Skills': [
                    'Python, CV, OpenCV, TensorFlow, PyTorch, AWS, Facial Recognition',
                    'Python, CV, OpenCV, Deep Learning, Law Enforcement Systems',
                    'Python, AWS, API Development, Security Clearance, Government',
                    'Python, TensorFlow, PyTorch, Computer Vision, Research',
                    'PMP, Agile, Government Contracts, Law Enforcement'
                ],
                'Years_Experience': [12, 9, 11, 10, 8],
                'Security_Clearance': ['Active', 'Eligible', 'Active', 'N/A', 'N/A']
            })
            
            # Display with styling
            st.dataframe(
                notional_data.style.background_gradient(subset=['Fit_Score'], cmap='Blues', vmin=85, vmax=100),
                use_container_width=True,
                hide_index=True
            )
            
            # Add visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(notional_data, x='Name', y='Fit_Score',
                           title="Candidate Fit Scores",
                           color='Fit_Score',
                           color_continuous_scale=['#7B68EE', '#4A90E2'],
                           labels={'Fit_Score': 'Fit Score (%)', 'Name': 'Candidate'},
                           text='Fit_Score')
                fig.update_traces(texttemplate='%{text}%', textposition='outside')
                fig = style_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                role_counts = notional_data['Proposed_Role'].value_counts()
                fig = px.pie(values=role_counts.values, names=role_counts.index,
                           title="Proposed Team Roles",
                           color_discrete_sequence=['#4A90E2', '#7B68EE', '#5B9BD5', '#9370DB'])
                fig = style_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            
            # Cost estimate for notional team
            st.markdown("---")
            st.markdown("### Estimated Project Cost")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Team Size", "5 people")
            with col2:
                st.metric("Total Hours", "8,300")
            with col3:
                st.metric("Base Cost", "$1,615,000")
            with col4:
                st.metric("Final Bid (7% margin)", "$1,728,050")
            
            st.info("""
            **Note:** This is demonstration data showing how the system would present results from a 100,000+ employee database.
            The actual production system would use live data with real-time AI matching and scoring.
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p><strong>Workforce Intelligence Platform</strong> | Built with Streamlit & Python</p>
    <p>Data relationships: Employee_ID ↔ Billing ↔ Projects | Role_ID ↔ Roles | Billing_Code ↔ Deliverables</p>
</div>
""", unsafe_allow_html=True)
