import os

def remove_bom_from_file(filepath):
    with open(filepath, 'rb') as f:
        raw = f.read()
    if raw.startswith(b'\xef\xbb\xbf'):
        print(f"Stripping BOM from {filepath}")
        raw = raw[3:]
        with open(filepath, 'wb') as f:
            f.write(raw)

for root, dirs, files in os.walk('.'):
    for fname in files:
        if fname.endswith('.py'):
            remove_bom_from_file(os.path.join(root, fname))

#avada kadavra