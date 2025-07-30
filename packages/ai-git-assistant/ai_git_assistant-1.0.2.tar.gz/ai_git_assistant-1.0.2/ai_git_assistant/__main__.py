#!/usr/bin/env python3

import subprocess
import os
import re
from collections import Counter
import random
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

def print_ascii_logo():
    print(r"""
      _________
     / ======= \
    / __________\
   | ___________ |
   | | -     - | |
   | |   Git   | |      Intelligent Commit Assistant
   | |_________| |
   \=___________=/
   / ''''''''''' \
  / ::::::::::::: \
 (_________________)
    """)

TYPES = {
    'feat': ['add', 'create', 'implement', 'new', 'feature'],
    'fix': ['fix', 'bug', 'error', 'issue', 'resolve', 'solve'],
    'refactor': ['refactor', 'restructure', 'clean', 'improve', 'simplify'],
    'chore': ['update', 'upgrade', 'bump', 'maintain', 'setup'],
    'test': ['test', 'assert', 'coverage', 'spec', 'validate'],
    'docs': ['document', 'comment', 'readme', 'guide', 'wiki'],
    'style': ['style', 'format', 'indent', 'css', 'layout'],
    'perf': ['performance', 'optimize', 'speed', 'efficiency', 'faster']
}

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model.pkl')

def run_git_command(args):
    result = subprocess.run(args, capture_output=True, text=True)
    return result.stdout.strip().splitlines() if result.stdout.strip() else []

def resolve_file_path(file_path):
    if os.path.exists(file_path):
        return os.path.abspath(file_path)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    possible_path = os.path.join(script_dir, file_path)
    if os.path.exists(possible_path):
        return possible_path
    
    basename = os.path.basename(file_path)
    if os.path.exists(basename):
        return os.path.abspath(basename)
    
    return None

def git_status_info():
    def get_files(command):
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return [resolve_file_path(f) for f in result.stdout.splitlines() if f]
        except subprocess.CalledProcessError:
            return []
    
    return {
        "staged": [f for f in get_files(["git", "diff", "--cached", "--name-only"]) if f],
        "unstaged": [f for f in get_files(["git", "diff", "--name-only"]) if f],
        "untracked": [f for f in get_files(["git", "ls-files", "--others", "--exclude-standard"]) if f]
    }

def create_branch():
    new_branch = input('¿Quieres crear una nueva rama? (S/s): ')
    if new_branch.lower() == 's':
        name = input('Ingresa el nombre de tu nueva rama: ')
        subprocess.run(["git", "checkout", "-b", name], check=True)
        return name
    else:
        current_branch = run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        print(f'ℹ️ Continuarás trabajando en la rama actual: {current_branch[0]}')
        return current_branch[0]

def add_files(files):
    if not files:
        print("No hay archivos para agregar.")
        return 0
    
    success = 0
    for file_path in files:
        resolved_path = resolve_file_path(file_path)
        if not resolved_path:
            print(f"✗ No se pudo encontrar: {file_path}")
            continue
        
        try:
            subprocess.run(["git", "add", resolved_path], check=True)
            print(f"✓ Agregado: {resolved_path}")
            success += 1
        except subprocess.CalledProcessError:
            print(f"✗ Error al agregar: {resolved_path}")
    
    return success

def detect_files_by_extension(extension):
    status = git_status_info()
    all_files = status["staged"] + status["unstaged"] + status["untracked"]
    return [f for f in all_files if f and f.lower().endswith(extension)]

def get_file_diff(file_path):
    try:
        result = subprocess.run(["git", "diff", "--cached", file_path], 
                              capture_output=True, text=True)
        return result.stdout
    except:
        return ""

def extract_changes(diff_text):
    relevant_lines = []
    for line in diff_text.split('\n'):
        if line.startswith('+') and not line.startswith('+++'):
            relevant_lines.append(line[1:].strip())
    return ' '.join(relevant_lines)

def train_model():
    X = []
    y = []
    
    for commit_type, keywords in TYPES.items():
        for keyword in keywords:
            examples = [
                f"Added {keyword} functionality",
                f"Implemented {keyword} feature",
                f"{keyword.capitalize()} module created",
                f"Applied {keyword} to improve code",
                f"New {keyword} implementation"
            ]
            X.extend(examples)
            y.extend([commit_type] * len(examples))
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000)),
        ('clf', MultinomialNB())
    ])
    
    pipeline.fit(X, y)
    joblib.dump(pipeline, MODEL_PATH)
    return pipeline

def load_or_train_model():
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except:
            print("Error al cargar el modelo existente. Entrenando uno nuevo...")
            return train_model()
    else:
        print("Entrenando modelo nuevo...")
        return train_model()

def get_file_type(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if ext in ['.py', '.js', '.java', '.cpp', '.c', '.h', '.ts', '.go', '.rb']:
        return 'code'
    elif ext in ['.md', '.txt', '.rst', '.pdf', '.doc', '.docx']:
        return 'docs'
    elif ext in ['.css', '.scss', '.less', '.html', '.xml']:
        return 'style'
    elif ext in ['.json', '.yaml', '.yml', '.toml', '.ini', '.conf']:
        return 'config'
    elif ext in ['.test.js', '.spec.py', '.test.py', '.test.ts']:
        return 'test'
    else:
        return 'other'

def analyze_changes(files):
    changes_text = ""
    file_types = Counter()
    
    for file in files:
        if os.path.exists(file):
            file_types[get_file_type(file)] += 1
            diff = get_file_diff(file)
            changes_text += extract_changes(diff) + " "
    
    predominant_type = file_types.most_common(1)[0][0] if file_types else 'other'
    return changes_text.strip(), predominant_type

def generate_commit_message(branch, files, changes_text, predominant_file_type, model):
    approaches = [
        lambda: generate_ml_based_message(branch, files, changes_text, predominant_file_type, model),
        lambda: generate_file_type_message(files, predominant_file_type),
        lambda: generate_thematic_message(changes_text, files),
        lambda: generate_descriptive_message(changes_text, files, predominant_file_type),
        lambda: generate_action_message(changes_text, files)
    ]
    
    previous_suggestions = []
    suggestion_index = 0
    
    while True:
        actual_index = suggestion_index % len(approaches)
        message = approaches[actual_index]()
        
        if message in previous_suggestions and len(previous_suggestions) < len(approaches):
            suggestion_index += 1
            continue
            
        previous_suggestions.append(message)
        
        print(f"\n💡 Sugerencia de commit #{suggestion_index + 1}:\n→ {message}")
        
        confirm = input("\n¿Deseas usar este mensaje? (S/s), (O/o) para otra opción o enter para ingresar tu commit: ")
        if confirm.lower() == 's':
            run_git_command(["git", "commit", "-m", message])
            print("✅ Commit realizado con éxito.")
            return message
        elif confirm.lower() == 'o':
            print("\n🔁 Generando otra opción...")
            suggestion_index += 1
            continue
        else:
            custom_message = input('Ingresa tu commit: ')
            run_git_command(["git", "commit", "-m", custom_message])
            print("✅ Commit realizado con éxito.")
            return custom_message

def generate_ml_based_message(branch, files, changes_text, predominant_file_type, model):
    if len(changes_text) < 10:
        branch_lower = branch.lower()
        commit_type = 'chore'
        
        for type_, keywords in TYPES.items():
            if any(keyword in branch_lower for keyword in keywords):
                commit_type = type_
                break
        
        if commit_type == 'chore':
            if predominant_file_type == 'code':
                commit_type = 'feat'
            elif predominant_file_type == 'docs':
                commit_type = 'docs'
            elif predominant_file_type == 'test':
                commit_type = 'test'
            elif predominant_file_type == 'style':
                commit_type = 'style'
        
        filename = os.path.basename(files[0]) if files else "cambios"
        return f"{commit_type}: cambios relacionados con {filename}"
    else:
        predicted_type = model.predict([changes_text])[0]
        
        words = re.findall(r'\b\w+\b', changes_text.lower())
        common_words = [w for w in Counter(words).most_common(3) if w[0] not in ['the', 'a', 'an', 'in', 'to', 'of']]
        
        if common_words:
            keywords = ' y '.join([w[0] for w in common_words])
            return f"{predicted_type}: {keywords} en {os.path.basename(files[0])}"
        else:
            filename = os.path.basename(files[0]) if files else "archivos"
            return f"{predicted_type}: actualización de {filename}"

def generate_file_type_message(files, predominant_file_type):
    type_to_commit = {
        'code': 'feat',
        'docs': 'docs',
        'test': 'test',
        'style': 'style',
        'config': 'chore',
        'other': 'chore'
    }
    
    commit_type = type_to_commit.get(predominant_file_type, 'chore')
    num_files = len(files)
    file_extensions = [os.path.splitext(f)[1] for f in files if os.path.splitext(f)[1]]
    most_common_ext = Counter(file_extensions).most_common(1)[0][0] if file_extensions else ""
    
    if num_files == 1:
        return f"{commit_type}: modificación de {os.path.basename(files[0])}"
    else:
        if most_common_ext:
            return f"{commit_type}: cambios en {num_files} archivos {most_common_ext}"
        else:
            return f"{commit_type}: actualización de múltiples archivos ({num_files})"

def generate_thematic_message(changes_text, files):
    words = re.findall(r'\b\w+\b', changes_text.lower())
    common_stop_words = ['the', 'a', 'an', 'in', 'to', 'of', 'and', 'or', 'for', 'with', 'on', 'at']
    filtered_words = [w for w in words if w not in common_stop_words and len(w) > 3]
    
    if filtered_words:
        word_count = Counter(filtered_words)
        mid_common_words = [w[0] for w in word_count.most_common()[len(word_count)//3:2*len(word_count)//3]]
        
        if mid_common_words:
            keywords = ' con '.join(random.sample(mid_common_words, min(2, len(mid_common_words))))
            commit_type = 'chore'
            for type_, keywords_list in TYPES.items():
                if any(kw in filtered_words for kw in keywords_list):
                    commit_type = type_
                    break
                    
            return f"{commit_type}: {keywords} en {os.path.basename(files[0]) if files else 'proyecto'}"

    commit_type = random.choice(['feat', 'refactor', 'chore'])
    return f"{commit_type}: mejoras en {os.path.basename(files[0]) if files else 'proyecto'}"

def generate_descriptive_message(changes_text, files, predominant_file_type):
    action_words = {
        'add': ['agregar', 'añadir', 'crear', 'implementar', 'nuevo'],
        'fix': ['arreglar', 'corregir', 'solucionar', 'reparar'],
        'update': ['actualizar', 'mejorar', 'modificar', 'cambiar'],
        'remove': ['eliminar', 'quitar', 'borrar', 'remover'],
        'refactor': ['refactorizar', 'reestructurar', 'simplificar']
    }
    
    words = re.findall(r'\b\w+\b', changes_text.lower())
    
    action = 'update'
    for act, keywords in action_words.items():
        if any(kw in words for kw in keywords):
            action = act
            break

    action_to_type = {
        'add': 'feat',
        'fix': 'fix',
        'update': 'chore',
        'remove': 'refactor',
        'refactor': 'refactor'
    }
    
    commit_type = action_to_type.get(action, 'chore')

    file_type_context = {
        'code': 'funcionalidad',
        'docs': 'documentación',
        'test': 'pruebas',
        'style': 'estilos',
        'config': 'configuración'
    }
    
    context = file_type_context.get(predominant_file_type, 'contenido')
    return f"{commit_type}: {action} {context} en {os.path.basename(files[0]) if files else 'proyecto'}"

def generate_action_message(changes_text, files):
    verbs = ['actualiza', 'mejora', 'modifica', 'optimiza', 'implementa', 'refactoriza']
    verb = random.choice(verbs)
    
    components = []
    for file in files:
        parts = file.split('/')
        if len(parts) > 1:
            components.append(parts[-2])
    
    most_common_component = Counter(components).most_common(1)[0][0] if components else "componente"
    return f"{verb} {most_common_component} en {os.path.basename(files[0]) if files else 'proyecto'}"

def handle_files_selection(files, message):
    if not files:
        return []
    
    print(f"\n{message}")
    for idx, file_path in enumerate(files):
        print(f" [{idx}] {file_path}")
    
    selection = input(
        "Ingresa los números (ej: 0,2,4)\n"
        "'t' para todos\n"
        "'n' para ninguno\n"
        "Opción: "
    ).strip().lower()
    
    if selection == 't':
        return files
    elif selection == 'n':
        return []
    else:
        try:
            selected_indices = [int(i) for i in selection.split(',')]
            return [
                files[i] 
                for i in selected_indices 
                if 0 <= i < len(files)
            ]
        except ValueError:
            print("⚠️ Entrada inválida. Usando ninguno.")
            return []

def prompt_testing_notes():
    print("\n¿Deseas agregar información para la sección de 'Consideraciones para Testing'? (s/n): ", end='')
    if input().strip().lower() == 's':
        print("Escribe lo que desees agregar (finaliza con Enter):")
        return input().strip()
    return 'N/A'

def prompt_compatible_apps():
    apps = []
    
    print("\n# Aplicaciones compatibles")
    print("| Aplicación  | Versión |")
    print("|-------------|---------|")
    
    app_count = 1
    while True:
        app_name = input(f"Nombre de la App {app_count} (deja vacío para terminar): ").strip()
        if not app_name:
            break
            
        version = input(f"Versión para {app_name}: ").strip()
        apps.append((app_name, version))
        app_count += 1
    
    table_lines = [
        "| Aplicación  | Versión |",
        "|-------------|---------|"
    ]
    
    for app, version in apps:
        table_lines.append(f"| {app.ljust(11)} | {version.ljust(7)} |")
    
    return '\n'.join(table_lines)

def generate_pr_template(branch_name, all_files, commit_msg):
    db_files = [f for f in all_files if f.lower().endswith('.sql')]
    
    testing_notes = prompt_testing_notes()
    compatible_apps = prompt_compatible_apps()

    content = f"""## Descripción

**Rama:** `{branch_name}`  
**Commit:** `{commit_msg or 'Sin mensaje'}`

## Configuraciones
{"**Se modificaron estos archivos SQL:**\n" + "\n".join(f"- {f}" for f in db_files) if db_files else "No hay cambios en base de datos"}

## Archivos Modificados
"""
    
    file_types = {
        'SQL': [f for f in all_files if f.lower().endswith('.sql')],
        'Código': [f for f in all_files if f.lower().endswith(('.py', '.js', '.java', '.cpp', '.c', '.h', '.ts'))],
        'Documentación': [f for f in all_files if f.lower().endswith(('.md', '.txt', '.rst'))],
        'Otros': [f for f in all_files if not f.lower().endswith(('.sql', '.py', '.js', '.java', '.cpp', '.c', '.h', '.ts', '.md', '.txt', '.rst'))]
    }

    for category, files in file_types.items():
        if files:
            content += f"\n### {category}\n" + "\n".join(f"- {f}" for f in files) + "\n"

    content += f"""
## Consideraciones para Testing
{testing_notes}

## Aplicaciones Compatibles
{compatible_apps}
"""

    with open("PR_suggest.md", "w", encoding="utf-8") as f:
        f.write(content.strip())
    
    print(f"\n✅ Archivo PR_suggest.md generado con {len(all_files)} archivos listados")
    print(f"📌 Archivos SQL incluidos: {len(db_files)}")

def main():
    print_ascii_logo()
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"\n📂 Directorio de trabajo: {os.getcwd()}")
    
    branch_name = create_branch()
    
    sql_files = detect_files_by_extension('.sql')
    if sql_files:
        print("\n🔍 Archivos SQL encontrados:")
        for sql_file in sql_files:
            print(f" - {sql_file}")
        
        proceed = input("\n¿Agregar archivos SQL? (S/s): ").lower() == 's'
        if proceed:
            added = add_files(sql_files)
            print(f"✅ {added}/{len(sql_files)} archivos SQL agregados")
    
    status = git_status_info()
    print("\n📊 Estado actual del repositorio:")
    print(f"- Staged: {len(status['staged'])} archivos")
    print(f"- Unstaged: {len(status['unstaged'])} archivos")
    print(f"- Untracked: {len(status['untracked'])} archivos")
    
    if status['unstaged']:
        selected_unstaged = handle_files_selection(
            status['unstaged'], 
            "Archivos con cambios sin agregar (unstaged):"
        )
        if selected_unstaged:
            add_files(selected_unstaged)
    
    if status['untracked']:
        selected_untracked = handle_files_selection(
            status['untracked'],
            "Archivos sin seguimiento (untracked):"
        )
        if selected_untracked:
            add_files(selected_untracked)
    
    status = git_status_info()
    all_files = status["staged"]

    if all_files:
        print("\nArchivos preparados para commit:")
        for f in all_files:
            print(" +", f)
        
        model = load_or_train_model()
        changes_text, predominant_file_type = analyze_changes(all_files)
        commit_msg = generate_commit_message(branch_name, all_files, changes_text, predominant_file_type, model)
    else:
        print("\nNo hay archivos preparados para commit")
        commit_msg = None
    
    if commit_msg:
        generate_pr_template(branch_name, all_files, commit_msg)
    
    print("\n¡Proceso completado con éxito!")

if __name__ == "__main__":
    main()