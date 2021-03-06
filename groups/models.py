from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
import misaka
from django.contrib.auth import get_user_model

User = get_user_model()
from django import template
register = template.Library()

class Group(model.models):
	name = models.CharField(max_length=256,unique=True)
	slug = models.SlugField(allow_unicode=True,unique=True)
	description = models.TextField(blank=True,default='')
	description_html = models.TextField(blank=True, editable=False,default=True)
	members = models.ManyToManyField(User,through='GroupMember')
	
	def __str__(self):
		return self.name
	
	def save(self,*args,**kwargs):
		self.slug = slugify(slef.name)
		self.description_html = misaka.html(self.description)
		super().save(*args,**kwargs)
	
	def get_absolute_url(self):
		return reverse('groups:single',kwargs={'slug':self.slug})
		
	class Meta:
		ordering = ['name']

class GroupMember(model.models):
	group = models.ForeignKey(Group, related_name='membership')
	user = models.ForeignKey(Group, related_name='user_groups')
	
	def __str__(self):
		return self.user.username
		
	class Meta:
		unique_together = ('group','user')
