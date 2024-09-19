from django.db import models

# Create your models here.
class Events(models.class (models.Model):
    name = models.CharField(max_length=100, ${blank=True, null=True}),
    desctiption=models.TextField(blank=True, null=True)
    date=models.DateField()
    location=models.models.CharField(max_length=100)
       

    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("s")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
)