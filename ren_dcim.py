import glob
import os
import os.path
import sys

from PIL import ExifTags, Image


def main(dir):
    files = glob.glob(os.path.join(dir, "*.jpg"))
    print(len(files))
    for file in files:
        hash = get_exifdate(file)
        if not hash:
            print(file, "** NO DATE **")
            continue
        date = hash["DateTime"].replace(":", "").replace(" ", "_")
        rename_file(file, date)


def get_exifdate(file):
    img = Image.open(file)
    hash = {}
    for k, v in img._exif.items():
        if k in ExifTags.TAGS:
            name = ExifTags.TAGS[k]
            if "date" in name.lower():
                hash[name] = v
    img.close()
    return hash


def rename_file(file, date):
    dir = os.path.dirname(file)
    new_name = os.path.join(dir, f"{date}.JPG")
    print(f"reanem {file} to { new_name}")
    os.rename(file, new_name)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("python -m ren_dcim <dir> [dir...]")
        exit()
    for dir in sys.argv[1:]:
        main(dir)
