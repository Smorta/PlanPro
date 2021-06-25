from django.db import models


class Responsable(models.Model):
    FirstName = models.CharField(max_length=100)
    Name = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.FirstName


class User(models.Model):
    Pseudo = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)

    def __str__(self):
        return self.Pseudo


class Chantier(models.Model):
    Name = models.CharField(max_length=100)
    Date_debut = models.DateField()
    Date_fin = models.DateField()
    Entite = models.CharField(max_length=100)

    def __str__(self):
        return self.Name


class Modification(models.Model):
    Name = models.CharField(max_length=100)
    id_chantier = models.ForeignKey(Chantier, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name


class Phase(models.Model):
    Name = models.CharField(max_length=100)
    Type = models.CharField(max_length=100, null=True)
    State = models.CharField(max_length=1, null=True)
    num = models.CharField(max_length=2)
    Date_debut = models.DateField(null=True, blank=True)
    Date_fin = models.DateField(null=True, blank=True)
    Deadline = models.DateField(null=True, blank=True)
    id_chantier = models.ForeignKey(Chantier, on_delete=models.CASCADE)
    id_Responsable = models.ManyToManyField(Responsable)

    def __str__(self):
        return self.Name
# Create your models here.
