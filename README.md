# CS340-Grazioso-Salvare-Dashboard
README — Grazioso Salvare Dashboard Application
Developer: Aaron Jones
Course: CS-340: Client/Server Development
Institution: Southern New Hampshire University
________________________________________
1. Project Overview & Required Functionality
This project implements a fully functional MongoDB-powered dashboard for Grazioso Salvare, an international animal-rescue training organization. The dashboard allows users to:
•	Retrieve and filter data from the Austin Animal Center Outcomes dataset
•	Apply four rescue-type filters
o	Water Rescue
o	Mountain/Wilderness Rescue
o	Disaster/Individual Tracking
o	Reset (unfiltered view)
•	View results in an interactive data table
•	Inspect breed distribution using a dynamic graph
•	View the geolocation of selected dogs on an interactive Leaflet map
•	Interact with all widgets using intuitive controls designed for non-technical users
•	View the Grazioso Salvare logo and developer identifier on the dashboard
This dashboard uses the MVC pattern:
•	Model: MongoDB + CRUD Python Module
•	View: Dash visual components (DataTable, Graphs, Leaflet Map)
•	Controller: Dash callbacks + CRUD module queries
________________________________________
Screenshots 
Dashboard Initial State (unfiltered)
 
Water Rescue Filter Applied
 
Mountain/Wilderness Rescue Filter Applied
 
Disaster/Individual Tracking Filter Applied
 
Reset (all animals restored)
 
2. Tools Used & Rationale
MongoDB (Model Layer)
MongoDB was chosen due to its:
•	Schema-flexible JSON-like documents
•	Easy integration with Python through PyMongo
•	Ability to handle large datasets efficiently
•	Built-in query operators ideal for rescue-type filtering
•	Fast development workflow suitable for Agile projects
MongoDB stores the Austin Animal Center dataset and provides the back-end model for CRUD access.
________________________________________
Python & Custom CRUD Module
A custom Python class (AnimalShelter) was developed to encapsulate:
•	Create
•	Read
•	Update
•	Delete
This module ensures:
•	Secure authentication
•	Reusable database operations
•	Clean separation between data logic and dashboard UI
The dashboard imports this module to execute dynamic queries based on user inputs.
________________________________________
Dash Framework (View + Controller Layers)
Dash was selected because it:
•	Enables rapid development of interactive web dashboards in Python
•	Provides visual components such as:
o	dash_table.DataTable
o	dcc.Graph
o	dash_leaflet maps
o	Button, dropdown, and radio-item controls
•	Uses a callback architecture that cleanly separates logic from presentation
•	Renders directly inside JupyterLab (ideal for this course environment)
________________________________________
Dash Leaflet (Geolocation Chart)
•	Displays latitude/longitude positions from the dataset
•	Allows interactive markers, tooltips, and popups
•	Provides a practical visualization needed by rescue personnel
________________________________________
Additional Tools
Tool	Purpose
Pandas	Converts MongoDB records into DataFrames for table rendering
Plotly Express	Generates dynamic charts (e.g., breed distribution pie chart)
Base64	Encodes the Grazioso Salvare logo for display in the dashboard
JupyterLab / Codio	Execution and testing environment
________________________________________
3. Steps Taken to Complete the Project
Step 1 — Import Data & Create MongoDB Database
•	Loaded AAC dataset using mongoimport
•	Created authenticated MongoDB user:
aacuser / password123
________________________________________
Step 2 — Develop CRUD Python Module
•	Implemented class constructor for authentication
•	Built create(), read(), update(), and delete() methods
•	Tested them using Python scripts and Jupyter Notebook
________________________________________
Step 3 — Build Base Dashboard
•	Imported Dash, Dash Leaflet, Plotly, and CRUD module
•	Loaded all records from the AAC database into a DataFrame
•	Built the initial data table
________________________________________
Step 4 — Add Interactive Filtering Controls
Created filter UI component (radio buttons or dropdowns) that trigger CRUD queries for:
•	Water Rescue
•	Mountain/Wilderness Rescue
•	Disaster/Individual Tracking
•	Reset
Each filter constructs appropriate MongoDB queries based on the Rescue Type Table.
________________________________________
Step 5 — Make Data Table Responsive to Filters
•	Added callbacks to refresh table contents based on selected rescue type
•	Enabled pagination, sorting, and single-row selection
________________________________________
Step 6 — Add Charts & Map
1.	Pie Chart: Shows distribution of breeds in current filtered dataset
2.	Geolocation Map:
o	Updates based on selected table row
o	Displays tooltip (breed) and popup (animal name)
________________________________________
Step 7 — Test & Capture Screenshots
•	Verified all rescue-type filters work correctly
•	Ensured both charts update dynamically
•	Saved required screenshots for final submission
________________________________________
4. Challenges & How They Were Resolved
Handling MongoDB ObjectId Crashes
•	Removing the _id field was necessary because Dash DataTable cannot render complex BSON types.
•	Fixed using:
•	df.drop(columns=['_id'], inplace=True)
Geolocation Index Errors
Some rows did not contain valid lat/long values.
Resolved by:
•	Adding default row selection
•	Using safe indexing inside callbacks
CRUD Authentication Issues
•	Incorrect quoting of username/password caused connection failures
•	Fixed by verifying URI formatting and using plain text credentials
Interactive Callbacks Not Triggering
•	Ensured all Input and Output component IDs matched exactly
•	Verified callback ordering and return structure
________________________________________
5. Portfolio Reflection
• Writing Maintainable, Readable, and Adaptable Programs

I focus on writing maintainable and adaptable programs by emphasizing modular design, clear separation of concerns, and consistent coding standards. In this project, the CRUD Python module developed in Project One was intentionally designed as a standalone, reusable component that encapsulates all database access logic. This allowed the dashboard code in Project Two to remain clean and focused solely on user interaction and visualization rather than database implementation details.

The primary advantage of this approach was flexibility. Because all database operations were abstracted into the CRUD module, changes to queries, authentication, or database structure could be made without modifying the dashboard code. This also made testing easier, since the CRUD functionality could be validated independently before integration. In the future, this CRUD module could be reused for additional dashboards, reporting tools, APIs, or automated data analysis scripts that require access to the same MongoDB dataset.

• Problem-Solving Approach as a Computer Scientist

When approaching this project, I treated the requirements as a real client engagement rather than a purely academic exercise. I began by analyzing Grazioso Salvare’s needs and translating them into technical requirements, such as specific database queries, filtering logic, and user interface behaviors. This differed from previous coursework that focused more on isolated programming concepts, as this project required integrating multiple technologies into a cohesive system.

I used an iterative, test-driven approach—building the database first, validating CRUD operations, then layering the dashboard functionality on top. Breaking the problem into smaller, manageable components (database model, CRUD logic, dashboard widgets, and callbacks) allowed me to isolate issues and resolve them efficiently. In future projects, I would apply the same strategy by gathering client requirements early, designing flexible data models, and prototyping database queries before committing to a full interface design.

• The Role of Computer Scientists and Why It Matters

Computer scientists design systems that transform raw data into meaningful, actionable information. In this project, the dashboard provides Grazioso Salvare with a powerful decision-support tool that allows staff to quickly identify dogs suited for specific rescue missions. By automating data filtering, visualization, and geolocation mapping, the application reduces manual effort, minimizes errors, and improves response time.

This type of work directly supports organizational goals by improving efficiency, accuracy, and scalability. For a company like Grazioso Salvare, having an intuitive dashboard backed by a robust database system enables better training decisions, more effective rescue operations, and ultimately helps save lives. This project demonstrates how computer science solutions can have tangible, real-world impact beyond the code itself.

