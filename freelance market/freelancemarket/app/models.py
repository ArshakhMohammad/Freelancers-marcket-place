from django.db import models


class Freelancer(models.Model):

    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    skills = models.CharField(max_length=300)
    location = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    bio = models.TextField(blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    is_blocked = models.BooleanField(default=False)
    warning_message = models.TextField(blank=True, null=True)

    profile_image = models.ImageField(
        upload_to='freelancer_profiles/',
        blank=True,
        null=True
    )

    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class Client(models.Model):
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    password = models.CharField(max_length=255)

    location = models.CharField(max_length=200)
    client_type = models.CharField(max_length=100)
    services = models.TextField()
    contact_method = models.CharField(max_length=50)
    is_blocked = models.BooleanField(default=False)
    warning_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name


class Job(models.Model):

    client = models.ForeignKey(Client,on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.IntegerField()
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    completion_requested = models.BooleanField(default=False)

    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "freelancer")

class Meta:
    unique_together = (
        "job",
        "freelancer"
    )

class Review(models.Model):

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE
    )

    freelancer = models.ForeignKey(
        Freelancer,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField()

    comment = models.TextField()