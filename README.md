# My GeoDev Lab Africa Project
How are waterways distributed across Abeokuta South LGA, and which areas are most vulnerable to flooding due to their proximity to these waterways?
Built over twelve months with GeoDev Lab Africa, Cohort One
See project-brief.md for the full brief





## Month 2: Development Environment and Early Python

- Week 5: Set up Python, VS Code and the terminal. Created and successfully ran `hello.py`.
- Week 6: set up the project with uv and added pandas. check.py prints the pandas version.
- Week 7: analyse.py reads wards.csv, converts each area and classifies each ward.
- Week 8: Created inspect_data.py to inspect my Month 1 dataset. The script reads CSV data using DictReader, handles missing values and summarises two numerical columns using a reusable function that returns statistical results.
- Week 9 – Consolidation and Refactoring

**Objective:** Refactor the Week 8 data inspection script into reusable Python functions and develop a capstone script for analysing multiple numeric columns.

**Functions implemented:**
- `read_rows()` – Reads records from a CSV file.
- `clean_values()` – Extracts and cleans numeric values.
- `summarise()` – Calculates count, minimum, maximum and average.
- `summarise_all()` – Generates summary statistics for multiple columns.

**Output:** Successfully generated summary statistics for selected numeric columns in the Month 1 dataset.

### Month 2 Reflection

One idea that became clearer to me during this week was how functions make Python scripts more organised and reusable. I am still working on understanding how different functions interact when building a larger programme. The capstone helped me see how Python can be used to inspect and summarise geographical data more efficiently. Overall, this week improved my understanding of data processing and code organisation.

## Month 3: geospatial Python and automation at the bottom of your main README, and under it: 
- Week 10: GeoPandas. Loaded, checked, joined and mapped my Abeokuta_bdry.gpkg in code.
