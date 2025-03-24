# Database Schema Documentation

## Overview
The database name is **EmployeeDB**, version **1.0**, and its description is: A sample database storing employee records, departments, and projects information.

## Tables
### employees
*Description:* Table containing employee details.

| Column Name | Data Type | Constraints | Description |
| --- | --- | --- | --- |
| employee_id | integer | primary key, auto_increment |  |
| first_name | varchar(50) | not null |  |
| last_name | varchar(50) | not null |  |
| email | varchar(100) | unique, not null |  |
| department_id | integer | foreign key |  |

### departments
*Description:* Table storing department information.

| Column Name | Data Type | Constraints | Description |
| --- | --- | --- | --- |
| department_id | integer | primary key, auto_increment |  |
| department_name | varchar(100) | not null |  |

### projects
*Description:* Table containing project details.

| Column Name | Data Type | Constraints | Description |
| --- | --- | --- | --- |
| project_id | integer | primary key, auto_increment |  |
| project_name | varchar(100) | not null |  |
| start_date | date | not null |  |
| end_date | date |  |  |

## Relationships
* one-to-many relationship from **departments** to **employees** via foreign key **department_id**: Each department can have multiple employees.

## Last Updated
March 16, 2025