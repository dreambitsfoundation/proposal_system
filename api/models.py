from django.db import models
from django.utils import timezone

class ModelTemplate(models.Model):
    created_by = models.CharField(max_length=30, default='')
    created_date = models.DateTimeField(editable=False)
    modified_by = models.CharField(max_length=30, default='')
    modified_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        return super(ModelTemplate, self).save(*args, **kwargs)


class Proposal(ModelTemplate):
    """
    This model is used to store the proposals
    """
    proposal_name = models.CharField(max_length=100, null=False, unique=True)
    description = models.TextField(default='')
    proposal_date = models.DateField(null=False)

