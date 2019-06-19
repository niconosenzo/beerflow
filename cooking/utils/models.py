from django.db import models


class CreationModificationDateMixin(models.Model):
    """
    Abstract base class with a creation
    and modification date and time
    """
    class Meta:
        abstract = True

    fecha_creacion = models.DateTimeField(("creation date and time"),
                                          auto_now_add=True)
    fecha_modificacion = models.DateTimeField(("modification date and time"),
                                              auto_now=True)
