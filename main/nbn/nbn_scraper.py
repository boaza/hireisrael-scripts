import requests
from lxml import html, etree
from urllib.parse import urlparse, parse_qs
from main.core.enums import JobType

import logging
logger = logging.getLogger(__name__)


class NbnScraper:
    _headers = {
        # requests without User-Agent are rejected with 403
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    }
    _job_type_map = {
        'full time': JobType.FullTime,
        'part time': JobType.PartTime,
        'freelance': JobType.Freelance,
        'shifts': JobType.Shifts
    }

    def scrape_job(self, url):
        try:
            logger.info(f"Scraping {url}")
            response = requests.get(url, headers=NbnScraper._headers)
            response.raise_for_status()
            tree = html.fromstring(response.content)
            return {
                'id': self._extract_job_id(tree),
                'url': self._extract_job_url(tree),
                'type': self._extract_job_type(tree),
                'title':  self._extract_job_title(tree),
                'description':  self._extract_job_description(tree)
            }
        except:
            logger.exception('Operation failed')

    @staticmethod
    def _get_elements(document: str | etree.ElementBase, xpath: str, limit: int = 1) -> etree.ElementBase:
        tree = html.fromstring(document) if isinstance(document, str) else document
        elements = tree.xpath(xpath)
        return elements[:limit]

    @staticmethod
    def _extract_job_id(document: str | etree.ElementBase) -> str:
        xpath = ('//head/link[@rel="shortlink"]')
        element = NbnScraper._get_elements(document, xpath)[0]
        url = element.get('href')
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        return query_params['p'][0]

    @staticmethod
    def _extract_job_url(document: str | etree.ElementBase) -> str:
        xpath = ('//head/meta[@property="og:url"]')
        element = NbnScraper._get_elements(document, xpath)[0]
        return element.attrib['content']

    @staticmethod
    def _extract_job_title(document: str | etree.ElementBase) -> str:
        # Job title is under:
        # <div id="page">
        #   <div id="main">
        #       ...
        #       <h1 class="page-title">
        #           <!-- Title -->
        #           Job Title
        #       </h1>
        #       ...
        #   </div>
        # </div>
        xpath = (
            '//div[@id="page"]'
            '//div[@id="main"]'
            '//*[@class[contains(., "page-title")]]'
        )
        element = NbnScraper._get_elements(document, xpath)[0]
        return element.text_content().strip()

    @staticmethod
    def _extract_job_description(document: str | etree.ElementBase) -> str:
        # Job description is under:
        # <div id="page">
        #   <div id="main">
        #       <div id="content" class="container content-area" role="main">
        #           <div class="job-overview-content row">
        #               <div class="job_listing-description job-overview col-md-9 col-sm-12">
        #                   <!-- Content -->
        #                   <h2 class="widget-title widget-title--job_listing-top job-overview-title">Overview</h2>
        #                   ...
        #               </div>
        #           </div>
        #       </div>
        #   </div>
        # </div>
        xpath = (
            '//div[@id="page"]'
            '//div[@id="main"]'
            '//div[@id="content"]'
            '/div[@class[contains(., "job-overview-content")]]'
            '/div[@class[contains(., "job_listing-description")]]'
        )
        element = NbnScraper._get_elements(document, xpath)[0]
        return ''.join(etree.tostring(child, encoding='unicode', method='html') for child in element)

    @staticmethod
    def _extract_job_type(document: str | etree.ElementBase) -> str:
        xpath = (
            '//div[@id="page"]'
            '//div[@id="main"]'
            '//ul[@class[contains(., "job-listing-meta")]]'
            '/li[@class[contains(., "job-type")]]'
        )
        items = NbnScraper._get_elements(document, xpath)
        job_types = [NbnScraper._job_type_map[job_type_str] for item in items
                     if (job_type_str := item.text_content().strip().lower()) in NbnScraper._job_type_map]
        return job_types[0] if job_types else None


if __name__ == '__main__':
    from pathlib import Path
    path = Path(__file__).parents[2] / r'tests\data\nbn-job.html'
    tree = html.parse(path)
    title = NbnScraper._extract_job_title(tree)
    description = NbnScraper._extract_job_description(tree)
    id = NbnScraper._extract_job_id(tree)
    url = NbnScraper._extract_job_url(tree)
    job_type = NbnScraper._extract_job_type(tree)

    print(f'{title}\n\n{description}\n\n{id}\n\n{job_type}\n\n{url}')
