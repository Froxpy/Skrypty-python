import shutil
from pathlib import Path

# 📌 Folder, w którym znajduje się ten skrypt
current_folder = Path(__file__).parent.resolve()

# 📦 Folder docelowy
dst_folder = current_folder / "nowy_folder"

# 🧪 Utwórz folder docelowy, jeśli nie istnieje
dst_folder.mkdir(parents=True, exist_ok=True)

# 🔁 Przenieś wszystkie pliki z folderu skryptu (z wyjątkiem samego skryptu)
for file in current_folder.iterdir():
    if file.is_file() and file.name != Path(__file__).name and file.parent != dst_folder:
        shutil.move(str(file), dst_folder / file.name)
        print(f"📁 Przeniesiono: {file.name}")
