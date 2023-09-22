from django.db import models

# Create your models here.
class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)

  def __str__(self):
    return self.firstname
    
#   adm = models.CharField(max_length=255)
# class NAME(models.Model):

#     title = models.CharField(max_length=255)
#     body = models.TextField()
#     date_created = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#     is_draft = models.BooleanField(default=True)
