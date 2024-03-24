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
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImU3OTRlZGFmLTVmNjEtNDRhOC04NjJiLTdmZGRhMWM1NTUyZSIsImRpc3BsYXlOYW1lIjoi15HXldei15YiLCJ0ZW4iOiIxODM5ZWExNi0zZGY0LTQ4YWItODkzNy03MjIxMDEyOGZmZDAiLCJjb21wYW55SWQiOiI2NTkzNTFiNS1iYjNkLTRkOTYtYTM4Mi0xZjZkZmI1MGFmZTEiLCJyb2xlIjoiY21wQWRtaW4iLCJ1c2VybmFtZSI6ImJvYXpAdGVuc29yLXRlY2guY28uaWwiLCJpYXQiOjE3MTEyNjc4NDgsImV4cCI6MTcxMTI4OTQ0OCwiYXVkIjoiaHR0cHM6Ly9saW5rYXRjaC5jb20vYXBwIiwiaXNzIjoiTGlua2F0Y2giLCJzdWIiOiJlNzk0ZWRhZi01ZjYxLTQ0YTgtODYyYi03ZmRkYTFjNTU1MmUifQ.FFqQC3GrjHmw_aEDC3wWYDyUoNXl-uhiYcgk5slqiGI'


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
