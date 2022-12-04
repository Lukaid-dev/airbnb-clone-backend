from django.db import models

class House(models.Model):

    '''
    * Model definition for Houses
    '''

    def __str__(self):
        return self.name

    name = models.CharField(max_length=140)
    price_per_night = models.IntegerField()
    description = models.TextField()
    address = models.CharField(max_length=140)
    pets_allowed = models.BooleanField(
        default=True, 
        help_text='Does this house allow pets?', 
        verbose_name='Pets allowed?',
    )