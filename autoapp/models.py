from django.db import models

class Credential(models.Model):
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email

class GroupLink(models.Model):
    group_name = models.CharField(max_length=255)
    group_url = models.URLField()

    def __str__(self):
        return self.group_name

class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    hashtags = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        return self.title

class PostSelection(models.Model):
    credential = models.ForeignKey(Credential, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupLink, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    selected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.credential.email} - {self.group.group_name} - {self.post.title}"