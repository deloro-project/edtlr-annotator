"""Contains the models."""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import re


def extract_entry(text: str) -> str | None:
    """Extract the entry from the provided text.

    Parameters
    ----------
    text: str, required
        The text from which to extract the entry.

    Returns
    -------
    entry: str
        The extracted entry, or None.
    """
    match = re.match(r'\*\*[^*]*\*\*', text)
    if match is None:
        return text

    entry = f'{match.group(0).replace("*", "")}'
    return entry


class Volume(models.Model):
    """Represents a volume of the dictionary."""

    id = models.AutoField(verbose_name="id", primary_key=True)
    name = models.CharField(unique=True, null=False, max_length=128)

    def __str__(self):
        """Override the string representation of the model."""
        return str(self.name)


class Page(models.Model):
    """Represents a pair of (page image, OCR text)."""

    id = models.AutoField(verbose_name="id", primary_key=True)
    volume = models.ForeignKey(Volume, on_delete=models.CASCADE, default=1)
    page_no = models.PositiveIntegerField(verbose_name="page_no", null=False)
    image_path = models.CharField(unique=True, null=False, max_length=1024)

    def __str__(self):
        """Override the string representation of the model."""
        return str(self.page_no)

    class Meta:
        """Metadata of the Page model."""

        constraints = [
            models.UniqueConstraint(fields=["volume", "page_no"],
                                    name="UX_volume_id_page_no")
        ]


class Entry(models.Model):
    """Represents a dictionary entry."""

    id = models.AutoField(verbose_name="id", primary_key=True)
    text = models.TextField(max_length=250_000, null=False)

    class Meta:
        """Defines metadata of the Entry model."""

        verbose_name_plural = "Entries"

    def __str__(self):
        """Override the string representation of the model."""
        return extract_entry(self.text)


class EntryPage(models.Model):
    """Represents an association between a page and a dictionary entry."""

    id = models.AutoField(verbose_name="id", primary_key=True)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    class Meta:
        """Defines the metadata of the PageEntry model."""

        constraints = [
            models.UniqueConstraint(fields=["entry", "page"],
                                    name="UX_entry_id_page_id")
        ]


class Annotation(models.Model):
    """Represents an annotation."""

    class AnnotationStatus(models.TextChoices):
        """Defines the possible values of an annotation status."""

        IN_PROGRESS = 'InProgress', _('In progress')
        COMPLETE = 'Complete', _('Complete')
        CONFLICT = 'Conflict', _('Conflict')

    id = models.AutoField(verbose_name="id", primary_key=True)
    entry = models.ForeignKey(Entry,
                              on_delete=models.CASCADE,
                              null=False,
                              default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    text = models.TextField(verbose_name="text", null=True, max_length=250_000)
    status = models.CharField(max_length=32,
                              choices=AnnotationStatus,
                              null=False,
                              default=AnnotationStatus.IN_PROGRESS)
    version = models.PositiveSmallIntegerField()
    row_creation_timestamp = models.DateTimeField(blank=False,
                                                  null=False,
                                                  default=timezone.now)
    row_update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Override the string representation of the model."""
        return extract_entry(self.text)
