🌟 Django REST Framework Views Overview
In this Django project, I've crafted a set of comprehensive REST API views to seamlessly manage companies, branches, users, and authentication. Below is a breakdown of the key views:

📌 User Management Views
🚀 UserCreateRetrieveUpdateAPIView:
Functionality: Enables CRUD operations for user profiles.
Serializers: Utilizes UserSerializer for creating users and UserUpdateSerializer for updates.
Permissions: Implements UserPermissions to manage access control.
🌐 UserCompanyWithBranchCreate:
Functionality: Facilitates the creation of a user, associated company, and branch in a single API call.
Consistency: Ensures data integrity through database transactions.
🔑 LogInView:
Functionality: Handles user authentication using TokenObtainPairView.
Validation: Employs LogInSerializer for input validation.
📌 Company & Branch Management Views
🏢 CompanyWithBranchCreate:
Functionality: Supports the creation of a company along with an associated branch.
Validation: Validates data using CompanySerializer and CompanyBranchSerializer.
Check: Verifies if the user already owns an active company to prevent duplicates.
🌳 BranchCreate:
Functionality: Provides a straightforward endpoint for creating company branches.
Security: Requires IsAuthenticated permission for access.
📌 Company Branch User Relations Views
🤝 AddUserToBranchCompany:
Functionality: Establishes a new relation between a user and a branch.
Validation: Uses CompanyBranchUserRelationSerializer for data validation.
Permissions: Employs custom permission company_primary_permission_factory.
🔄 UpdateUserInBranchCompany:
Functionality: Enables updates to user permissions within a branch.
Validation: Validates input using CompanyBranchUserRelationSerializer.
📋 ListUserBranchRelations:
Functionality: Lists all user-branch relations associated with a specific branch.
Filtering: Filters relations using Branch-Company-ID from request headers.
🛠️ Key Features & Best Practices:
Data Integrity: Robust data validation using serializers.
Access Control: Utilizes a combination of custom and built-in permission classes.
Consistency: Ensures atomicity and data integrity through database transactions.
These views collectively offer a robust backend solution, streamlining the API endpoints for managing various entities effectively.

🚀 Automating Django CI with GitHub Actions
I've implemented a Continuous Integration (CI) pipeline using GitHub Actions to automate the testing and deployment process for this Django project.

📋 Workflow Details:
Name: Django CI
Trigger: Activates on every push to the master branch.
Concurrency: Configured to run a single workflow instance on the master branch to prevent overlap.
🛠️ Pipeline Steps:
1️⃣ Checkout Code: Fetches the latest codebase from the repository.
2️⃣ Set up Python 3.11: Installs and configures Python 3.11.
3️⃣ Cache Dependencies: Speeds up subsequent runs by caching Python dependencies.
4️⃣ Install PostgreSQL Prerequisites: Prepares environment with libpq-dev for PostgreSQL.
5️⃣ Install Python Dependencies: Installs project-specific Python packages.
6️⃣ Run Migrations: Executes Django database migrations to ensure database schema consistency.
7️⃣ Run Tests: Executes comprehensive Django test suite using python manage.py test.

🔒 Best Practices Implemented:
Sensitive Data: Utilizes GitHub secrets to securely store environment variables.
Dependency Caching: Optimizes build time by caching Python dependencies.
Isolated Testing: Ensures tests run on a dedicated testing database for data isolation.
Service Health Check: Incorporates a health check for PostgreSQL to ensure database availability.
Future Enhancements: Plans to integrate test coverage reporting for enhanced visibility.
Automating CI with GitHub Actions fosters a development environment where code is continuously tested, ensuring high-quality and reliable software releases.

