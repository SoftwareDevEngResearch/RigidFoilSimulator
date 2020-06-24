import numpy as np
import os
from . import processWallshear as pW


def refile(files, geo, dyn, status = 'processed'):
    file_names = [f for f in os.listdir(files.data_path) if os.path.isfile(os.path.join(files.data_path, f))]
    file_names = list(filter(lambda x:(x.find("les") >= 0 or x.find("wallshear") >0), file_names))
    if not status == 'processed':
        pW.wallshearData(files, dyn, geo, 1)

    