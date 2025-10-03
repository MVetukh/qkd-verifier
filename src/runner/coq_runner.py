# src/runner/coq_runner.py - минимальный запускатель
import subprocess
import os
from pathlib import Path

def run_coq_verification(coq_file: str) -> bool:
    """Запускает Coq верификацию"""
    try:
        # Проверяем существование файла
        coq_path = Path("coq") / coq_file
        if not coq_path.exists():
            print(f"Файл {coq_path} не найден!")
            return False
            
        # Запускаем coqc
        result = subprocess.run(
            ["coqc", coq_file], 
            cwd="coq",
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Coq ошибка: {result.stderr}")
            return False
            
        print("Coq верификация успешна!")
        return True
        
    except FileNotFoundError:
        print("Coq не установлен или не найден в PATH!")
        return False
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return False
    
# src/runner/coq_runner.py (в конец файла)
def main():
    """
    CLI: qkd-coqc [relative/path/to/.v]
    По умолчанию компилирует coq/Generated/b92_inst.v
    """
    import sys
    target = "Generated/b92_inst.v"
    if len(sys.argv) > 1:
        target = sys.argv[1]
    ok = run_coq_verification(target)
    if not ok:
        raise SystemExit(1)
