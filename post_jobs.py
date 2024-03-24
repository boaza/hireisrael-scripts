import glob
import json
import logging
import os
from argparse import ArgumentParser
from pathlib import Path

from main.linkatch import LinkatchClient
from main.linkatch.core import LinkatchJobModel
from main.linkatch.utilities import nbn_description_to_linkatch

logging.basicConfig(format="[%(levelname)s] %(asctime)s %(message)s", level=logging.INFO)

linkatch = LinkatchClient()
token = None


def post_jobs(jobs_folder: str | Path):
    linkatch.login(token=token)
    jobs_folder = Path(jobs_folder)
    jobs_files = glob.glob(str(jobs_folder / '*.json'))
    for jobs_file in jobs_files:
        with open(jobs_file) as f:
            raw = json.load(f)
            raw['description'] = nbn_description_to_linkatch(raw)
            model = LinkatchJobModel(**raw, internalId=raw['id'], schedule=raw['type'])
            linkatch.post_job(model)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("jobs_folder", help="Path to NBN jobs folder.")
    args = parser.parse_args()

    post_jobs(args.jobs_folder)
