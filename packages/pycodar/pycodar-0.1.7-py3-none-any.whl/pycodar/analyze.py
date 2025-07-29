import os
import ast
import sys
import importlib
from typing import Dict, Tuple, List, Set, Optional
from collections import defaultdict

def count_functions_and_classes(file_path: str) -> Tuple[int, int]:
    """Count the number of functions and classes in a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        tree = ast.parse(content)
        
        num_functions = len([node for node in ast.walk(tree) 
                           if isinstance(node, ast.FunctionDef)])
        num_classes = len([node for node in ast.walk(tree) 
                          if isinstance(node, ast.ClassDef)])
        
        return num_functions, num_classes
    except:
        return 0, 0

def get_file_size_kb(file_path: str) -> float:
    """Get file size in KB."""
    return os.path.getsize(file_path) / 1024

def count_lines(file_path: str) -> int:
    """Count number of lines in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return sum(1 for _ in file)
    except:
        return 0

class CodeElementVisitor(ast.NodeVisitor):
    """AST visitor that tracks definitions and calls."""
    
    def __init__(self, file_path: str, module_name: Optional[str] = None):
        self.file_path = file_path
        self.module_name = module_name or os.path.basename(file_path).replace('.py', '')
        
        # Track defined elements
        self.defined_functions = set()
        self.defined_classes = set()
        self.defined_methods = defaultdict(set)  # class_name -> methods
        
        # Track imports
        self.imports = set()
        self.from_imports = defaultdict(set)  # module -> names
        self.import_aliases = {}  # alias -> original
        
        # Track calls
        self.function_calls = defaultdict(int)  # func_name -> count
        self.method_calls = defaultdict(lambda: defaultdict(int))  # class_name -> {method_name -> count}
        self.imported_calls = defaultdict(int)  # imported_name -> count
        
        # Track attribute access
        self.attribute_access = defaultdict(set)  # object_name -> set of attributes
        
        # Track variable assignments and references
        self.variable_assignments = defaultdict(set)  # var_name -> set of assigned values (class/func names)
        self.variable_references = set()  # set of variable names that are referenced
        
        # Track class instantiations
        self.class_instantiations = defaultdict(int)  # class_name -> count
        
        # Track current context
        self.current_class = None
        self.current_function = None
        self.context_stack = []
    
    def visit_FunctionDef(self, node):
        if self.current_class:
            # This is a method
            full_name = f"{self.current_class}.{node.name}"
            self.defined_methods[self.current_class].add(node.name)
        else:
            # This is a function
            full_name = f"{self.module_name}.{node.name}"
            self.defined_functions.add(node.name)
        
        # Save current context
        prev_function = self.current_function
        self.current_function = node.name
        self.context_stack.append(('function', node.name))
        
        # Continue visiting the function body
        self.generic_visit(node)
        
        # Restore previous context
        self.current_function = prev_function
        self.context_stack.pop()
    
    def visit_ClassDef(self, node):
        class_name = node.name
        self.defined_classes.add(class_name)
        
        # Save the previous context and set the new one
        prev_class = self.current_class
        self.current_class = class_name
        self.context_stack.append(('class', class_name))
        
        # Check for class decorators - these indicate the class is used
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                self.function_calls[decorator.id] += 1
            elif isinstance(decorator, ast.Attribute) and isinstance(decorator.value, ast.Name):
                self.method_calls[decorator.value.id][decorator.attr] += 1
        
        # Visit class body
        self.generic_visit(node)
        
        # Restore the previous context
        self.current_class = prev_class
        self.context_stack.pop()
    
    def visit_Import(self, node):
        for name in node.names:
            imported_name = name.name
            alias = name.asname or imported_name
            self.imports.add(imported_name)
            
            # Track import aliases
            if name.asname:
                self.import_aliases[alias] = imported_name
    
    def visit_ImportFrom(self, node):
        if node.module:
            for name in node.names:
                imported_name = name.name
                alias = name.asname or imported_name
                self.from_imports[node.module].add(imported_name)
                
                # Track import aliases
                if name.asname:
                    if node.module == '.':
                        self.import_aliases[alias] = f"{imported_name}"
                    else:
                        self.import_aliases[alias] = f"{node.module}.{imported_name}"
    
    def visit_Call(self, node):
        # Track function/method calls
        if isinstance(node.func, ast.Name):
            # Direct function call
            func_name = node.func.id
            self.function_calls[func_name] += 1
            
            # Check if this is a class instantiation
            if func_name[0].isupper():  # Classes typically start with uppercase
                self.class_instantiations[func_name] += 1
                
        elif isinstance(node.func, ast.Attribute):
            # Method call or imported module function call
            if isinstance(node.func.value, ast.Name):
                obj_name = node.func.value.id
                method_name = node.func.attr
                
                # Store both as method call and as attribute access
                self.method_calls[obj_name][method_name] += 1
                self.attribute_access[obj_name].add(method_name)
        
        # Check for getattr, hasattr, etc. which might be used for dynamic attribute access
        if isinstance(node.func, ast.Name) and node.func.id in ('getattr', 'hasattr', 'setattr'):
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Str):
                if isinstance(node.args[0], ast.Name):
                    obj_name = node.args[0].id
                    attr_name = node.args[1].s
                    self.attribute_access[obj_name].add(attr_name)
        
        # Continue visiting for nested calls
        self.generic_visit(node)
    
    def visit_Assign(self, node):
        # Track variable assignments
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id
                
                # Check if assigning a class or function
                if isinstance(node.value, ast.Name):
                    self.variable_assignments[var_name].add(node.value.id)
                elif isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                    # Assigning result of a function/class instantiation
                    self.variable_assignments[var_name].add(node.value.func.id)
        
        self.generic_visit(node)
    
    def visit_Name(self, node):
        # Track variable references
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            self.variable_references.add(node.id)
        
        self.generic_visit(node)
    
    def visit_Attribute(self, node):
        # Track attribute access separate from method calls
        if isinstance(node.value, ast.Name):
            obj_name = node.value.id
            attr_name = node.attr
            self.attribute_access[obj_name].add(attr_name)
        
        self.generic_visit(node)
    
    def visit_Return(self, node):
        # Track return values which might be classes or functions
        if isinstance(node.value, ast.Name):
            # If returning a name, it's being used
            self.variable_references.add(node.value.id)
        
        self.generic_visit(node)
    
    def visit_Decorator(self, node):
        # Track usage of functions as decorators
        if isinstance(node, ast.Name):
            self.function_calls[node.id] += 1
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            self.method_calls[node.value.id][node.attr] += 1
        
        self.generic_visit(node)

def analyze_code_connections(directory: str) -> Dict:
    """Analyze code connections in a directory."""
    # Map to track all defined elements
    all_definitions = {
        'functions': set(),  # Set of "module.function" strings
        'classes': set(),    # Set of "module.class" strings
        'methods': defaultdict(set),  # "class" -> set of methods
    }
    
    # Maps to track all calls
    all_calls = {
        'functions': defaultdict(int),  # "function_name" -> count
        'methods': defaultdict(lambda: defaultdict(int)),  # "class" -> {"method" -> count}
        'imports': defaultdict(int),  # "module" -> count
        'class_instantiations': defaultdict(int),  # "class_name" -> count
        'attribute_access': defaultdict(set),  # "object_name" -> set of attributes
    }
    
    # Maps to track per-file elements
    file_elements = {}  # file_path -> visitor
    
    # Maps for imported module resolution
    module_functions = {}  # module_name -> set of functions
    module_classes = {}    # module_name -> set of classes
    
    # First pass: collect all definitions
    for root, _, files in os.walk(directory):
        if '.git' in root or '__pycache__' in root or '.pytest_cache' in root:
            continue
        
        for file in files:
            if not file.endswith('.py'):
                continue
                
            file_path = os.path.join(root, file)
            module_name = os.path.relpath(file_path, directory).replace('/', '.').replace('\\', '.').replace('.py', '')
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read(), filename=file_path)
                
                visitor = CodeElementVisitor(file_path, module_name)
                visitor.visit(tree)
                
                # Store the visitor for the second pass
                file_elements[file_path] = visitor
                
                # Add definitions to the global maps
                for func in visitor.defined_functions:
                    full_func = f"{module_name}.{func}"
                    all_definitions['functions'].add(full_func)
                    
                    # Add to module functions map
                    if module_name not in module_functions:
                        module_functions[module_name] = set()
                    module_functions[module_name].add(func)
                
                for cls in visitor.defined_classes:
                    full_class = f"{module_name}.{cls}"
                    all_definitions['classes'].add(full_class)
                    
                    # Add to module classes map
                    if module_name not in module_classes:
                        module_classes[module_name] = set()
                    module_classes[module_name].add(cls)
                    
                for cls, methods in visitor.defined_methods.items():
                    full_class = f"{module_name}.{cls}"
                    all_definitions['methods'][full_class].update(methods)
            except Exception as e:
                print(f"Error parsing {file_path}: {e}")
    
    # Second pass: analyze calls and determine what's called vs. what's defined
    for file_path, visitor in file_elements.items():
        # Process function calls
        for func_name, count in visitor.function_calls.items():
            all_calls['functions'][func_name] += count
        
        # Process method calls
        for cls_name, methods in visitor.method_calls.items():
            for method_name, count in methods.items():
                all_calls['methods'][cls_name][method_name] += count
        
        # Process class instantiations
        for cls_name, count in visitor.class_instantiations.items():
            all_calls['class_instantiations'][cls_name] += count
        
        # Process attribute access
        for obj_name, attrs in visitor.attribute_access.items():
            all_calls['attribute_access'][obj_name].update(attrs)
        
        # Process imports
        for import_name in visitor.imports:
            all_calls['imports'][import_name] += 1
        
        for module, names in visitor.from_imports.items():
            all_calls['imports'][module] += 1
    
    # Identify potentially dead code (defined but not called)
    dead_code = {
        'functions': set(),
        'classes': set(),
        'methods': defaultdict(set),
    }
    
    # Build a set of special method names that are called implicitly
    implicit_methods = {
        '__init__', '__new__', '__del__', '__repr__', '__str__', 
        '__bytes__', '__format__', '__lt__', '__le__', '__eq__', '__ne__', 
        '__gt__', '__ge__', '__hash__', '__bool__', '__getattr__', '__getattribute__',
        '__setattr__', '__delattr__', '__dir__', '__get__', '__set__', '__delete__',
        '__slots__', '__call__', '__len__', '__getitem__', '__setitem__', '__delitem__',
        '__iter__', '__reversed__', '__contains__', '__add__', '__sub__', '__mul__',
        '__matmul__', '__truediv__', '__floordiv__', '__mod__', '__divmod__', '__pow__',
        '__lshift__', '__rshift__', '__and__', '__xor__', '__or__', '__radd__', '__rsub__',
        '__rmul__', '__rmatmul__', '__rtruediv__', '__rfloordiv__', '__rmod__', '__rdivmod__',
        '__rpow__', '__rlshift__', '__rrshift__', '__rand__', '__rxor__', '__ror__',
        '__iadd__', '__isub__', '__imul__', '__imatmul__', '__itruediv__', '__ifloordiv__',
        '__imod__', '__ipow__', '__ilshift__', '__irshift__', '__iand__', '__ixor__', '__ior__',
        '__neg__', '__pos__', '__abs__', '__invert__', '__complex__', '__int__', '__float__',
        '__round__', '__trunc__', '__floor__', '__ceil__', '__enter__', '__exit__',
        '__await__', '__aiter__', '__anext__', '__aenter__', '__aexit__'
    }
    
    # Check for potentially dead functions
    for full_func in all_definitions['functions']:
        module, func = full_func.rsplit('.', 1)
        
        # Skip if function is called directly
        if func in all_calls['functions']:
            continue
            
        # Skip if function is exported in __init__ (likely part of public API)
        if module.endswith('__init__'):
            continue
            
        # Skip if function starts with underscore (private implementation detail)
        if func.startswith('_'):
            continue
            
        # Skip if function is used via a module import
        # e.g., import mymodule; mymodule.func()
        module_basename = module.split('.')[-1]
        if (module_basename in all_calls['attribute_access'] and 
            func in all_calls['attribute_access'][module_basename]):
            continue
            
        # Skip main functions
        if func == 'main':
            continue
            
        # If we get here, the function is potentially dead
        dead_code['functions'].add(full_func)
    
    # Check for potentially dead classes
    for full_class in all_definitions['classes']:
        module, cls = full_class.rsplit('.', 1)
        
        # Skip if class is instantiated directly
        if cls in all_calls['class_instantiations']:
            continue
            
        # Skip if class is called directly (e.g., used as a decorator)
        if cls in all_calls['functions']:
            continue
            
        # Skip if class is accessed via module
        module_basename = module.split('.')[-1]
        if (module_basename in all_calls['attribute_access'] and 
            cls in all_calls['attribute_access'][module_basename]):
            continue
            
        # Skip if class methods are called
        if cls in all_calls['methods']:
            continue
            
        # Skip if class is exported in __init__ (likely part of public API)
        if module.endswith('__init__'):
            continue
            
        # Skip if class starts with underscore (private implementation detail)
        if cls.startswith('_'):
            continue
        
        # Skip if it's a base class that other classes inherit from
        # TODO: Add inheritance tracking
            
        # If we get here, the class is potentially dead
        dead_code['classes'].add(full_class)
    
    # Check for potentially dead methods
    for full_class, methods in all_definitions['methods'].items():
        module, cls = full_class.rsplit('.', 1)
        
        # If class is instantiated, special methods might be called implicitly
        class_is_used = (cls in all_calls['class_instantiations'] or 
                          cls in all_calls['functions'] or
                          cls in all_calls['methods'])
        
        for method in methods:
            # Skip special methods if class is used
            if method in implicit_methods and class_is_used:
                continue
                
            # Skip if method is called
            if cls in all_calls['methods'] and method in all_calls['methods'][cls]:
                continue
                
            # Skip if method is private
            if method.startswith('_') and not method.startswith('__'):
                continue
            
            # Skip common test methods
            if method.startswith('test_'):
                continue
                
            # Skip if method is accessed as attribute
            if cls in all_calls['attribute_access'] and method in all_calls['attribute_access'][cls]:
                continue
            
            # If we get here, the method is potentially dead
            if not class_is_used:  # Only mark methods as dead if their class is unused
                dead_code['methods'][full_class].add(method)
    
    return {
        'definitions': all_definitions,
        'calls': all_calls,
        'dead_code': dead_code,
        'file_elements': file_elements
    }

def analyze_directory(directory: str) -> Dict:
    """Analyze a directory and return metrics."""
    total_size = 0
    total_files = 0
    total_functions = 0
    total_classes = 0
    total_lines = 0
    file_structure = []
    lines_by_folder = {}
    
    for root, dirs, files in os.walk(directory):
        if '.git' in root or '__pycache__' in root or '.pytest_cache' in root:
            continue
            
        relative_path = os.path.relpath(root, directory)
        if relative_path == '.':
            relative_path = ''
        
        folder_lines = 0
        folder_files = []
        
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip non-Python files for function/class counting
            is_python = file.endswith('.py')
            
            size_kb = get_file_size_kb(file_path)
            lines = count_lines(file_path)
            
            if is_python:
                funcs, classes = count_functions_and_classes(file_path)
                total_functions += funcs
                total_classes += classes
            else:
                funcs, classes = 0, 0
            
            total_size += size_kb
            total_files += 1
            total_lines += lines
            folder_lines += lines
            
            file_info = {
                'name': file,
                'size_kb': round(size_kb, 2),
                'lines': lines,
                'functions': funcs,
                'classes': classes
            }
            folder_files.append(file_info)
        
        if folder_files:
            file_structure.append({
                'path': relative_path,
                'files': folder_files
            })
            lines_by_folder[relative_path] = folder_lines
    
    # Analyze code connections
    code_connections = analyze_code_connections(directory)
    
    return {
        'total_size_kb': round(total_size, 2),
        'total_files': total_files,
        'total_functions': total_functions,
        'total_classes': total_classes,
        'total_lines': total_lines,
        'file_structure': file_structure,
        'lines_by_folder': lines_by_folder,
        'code_connections': code_connections
    }

def generate_report():
    """Generate and print the project analysis report."""
    print("=== BEAMZ Project Analysis Report ===\n")
    
    # Analyze the project
    project_root = '.'
    core_package = './beamz'
    
    project_metrics = analyze_directory(project_root)
    core_metrics = analyze_directory(core_package)
    
    # 1. Project File Structure
    print("1. Project File Structure:")
    for folder in project_metrics['file_structure']:
        path = folder['path']
        print(f"\n{'  ' if path else ''}{path or 'Root'}:")
        for file in folder['files']:
            print(f"  {'  ' if path else ''}{file['name']} "
                  f"({file['size_kb']:.2f}KB, {file['lines']} lines)")
    
    # 2. Project Size
    print(f"\n2. Project Size:")
    print(f"Total size: {project_metrics['total_size_kb']:.2f}KB")
    print(f"Core package size: {core_metrics['total_size_kb']:.2f}KB")
    
    # 3. Number of Files
    print(f"\n3. Number of Files:")
    print(f"Total files: {project_metrics['total_files']}")
    print(f"Core package files: {core_metrics['total_files']}")
    
    # 4. Functions and Classes
    print(f"\n4. Functions and Classes:")
    print(f"Total functions: {project_metrics['total_functions']}")
    print(f"Total classes: {project_metrics['total_classes']}")
    print(f"Core package functions: {core_metrics['total_functions']}")
    print(f"Core package classes: {core_metrics['total_classes']}")
    
    # 5. Lines of Code
    print(f"\n5. Lines of Code:")
    print("By folder:")
    for folder, lines in project_metrics['lines_by_folder'].items():
        if folder.startswith('beamz'):
            print(f"  {folder or 'Root'}: {lines} lines")
    print(f"\nCore package total: {core_metrics['total_lines']} lines")
    print(f"Project total: {project_metrics['total_lines']} lines")

def is_standard_library(module_name: str) -> bool:
    """Check if a module is part of the Python standard library."""
    try:
        # Handle relative imports
        if module_name.startswith('.'):
            return False
            
        # Handle submodules
        base_module = module_name.split('.')[0]
        
        # Check if it's a built-in module
        if base_module in sys.stdlib_module_names:
            return True
            
        # Try to import the module to check if it's in stdlib
        spec = importlib.util.find_spec(base_module)
        if spec is None:
            return False
            
        # Check if the module is in the standard library path
        stdlib_path = os.path.dirname(os.__file__)
        return spec.origin and stdlib_path in spec.origin
    except:
        return False

def analyze_dependencies(directory: str) -> Dict[str, Set[str]]:
    """
    Analyze Python files in a directory and return their external dependencies.
    
    Args:
        directory: Path to the directory to analyze
        
    Returns:
        Dict containing:
        - 'external_packages': Set of external package names
        - 'standard_library': Set of standard library modules used
        - 'file_dependencies': Dict mapping file paths to their dependencies
    """
    result = {
        'external_packages': set(),
        'standard_library': set(),
        'file_dependencies': {}
    }
    
    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith('.py'):
                continue
                
            file_path = os.path.join(root, file)
            file_deps = {
                'external': set(),
                'standard_library': set()
            }
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            module_name = name.name.split('.')[0]  # Get base package name
                            if is_standard_library(module_name):
                                result['standard_library'].add(module_name)
                                file_deps['standard_library'].add(module_name)
                            else:
                                result['external_packages'].add(module_name)
                                file_deps['external'].add(module_name)
                                
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            module_name = node.module.split('.')[0]  # Get base package name
                            if is_standard_library(module_name):
                                result['standard_library'].add(module_name)
                                file_deps['standard_library'].add(module_name)
                            else:
                                result['external_packages'].add(module_name)
                                file_deps['external'].add(module_name)
                                
            except Exception as e:
                print(f"Error analyzing {file_path}: {str(e)}")
                continue
                
            result['file_dependencies'][file_path] = file_deps
            
    return result

if __name__ == "__main__":
    generate_report() 