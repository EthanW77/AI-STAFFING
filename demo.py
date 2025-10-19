"""
Demonstration script for Workforce Intelligence Platform
Shows key features and database relationships
"""

from database import WorkforceDatabase
import pandas as pd

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def main():
    print("\n🚀 Workforce Intelligence Platform - Demo\n")
    
    # Initialize database
    print("Initializing database...")
    db = WorkforceDatabase(data_folder="Data")
    print()
    
    # ========================================================================
    # DEMO 1: Employee Directory with Relationships
    # ========================================================================
    print_section("DEMO 1: Employee Directory (employees ↔ roles)")
    
    print("Finding all employees with Python skills:")
    employees = db.get_employee_directory(skills=["Python"])
    print(employees[['Employee_ID', 'Name', 'Job_Title', 'Location', 'Skills', 'Standard_Role']])
    print(f"\n✓ Found {len(employees)} employees with Python skills")
    
    # ========================================================================
    # DEMO 2: Projects Dashboard
    # ========================================================================
    print_section("DEMO 2: Projects Dashboard")
    
    print("All projects in Law Enforcement industry:")
    projects = db.get_projects_dashboard(industry="Law Enforcement")
    print(projects[['Billing_Code', 'Project_Name', 'Client', 'Technologies', 'Dollar_Amount']])
    print(f"\n✓ Found {len(projects)} Law Enforcement projects")
    print(f"✓ Total value: ${projects['Dollar_Amount'].sum():,.0f}")
    
    # ========================================================================
    # DEMO 3: Billing by Employee (employees ↔ billing ↔ projects)
    # ========================================================================
    print_section("DEMO 3: Billing by Employee (employees ↔ billing ↔ projects)")
    
    print("Hours billed by Alice Ward (Employee 10001):")
    billing = db.get_billing_by_employee(employee_id=10001)
    print(billing[['Name', 'Project_Name', 'Client', 'Year', 'Hours_Billed', 'Role_in_Project']])
    print(f"\n✓ Total hours: {billing['Hours_Billed'].sum():,.0f}")
    
    # ========================================================================
    # DEMO 4: Billing by Project (projects ↔ billing ↔ employees)
    # ========================================================================
    print_section("DEMO 4: Billing by Project (projects ↔ billing ↔ employees)")
    
    print("Team members on TX Facial Rec project (PC-001):")
    project_team = db.get_billing_by_project(billing_code="PC-001")
    print(project_team[['Project_Name', 'Name', 'Job_Title', 'Hours_Billed', 'Role_in_Project']])
    print(f"\n✓ Team size: {len(project_team)} members")
    print(f"✓ Total hours: {project_team['Hours_Billed'].sum():,.0f}")
    
    # ========================================================================
    # DEMO 5: Resume Matrix (employees ↔ resume_data)
    # ========================================================================
    print_section("DEMO 5: Resume Matrix (employees ↔ resume_data)")
    
    print("Resume for Carol Singh (Employee 10003):")
    resume = db.get_resume_matrix(employee_id=10003)
    if len(resume) > 0:
        emp = resume.iloc[0]
        print(f"Name: {emp['Name']}")
        print(f"Job Title: {emp['Job_Title']}")
        print(f"Location: {emp['Location']}")
        print(f"Skills: {emp['Skills']}")
        print(f"Education: {emp['Education']}")
        print(f"Experience: {emp['Experience']}")
        print(f"Certifications: {emp['Certifications']}")
        print(f"Summary: {emp['Summary']}")
    
    # ========================================================================
    # DEMO 6: Deliverables Tracker (projects ↔ deliverables)
    # ========================================================================
    print_section("DEMO 6: Deliverables Tracker (projects ↔ deliverables)")
    
    print("All Computer Vision deliverables:")
    deliverables = db.get_deliverables_tracker(topic_area="Computer Vision")
    print(deliverables[['Project_Name', 'Deliverable', 'Date_Completed', 'Client', 'Technologies']])
    print(f"\n✓ Found {len(deliverables)} CV deliverables")
    
    # ========================================================================
    # DEMO 7: Analytics by Industry
    # ========================================================================
    print_section("DEMO 7: Analytics by Industry")
    
    print("Hours and revenue by industry/client:")
    analytics = db.get_analytics_by_industry()
    print(analytics)
    print(f"\n✓ Total hours across all industries: {analytics['Total_Hours'].sum():,.0f}")
    print(f"✓ Total revenue: ${analytics['Total_Revenue'].sum():,.0f}")
    
    # ========================================================================
    # DEMO 8: Skills Distribution
    # ========================================================================
    print_section("DEMO 8: Skills Distribution")
    
    print("Staff distribution by skill:")
    skills = db.get_analytics_by_skill()
    print(skills)
    
    # ========================================================================
    # DEMO 9: Role Distribution (employees ↔ roles)
    # ========================================================================
    print_section("DEMO 9: Role Distribution (employees ↔ roles)")
    
    print("Staff distribution by role:")
    roles = db.get_analytics_by_role()
    print(roles)
    
    # ========================================================================
    # DEMO 10: Complex Search
    # ========================================================================
    print_section("DEMO 10: Complex Search - Multi-table Relationships")
    
    print("Example 1: Senior Python engineers in Texas with Law Enforcement experience")
    results = db.complex_search(
        skills=["Python"],
        location="Texas",
        role="Senior Engineer",
        industry_experience="Law Enforcement"
    )
    if len(results) > 0:
        print(results[['Employee_ID', 'Name', 'Job_Title', 'Location', 'Skills', 
                       'Industries_Worked', 'Total_Hours_Billed']])
    else:
        print("No matching employees found")
    print(f"\n✓ Found {len(results)} matching employees")
    
    print("\n" + "-"*80 + "\n")
    
    print("Example 2: Computer Vision experts with Federal client experience")
    results = db.complex_search(
        skills=["CV"],
        client_experience="Federal"
    )
    if len(results) > 0:
        print(results[['Employee_ID', 'Name', 'Job_Title', 'Skills', 
                       'Clients_Worked', 'Total_Hours_Billed']])
    else:
        print("No matching employees found")
    print(f"\n✓ Found {len(results)} matching employees")
    
    # ========================================================================
    # DEMO 11: Employee Project History (Full relationship chain)
    # ========================================================================
    print_section("DEMO 11: Employee Project History (employees → billing → projects → deliverables)")
    
    print("Complete project history for Alice Ward (10001):")
    history = db.get_employee_project_history(employee_id=10001)
    print(history[['Project_Name', 'Client', 'Industry', 'Year', 
                   'Hours_Billed', 'Role_in_Project', 'Deliverable']].drop_duplicates())
    
    # ========================================================================
    # Summary
    # ========================================================================
    print_section("✅ Demo Complete - Summary")
    
    print("Database Statistics:")
    print(f"  • Total Employees: {len(db.employees_df)}")
    print(f"  • Total Projects: {len(db.projects_df)}")
    print(f"  • Total Billing Records: {len(db.billing_df)}")
    print(f"  • Total Deliverables: {len(db.deliverables_df)}")
    print(f"  • Total Roles: {len(db.roles_df)}")
    print(f"  • Total Hours Billed: {db.billing_df['Hours_Billed'].sum():,.0f}")
    print(f"  • Total Revenue: ${db.projects_df['Dollar_Amount'].sum():,.0f}")
    
    print("\nRelationships Established:")
    print("  ✓ Employee_ID: employees ↔ billing, resume_data")
    print("  ✓ Billing_Code: projects ↔ billing, deliverables")
    print("  ✓ Role_ID: employees ↔ roles")
    
    print("\nNext Steps:")
    print("  1. Run the web app: streamlit run app.py")
    print("  2. Explore the interactive dashboard")
    print("  3. Try the complex search feature")
    print("  4. Export results as CSV")
    
    print("\n" + "="*80 + "\n")
    
    # Close database
    db.close()

if __name__ == "__main__":
    main()
