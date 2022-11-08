from django.db import models


class QuestionCategory(models.Model):
    name = models.CharField("Categoria", max_length=200)

    class Meta:
        verbose_name = "Categoria da duvida"
        verbose_name_plural = "Categorias das duvidas"

    def __str__(self):
        return self.name


class Question(models.Model):
    question = models.CharField("Duvida", max_length=200)
    answer = models.TextField("Resposta")
    active = models.BooleanField(default=True)
    category = models.ForeignKey("core.QuestionCategory", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Duvidas Frequente"
        verbose_name_plural = "Duvidas Frequentes"

    def __str__(self):
        return self.question


class Address(models.Model):
    state = models.CharField("UF", max_length=30,blank=True)
    street = models.CharField("Rua", max_length=30,blank=True)
    city = models.CharField("Cidade", max_length=30,blank=True)
    zipcode = models.CharField("CEP", max_length=30,blank=True)
    country = models.CharField("Pais", max_length=30,blank=True)
    neighborhood = models.CharField("Bairro", max_length=30,blank=True)
    street_number = models.CharField("Numero", max_length=30,blank=True)
    complement = models.CharField(
        "Complemento", max_length=30, null=True, blank=True, default=""
    )

    class Meta:
        verbose_name = "Endereço da Loja"
        verbose_name_plural = "Endereços da Loja"

    def __str__(self):
        return f"{self.street}, {self.street_number} , {self.zipcode}"

    def get_short_address(self):
        return f"{self.street}, {self.street_number} ,{self.complement} ,{self.zipcode}"

    def get_full_address(self):
        return f"{self.street}, {self.street_number} ,{self.complement} ,{self.zipcode} {self.city}, {self.state} {self.contry}"
