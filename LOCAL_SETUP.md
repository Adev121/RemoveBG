# Local Setup Guide for Background Remover Application

## Prerequisites
1. Python 3.11 or later
2. Visual Studio Code
3. PostgreSQL database
4. remove.bg API key (Get it from [remove.bg](https://www.remove.bg/api))

## Setup Steps

### 1. Clone the Repository
1. Create a new directory for your project
2. Copy all the project files to your local directory

### 2. Set Up Python Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install flask flask-sqlalchemy psycopg2-binary requests gunicorn werkzeug email-validator
```

### 3. Database Setup
1. Install PostgreSQL if not already installed
2. Create a new database for the application
3. Create a `.env` file in the project root with the following variables:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
REMOVE_BG_API_KEY=your_remove_bg_api_key
```

### 4. Project Structure
Ensure your project structure looks like this:
```
your-project/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/
│   └── index.html
├── app.py
├── main.py
├── models.py
└── .env
```

### 5. Running the Application

1. Open the project in VSCode
2. Make sure your virtual environment is activated
3. Run the following commands in the terminal:
```bash
# Initialize the database
python
>>> from app import db
>>> db.create_all()
>>> exit()

# Start the application
python main.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Common Issues and Solutions

### Database Connection Issues
- Ensure PostgreSQL service is running
- Verify database credentials in `.env` file
- Check if the database exists

### Package Installation Issues
If you encounter any package installation issues:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Port Already in Use
If port 5000 is already in use:
- Change the port number in `main.py`
- Kill the process using port 5000 (use `netstat -ano` on Windows or `lsof -i :5000` on Unix)

## Development Tips
1. Use VSCode's Python extension for better development experience
2. Install the "Python" and "SQLite" extensions in VSCode
3. Use the integrated terminal in VSCode for running commands
4. Enable VSCode's auto-save feature

## API Testing
To test the remove.bg API integration:
1. Ensure your API key is correctly set in the `.env` file
2. Try uploading a test image through the interface
3. Check the application logs for any API-related errors

## Debugging
1. The application runs in debug mode by default
2. Check the terminal for error messages
3. Use VSCode's debugging features:
   - Set breakpoints in your code
   - Use the Debug panel (Ctrl+Shift+D)
   - Watch variables and step through code

## Additional Notes
- Keep your API key secure and never commit it to version control
- The application uses a temporary folder for storing processed images
- The database stores processing history for uploaded images
