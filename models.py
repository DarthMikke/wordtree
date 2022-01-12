from django.db import models

# Create your models here.
class Language(models.Model):
	name = models.CharField(max_length=200, blank=True, default="")
	short_name = models.CharField(max_length=10)

	def __str__(self):
		return self.name


class Word(models.Model):
	text = models.CharField(max_length=200)
	reconstructed = models.BooleanField(default=False)
	language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL)
	parent = models.ForeignKey('self', on_delete=models.CASCADE)
	approved = models.BooleanField(default=False)
	romanized = models.CharField(max_length=200, blank=True, default="")
	source = models.CharField(max_length=200, blank=True, default="")

	def romanize(self):
		if self.romanized != "":
			return f"{self.romanized} ({self.text})"
		else:
			return self.text

	def __str__(self):
		return f"{self.text} ({self.language.short_name})"
