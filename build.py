import shutil
import PyInstaller.__main__

try:
    shutil.rmtree("dist")
except FileNotFoundError:
    pass

PyInstaller.__main__.run([
    "--onefile",
    "--hidden-import", "tbot.tbot_client",
    "TBoT-Twitch/main.py"
])

PyInstaller.__main__.run([
    "--onefile",
    "configure-secrets.py"
])

for folder in (
    "Configuration",
    "Data",
    "Language",
    "Sounds",
    "Sqlite",
    "TBoT_Overlay"
):
    shutil.copytree(folder, f"dist/{folder}")
