# bugfinder
BugFinder is a static code analysis tool designed to identify potential bugs and security vulnerabilities in your code. This tool was developed in Italian but has English documentation for broader accessibility.
Mostra immagine
📋 Description
BugFinder scans your code to detect common programming errors, security risks, and bad practices. It supports multiple programming languages and provides detailed reports to help you improve your code quality.
Key Features:

Analyzes individual files or entire directories
Identifies common bug patterns and security vulnerabilities
Supports multiple programming languages (C/C++, Python, JavaScript, Java, PHP)
Generates reports in various formats (console, HTML, JSON)
Easy-to-use command-line interface


Note: While the tool's internal code and comments are in Italian, all output reports can be configured to display in English.

🔧 Installation
Prerequisites

Python 3.6 or higher

Installation Steps

Clone the repository:

bashgit clone https://github.com/yourusername/bugfinder.git
cd bugfinder

No additional dependencies are required as BugFinder uses only Python standard libraries.
Make the script executable (Linux/Mac):

bashchmod +x bugfinder.py
🚀 Usage
Basic Usage
Run BugFinder by specifying the path to analyze:
bashpython bugfinder.py /path/to/your/code
Advanced Options
BugFinder provides several command-line options for customization:
usage: bugfinder.py [-h] [-e EXTENSIONS [EXTENSIONS ...]] [-f {console,html,json}] [-x EXCLUDE [EXCLUDE ...]] path

path: Path to the file or directory to analyze
-e, --extensions: File extensions to analyze (default: .c, .cpp, .h, .hpp, .py, .js, .java, .php)
-f, --format: Output report format (choices: console, html, json; default: console)
-x, --exclude: Directories to exclude from analysis (default: node_modules, venv, pycache, .git)
-h, --help: Show help message

Examples
Analyze a single file:
bashpython bugfinder.py myfile.py
Analyze a directory with specific file extensions:
bashpython bugfinder.py ./myproject -e .py .js
Generate an HTML report:
bashpython bugfinder.py ./myproject -f html
Exclude specific directories:
bashpython bugfinder.py ./myproject -x node_modules build dist
📊 Output Examples
Console Output
/path/to/myproject/app.py
----------------------
  Line 42: memory_leak
    Possible memory leak: memory allocation without corresponding free
    Code: ptr = malloc(sizeof(int) * 10);

  Line 78: sql_injection
    Possible SQL injection: use parameterized queries
    Code: query("SELECT * FROM users WHERE name = '" + user_input + "'");

Total potential bugs found: 2
HTML Report
The HTML report provides a more visual representation of the issues:
Mostra immagine
JSON Report
The JSON report is ideal for integration with other tools:
json[
  {
    "file": "/path/to/myproject/app.py",
    "line": 42,
    "type": "memory_leak",
    "description": "Possible memory leak: memory allocation without corresponding free",
    "code": "ptr = malloc(sizeof(int) * 10);"
  },
  {
    "file": "/path/to/myproject/app.py",
    "line": 78,
    "type": "sql_injection",
    "description": "Possible SQL injection: use parameterized queries",
    "code": "query(\"SELECT * FROM users WHERE name = '\" + user_input + \"'\");"
  }
]
🛠️ Supported Bug Patterns
BugFinder detects various types of potential issues, including:

Memory leaks and resource leaks
Null pointer dereferences
Buffer overflows
Uninitialized variables
Division by zero
Integer overflows
Format string vulnerabilities
Race conditions
SQL injections
Infinite loops
Swallowed exceptions
Language-specific issues for Python and JavaScript

🔄 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
