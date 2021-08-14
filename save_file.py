import urllib.request
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
