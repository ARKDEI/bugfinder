#!/usr/bin/env python3
# BugFinder - Strumento per identificare potenziali bug nel codice
# Autore: Claude

import os
import re
import sys
import argparse
from collections import defaultdict

class BugFinder:
    def __init__(self):
        self.bug_patterns = {
            "memory_leak": (
                r"malloc\s*\(.+\)(?!.*free)", 
                "Possibile memory leak: allocazione di memoria senza free corrispondente"
            ),
            "null_pointer": (
                r"(?:\w+\s*=\s*NULL|\w+\s*=\s*0).*\n.*\w+\s*->", 
                "Possibile dereferenziazione di puntatore NULL"
            ),
            "buffer_overflow": (
                r"(strcpy|strcat|gets)\s*\(", 
                "Rischio di buffer overflow: usa strncpy, strncat o fgets"
            ),
            "uninitialized_var": (
                r"(?:\w+\s+\w+;)(?!.*=).*\n.*\1", 
                "Variabile potenzialmente non inizializzata"
            ),
            "division_by_zero": (
                r"/\s*(?:0|(?:\w+\s*\+\s*)*(?:\w+\s*-\s*)\1)", 
                "Possibile divisione per zero"
            ),
            "integer_overflow": (
                r"(?:int|short|long)\s+\w+\s*=\s*(?:INT_MAX|SHRT_MAX|LONG_MAX)(?:\s*\+|\+\+)", 
                "Rischio di integer overflow"
            ),
            "format_string": (
                r"printf\s*\(\s*\w+\s*\)", 
                "Vulnerabilità format string: usa printf(\"%s\", var)"
            ),
            "resource_leak": (
                r"(?:fopen|open|socket)\s*\(.+\)(?!.*(?:fclose|close))", 
                "Possibile resource leak: risorsa aperta senza close corrispondente"
            ),
            "race_condition": (
                r"(?:pthread_create|std::thread).*(?:shared|global)", 
                "Potenziale race condition su variabile condivisa"
            ),
            "sql_injection": (
                r"(?:execute|query)\s*\(.*\+.*\)", 
                "Possibile SQL injection: usa query parametrizzate"
            ),
            "infinite_loop": (
                r"while\s*\(\s*(?:1|true)\s*\)(?!.*break)", 
                "Loop infinito potenziale: nessun break trovato"
            ),
            "exception_swallow": (
                r"try\s*{.*}\s*catch\s*\(.+\)\s*{\s*}", 
                "Eccezione catturata ma non gestita"
            ),
        }
        
        # Modelli comuni per Python
        self.python_patterns = {
            "except_all": (
                r"except\s*:",
                "Evita 'except:' generico, specifica le eccezioni da catturare"
            ),
            "mutable_default": (
                r"def\s+\w+\s*\(.*=\s*(?:\[\]|{}|\(\))",
                "Parametro di default mutabile, può causare comportamenti inattesi"
            ),
            "global_var": (
                r"global\s+\w+",
                "Uso di variabile globale può causare effetti collaterali indesiderati"
            ),
            "eval_usage": (
                r"eval\s*\(",
                "Uso di eval() è potenzialmente pericoloso"
            ),
            "shell_injection": (
                r"os\.system\s*\(.*\+.*\)|subprocess\.call\s*\(.*shell\s*=\s*True.*\+.*\)",
                "Possibile iniezione di comandi shell"
            ),
            "duplicate_keys": (
                r"{.*:\s*.*,.*:\s*.*}",
                "Controlla chiavi duplicate nei dizionari"
            ),
        }
        
        # Modelli comuni per JavaScript
        self.js_patterns = {
            "triple_equals": (
                r"==(?![=])|!=(?![=])",
                "Usa === e !== invece di == e != per evitare coercizioni di tipo"
            ),
            "global_leak": (
                r"(?<!\bvar\b|\blet\b|\bconst\b)\s+\w+\s*=",
                "Possibile leak di variabile globale, usa var/let/const"
            ),
            "promise_no_catch": (
                r"\.then\s*\(.*\)(?!\.catch)",
                "Promise senza .catch() per gestire errori"
            ),
            "alert_debug": (
                r"alert\s*\(",
                "Alert trovato, rimuovi prima della produzione"
            ),
            "eval_usage": (
                r"eval\s*\(",
                "Uso di eval() è potenzialmente pericoloso"
            ),
        }

    def analyze_file(self, file_path):
        """Analizza un file alla ricerca di pattern di bug"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            file_ext = os.path.splitext(file_path)[1].lower()
            issues = []
            
            # Seleziona i pattern appropriati in base all'estensione del file
            if file_ext in ['.py']:
                all_patterns = {**self.bug_patterns, **self.python_patterns}
            elif file_ext in ['.js', '.ts', '.jsx', '.tsx']:
                all_patterns = {**self.bug_patterns, **self.js_patterns}
            else:
                all_patterns = self.bug_patterns
                
            # Cerca corrispondenze per ogni pattern
            for bug_type, (pattern, description) in all_patterns.items():
                matches = re.finditer(pattern, content, re.MULTILINE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    line_content = content.splitlines()[line_num - 1].strip()
                    issues.append({
                        'file': file_path,
                        'line': line_num,
                        'type': bug_type,
                        'description': description,
                        'code': line_content
                    })
            
            return issues
        except Exception as e:
            print(f"Errore nell'analisi del file {file_path}: {str(e)}")
            return []

    def analyze_directory(self, directory_path, extensions=None, excluded_dirs=None):
        """Analizza ricorsivamente tutti i file in una directory"""
        if extensions is None:
            extensions = ['.c', '.cpp', '.h', '.hpp', '.py', '.js', '.java', '.php']
        
        if excluded_dirs is None:
            excluded_dirs = ['node_modules', 'venv', '__pycache__', '.git']
            
        all_issues = []
        
        for root, dirs, files in os.walk(directory_path):
            # Salta le directory escluse
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    issues = self.analyze_file(file_path)
                    all_issues.extend(issues)
        
        return all_issues

    def generate_report(self, issues, output_format='console'):
        """Genera un report dei problemi trovati"""
        if not issues:
            print("Nessun potenziale bug trovato!")
            return
        
        if output_format == 'console':
            issues_by_file = defaultdict(list)
            for issue in issues:
                issues_by_file[issue['file']].append(issue)
            
            for file, file_issues in issues_by_file.items():
                print(f"\n\033[1m{file}\033[0m")
                print("-" * len(file))
                
                for issue in sorted(file_issues, key=lambda x: x['line']):
                    print(f"  Linea {issue['line']}: \033[91m{issue['type']}\033[0m")
                    print(f"    {issue['description']}")
                    print(f"    Codice: \033[93m{issue['code']}\033[0m\n")
                
            print(f"\nTotale potenziali bug trovati: {len(issues)}")
        
        elif output_format == 'html':
            # Implementazione del report HTML
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>BugFinder Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    h1 { color: #333; }
                    .file { margin-top: 20px; border-bottom: 1px solid #ccc; padding-bottom: 5px; }
                    .issue { margin: 10px 0; padding: 10px; background-color: #f8f8f8; border-left: 4px solid #e74c3c; }
                    .issue-type { color: #e74c3c; font-weight: bold; }
                    .issue-desc { color: #333; }
                    .code { background-color: #f1c40f; padding: 2px 5px; font-family: monospace; }
                </style>
            </head>
            <body>
                <h1>BugFinder Report</h1>
            """
            
            issues_by_file = defaultdict(list)
            for issue in issues:
                issues_by_file[issue['file']].append(issue)
            
            for file, file_issues in issues_by_file.items():
                html_content += f'<div class="file"><h2>{file}</h2>'
                
                for issue in sorted(file_issues, key=lambda x: x['line']):
                    html_content += f"""
                    <div class="issue">
                        <p>Linea {issue['line']}: <span class="issue-type">{issue['type']}</span></p>
                        <p class="issue-desc">{issue['description']}</p>
                        <p>Codice: <span class="code">{issue['code']}</span></p>
                    </div>
                    """
                
                html_content += '</div>'
            
            html_content += f'<p>Totale potenziali bug trovati: {len(issues)}</p>'
            html_content += '</body></html>'
            
            with open('bugfinder_report.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Report HTML salvato come bugfinder_report.html")
        
        elif output_format == 'json':
            import json
            with open('bugfinder_report.json', 'w', encoding='utf-8') as f:
                json.dump(issues, f, indent=2)
            print(f"Report JSON salvato come bugfinder_report.json")

def main():
    parser = argparse.ArgumentParser(description='BugFinder - Strumento per identificare potenziali bug nel codice')
    parser.add_argument('path', help='Percorso del file o della directory da analizzare')
    parser.add_argument('-e', '--extensions', nargs='+', default=['.c', '.cpp', '.h', '.hpp', '.py', '.js', '.java', '.php'],
                        help='Estensioni di file da analizzare')
    parser.add_argument('-f', '--format', choices=['console', 'html', 'json'], default='console',
                        help='Formato del report di output')
    parser.add_argument('-x', '--exclude', nargs='+', default=['node_modules', 'venv', '__pycache__', '.git'],
                        help='Directory da escludere')
    
    args = parser.parse_args()
    
    bug_finder = BugFinder()
    
    if os.path.isfile(args.path):
        issues = bug_finder.analyze_file(args.path)
    elif os.path.isdir(args.path):
        issues = bug_finder.analyze_directory(args.path, args.extensions, args.exclude)
    else:
        print(f"Errore: Il percorso '{args.path}' non esiste")
        return 1
    
    bug_finder.generate_report(issues, args.format)
    return 0

if __name__ == "__main__":
    sys.exit(main())
