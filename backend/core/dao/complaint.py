from .base import BaseDAO
from core.models import Complaint


class ComplaintDao(BaseDAO[Complaint]):
    model = Complaint
