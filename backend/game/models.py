from django.db import models

class Round(models.Model):
    id_round = models.IntegerField()
    subject_id = models.CharField(max_length=255)
    player = models.CharField(max_length=255)
    value = models.IntegerField(default=0)
    role = models.CharField(max_length=255)
    new_role = models.CharField(max_length=255)
    choice = models.BooleanField(default=False)
    reward = models.IntegerField(default=0)
    tracking = models.JSONField()
    time = models.FloatField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Round {self.id_round} - {self.subject_id} : {self.role} to {self.new_role}"

class Trial(models.Model):
    id_trial = models.IntegerField(default=0)
    round = models.IntegerField(default=0)
    proposition = models.IntegerField(default=0)
    commander_choice = models.BooleanField(default=False)
    tracking = models.JSONField()
    time = models.FloatField(default = 0)
    role = models.CharField(max_length=255)
    subject_id = models.CharField(max_length=255)
    reward = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} ({self.subject_id}) - {self.id_trial}/{self.round}"

class Calibration(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    trajectories = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id


class Form(models.Model):
    subject_id = models.CharField(max_length=255, primary_key=True)
    age = models.IntegerField(default = 0)
    genre = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    main = models.CharField(max_length=100)
    souris = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject_id