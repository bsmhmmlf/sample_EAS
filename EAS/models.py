from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=32)
    grade = models.IntegerField()
    former = models.ForeignKey('self', on_delete=models.CASCADE)

class User(models.Model):
    username = models.CharField(primary_key=True, unique=True, null=False, max_length=32)
    password = models.CharField(null=False, max_length=32)
    grade = models.IntegerField()
    learned_courses = models.ManyToManyField(Course)

