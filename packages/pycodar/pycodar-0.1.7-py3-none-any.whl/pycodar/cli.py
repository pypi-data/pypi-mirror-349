#!/usr/bin/env python3
import argparse
from .analyze import analyze_directory, analyze_dependencies
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich import box
import ast
import fnmatch
from collections import defaultdict

console = Console()

class TestClass:
    def __init__(self):
        self.name = "Test"

    def test_method(self):
        print("Test")


def extract_code_structure(file_path: str) -> dict:
    """Extract functions, classes, and methods from a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        tree = ast.parse(content)
        structure = {
            'functions': [],
            'classes': []
        }
        
        # First pass: set parent relationships
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node
        
        # Second pass: collect structure
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not hasattr(node, 'parent') or not isinstance(node.parent, ast.ClassDef):
                    # Top-level function
                    structure['functions'].append({
                        'name': node.name,
                        'lineno': node.lineno
                    })
            elif isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'lineno': node.lineno,
                    'methods': []
                }
                # Collect methods (functions defined within the class)
                for child in node.body:
                    if isinstance(child, ast.FunctionDef):
                        class_info['methods'].append({
                            'name': child.name,
                            'lineno': child.lineno
                        })
                structure['classes'].append(class_info)
        
        return structure
    except Exception as e:
        console.print(f"[yellow]Warning: Could not parse {file_path}: {str(e)}[/yellow]")
        return {'functions': [], 'classes': []}

def create_structure_tree(metrics):
    """Create a rich tree showing file structure with code elements."""
    # Start with root node
    tree = Tree("📁 Root", style="bold blue")
    
    # Sort folders and files for consistent display
    sorted_folders = sorted(metrics['file_structure'], key=lambda x: x['path'] or '')
    
    for folder in sorted_folders:
        path = folder['path'] or 'Root'
        if path == 'Root':
            # Add files directly to root if they're in the root directory
            folder_tree = tree
        else:
            folder_tree = tree.add(f"📁 {path}", style="cyan")
        
        # Sort files for consistent display
        sorted_files = sorted(folder['files'], key=lambda x: x['name'])
        
        for file in sorted_files:
            if file['name'].endswith('.py'):
                # Get code structure for Python files
                file_path = str(Path(folder['path']) / file['name']) if folder['path'] else file['name']
                structure = extract_code_structure(file_path)
                
                # Create file node with code structure
                file_node = folder_tree.add(f"📄 {file['name']}", style="yellow")
                
                # Add classes
                for class_info in structure['classes']:
                    class_node = file_node.add(f"🔷 {class_info['name']}", style="green")
                    for method in class_info['methods']:
                        class_node.add(f"🔹 {method['name']}", style="blue")
                
                # Add top-level functions
                for func in structure['functions']:
                    file_node.add(f"🔸 {func['name']}", style="magenta")
            else:
                # Non-Python files
                folder_tree.add(f"📄 {file['name']}", style="yellow")
    
    return tree

def parse_ignore_file(file_path: Path) -> list:
    """Parse an ignore file and return list of patterns."""
    if not file_path.exists():
        return []
    
    patterns = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                patterns.append(line)
    return patterns

def should_ignore(path: Path, ignore_patterns: list) -> bool:
    """Check if a path should be ignored based on patterns."""
    try:
        # Convert path to string relative to current directory
        rel_path = str(path.relative_to(Path.cwd()))
    except ValueError:
        # If path is in current directory, use just the filename
        rel_path = path.name
    
    for pattern in ignore_patterns:
        # Handle directory patterns (ending with /)
        if pattern.endswith('/'):
            if fnmatch.fnmatch(rel_path, pattern[:-1]) or \
               fnmatch.fnmatch(rel_path, pattern + '*'):
                return True
        # Handle regular patterns
        elif fnmatch.fnmatch(rel_path, pattern):
            return True
    return False

def get_ignore_patterns(base_path: Path) -> list:
    """Get combined ignore patterns from .gitignore and .codarignore."""
    codarignore_path = base_path / '.codarignore'
    gitignore_path = base_path / '.gitignore'
    
    # Get patterns from .codarignore
    codar_patterns = parse_ignore_file(codarignore_path)
    
    # Get patterns from .gitignore
    gitignore_patterns = parse_ignore_file(gitignore_path)
    
    # Always ignore the ignore files themselves
    always_ignore = ['.gitignore', '.codarignore']
    
    # Combine patterns, with .codarignore taking priority
    return always_ignore + codar_patterns + gitignore_patterns

def format_size(size_kb):
    """Format size in KB to a human-readable format."""
    if size_kb < 1024:
        return f"{size_kb:.2f}KB"
    elif size_kb < 1024 * 1024:
        return f"{size_kb/1024:.2f}MB"
    else:
        return f"{size_kb/(1024*1024):.2f}GB"

def count_code_metrics(file_path: str) -> tuple:
    """Count code, comments, and empty lines in a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Parse the file
        tree = ast.parse(content)
        
        # Count comments
        comment_lines = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                comment_lines.add(node.lineno)
        
        # Count total lines and empty lines
        total_lines = len(content.splitlines())
        empty_lines = sum(1 for line in content.splitlines() if not line.strip())
        
        # Calculate code lines (total - comments - empty)
        code_lines = total_lines - len(comment_lines) - empty_lines
        
        return code_lines, len(comment_lines), empty_lines
    except:
        return 0, 0, 0

def create_metrics_table(metrics):
    """Create a rich table for basic metrics."""
    table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Total Size", format_size(metrics['total_size_kb']))
    table.add_row("Total Files", str(metrics['total_files']))
    table.add_row("Total Directories", str(metrics['total_directories']))
    table.add_row("Total Lines", f"{metrics['total_lines']:,}")
    table.add_row("Code Lines", f"{metrics['total_code_lines']:,}")
    table.add_row("Comment Lines", f"{metrics['total_comment_lines']:,}")
    table.add_row("Empty Lines", f"{metrics['total_empty_lines']:,}")
    table.add_row("Functions", f"{metrics['total_functions']:,}")
    table.add_row("Classes", f"{metrics['total_classes']:,}")
    
    return table

def create_code_connections_table(code_connections):
    """Create a table showing most called functions and methods."""
    table = Table(box=box.ROUNDED, show_header=True, padding=(0, 2))
    table.add_column("Type", style="cyan")
    table.add_column("Name", style="yellow")
    table.add_column("Called", style="green", justify="right")
    
    # Add function calls (top 10)
    function_calls = sorted(
        [(name, count) for name, count in code_connections['calls']['functions'].items()],
        key=lambda x: x[1], reverse=True
    )[:10]
    
    for name, count in function_calls:
        table.add_row("Function", name, str(count))
    
    # Add method calls (top 10)
    method_calls = []
    for cls, methods in code_connections['calls']['methods'].items():
        for method, count in methods.items():
            method_calls.append((f"{cls}.{method}", count))
    
    method_calls = sorted(method_calls, key=lambda x: x[1], reverse=True)[:10]
    
    for name, count in method_calls:
        table.add_row("Method", name, str(count))
    
    return table

def create_dead_code_table(code_connections):
    """Create a table showing potentially dead code."""
    table = Table(box=box.ROUNDED, show_header=True, padding=(0, 2))
    table.add_column("Type", style="cyan")
    table.add_column("Name", style="yellow")
    
    # Add potentially dead functions
    for func in sorted(code_connections['dead_code']['functions']):
        if not func.startswith('_'):  # Skip private functions
            table.add_row("Function", func)
    
    # Add potentially dead classes
    for cls in sorted(code_connections['dead_code']['classes']):
        if not cls.startswith('_'):  # Skip private classes
            table.add_row("Class", cls)
    
    # Add potentially dead methods
    for cls, methods in code_connections['dead_code']['methods'].items():
        for method in sorted(methods):
            if not method.startswith('_'):  # Skip private methods
                table.add_row("Method", f"{cls}.{method}")
    
    return table

def create_code_connections_tree(code_connections):
    """Create a tree showing code connections and imports."""
    # Start with root node
    tree = Tree("🔄 Code Connections", style="bold blue")
    
    # Add imports section
    imports_node = tree.add("📥 Most Imported Modules", style="cyan")
    import_counts = sorted(
        [(module, count) for module, count in code_connections['calls']['imports'].items()],
        key=lambda x: x[1], reverse=True
    )[:10]
    
    for module, count in import_counts:
        imports_node.add(f"{module} ({count} imports)", style="yellow")
    
    # Add functions section - most called
    functions_node = tree.add("🔸 Most Called Functions", style="magenta")
    function_calls = sorted(
        [(name, count) for name, count in code_connections['calls']['functions'].items()],
        key=lambda x: x[1], reverse=True
    )[:10]
    
    for name, count in function_calls:
        functions_node.add(f"{name} ({count} calls)", style="green")
    
    # Add methods section - most called
    methods_node = tree.add("🔹 Most Called Methods", style="blue")
    method_calls = []
    for cls, methods in code_connections['calls']['methods'].items():
        for method, count in methods.items():
            method_calls.append((f"{cls}.{method}", count))
    
    method_calls = sorted(method_calls, key=lambda x: x[1], reverse=True)[:10]
    
    for name, count in method_calls:
        methods_node.add(f"{name} ({count} calls)", style="green")
    
    return tree

def create_file_table(metrics):
    """Create a rich table for file distribution."""
    table = Table(box=box.ROUNDED, show_header=True, padding=(0, 2))
    table.add_column("Path", style="cyan")
    table.add_column("File", style="yellow")
    table.add_column("Code", style="green", justify="right")
    table.add_column("Comments", style="blue", justify="right")
    table.add_column("Empty", style="magenta", justify="right")
    table.add_column("Total", style="green", justify="right")
    table.add_column("Size", style="blue", justify="right")
    
    for folder in metrics['file_structure']:
        path = folder['path'] or 'Root'
        for file in folder['files']:
            table.add_row(
                path,
                file['name'],
                f"{file['code_lines']:,}",
                f"{file['comment_lines']:,}",
                f"{file['empty_lines']:,}",
                f"{file['lines']:,}",
                format_size(file['size_kb'])
            )
    
    return table

def print_stats(metrics):
    """Print formatted statistics from the analysis."""
    # Basic Metrics
    console.print("\n[bold cyan]📊 Basic Metrics[/bold cyan]")
    console.print(create_metrics_table(metrics))

def print_structure(metrics):
    """Print file structure tree."""
    console.print("\n[bold cyan]🌳 File Structure[/bold cyan]")
    console.print(create_structure_tree(metrics))

def print_files(metrics):
    """Print file distribution table."""
    console.print("\n[bold cyan]📁 File Distribution[/bold cyan]")
    console.print(create_file_table(metrics))

def print_calls(metrics):
    """Print code connections information."""
    if 'code_connections' in metrics:
        console.print("\n[bold cyan]🔗 Code Connections[/bold cyan]")
        console.print(create_code_connections_tree(metrics['code_connections']))
        
        console.print("\n[bold cyan]📊 Most Called Elements[/bold cyan]")
        console.print(create_code_connections_table(metrics['code_connections']))
    else:
        console.print("\n[bold red]Error: Code connections analysis not available[/bold red]")

def print_dead_code(metrics):
    """Print potentially unused code."""
    if 'code_connections' in metrics:
        # Only show dead code if there is any
        dead_code_count = (
            len(metrics['code_connections']['dead_code']['functions']) +
            len(metrics['code_connections']['dead_code']['classes']) +
            sum(len(methods) for methods in metrics['code_connections']['dead_code']['methods'].values())
        )
        
        if dead_code_count > 0:
            console.print("\n[bold red]💀 Potentially Unused Code[/bold red]")
            console.print(create_dead_code_table(metrics['code_connections']))
        else:
            console.print("\n[bold green]✓ No potentially unused code found[/bold green]")
    else:
        console.print("\n[bold red]Error: Dead code analysis not available[/bold red]")

def print_dependencies(directory: str):
    """Print dependency analysis results."""
    console.print("\n[bold blue]📦 Dependency Analysis[/bold blue]")
    
    deps = analyze_dependencies(directory)
    
    # Create table for external packages
    if deps['external_packages']:
        table = Table(title="External Dependencies", box=box.ROUNDED)
        table.add_column("Package", style="cyan")
        table.add_column("Files Using It", style="green")
        
        # Count package usage across files
        package_usage = defaultdict(list)
        for file_path, file_deps in deps['file_dependencies'].items():
            for package in file_deps['external']:
                package_usage[package].append(Path(file_path).name)
        
        # Add rows sorted by package name
        for package in sorted(deps['external_packages']):
            files = package_usage[package]
            table.add_row(
                package,
                ", ".join(sorted(files))
            )
        
        console.print(table)
    else:
        console.print("[yellow]No external dependencies found.[/yellow]")
    
    # Create table for standard library usage
    if deps['standard_library']:
        table = Table(title="Standard Library Usage", box=box.ROUNDED)
        table.add_column("Module", style="cyan")
        table.add_column("Files Using It", style="green")
        
        # Count module usage across files
        module_usage = defaultdict(list)
        for file_path, file_deps in deps['file_dependencies'].items():
            for module in file_deps['standard_library']:
                module_usage[module].append(Path(file_path).name)
        
        # Add rows sorted by module name
        for module in sorted(deps['standard_library']):
            files = module_usage[module]
            table.add_row(
                module,
                ", ".join(sorted(files))
            )
        
        console.print(table)
    else:
        console.print("[yellow]No standard library modules used.[/yellow]")

def print_all(metrics):
    """Print all information from all commands."""
    print_stats(metrics)
    console.print("\n")
    
    print_structure(metrics)
    console.print("\n")
    
    print_files(metrics)
    console.print("\n")
    
    print_calls(metrics)
    console.print("\n")
    
    print_dead_code(metrics)
    console.print("\n")
    
    print_dependencies(str(Path(args.directory).resolve()))
    console.print("\n")

def print_help():
    """Print help information about PyCodar commands."""
    console.print("\n[bold cyan]PyCodar: A Radar for Your Code[/bold cyan]")
    console.print("A simple tool for auditing and understanding your (python) codebase.\n")
    
    # Create a table for commands
    table = Table(box=box.ROUNDED, show_header=True, padding=(0, 2))
    table.add_column("Command", style="yellow")
    table.add_column("Description", style="green")
    
    # Add commands and their descriptions
    table.add_row("pycodar stats", "Summarizes the most basic stats of your directory in a single table. 📊")
    table.add_row("pycodar strct", "Displays the file structure of all the files, their functions, classes, and methods in a nicely colored tree. 🗂️")
    table.add_row("pycodar files", "Shows a table of all the files with counts of the lines of code, comments, empty lines, total lines, and file size. 📋")
    table.add_row("pycodar calls", "Counts how often elements (modules, functions, methods) of your code are called within the code. 📞")
    table.add_row("pycodar dead", "Finds (likely) unused code. ☠️")
    table.add_row("pycodar deps", "Shows which external packages and standard library modules are used in your code. 📦")
    table.add_row("pycodar all", "Shows all information from all commands in sequence. 🔍")
    table.add_row("pycodar help", "Shows this help information. ℹ️")
    
    console.print(table)
    console.print("\n")

def process_directory(args):
    """Process a directory and return metrics."""
    base_path = Path(args.path)
    if not base_path.exists():
        console.print(f"[red]Error: Path '{base_path}' does not exist[/red]", file=sys.stderr)
        sys.exit(1)
    
    # Get ignore patterns
    ignore_patterns = get_ignore_patterns(base_path)
    
    # Enhance the metrics with code analysis
    metrics = analyze_directory(str(base_path))
    
    # Add code metrics
    total_code_lines = 0
    total_comment_lines = 0
    total_empty_lines = 0
    total_directories = 0
    filtered_file_structure = []
    
    for folder in metrics['file_structure']:
        folder_path = Path(folder['path']) if folder['path'] else Path('.')
        if should_ignore(folder_path, ignore_patterns):
            continue
            
        filtered_files = []
        for file in folder['files']:
            file_path = folder_path / file['name']
            if should_ignore(file_path, ignore_patterns):
                continue
                
            if file['name'].endswith('.py'):
                code_lines, comment_lines, empty_lines = count_code_metrics(str(file_path))
                file['code_lines'] = code_lines
                file['comment_lines'] = comment_lines
                file['empty_lines'] = empty_lines
                total_code_lines += code_lines
                total_comment_lines += comment_lines
                total_empty_lines += empty_lines
            else:
                file['code_lines'] = 0
                file['comment_lines'] = 0
                file['empty_lines'] = 0
            
            filtered_files.append(file)
        
        if filtered_files:
            folder['files'] = filtered_files
            filtered_file_structure.append(folder)
            total_directories += 1
    
    metrics['file_structure'] = filtered_file_structure
    metrics['total_code_lines'] = total_code_lines
    metrics['total_comment_lines'] = total_comment_lines
    metrics['total_empty_lines'] = total_empty_lines
    metrics['total_directories'] = total_directories
    metrics['total_files'] = sum(len(folder['files']) for folder in filtered_file_structure)
    
    return metrics

def main():
    parser = argparse.ArgumentParser(description='PyCodar - A Radar for Your Code')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Common path argument for all commands
    path_help = 'Path to analyze (default: current directory)'
    
    # Stats command - Shows basic metrics
    stats_parser = subparsers.add_parser('stats', help='Show basic code metrics and statistics')
    stats_parser.add_argument('--path', default='.', help=path_help)
    
    # Structure command - Shows file structure tree
    strct_parser = subparsers.add_parser('strct', help='Display file structure with functions, classes, and methods')
    strct_parser.add_argument('--path', default='.', help=path_help)
    
    # Files command - Shows file distribution table
    files_parser = subparsers.add_parser('files', help='Show table of files with line counts')
    files_parser.add_argument('--path', default='.', help=path_help)
    
    # Calls command - Shows code connections information
    calls_parser = subparsers.add_parser('calls', help='Count how often code elements are called')
    calls_parser.add_argument('--path', default='.', help=path_help)
    
    # Dead code command - Shows potentially unused code
    dead_parser = subparsers.add_parser('dead', help='Find potentially unused code')
    dead_parser.add_argument('--path', default='.', help=path_help)
    
    # Dependencies command - Shows dependency analysis
    deps_parser = subparsers.add_parser('deps', help='Show dependency analysis results')
    deps_parser.add_argument('--path', default='.', help=path_help)
    
    # All command - Shows all information
    all_parser = subparsers.add_parser('all', help='Show all information from all commands')
    all_parser.add_argument('--path', default='.', help=path_help)
    
    # Help command - Shows help information
    help_parser = subparsers.add_parser('help', help='Show help information about PyCodar commands')
    
    args = parser.parse_args()
    
    if args.command == 'help':
        print_help()
    elif args.command in ('stats', 'strct', 'files', 'calls', 'dead', 'deps', 'all'):
        # Process directory and get metrics
        metrics = process_directory(args)
        
        # Display requested information based on command
        if args.command == 'stats':
            print_stats(metrics)
            console.print("\n")
        elif args.command == 'strct':
            print_structure(metrics)
            console.print("\n")
        elif args.command == 'files':
            print_files(metrics)
            console.print("\n")
        elif args.command == 'calls':
            print_calls(metrics)
            console.print("\n")
        elif args.command == 'dead':
            print_dead_code(metrics)
            console.print("\n")
        elif args.command == 'deps':
            print_dependencies(str(Path(args.path).resolve()))
            console.print("\n")
        elif args.command == 'all':
            print_all(metrics)
    else:
        # If no command is provided, show help
        print_help()

if __name__ == '__main__':
    main() 