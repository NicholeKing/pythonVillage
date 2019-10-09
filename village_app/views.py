from django.shortcuts import render, redirect
from .models import User, Character, Job, Messages
import random

def sign_in(request):
	return render(request, "register.html")

def check_reg(request):
	check = User.objects.register(request.POST)
	if check['is_valid']:
		request.session['reg_errors'] = {}
		request.session['uid'] = check['user'].id
		return redirect('/createChar')
	else:
		request.session['reg_errors'] = check['reg_errors']
		return redirect('/')

def check_log(request):
	check = User.objects.login(request.POST)
	if check['is_valid']:
		request.session['log_errors'] = {}
		request.session['uid'] = check['user'].id
		user = User.objects.get(id=request.session['uid'])
		char = Character.objects.get(player_id=user.id)
		request.session['cid'] = char.id
		return redirect('/dashboard')
	else:
		request.session['log_errors'] = check['log_errors']
		return redirect('/')

def char_create(request):
	if 'uid' not in request.session:
		return redirect('/')
	if 'cid' in request.session:
		return redirect('/dashboard')
	return render(request, "create.html")

def char_validation(request):
	check = Character.objects.char_validation(request.POST, request.session['uid'])
	if check['is_valid']:
		user = User.objects.get(id=request.session['uid'])
		char = Character.objects.get(player_id=user.id)
		request.session['cid'] = char.id
		request.session['char_errors'] = {}
		return redirect('/dashboard')
	else:
		request.session['char_errors'] = check['char_errors']
		return redirect('/createChar')

def dashboard(request):
	if 'uid' not in request.session:
		return redirect('/')
	if 'activity_log' not in request.session:
		request.session['activity_log'] = []
	char = Character.objects.get(id=request.session['cid'])
	received = Character.objects.get(id=request.session['uid']).receiver.all()
	context = {
		"person": Character.objects.get(id=request.session['uid']),
		"received": received,
		"char": char,
	}
	return render(request, "dashboard.html", context)

def find_job(request):
	if 'uid' not in request.session:
		return redirect('/')
	return render(request, "find_job.html", {"all_jobs": Job.objects.all(), "char": Character.objects.get(id=request.session['cid'])})

def post_job(request):
	if 'uid' not in request.session:
		return redirect('/')
	return render(request, "post_job.html", {"char": Character.objects.get(id=request.session['cid'])})

def job_valid(request):
	check = Job.objects.job_valid(request.POST, request.session['uid'])
	poster = Character.objects.get(id=request.session['cid'])
	if check['is_valid']:
		request.session['job_errors'] = {}
		request.session['activity_log'].insert(0, "You posted a job! Your standing in the village increased by 1!")
		if poster.standing < 101:
			poster.standing = poster.standing + 1
		poster.save()
		return redirect('/findJob')
	else:
		request.session['job_errors'] = check['job_errors']
		return redirect('/postJob')

def job_details(request, id):
	if 'uid' not in request.session:
		return redirect('/')
	return render(request, "job_details.html", {"details": Job.objects.get(id=id), "char": Character.objects.get(id=request.session['cid'])})

def job_delete(request, id):
	post = Job.objects.get(id=id)
	post.delete()
	return redirect('/findJob')

def job_result(request, id):
	#setting variables up
	quest = Job.objects.get(id=id)
	taker = Character.objects.get(id=request.session['cid'])
	poster = Character.objects.get(id=quest.poster.id)

	#declaring you took the job
	request.session['activity_log'].insert(0, "You took " + poster.char_name + "'s job request!")

	#setting up job number
	if quest.job_occupation == "Artist" or quest.job_occupation == "Entertainer":
		job_num = 1
	if quest.job_occupation == "Simple Villager" or quest.job_occupation == "Farmer" or quest.job_occupation == "Scholar":
		job_num = 2
	if quest.job_occupation == "Blacksmith" or quest.job_occupation == "Mechanic" or quest.job_occupation == "Merchant":
		job_num = 3
	if quest.job_occupation == "Sailor" or quest.job_occupation == "Adventurer":
		job_num = 4
	if quest.job_occupation == "Hunter" or quest.job_occupation == "Mercenary/Assassin" or quest.job_occupation == "Soldier":
		job_num = 5

	#setting up your occ number
	if taker.occupation == "Artist" or taker.occupation == "Entertainer":
		occ_num = 1
	if taker.occupation == "Simple Villager" or taker.occupation == "Farmer" or taker.occupation == "Scholar":
		occ_num = 2
	if taker.occupation == "Blacksmith" or taker.occupation == "Mechanic" or taker.occupation == "Merchant":
		occ_num = 3
	if taker.occupation == "Sailor" or taker.occupation == "Adventurer":
		occ_num = 4
	if taker.occupation == "Hunter" or taker.occupation == "Mercenary/Assassin" or taker.occupation == "Soldier":
		occ_num = 5

	#setting up pet numbers
	if taker.pet == "Cat" or taker.pet == "Small Bird" or taker.pet == "Dog":
		pet_num = 1
	if taker.pet == "Pegasus" or taker.pet == "Golem" or taker.pet == "Sentient Blob" or taker.pet == "Unicorn":
		pet_num = 2
	if taker.pet == "Wolf" or taker.pet == "Giant Eagle" or taker.pet == "Alien Creature" or taker.pet == "Serpent" or taker.pet == "Giant Spider" or taker.pet == "Giant Crab":
		pet_num = 3
	if taker.pet == "Griffin" or taker.pet == "Lion" or taker.pet == "Tiger" or taker.pet == "Giant Bear" or taker.pet == "Chimera":
		pet_num = 4
	if taker.pet == "Dragon" or taker.pet == "Leviathan" or taker.pet == "Yeti":
		pet_num = 5

	#standing bonus is always 10%
	standing_bonus = int(taker.standing) * 0.1

	#if the numbers match
	if occ_num == job_num:
		#if the occupations match, biggest potential bonus
		if taker.occupation == quest.job_occupation:
			rand_bonus = random.uniform(0.2, 0.45)
		#if the numbers just match but not the occ, semi large bonus
		else:
			rand_bonus = random.uniform(0.1, 0.35)

	#if the numbers don't match
	else:
		difference = occ_num - job_num
		if abs(difference) == 1:
			rand_bonus = random.uniform(-0.2, 0.25)
		else:
			rand_bonus = random.uniform(-1, 0.15)
	#calculate occupation bonus		
	occ_bonus = int(quest.reward) * rand_bonus

	#calculate pet contribution
	#if numbers match, only slight potential for mayhem, more chance of bonus
	if pet_num == job_num:
		prand_bonus = random.uniform(-0.1, 0.4)
	else:
		#if numbers are within 1 of each other, higher chance of mayhem
		diff = pet_num - job_num
		#number was 1 off, slightly higher chance of mayhem
		if abs(diff) == 1:
			prand_bonus = random.uniform(-0.15, 0.25)
		#if number was 2 off, even higher chance
		if abs(diff) == 2:
			prand_bonus = random.uniform(-0.2, 0.2)
		#if number was 3 off, almost assured chance of mayhem
		else:
			prand_bonus = random.uniform(-0.35, 0.1)
	#calculate pet bonus
	pet_bonus = int(quest.reward) * prand_bonus
	if int(pet_bonus) == 0:
		request.session['activity_log'].insert(0, str(taker.pet_name) + " had no effect on the job and brought 0 extra gold!")
	elif int(pet_bonus) < 0:
		request.session['activity_log'].insert(0, str(taker.pet_name) + " caused trouble and cost you " + str(int(abs(pet_bonus))) + " gold!")
	else:
		request.session['activity_log'].insert(0, str(taker.pet_name) + " helped on your mission and earned you " + str(int(pet_bonus)) + " extra gold!")

	#calculate total
	total = int(quest.reward) + int(standing_bonus) + int(occ_bonus) + int(pet_bonus)

	print(quest.reward)
	print(standing_bonus)
	print(occ_bonus)
	print(pet_bonus)
	print(total)

	#setting that total into a session for use
	request.session['total'] = total
	#parsing out reward and payback
	if total > quest.reward:
		taker.gold = int(taker.gold) + int(total)
		taker.save()
		poster.gold = int(poster.gold)-int(quest.reward)
		poster.save()
		if taker.standing < 101:
			taker.standing = taker.standing + 1
		else:
			taker.standing = 100
		taker.save()
		request.session['activity_log'].insert(0, "You earned " + str(request.session['total']) + " gold!")
		request.session['activity_log'].insert(0, "Your standing in the village increased by 1!")
	elif total < 0:
		taker.gold = int(taker.gold) + int(total)
		taker.save()
		poster.gold = int(poster.gold) - int(total)
		poster.save()
		taker.standing = taker.standing - 5
		taker.save()
		request.session['activity_log'].insert(0, "You lost " + str(abs(request.session['total'])) + " gold to pay for damages!")
		request.session['activity_log'].insert(0, "Chaos on the job!! Your standing in the village decreased by 5!")
	elif total < quest.reward:
		taker.gold = taker.gold + int(total)
		taker.save()
		poster.gold = int(poster.gold)-int(total)
		poster.save()
		taker.standing = taker.standing - 2
		taker.save()
		request.session['activity_log'].insert(0, "You were docked " + str(diff) + " gold for problems on the job... You still earned " + str(request.session['total']) + " gold!")
		request.session['activity_log'].insert(0, "Your standing in the village decreased by 2!")
	else:
		taker.gold = int(taker.gold) + int(total)
		taker.save()
		poster.gold = int(poster.gold)-int(quest.reward)
		poster.save()
		if taker.standing < 101:
			taker.standing = taker.standing + 1
		else:
			taker.standing = 100
		taker.save()
		request.session['activity_log'].insert(0, "You earned " + str(request.session['total']) + " gold!")
		request.session['activity_log'].insert(0, "Your standing in the village increased by 1!")

	#wrapping up job
	quest.available = False
	quest.save()
			
	#if you fall below 0 gold due to mission problem, all your job postings disappear
	if taker.gold <= 0:
		person = Job.objects.filter(poster_id=taker.id)
		request.session['activity_log'].insert(0, "You're out of funds! All your job postings were removed!")
		for task in person:
			task.available = False
			task.save()
	#if the poster falls below 0 gold due to reward payout, all their job postings disappear
	if poster.gold <= 0:
		person = Job.objects.filter(poster_id=poster.id)
		request.session['activity_log'].insert(0, "You're out of funds! All your job postings were removed!")
		for task in person:
			task.available = False
			task.save()
	return redirect('/tookJob')

def took_job(request):
	if 'uid' not in request.session:
		return redirect('/')
	context = {
		"total": request.session['activity_log'][1],
		"standing": request.session['activity_log'][0],
		"pet": request.session['activity_log'][2],
	}
	return render(request, "quest.html", context)

def char_bio(request, id):
	if 'uid' not in request.session:
		return redirect('/')
	character = Character.objects.get(id=id)
	friends = Character.objects.get(id=id).friend.all()
	context = {
		"char": Character.objects.get(id=request.session['cid']),
		"person": Character.objects.get(id=id),
		"friends": friends
	}
	return render(request, "char_bio.html", context)

def edit(request, id):
	if 'uid' not in request.session:
		return redirect('/')
	if id != request.session['uid']:
		return redirect('/dashboard')
	context = {
		"char": Character.objects.get(id=request.session['cid'])
	}
	return render(request, "edit.html", context)

def edit_form(request):
	check = Character.objects.edit_validation(request.POST, request.session['uid'])
	if check['is_valid']:
		request.session['char_errors'] = {}
		return redirect('/dashboard')
	else:
		char = Character.objects.get(id=request.session['uid'])
		request.session['char_errors'] = check['char_errors']
		return redirect(f'/edit/{ char.id }')
	return redirect('/dashboard')

def friends(request):
	if 'uid' not in request.session:
		return redirect('/')
	all_villagers = Character.objects.all()
	friends = Character.objects.get(id=request.session['cid']).friend.all()
	others = all_villagers.difference(friends)
	context = {
		"friends": friends,
		"others": others,
		"char": Character.objects.get(id=request.session['cid'])
	}
	return render(request, "friends.html", context)

def add_friend(request, id):
	new = Character.objects.get(id=id)
	new.friend.add(Character.objects.get(id=request.session['uid']))
	return redirect('/villagers')

def remove_friend(request, id):
	old = Character.objects.get(id=id)
	old.friend.remove(Character.objects.get(id=request.session['uid']))
	return redirect('/villagers')

def messages(request):
	if 'uid' not in request.session:
		return redirect('/')
	sent = Character.objects.get(id=request.session['cid']).sender.all()
	received = Character.objects.get(id=request.session['cid']).receiver.all()
	context = {
		"all_chars": Character.objects.all(),
		"sent": sent,
		"received": received,
		"char": Character.objects.get(id=request.session['uid'])
	}
	return render(request, "messages.html", context)

def send(request):
	check = Messages.objects.mess_valid(request.POST, request.session['uid'])
	if check['is_valid']:
		request.session['mess_errors'] = {}
		return redirect('/messages')
	else: 
		request.session['mess_errors'] = check['mess_errors']
		return redirect('/messages')

def viewMess(request, message_id):
	get_mess = Messages.objects.get(id=message_id)
	sent_by = get_mess.sender.id
	get_rec = get_mess.receiver.char_name
	print(get_rec)
	sender_id = Character.objects.get(id=sent_by)
	request.session['message'] = get_mess.content
	request.session['sent'] = sender_id.char_name
	request.session['sent_by'] = sender_id.id
	request.session['rec_by'] = get_rec
	return redirect('/messages')

def logout(request):
	request.session.clear()
	return redirect('/')
