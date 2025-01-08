import gzip
import shutil
def unzip(path: str):
    with gzip.open(path, 'rb') as f_in:
        with open(path[0:len(path) - 3], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
