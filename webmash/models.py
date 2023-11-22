from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image,ExifTags
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import os

class Writer(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	ProfilePic=models.ImageField(upload_to='UserAvatar')
	name=models.CharField(max_length=100)
	bio=models.CharField(max_length=200)

	def save(self,*args,**kwargs):
		if self.ProfilePic:
			ima = Image.open(self.ProfilePic)
			if ima.mode!='RGB':
				imr=ima.convert('RGB')
				ima=imr
			w,h=ima.size
			if(w>=h):
				marker=h
			else:
				marker=w
			output = BytesIO()
			imager=ima.crop((0,0,marker,marker))
			#Resize/modify the image
			im = imager.resize((600,600),Image.ANTIALIAS)
			print(im)
			#after modifications, save it to the output
			im.save(output, format='JPEG', quality=95)
			output.seek(0)#change the imagefield value to be the newley modifed image value
			self.ProfilePic = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.ProfilePic.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

		super(Writer,self).save()

class Category(models.Model):
	text=models.CharField(max_length=100,blank=False,unique=True)

	def __str__(self):
		return self.text

class AboutUs(models.Model):
	text=models.CharField(max_length=10000,blank=False)

class PostTags(models.Model):
	text=models.CharField(max_length=25,blank=False,unique=True)

	def __str__(self):
		return self.text
 
class Post(models.Model):
	writer=models.ForeignKey(Writer,on_delete=models.CASCADE)
	first_image=models.ImageField(upload_to='PostImage',blank=True,null=True)
	Category=models.ForeignKey(Category,on_delete=models.CASCADE)
	heading=models.CharField(max_length=200,blank=False)
	meta=models.CharField(max_length=1000,blank=False)
	post_date=models.DateTimeField(default=timezone.now)
	content = RichTextUploadingField()
	archieved=models.BooleanField(default=False)
	posttags=models.ManyToManyField(PostTags)

	def save(self,*args,**kwargs):
		if self.first_image:
			ima = Image.open(self.first_image)
			if ima.mode!='RGB':
				imr=ima.convert('RGB')
				ima=imr
			w,h=ima.size
			if(w>=h):
				marker=h
			else:
				marker=w
			output = BytesIO()
			imager=ima.crop((0,0,marker,marker))
			#Resize/modify the image
			im = imager.resize((720,1080),Image.ANTIALIAS)
			print(im)
			#after modifications, save it to the output
			im.save(output, format='JPEG', quality=95)
			output.seek(0)#change the imagefield value to be the newley modifed image value
			self.first_image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.first_image
				.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

		super(Post,self).save()

	def getyear(self):
		return self.post_date.strftime("%B %d %Y")

	def full_month(self):
		return self.post_date.strftime("%B %d %Y")


# Create your models here.
