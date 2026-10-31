from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    manager = models.ForeignKey("employees.Employee", null=True, blank=True, on_delete=models.SET_NULL, related_name="managed_departments")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
