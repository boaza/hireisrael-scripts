import json
import logging
from argparse import ArgumentParser
from pathlib import Path

from main.nbn import NbnScraper

logging.basicConfig(format="[%(levelname)s] %(asctime)s %(message)s", level=logging.INFO)

scraper = NbnScraper()


def scrape_jobs(urls_file: str | Path, output_dir: str | Path):
    with open(urls_file) as f:
        urls = f.readlines()
    output_dir = Path(output_dir)
    for url in urls:
        try:
            job = scraper.scrape_job(url)
            with open(output_dir / f'{job["id"]}.json', 'wt') as f:
                json.dump(job, f, indent=2)
        except Exception as e:
            print('Failed scraping job - skipping')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("urls_file", help="Path to the jobs URLs list file.")
    parser.add_argument("--output-folder", help="Path to the output folder where results will be stored.", default='nbn_jobs')
    args = parser.parse_args()

    scrape_jobs(args.urls_file, args.output_folder)
