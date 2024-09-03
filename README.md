# Trans Acnr

## Overview
This project is a Django-based application for managing and analyzing production plans and Station Sop. It provides functionality to track daily production plans, actual production, and generate reports in various formats.

## Features

- Daily production plan entry and tracking
- Comparison of planned vs actual production
- Filtering by date range and unit
- Export data to PDF and Excel formats
- Interactive data visualization (if applicable)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/ft-prince/ACNR_1.git
   cd ACNR_1
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser (for admin access):
   ```
   python manage.py createsuperuser
   ```

## Usage

1. Start the development server:
   ```
   python manage.py runserver
   ```

2. Access the application at `http://localhost:8000/screen`

4. Log in with your superuser credentials to access the admin panel and manage data.

5. Use the main interface to view production plans, filter data, and generate reports.

## Exporting Data

### PDF Export
- Navigate to the production plan total list view.
- Use the date range and unit filters as needed.
- Click on the "Export to PDF" button to generate and download a PDF report.

### Excel Export
- Navigate to the production plan total list view.
- Use the date range and unit filters as needed.
- Click on the "Export to Excel" button to generate and download an Excel file.

## Models

### Unit
- Represents a production unit with a unique code and model name.

### ProductionPlanTotal
- Represents daily production plan totals for each unit.
- Includes fields for planned and actual quantities.

## Views

- `ProductionPlanTotalListView`: Displays a list of production plan totals with filtering options.
- `export_production_plan_total_pdf_auto`: Generates a PDF report of production plan totals.
- `export_production_plan_total_to_excel_auto`: Exports production plan totals to an Excel file.
- `and much more`

## Contact

Renata Iot
Project Link: (https://github.com/ft-prince/ACNR_1)
