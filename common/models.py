from django.db import models

# Abstract model for common fields


class CommonModel(models.Model):
    """Common Model Definition"""

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
