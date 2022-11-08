from django.db import models

# Create your models here.


class Subscribe(models.Model):

    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    stopped =  models.DateField(null=True)
    class Meta: 
        verbose_name = "Inscrito da Newsletter"
        verbose_name_plural = "Inscritos da Newsletter"
        ordering = ['-created',]

    def __str__(self):
        return self.email  


class Contact(models.Model):

    email = models.EmailField()
    nome = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    created =  models.DateTimeField(auto_now_add=True)
    whatapp_enable = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"
        ordering = ['-created']

    def __str__(self):
        return self.nome
