from pydantic import BaseModel
from typing import Literal

from main.core.enums import JobType


class LinkatchJobModel(BaseModel):
    title: str = None
    schedule: JobType = None
    description: str = None
    internalId: str = None
    innerRecruiter: str = 'NBN'                                 # Nefesh be Nefesh
    companyId: str = '659351b5-bb3d-4d96-a382-1f6dfb50afe1'     # HireIsrael
    leadEmails: list[str] = [r'resumes@nbn.org.il']             # Nefesh be Nefesh
