from django.db import models
import string

# Create your models here.

divisions = list(string.ascii_uppercase)



class branch_choices(models.TextChoices):
    AI = 'AI & DS'
    MECH = 'Mechanical'
    CIVIL = 'Civil'
    IT = 'IT'
    CS = 'CS'
    ENTC = 'ENTC'

class division_choices(models.TextChoices):
    A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z = list(string.ascii_uppercase)


class Student(models.Model):
    PRN = models.IntegerField(primary_key=True)
    Roll = models.IntegerField()
    Name = models.CharField(max_length=100)
    Year = models.CharField(max_length=20)
    Division = models.CharField(max_length=1, choices=division_choices.choices)
    Batch = models.CharField(max_length=2)
    Branch = models.CharField(max_length=50, choices=branch_choices.choices)

    def __str__(self) -> str:
        return "%s" % (self.Roll)

class Course(models.Model):
    Code = models.CharField(max_length=10, primary_key=True)
    Name = models.CharField(max_length=100)
    Credit = models.IntegerField()
    Description = models.TextField()

    def __str__(self) -> str:
        return "%s" % (self.Name)

class Attandance(models.Model):
    sr_no = models.AutoField(primary_key=True)
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Day = models.DateField()
    TimeSlot = models.TimeField()
    present = models.BooleanField()

    def __str__(self) -> str:
        return "%s" % (self.Student)
    