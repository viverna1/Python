import zipfile

with zipfile.ZipFile("example.zip", "a") as archive:
    archive.write(".zipfile.py")
