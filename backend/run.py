import sys
import os

# # If the user runs `python run.py` with a system Python, prefer re-execing
# # into the project's virtualenv Python so installed packages (Flask-SQLAlchemy)
# # are available. This makes `python run.py` work without manual venv activation.
# venv_dir = os.path.join(os.path.dirname(__file__), 'env')
# venv_python = os.path.join(venv_dir, 'Scripts', 'python.exe')

# if os.path.exists(venv_python):
#     try:
#         # Normalize paths for comparison on Windows
#         current_python = os.path.normcase(os.path.abspath(sys.executable))
#         target_python = os.path.normcase(os.path.abspath(venv_python))
#         if current_python != target_python:
#             print(f"Switching to project's venv python: {venv_python}")
#             # Replace current process with the venv python running the same script
#             os.execv(venv_python, [venv_python] + sys.argv)
#     except Exception:
#         # If execv fails for some reason, fall through and attempt to run anyway
#         pass
# else:
#     print("Warning: project virtualenv not found at:", venv_python)

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)