from PyInstaller.utils.hooks import collect_submodules, copy_metadata

# Coletar todos os submódulos do selenium
hiddenimports = collect_submodules('selenium')

# Copiar metadados do selenium
datas = copy_metadata('selenium')