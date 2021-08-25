import os
import urllib.request
import zipfile
from typing import Any

from tqdm import tqdm


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def save_file(url: str, file_path: Any):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc='Downloading') as t:
        urllib.request.urlretrieve(url, filename=file_path, reporthook=t.update_to)

    return file_path


def unzip_dl(name: str, zip_path: Any) -> None:
    """Ask the user whether they'd like to unzip the download or not."""
    # Remove special characters from folder name
    name = f"{name.replace(':', '-').replace('?', '-')}"
    folder_path = os.path.join("./Games", name)

    # Unzip the contents
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in tqdm(zip_ref.infolist(), desc='Extracting'):
            try:
                zip_ref.extract(member, folder_path)
            except zipfile.error:
                pass

    os.remove(zip_path)
