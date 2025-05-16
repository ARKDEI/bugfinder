BugFinder
A static code analysis tool designed to identify potential bugs and security vulnerabilities in your code.
Note: The tool's console output and comments are in Italian.
Description
BugFinder is a Python-based static analysis tool that scans your code to detect common programming errors, potential bugs, and security vulnerabilities. It supports multiple programming languages including C/C++, Python, JavaScript, Java, and PHP.
The tool works by analyzing source code files against a library of predefined pattern-matching rules that correspond to common programming mistakes and anti-patterns.
Features

Multi-language support: Analyzes C/C++, Python, JavaScript, Java, PHP and more
Directory or single file analysis: Scan entire projects or individual files
Customizable file extensions: Focus on specific file types
Multiple report formats: Console, HTML, or JSON output
Directory exclusion: Skip specific directories (like node_modules, venv)
Detects common issues such as:

Memory and resource leaks
Null pointer dereferences
Buffer overflows
Uninitialized variables
Division by zero
Integer overflows
Format string vulnerabilities
Race conditions
SQL injection risks
Infinite loops
Exception handling problems
Language-specific issues (Python, JavaScript)



Installation

Ensure you have Python 3.x installed on your system
Clone this repository:
git clone https://github.com/yourusername/bugfinder.git
cd bugfinder

No additional dependencies required - the tool uses only Python standard libraries

Usage
Basic Usage
bashpython bugfinder.py /path/to/your/code
Command Line Options
usage: bugfinder.py [-h] [-e EXTENSIONS [EXTENSIONS ...]] [-f {console,html,json}] [-x EXCLUDE [EXCLUDE ...]] path

BugFinder - Tool to identify potential bugs in code

positional arguments:
  path                  Path to the file or directory to analyze

optional arguments:
  -h, --help            show this help message and exit
  -e EXTENSIONS [EXTENSIONS ...], --extensions EXTENSIONS [EXTENSIONS ...]
                        File extensions to analyze (default: ['.c', '.cpp', '.h', '.hpp', '.py', '.js', '.java', '.php'])
  -f {console,html,json}, --format {console,html,json}
                        Output report format (default: console)
  -x EXCLUDE [EXCLUDE ...], --exclude EXCLUDE [EXCLUDE ...]
                        Directories to exclude (default: ['node_modules', 'venv', '__pycache__', '.git'])
Usage Examples

Analyze a specific file:
bashpython bugfinder.py yourfile.py

Analyze all code in the current directory:
bashpython bugfinder.py .

Generate an HTML report:
bashpython bugfinder.py your_project/ -f html

Analyze only Python and JavaScript files:
bashpython bugfinder.py your_project/ -e .py .js

Exclude specific directories:
bashpython bugfinder.py your_project/ -x node_modules build dist

Combine multiple options:
bashpython bugfinder.py your_project/ -e .py .js -f json -x venv tests


Output Examples
Console Output
/path/to/your/code/file.py
------------------------
  Line 45: memory_leak
    Possible memory leak: memory allocation without corresponding free
    Code: ptr = malloc(sizeof(int) * 10);

  Line 78: buffer_overflow
    Buffer overflow risk: use strncpy, strncat or fgets
    Code: strcpy(dest, source);

Total potential bugs found: 2
HTML Output
The HTML report will be saved as bugfinder_report.html in the current directory and includes:

A list of all files with issues
Line numbers where problems were found
Bug type and description for each issue
Color-coded snippets of problematic code

JSON Output
The JSON report will be saved as bugfinder_report.json and contains a structured representation of all detected issues, making it easy to integrate with other tools or custom reporting systems.
Limitations

False positives are possible due to the pattern-matching approach
The tool cannot detect logical errors that don't match predefined patterns
Some language-specific features might not be fully supported
The analysis doesn't account for code execution paths
