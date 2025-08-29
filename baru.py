from PIL import Image, PngImagePlugin
import os

INPUT_FOLDER = "images"
os.makedirs(INPUT_FOLDER, exist_ok=True)

# Buat file PNG sederhana
def create_png(filename):
    img = Image.new('RGB', (10, 10), color='red')

    # Tambahkan metadata
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Author", "StrongBee")
    meta.add_text("Software", "Python Metadata Tester")
    meta.add_text("Description", "Simulated test image with metadata")
    
    img.save(filename, pnginfo=meta)
    print(f"[+] Created {filename} with metadata")

# Modifikasi file untuk simulasi "bad input"
def corrupt_file(filename):
    with open(filename, "rb") as f:
        data = bytearray(f.read())
    data.extend(b"\x00" * 1024)  # Tambah data acak
    corrupt_name = filename.replace(".png", "_corrupt.png")
    with open(corrupt_name, "wb") as f:
        f.write(data)
    print(f"[!] Created corrupt file: {corrupt_name}")
    return corrupt_name

# Tes membuka file gambar
def test_open_image(filename):
    from PIL import Image, ImageFile
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    try:
        img = Image.open(filename)
        img.load()
        print(f"[OK] Loaded {filename} successfully")
    except Exception as e:
        print(f"[CRASH] {filename} caused error: {e}")

if __name__ == "__main__":
    normal_file = os.path.join(INPUT_FOLDER, "test.png")
    create_png(normal_file)
    test_open_image(normal_file)

    corrupt_file_name = corrupt_file(normal_file)
    test_open_image(corrupt_file_name)
