from django.db import models
from django.utils import timezone 


class UserDetail(models.Model):
    userID = models.BigIntegerField(primary_key=True)
    rank = models.PositiveIntegerField(default=0)
    xp = models.BigIntegerField(default=0)
    promoted_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.userID} |||||| {self.rank} with {self.xp}'

    class Meta:
        ordering = ('rank','-promoted_date')

