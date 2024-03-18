import requests
from lxml import html, etree

from main.linkatch.linkatch_settings import LinkatchSettings
import base64

import logging

from main.linkatch.core import LinkatchJobModel
from main.core.enums import JobType

logger = logging.getLogger(__name__)


class LinkatchClient:
    settings = LinkatchSettings()
    urls = {
        'login': settings.url + '/app/login',
        'new_job': settings.url + '/app/jobs'
    }
    job_type_map = {
        JobType.FullTime: 'full',
        JobType.PartTime: 'part',
        JobType.Freelance: 'freelance',
        JobType.Shifts: 'shifts'
    }

    def __init__(self):
        self._headers = {
            # requests without User-Agent are rejected with 403
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
        }

    def login(self):
        logger.info(f'Attempting login with username: {self.settings.username}')
        try:
            response = requests.post(self.urls['login'], json={'username': self.settings.username, 'password': self.settings.password.get_secret_value()})
            response.raise_for_status()
            self._headers['authorization'] = f'Bearer {response.json()["access_token"]}'
            logger.info('Login successful')
        except:
            logger.exception(f'Operation failed')

    def post_job(self, job: LinkatchJobModel):
        try:
            logger.info(f'Posting new job: {job.title}')
            data = self._prepare_job_dict(job)
            response = requests.post(self.urls['new_job'], json=data, headers=self._headers)
            response.raise_for_status()
            logger.info('Operation successful')
        except:
            logger.exception(f'Operation failed')

    @staticmethod
    def _prepare_job_dict(job: LinkatchJobModel) -> dict:
        overrides = {
            'title': job.title.strip(),
            'schedule': LinkatchClient.job_type_map.get(job.schedule),
            'description': base64.b64encode(job.description.encode('utf8')).decode('utf8')
        }
        result = job.model_dump() | overrides
        return result


if __name__ == '__main__':
    client = LinkatchClient()
    client.login()
    print('done')
