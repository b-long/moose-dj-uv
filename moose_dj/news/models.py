# Create your models here.
from django.db import models
from django.urls import reverse


class MyModelName(models.Model):
    """A typical class defining a model, derived from the Model class.

    Inspired by:
    https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models#model_definition
    """

    # Fields
    my_field_name: models.CharField = models.CharField(
        max_length=20, help_text="Enter field documentation"
    )
    # …

    # Metadata
    class Meta:
        ordering = ["-my_field_name"]

    def __str__(self) -> str:
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.my_field_name

    # Methods
    def get_absolute_url(self) -> str:
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse("model-detail-view", args=[str(self.id)])  # type: ignore [attr-defined]