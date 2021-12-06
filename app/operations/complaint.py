
from app.models.complaint import Complaint
class CreateComplaint:
    @classmethod
    def new(self, **data):
        new_complaint = Complaint(**data)
        return new_complaint
