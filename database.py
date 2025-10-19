"""
Database module for Workforce Intelligence Platform
Handles data loading, relationships, and query operations

Relationships:
- Employee_ID: employees -> billing, resume_data
- Billing_Code: projects -> billing, deliverables
- Role_ID: employees -> roles
"""

import pandas as pd
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional
import re


class WorkforceDatabase:
    """Main database class for managing workforce data with proper relationships"""
    
    def __init__(self, data_folder: str = "Data"):
        """Initialize database with data folder path"""
        self.data_folder = Path(data_folder)
        self.conn = sqlite3.connect(':memory:', check_same_thread=False)
        
        # DataFrames for each table
        self.employees_df = None
        self.projects_df = None
        self.billing_df = None
        self.resume_df = None
        self.deliverables_df = None
        self.roles_df = None
        
        # Load all data
        self.load_all_data()
    
    def load_all_data(self):
        """Load all CSV files into pandas DataFrames and SQLite with relationships"""
        
        # Load employees (primary key: Employee_ID, foreign key: Role_ID)
        employees_file = self.data_folder / "EmployeeID-Name-Email-RoleID-JobTitle-Location-Skills-LinkedInURL.csv"
        self.employees_df = pd.read_csv(employees_file)
        self.employees_df.to_sql('employees', self.conn, if_exists='replace', index=False)
        
        # Load roles (primary key: Role_ID)
        roles_file = self.data_folder / "RoleID-StandardRole-RoleTitleVariants.csv"
        self.roles_df = pd.read_csv(roles_file)
        self.roles_df.to_sql('roles', self.conn, if_exists='replace', index=False)
        
        # Load projects (primary key: Billing_Code)
        projects_file = self.data_folder / "BillingCode-ProjectName-Client-Industry-Technologies-DollarAmount-ProjectScope.csv"
        self.projects_df = pd.read_csv(projects_file)
        self.projects_df.to_sql('projects', self.conn, if_exists='replace', index=False)
        
        # Load billing (foreign keys: Billing_Code, Employee_ID)
        billing_file = self.data_folder / "BillingCode-EmployeeID-Year-HoursBilled-RoleinProject.csv"
        self.billing_df = pd.read_csv(billing_file)
        self.billing_df.to_sql('billing', self.conn, if_exists='replace', index=False)
        
        # Load resume data (foreign key: Employee_ID)
        resume_file = self.data_folder / "EmployeeID-Education-Experience-Certifications-Summary.csv"
        self.resume_df = pd.read_csv(resume_file)
        self.resume_df.to_sql('resume_data', self.conn, if_exists='replace', index=False)
        
        # Load deliverables (foreign key: Billing_Code)
        deliverables_file = self.data_folder / "BillingCode-Deliverable-DateCompleted-TopicArea-Technologies-Client-Codebase.csv"
        self.deliverables_df = pd.read_csv(deliverables_file)
        self.deliverables_df.to_sql('deliverables', self.conn, if_exists='replace', index=False)
        
        print("✓ All data loaded successfully with relationships established")
    
    def get_employee_directory(self, 
                              skills: Optional[List[str]] = None,
                              role: Optional[str] = None,
                              location: Optional[str] = None,
                              title: Optional[str] = None) -> pd.DataFrame:
        """
        Get filtered employee directory with role information
        Uses relationship: employees.Role_ID -> roles.Role_ID
        """
        query = """
        SELECT 
            e.Employee_ID,
            e.Name,
            e.Email,
            e.Job_Title,
            e.Location,
            e.Skills,
            r.Standard_Role,
            e.LinkedIn_URL
        FROM employees e
        LEFT JOIN roles r ON e.Role_ID = r.Role_ID
        WHERE 1=1
        """
        
        params = []
        
        if role:
            query += " AND r.Standard_Role LIKE ?"
            params.append(f"%{role}%")
        
        if location:
            query += " AND e.Location LIKE ?"
            params.append(f"%{location}%")
        
        if title:
            query += " AND e.Job_Title LIKE ?"
            params.append(f"%{title}%")
        
        df = pd.read_sql_query(query, self.conn, params=params)
        
        # Filter by skills if provided
        if skills:
            mask = df['Skills'].apply(lambda x: any(skill.lower() in str(x).lower() for skill in skills))
            df = df[mask]
        
        return df
    
    def get_projects_dashboard(self,
                              client: Optional[str] = None,
                              technology: Optional[str] = None,
                              min_amount: Optional[float] = None,
                              max_amount: Optional[float] = None,
                              industry: Optional[str] = None) -> pd.DataFrame:
        """Get filtered projects dashboard"""
        query = "SELECT * FROM projects WHERE 1=1"
        params = []
        
        if client:
            query += " AND Client LIKE ?"
            params.append(f"%{client}%")
        
        if industry:
            query += " AND Industry LIKE ?"
            params.append(f"%{industry}%")
        
        if min_amount:
            query += " AND Dollar_Amount >= ?"
            params.append(min_amount)
        
        if max_amount:
            query += " AND Dollar_Amount <= ?"
            params.append(max_amount)
        
        df = pd.read_sql_query(query, self.conn, params=params)
        
        # Filter by technology if provided
        if technology:
            mask = df['Technologies'].apply(lambda x: technology.lower() in str(x).lower())
            df = df[mask]
        
        return df
    
    def get_billing_by_employee(self, employee_id: Optional[int] = None) -> pd.DataFrame:
        """
        Get billing hours by employee with project details
        Uses relationships: billing.Employee_ID -> employees.Employee_ID
                          billing.Billing_Code -> projects.Billing_Code
        """
        query = """
        SELECT 
            b.Employee_ID,
            e.Name,
            b.Billing_Code,
            p.Project_Name,
            p.Client,
            b.Year,
            b.Hours_Billed,
            b.Role_in_Project
        FROM billing b
        LEFT JOIN employees e ON b.Employee_ID = e.Employee_ID
        LEFT JOIN projects p ON b.Billing_Code = p.Billing_Code
        WHERE 1=1
        """
        
        params = []
        if employee_id:
            query += " AND b.Employee_ID = ?"
            params.append(employee_id)
        
        query += " ORDER BY b.Year DESC, b.Hours_Billed DESC"
        
        return pd.read_sql_query(query, self.conn, params=params)
    
    def get_billing_by_project(self, billing_code: Optional[str] = None) -> pd.DataFrame:
        """
        Get billing hours by project with employee details
        Uses relationships: billing.Billing_Code -> projects.Billing_Code
                          billing.Employee_ID -> employees.Employee_ID
        """
        query = """
        SELECT 
            b.Billing_Code,
            p.Project_Name,
            p.Client,
            b.Employee_ID,
            e.Name,
            e.Job_Title,
            b.Year,
            b.Hours_Billed,
            b.Role_in_Project
        FROM billing b
        LEFT JOIN projects p ON b.Billing_Code = p.Billing_Code
        LEFT JOIN employees e ON b.Employee_ID = e.Employee_ID
        WHERE 1=1
        """
        
        params = []
        if billing_code:
            query += " AND b.Billing_Code = ?"
            params.append(billing_code)
        
        query += " ORDER BY b.Hours_Billed DESC"
        
        return pd.read_sql_query(query, self.conn, params=params)
    
    def get_billing_by_year(self, year: Optional[int] = None) -> pd.DataFrame:
        """Get billing summary by year"""
        query = """
        SELECT 
            b.Year,
            p.Client,
            p.Industry,
            p.Project_Name,
            SUM(b.Hours_Billed) as Total_Hours,
            COUNT(DISTINCT b.Employee_ID) as Employee_Count
        FROM billing b
        LEFT JOIN projects p ON b.Billing_Code = p.Billing_Code
        WHERE 1=1
        """
        
        params = []
        if year:
            query += " AND b.Year = ?"
            params.append(year)
        
        query += " GROUP BY b.Year, p.Client, p.Industry, p.Project_Name"
        query += " ORDER BY b.Year DESC, Total_Hours DESC"
        
        return pd.read_sql_query(query, self.conn, params=params)
    
    def get_resume_matrix(self, employee_id: Optional[int] = None) -> pd.DataFrame:
        """
        Get resume and skills matrix for employees
        Uses relationship: resume_data.Employee_ID -> employees.Employee_ID
        """
        query = """
        SELECT 
            e.Employee_ID,
            e.Name,
            e.Job_Title,
            e.Location,
            e.Skills,
            r.Education,
            r.Experience,
            r.Certifications,
            r.Summary,
            e.LinkedIn_URL
        FROM employees e
        LEFT JOIN resume_data r ON e.Employee_ID = r.Employee_ID
        WHERE 1=1
        """
        
        params = []
        if employee_id:
            query += " AND e.Employee_ID = ?"
            params.append(employee_id)
        
        return pd.read_sql_query(query, self.conn, params=params)
    
    def get_deliverables_tracker(self,
                                billing_code: Optional[str] = None,
                                topic_area: Optional[str] = None,
                                client: Optional[str] = None,
                                technology: Optional[str] = None) -> pd.DataFrame:
        """
        Get deliverables with project details
        Uses relationship: deliverables.Billing_Code -> projects.Billing_Code
        """
        query = """
        SELECT 
            d.Billing_Code,
            p.Project_Name,
            d.Deliverable,
            d.Date_Completed,
            d.Topic_Area,
            d.Technologies,
            d.Client,
            d.Codebase,
            p.Industry,
            p.Dollar_Amount
        FROM deliverables d
        LEFT JOIN projects p ON d.Billing_Code = p.Billing_Code
        WHERE 1=1
        """
        
        params = []
        
        if billing_code:
            query += " AND d.Billing_Code = ?"
            params.append(billing_code)
        
        if topic_area:
            query += " AND d.Topic_Area LIKE ?"
            params.append(f"%{topic_area}%")
        
        if client:
            query += " AND d.Client LIKE ?"
            params.append(f"%{client}%")
        
        df = pd.read_sql_query(query, self.conn, params=params)
        
        # Filter by technology if provided
        if technology:
            mask = df['Technologies'].apply(lambda x: technology.lower() in str(x).lower())
            df = df[mask]
        
        return df
    
    def get_analytics_by_industry(self) -> pd.DataFrame:
        """
        Aggregate total billed hours by industry and client
        Uses relationship: billing.Billing_Code -> projects.Billing_Code
        """
        query = """
        SELECT 
            p.Industry,
            p.Client,
            COUNT(DISTINCT p.Billing_Code) as Project_Count,
            SUM(b.Hours_Billed) as Total_Hours,
            COUNT(DISTINCT b.Employee_ID) as Employee_Count,
            SUM(p.Dollar_Amount) as Total_Revenue
        FROM billing b
        LEFT JOIN projects p ON b.Billing_Code = p.Billing_Code
        GROUP BY p.Industry, p.Client
        ORDER BY Total_Hours DESC
        """
        
        return pd.read_sql_query(query, self.conn)
    
    def get_analytics_by_skill(self) -> pd.DataFrame:
        """Count of staff distribution by skill"""
        # Parse skills from employees
        skills_data = []
        for _, row in self.employees_df.iterrows():
            if pd.notna(row['Skills']):
                skills = [s.strip() for s in str(row['Skills']).split(';')]
                for skill in skills:
                    skills_data.append({
                        'Skill': skill,
                        'Employee_ID': row['Employee_ID'],
                        'Name': row['Name'],
                        'Location': row['Location']
                    })
        
        skills_df = pd.DataFrame(skills_data)
        
        # Aggregate by skill
        summary = skills_df.groupby('Skill').agg({
            'Employee_ID': 'count',
            'Location': lambda x: ', '.join(sorted(set(x)))
        }).reset_index()
        
        summary.columns = ['Skill', 'Employee_Count', 'Locations']
        summary = summary.sort_values('Employee_Count', ascending=False)
        
        return summary
    
    def get_analytics_by_role(self) -> pd.DataFrame:
        """
        Count of staff distribution by role
        Uses relationship: employees.Role_ID -> roles.Role_ID
        """
        query = """
        SELECT 
            r.Standard_Role,
            COUNT(e.Employee_ID) as Employee_Count,
            GROUP_CONCAT(DISTINCT e.Location) as Locations
        FROM employees e
        LEFT JOIN roles r ON e.Role_ID = r.Role_ID
        GROUP BY r.Standard_Role
        ORDER BY Employee_Count DESC
        """
        
        return pd.read_sql_query(query, self.conn)
    
    def complex_search(self,
                      skills: Optional[List[str]] = None,
                      location: Optional[str] = None,
                      role: Optional[str] = None,
                      client_experience: Optional[str] = None,
                      industry_experience: Optional[str] = None,
                      min_years_exp: Optional[int] = None) -> pd.DataFrame:
        """
        Complex search across multiple tables with relationships
        Example: Find all senior Python engineers in Texas who worked on law enforcement projects
        
        Uses relationships:
        - employees.Employee_ID -> billing.Employee_ID -> projects.Billing_Code
        - employees.Role_ID -> roles.Role_ID
        - employees.Employee_ID -> resume_data.Employee_ID
        """
        query = """
        SELECT DISTINCT
            e.Employee_ID,
            e.Name,
            e.Email,
            e.Job_Title,
            e.Location,
            e.Skills,
            r.Standard_Role,
            rd.Education,
            rd.Experience,
            rd.Certifications,
            GROUP_CONCAT(DISTINCT p.Client) as Clients_Worked,
            GROUP_CONCAT(DISTINCT p.Industry) as Industries_Worked,
            SUM(b.Hours_Billed) as Total_Hours_Billed
        FROM employees e
        LEFT JOIN roles r ON e.Role_ID = r.Role_ID
        LEFT JOIN resume_data rd ON e.Employee_ID = rd.Employee_ID
        LEFT JOIN billing b ON e.Employee_ID = b.Employee_ID
        LEFT JOIN projects p ON b.Billing_Code = p.Billing_Code
        WHERE 1=1
        """
        
        params = []
        
        if role:
            query += " AND r.Standard_Role LIKE ?"
            params.append(f"%{role}%")
        
        if location:
            query += " AND e.Location LIKE ?"
            params.append(f"%{location}%")
        
        if client_experience:
            query += " AND p.Client LIKE ?"
            params.append(f"%{client_experience}%")
        
        if industry_experience:
            query += " AND p.Industry LIKE ?"
            params.append(f"%{industry_experience}%")
        
        query += " GROUP BY e.Employee_ID, e.Name, e.Email, e.Job_Title, e.Location, e.Skills, r.Standard_Role, rd.Education, rd.Experience, rd.Certifications"
        
        df = pd.read_sql_query(query, self.conn, params=params)
        
        # Filter by skills if provided
        if skills:
            mask = df['Skills'].apply(lambda x: any(skill.lower() in str(x).lower() for skill in skills))
            df = df[mask]
        
        # Filter by years of experience if provided
        if min_years_exp:
            def extract_years(exp_str):
                if pd.isna(exp_str):
                    return 0
                matches = re.findall(r'(\d+)y', str(exp_str))
                return sum(int(m) for m in matches) if matches else 0
            
            mask = df['Experience'].apply(lambda x: extract_years(x) >= min_years_exp)
            df = df[mask]
        
        return df
    
    def get_employee_project_history(self, employee_id: int) -> pd.DataFrame:
        """
        Get complete project history for an employee
        Uses relationships: employees -> billing -> projects, deliverables
        """
        query = """
        SELECT 
            e.Name,
            e.Job_Title,
            p.Project_Name,
            p.Client,
            p.Industry,
            p.Technologies,
            b.Year,
            b.Hours_Billed,
            b.Role_in_Project,
            d.Deliverable,
            d.Date_Completed
        FROM employees e
        LEFT JOIN billing b ON e.Employee_ID = b.Employee_ID
        LEFT JOIN projects p ON b.Billing_Code = p.Billing_Code
        LEFT JOIN deliverables d ON b.Billing_Code = d.Billing_Code
        WHERE e.Employee_ID = ?
        ORDER BY b.Year DESC, b.Hours_Billed DESC
        """
        
        return pd.read_sql_query(query, self.conn, params=[employee_id])
    
    def close(self):
        """Close database connection"""
        self.conn.close()
