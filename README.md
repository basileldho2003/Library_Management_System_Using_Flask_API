### Requirements :
[Python](https://www.python.org/) (supported versions only) 

## STEPS TO RUN THE PROJECT

1. Install Python.
2. Open Terminal and clone the repository (ensure that git is installed).
3. Install virtualenv (```pip install virtualenv```)
4. Create new virtualenv (```virtualenv flaskenv```)
5. Activate virtualenv.
6. Install flask (```pip install Flask```)
7. Run the python file (```python app.py```)
8. Use any REST API client for testing CRUD operations.

## DESIGN CHOICES

1. Modular Structure
- Database Initialization:
  - The ```db_connector``` function initializes the database and creates required tables (```books``` and ```members```) if they don't already exist.
  - Ensures database setup is done at the start of the application lifecycle.
- Separation of Concerns:
  - Routes for books and members are implemented as separate functions, ensuring modularity and ease of management.
  - Each route clearly handles specific HTTP methods like ```GET```, ```POST```, ```PUT```, and ```DELETE```.
2. Database Management
- SQLite Database:
  - SQLite is used for simplicity and portability in small to medium-scale applications.
  - Queries are constructed dynamically using parameterized statements to prevent SQL injection.
- Connection Handling:
  - Connections are opened at the beginning of each operation and closed in a finally block to ensure resources are freed properly.
  - This prevents database locks and potential memory issues.
3. API Design
- RESTful Routes:
  - The routes are designed to follow RESTful principles:
    - ```GET```: Retrieve data (all records or by ID).
    - ```POST```: Add new records.
    - ```PUT```: Update existing records.
    - ```DELETE```: Remove records.
  - Each route is tailored to either books or members.
- Dynamic Queries:
  - Updates and inserts dynamically fetch required fields and fill in defaults for missing ones (e.g., keeping original values or using ```CURRENT_DATE```).
4. Error Handling
- Database Errors:
  - Errors from SQLite operations are caught and returned as JSON responses with a 500 status code.
  - Provides meaningful error messages for debugging and user feedback.
- Validation:
  - Inputs are validated to ensure required fields like ```title``` and ```author``` (for ```books```) or ```name``` and ```email``` (for ```members```) are provided.
  - Appropriate error messages are returned when required fields are missing.
5. Usability
- Readable Output:
  - JSON responses are structured to provide meaningful feedback, such as success messages or detailed error descriptions.
  - Record data is formatted as dictionaries for readability and consistency.
- Default Values:
  - Membership dates default to the current date (```CURRENT_DATE```) to simplify user input.
6. Security
- Parameterized Queries:
  - Avoids SQL injection by using ? placeholders in queries instead of string interpolation for user inputs.
- Minimal Error Exposure:
  - Error responses do not expose sensitive information about the database or internal workings of the API.
7. API Behavior
- CRUD Operations:
  - Each route implements full CRUD functionality for both books and members.
  - Ensures consistent behavior for retrieving, creating, updating, and deleting records.
- Unique Constraints:
  - The email field in the members table is unique to prevent duplicate entries.

## LIMITATIONS

1. Scalability:
- SQLite is not suitable for high-concurrency applications.
- For production systems, consider using a more robust database like PostgreSQL or MySQL.
2. Error Handling:
- The current implementation provides basic error handling, which might not cover edge cases like corrupted database files.
3. Testing:
- No automated tests are included. Unit tests and integration tests would improve reliability.
4. Search functionality for books by title or author unavailable.
5. Pagination and token-based authentication not supported yet.
 
