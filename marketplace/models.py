from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver



@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        if not Student.objects.filter(email=instance.email).exists():
            Student.objects.create(user=instance, email=instance.email)
        else:
            print(f"Student with email {instance.email} already exists.")
            
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 50, unique = True)
    bio = models.TextField(blank = True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')

    def __str__(self):
        return f'{self.user.username}'

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    reactions = models.ManyToManyField('Reaction', blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.timestamp}'

class Reaction(models.Model):
    emoji = models.CharField(max_length=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.emoji} by {self.user.username}'

class Review(models.Model):
    product = models.ForeignKey('products.Product', on_delete = models.CASCADE, related_name = 'reviews')
    reviewer = models.ForeignKey(User, on_delete = models.CASCADE)
    rating = models.PositiveIntegerField(validators = [MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank = True)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'Review for {self.product.title} by {self.reviewer.username}'

    class Meta:
        unique_together = (('product', 'reviewer'),)
        index_together = (('product', 'reviewer'),)
