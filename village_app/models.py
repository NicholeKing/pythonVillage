from django.db import models
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
AGE_REGEX = re.compile(r'^[0-9]+$')

class UserManager(models.Manager):
	def register(self, postData):
		valid = {
			"is_valid": True,
			"user": None,
			"reg_errors": {}
		}
		#Validate name exists and >3
		if len(postData['name'])<1:
			valid['reg_errors']['name'] = "Name is required!"
		elif len(postData['name'])<3:
			valid['reg_errors']['name'] = "Name must be at least 3 characters in length!"
		#Validate email exists, follows regex, doesn't already exist in db
		if len(postData['email'])<1:
			valid['reg_errors']['email'] = "Email is required!"
		elif not EMAIL_REGEX.match(postData['email']):
			valid['reg_errors']['email'] = "Inavlid email format"
		else:
			valid['user'] = User.objects.filter(email=postData['email'].lower())
			if len(valid['user']) > 0:
				valid['reg_errors']['email'] = "Email in use!"
		#Validate password exists and matches pass_confirm, then hash password
		if len(postData['password'])<1:
			valid['reg_errors']['password'] = "Password is required!"
		elif len(postData['password'])<8:
			valid['reg_errors']['password'] = "Password must be at least 8 characters!"
		elif len(postData['password'])>20:
			valid['reg_errors']['password'] = "Password cannot be over 20 characters!"
		if len(postData['pass_confirm'])<1:
			valid['reg_errors']['pass_confirm'] = "Password Confirm required!"
		elif postData['password'] != postData['pass_confirm']:
			valid['reg_errors']['pass_confirm'] = "Passwords must match!"

		if len(valid['reg_errors']) == 0:
			valid['user'] = User.objects.create(
				name=postData['name'],
				email=postData['email'].lower(),
				password=bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()
				)
		else:
			valid['is_valid'] = False
		return valid

	def login(self, postData):
		valid = {
		'is_valid': True,
		'user': None,
		'log_errors': {}
		}
		#validate correct email
		if len(postData['email'])<1:
			valid['log_errors']['email'] = "Email is required!"
		else:
			valid['user'] = User.objects.filter(email=postData['email'].lower())
			if len(valid['user']) == 0:
				valid['log_errors']['email'] = "Invalid Login"

		#validate password exists
		if len(postData['password'])<1:
			valid['log_errors']['password'] = "Password is required!"
		#check for correct login
		if len(valid['log_errors']) == 0:
			valid['user'] = valid['user'][0]
			check=bcrypt.checkpw(postData['password'].encode(), valid['user'].password.encode())
			#if it comes back false, incorrect login
			if not check:
				valid['is_valid'] = False
				valid['log_errors']['email'] = "Invalid login"
		else:
			valid['is_valid'] = False
		return valid

class User(models.Model):
	name=models.CharField(max_length=255)
	email=models.CharField(max_length=255)
	password=models.CharField(max_length=255)
	objects=UserManager()

class CharacterManager(models.Manager):
	def char_validation(self, postData, user_id):
		valid = {
			"is_valid": True,
			"char": None,
			"char_errors": {},
		}
		#Validate char_name exists
		if len(postData['char_name'])<1:
			valid['char_errors']['char_name'] = "You must have a name!"
		#Validate age exists and is an integer
		if len(postData['age']) <1:
			valid['char_errors']['age'] = "You must have an age!"
		elif not AGE_REGEX.match(postData['age']):
			valid['char_errors']['age'] = "Only whole numbers permitted"
		#Validate description exists and >10
		if len(postData['description'])<1:
			valid['char_errors']['description'] = "Description required!"
		elif len(postData['description'])<10:
			valid['char_errors']['description'] = "Description must be at least 10 characters in length!"
		#Validate pet_name exists
		if len(postData['pet_name'])<1:
			valid['char_errors']['pet_name'] = "Pet must have a name!"

		if len(valid['char_errors']) == 0:
			valid['char'] = Character.objects.create(
				char_name=postData['char_name'],
				race=postData['race'],
				gender=postData['gender'],
				age=postData['age'],
				occupation=postData['occupation'],
				pet=postData['pet'],
				pet_name=postData['pet_name'],
				description=postData['description'],
				player_id=user_id
				)
		else:
			valid['is_valid'] = False
		return valid

	def edit_validation(self, postData, char_id):
		valid = {
			"is_valid": True,
			"char_errors": {},
		}
		#Validate char_name exists
		if len(postData['char_name'])<1:
			valid['char_errors']['char_name'] = "You must have a name!"
		#Validate age exists and is an integer
		if len(postData['age']) <1:
			valid['char_errors']['age'] = "You must have an age!"
		elif not AGE_REGEX.match(postData['age']):
			valid['char_errors']['age'] = "Only whole numbers permitted"
		#Validate description exists and >10
		if len(postData['description'])<1:
			valid['char_errors']['description'] = "Description required!"
		elif len(postData['description'])<10:
			valid['char_errors']['description'] = "Description must be at least 10 characters in length!"
		#Validate pet_name exists
		if len(postData['pet_name'])<1:
			valid['char_errors']['pet_name'] = "Pet must have a name!"

		if len(valid['char_errors']) == 0:
			char = Character.objects.get(id=char_id)
			char.char_name = postData['char_name']
			char.race = postData['race']
			char.gender = postData['gender']
			char.age = postData['age']
			char.occupation = postData['occupation']
			char.description = postData['description']
			char.pet = postData['pet']
			char.pet_name = postData['pet_name']
			char.save()
		else:
			valid['is_valid'] = False
		return valid

class Character(models.Model):
	char_name=models.CharField(max_length=255)
	race=models.CharField(max_length=45)
	gender=models.CharField(max_length=45)
	age=models.IntegerField()
	occupation=models.CharField(max_length=45)
	description=models.TextField()
	pet=models.CharField(max_length=45)
	pet_name=models.CharField(max_length=255)
	gold=models.IntegerField(default=100)
	standing=models.IntegerField(default=20)
	player=models.ForeignKey(User, on_delete=models.CASCADE, related_name="player")
	friend=models.ManyToManyField("self", related_name="friend")
	objects=CharacterManager()

class JobManager(models.Manager):
	def job_valid(self, postData, user_id):
		poster = Character.objects.get(id=user_id)
		valid = {
			"is_valid": True,
			"job": None,
			"job_errors": {}
		}
		#Validate job_title exists and >5
		if len(postData['job_title'])<1:
			valid['job_errors']['job_title'] = "Title is required!"
		if len(postData['job_title'])<5:
			valid['job_errors']['job_title'] = "Title must be longer than 5 characters"
		#Validate description exists and >10
		if len(postData['description'])<1:
			valid['job_errors']['description'] = "Description is required!"
		if len(postData['description'])<10:
			valid['job_errors']['description'] = "Description must be at least 10 characters!"
		#Validate reward exists, >10, and is an integer
		if len(postData['reward'])<1:
			valid['job_errors']['reward'] = "There must be a reward!"
		if len(postData['reward'])<2:
			valid['job_errors']['reward'] = "Reward must be at least 10 gold!"
		elif not AGE_REGEX.match(postData['reward']):
			valid['job_errors']['reward'] = "Only whole numbers allowed!"
		if poster.gold <= 0:
			valid['job_errors']['reward'] = "You do not have the funds to post a job!"

		if len(valid['job_errors'])==0:
			valid['job'] = Job.objects.create(
				job_title=postData['job_title'],
				job_description=postData['description'],
				job_occupation=postData['job_occupation'],
				reward=postData['reward'],
				poster_id=user_id
				)
		else:
			valid['is_valid'] = False
		return valid

class Job(models.Model):
	job_title=models.CharField(max_length=100)
	job_description=models.TextField()
	job_occupation=models.CharField(max_length=45)
	reward=models.IntegerField()
	available=models.BooleanField(default=True)
	poster=models.ForeignKey(Character, on_delete=models.CASCADE, related_name="poster")
	objects=JobManager()

class MessagesManager(models.Manager):
	def mess_valid(self, postData, user_id):
		valid = {
			"is_valid": True,
			"mess": None,
			"mess_errors": {}
		}
		#Validate content exists
		if len(postData['content'])<1:
			valid['mess_errors']['content'] = "Message must have content!"

		if len(valid['mess_errors'])==0:
			valid['mess'] = Messages.objects.create(
				content=postData['content'],
				sender_id=user_id,
				receiver_id=postData['receiver']
				)
		else:
			valid['is_valid'] = False
		return valid

class Messages(models.Model):
	content=models.TextField()
	sender=models.ForeignKey(Character, on_delete=models.CASCADE, related_name="sender")
	receiver=models.ForeignKey(Character, on_delete=models.CASCADE, related_name="receiver")
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)
	objects=MessagesManager()

