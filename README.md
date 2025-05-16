*BugFinder
A static code analysis tool designed to identify potential bugs and security vulnerabilities in your code.
Note: The tool's console output and comments are in Italian.
Description
BugFinder is a Python-based static analysis tool that scans your code to detect common programming errors, potential bugs, and security vulnerabilities. It supports multiple programming languages including C/C++, Python, JavaScript, Java, and PHP.
The tool works by analyzing source code files against a library of predefined pattern-matching rules that correspond to common programming mistakes and anti-patterns.
*Features

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

No additional dependencies required - the tool uses only Python standard libraries
