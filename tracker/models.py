from django.db import models

#User model
class User_Person(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(primary_key=True, unique=True)

#Application model
class Application(models.Model):
    app_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User_Person, on_delete=models.CASCADE)
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    date_applied = models.DateField(null=True, blank=True) 
    status = models.CharField(max_length=25, choices=[
        ('Applied', 'Applied'),
        ('Interviewing', 'Interviewing'),
        ('Offer Received', 'Offer Received'),
        ('Rejected', 'Rejected'),
    ])

    #take the skills as a text input 
    skills = models.CharField(max_length=255, blank=True)
    #use the default save method to break down the skills into a set from a string 
    def save(self, *args, **kwargs):
        if self.skills:
            self.skills = ",".join([skill.strip() for skill in self.skills.split(",")]) 
        super().save(*args, **kwargs)

    #getting the skills 
    def get_skills(self):
        if not self.skills:
            return []
        return [skill.strip() for skill in self.skills.split(",")]

    

#Application Match Model 
class ApplicationMatch(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    match_percentage = models.FloatField()

    #for debugging issues : defaulted the sqlite database name to this 
    class Meta:
        db_table = 'tracker_applicationmatch' 