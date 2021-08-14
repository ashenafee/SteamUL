import os
from typing import Any
from progress.spinner import Spinner

import requests


def save_file(element: str, file_path: Any) -> None:
    r = requests.get(element, stream=True)
    flag = True
    if r.ok:
        spinner = Spinner('Downloading ', check_tty=False, hide_cursor=False)
        while flag:
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 8):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        os.fsync(f.fileno())
                    spinner.next()
                spinner.finish()
            flag = False
        print('Download complete')
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))
