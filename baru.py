from PIL import Image, ImageFile
import piexif
import os

# Enable loading of truncated images (untuk testing)
ImageFile.LOAD_TRUNCATED_IMAGES = True

INPUT_FOLDER = "images"
os.makedirs(INPUT_FOLDER, exist_ok=True)

# Buat file PNG sederhana
def create_png(filename):
    img = Image.new('RGB', (10, 10), color='red')
    img.save(filename)
    print(f"[+] Created {filename}")

# Tambahkan metadata EXIF
def add_metadata(filename):
    zeroth_ifd = {
        piexif.ImageIFD.Make: u"StrongBee",
        piexif.ImageIFD.Model: u"SimulatedCamera",
        piexif.ImageIFD.Software: u"Python Metadata Tester"
    }
    exif_dict = {"0th": zeroth_ifd}
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, filename)
    print(f"[+] Metadata added to {filename}")

# Modifikasi file untuk simulasi "bad input"
def corrupt_file(filename):
    with open(filename, "rb") as f:
        data = bytearray(f.read())
    # Tambahkan data acak di akhir file
    data.extend(b"\x00" * 1024)  # 1 KB "overflow"
    corrupt_name = filename.replace(".png", "_corrupt.png")
    with open(corrupt_name, "wb") as f:
        f.write(data)
    print(f"[!] Created corrupt file: {corrupt_name}")
    return corrupt_name

# Tes membuka file gambar
def test_open_image(filename):
    try:
        img = Image.open(filename)
        img.load()
        print(f"[OK] Loaded {filename} successfully")
    except Exception as e:
        print(f"[CRASH] {filename} caused error: {e}")

if __name__ == "__main__":
    # Buat dan tes file normal
    normal_file = os.path.join(INPUT_FOLDER, "test.png")
    create_png(normal_file)
    add_metadata(normal_file)
    test_open_image(normal_file)

    # Buat dan tes file "corrupt"
    corrupt_file_name = corrupt_file(normal_file)
    test_open_image(corrupt_file_name)
