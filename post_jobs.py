import glob
import json
import logging
from argparse import ArgumentParser
from pathlib import Path

from main.linkatch import LinkatchClient
from main.linkatch.types import LinkatchJobModel

logging.basicConfig(format="[%(levelname)s] %(asctime)s %(message)s", level=logging.INFO)

linkatch = LinkatchClient()


def post_jobs(jobs_folder: str | Path):
    linkatch.login()
    jobs_folder = Path(jobs_folder)
    jobs_files = glob.glob(str(jobs_folder / '*.json'))
    for jobs_file in jobs_files:
        with open(jobs_file) as f:
            raw = json.load(f)
            raw['internalId'] = raw['id']
            model = LinkatchJobModel(**raw)
            linkatch.post_job(model)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("jobs_folder", help="Path to NBN jobs folder.")
    args = parser.parse_args()

    post_jobs(args.jobs_folder)
