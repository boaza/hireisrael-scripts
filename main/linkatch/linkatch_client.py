import base64
import logging

import requests

from main.core.enums import JobType
from main.linkatch.core import LinkatchJobModel
from main.linkatch.linkatch_settings import LinkatchSettings

logger = logging.getLogger(__name__)


class LinkatchClient:
    settings = LinkatchSettings()
    urls = {
        'login': settings.url + '/app/login',
        'new_job': settings.url + '/app/jobs',
        'query_jobs': settings.url + '/app/jobs/query'
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

    def login(self, token: str = None):
        logger.info(f'Attempting login with username: {self.settings.username}')
        try:
            if token is None:
                response = requests.post(self.urls['login'], json={'username': self.settings.username, 'password': self.settings.password.get_secret_value()})
                response.raise_for_status()
                token = response.json()["access_token"]
            self._headers['authorization'] = f'Bearer {token}'
            logger.info('Login successful')
        except:
            logger.exception(f'Operation failed')

    def post_job(self, job: LinkatchJobModel):
        logger.info(f'Posting new job: {job.title}')
        job_exists = self.query_jobs(job)
        if not job_exists:
            data = self._prepare_job_dict(job)
            response = requests.post(self.urls['new_job'], json=data, headers=self._headers)
            response.raise_for_status()
            logger.info('Operation successful')
        else:
            logger.warning(f'Job with Internal ID {job.internalId} already exists - skipping')

    def query_jobs(self, job: LinkatchJobModel) -> list[dict]:
        try:
            logger.debug(f'Searching for job with ID: {id}')
            data = {
                'query': {
                    'companyId': job.companyId,
                    'internalId': {'op': 'ilike', 'value': f'%{job.internalId.strip()}%'}
                }
            }
            response = requests.post(self.urls['query_jobs'], json=data, headers=self._headers)
            response.raise_for_status()
            return response.json()['items']
        except:
            logger.exception(f'Operation failed')

    @staticmethod
    def _prepare_job_dict(job: LinkatchJobModel) -> dict:
        overrides = {
            'title': job.title.strip(),
            'schedule': LinkatchClient.job_type_map.get(job.schedule),
            'description': base64.b64encode(job.description.encode('utf8')).decode('utf8'),
            'location': {'title': job.location}
        }
        result = job.model_dump() | overrides
        return result


if __name__ == '__main__':
    client = LinkatchClient()
    client.login()
    print('done')
