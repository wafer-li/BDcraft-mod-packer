import os
import shutil
import zipfile

meta_filename = 'pack.mcmeta'
meta_content = '''
{
    "pack": {
        "pack_format": 3,
        "description": "BDcraft-Modded 1.12.2 Textture Pack"
    }
}
'''


def pack(root_dir):
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)
    os.chdir(root_dir)
    root_dir = os.getcwd()
    for zip_file_name in [it for it in os.listdir(root_dir) if zipfile.is_zipfile(it)]:
        zip_file = zipfile.ZipFile(zip_file_name)
        for asset in [it for it in zip_file.infolist()
                      if os.path.normpath(it.filename).count(os.sep) > 1 and not it.is_dir()]:
            zip_file.extract(asset)
        zip_file.close()
        os.remove(zip_file_name)

    output = zipfile.ZipFile('BDcraft-moded-1-12-2.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(root_dir):
        relative_path = root[len(root_dir) + 1:]
        if relative_path.count(os.sep) > 0:  # root ==  asserts/lowcase
            for f in files:
                print('Packing file {}'.format(f))
                output.write(os.path.join(root, f), os.path.join(relative_path, f))
                os.remove(os.path.join(root, f))
    for dir_ in [it for it in os.listdir(root_dir) if os.path.isdir(it)]:
        shutil.rmtree(dir_, ignore_errors=True)
    output.writestr(meta_filename, meta_content)
    output.close()
