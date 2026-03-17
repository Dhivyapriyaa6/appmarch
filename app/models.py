from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities', null=True, blank=True)
    team_name = models.CharField(max_length=100)
    members = models.TextField(help_text="Comma-separated member names")
    description = models.TextField()
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name_plural = "Activities"

    def __str__(self):
        return f"{self.team_name} - {self.date}"

    def get_members_list(self):
        return [m.strip() for m in self.members.split(',') if m.strip()]

    def member_count(self):
        return len(self.get_members_list())

    def primary_photo(self):
        return self.photos.first()


class ActivityPhoto(models.Model):
    activity = models.ForeignKey(Activity, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='activities/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return f"Photo for {self.activity}"
class ActivityDocument(models.Model):
    activity = models.ForeignKey(Activity, related_name='documents', on_delete=models.CASCADE)
    file = models.FileField(upload_to='activity_docs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return f"Document for {self.activity}"

    def filename(self):
        import os
        return os.path.basename(self.file.name)
