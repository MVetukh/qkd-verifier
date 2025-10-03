#!/usr/bin/env python3
"""
Скрипт для вывода структуры проекта и содержимого файлов
Игнорирует системные папки (.vscode, .venv, .git и т.д.)
"""

import os
import pathlib

def should_ignore(path):
    """Проверяет, нужно ли игнорировать папку/файл"""
    ignore_list = {'.vscode', '.venv', '.git', '__pycache__', '.pytest_cache', 
                   'node_modules', 'build', 'dist', '*.egg-info', '.coverage'}
    path_str = str(path)
    return any(ignore in path_str for ignore in ignore_list) or path.name.startswith('.')

def is_target_file(file_path):
    """Проверяет, является ли файл целевым для отображения содержимого"""
    target_extensions = {'.py', '.h', '.toml', '.yaml', '.yml', '.md', '.txt'}
    return file_path.suffix in target_extensions

def print_directory_structure(start_path, prefix="", is_last=True, is_root=True):
    """Рекурсивно выводит структуру папок"""
    if should_ignore(start_path) and not is_root:
        return
    
    if is_root:
        print("📁 Структура проекта:")
        print(f"{start_path.name}/")
        prefix = "└── " if is_last else "├── "
    
    items = []
    try:
        items = sorted([item for item in start_path.iterdir() 
                       if not should_ignore(item)])
    except PermissionError:
        pass
    
    dirs = [item for item in items if item.is_dir()]
    files = [item for item in items if item.is_file() and is_target_file(item)]
    
    all_items = dirs + files
    
    for i, item in enumerate(all_items):
        is_last_item = i == len(all_items) - 1
        connector = "└── " if is_last_item else "├── "
        
        if item.is_dir():
            print(f"{prefix}{connector}{item.name}/")
            new_prefix = prefix + ("    " if is_last_item else "│   ")
            print_directory_structure(item, new_prefix, is_last_item, False)
        else:
            print(f"{prefix}{connector}{item.name}")

def print_file_contents(start_path):
    """Выводит содержимое целевых файлов"""
    print("\n\n📄 Содержимое файлов:")
    print("=" * 60)
    
    for file_path in start_path.rglob('*'):
        if file_path.is_file() and is_target_file(file_path) and not should_ignore(file_path):
            try:
                # Пропускаем бинарные файлы
                if file_path.suffix in {'.py', '.h', '.toml', '.yaml', '.yml', '.md', '.txt'}:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    print(f"\n🎯 Файл: {file_path.relative_to(start_path)}")
                    print("-" * 40)
                    print(content)
                    print("=" * 60)
            except (UnicodeDecodeError, PermissionError, Exception) as e:
                print(f"\n❌ Не удалось прочитать файл {file_path}: {e}")
                print("=" * 60)

def main():
    """Основная функция"""
    current_dir = pathlib.Path.cwd()
    
    print("🔍 Анализ структуры проекта...")
    print(f"📂 Текущая директория: {current_dir}")
    print()
    
    # Выводим структуру папок
    print_directory_structure(current_dir)
    
    # Выводим содержимое файлов
    print_file_contents(current_dir)
    
    print("\n✅ Анализ завершен!")

if __name__ == "__main__":
    main()