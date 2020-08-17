from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import datetime,timezone
from onlinestore.forms import *
from django.http import HttpResponse, Http404
from onlinestore.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.dateparse import parse_datetime
import json
from django.core.serializers.json import DjangoJSONEncoder
# Generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator
# Send mail from within Django
from django.core.mail import send_mail
# Create your views here.

def home_action(request):
	context = {}
	if request.user.is_authenticated:
		profile = get_object_or_404(Profile, user=request.user)
		context['profile'] = profile
		context['favorite'] = profile.favorite.count()
		context['cart_num'] = Item.objects.filter(status=0,requests__in=[profile]).count()
	else:
		context['profile'] = []
		context['favorite'] = 0
		context['cart_num'] = 0
	items = Item.objects.filter(status=0).order_by("date_created").reverse()
	context['items'] = items
	context['user'] = request.user
	context['num'] = items.count()
	if context['num'] == 0:
		context['ad1'] = {'name':'BLANK','price':'12','original_price':'60'}
		context['ad2'] = {'name':'BLANK','price':'12','original_price':'60'}
	elif context['num'] == 1:
		context['ad1'] = items[0]
		context['ad2'] = {'name':'BLANK','price':'12','original_price':'60'}
	else:
		context['ad1'] = items[0]
		context['ad2'] = items[1]
	return render(request, 'onlinestore/home.html', context)

@login_required
def edit_profile(request,id):
	profile = Profile.objects.get(user_id=id)
	context = {}
	form = ProfileForm(request.POST, request.FILES, instance=profile)
	if not form.is_valid():
		context['form'] = form
	elif 'profile_picture' in request.FILES:
		profile.content_type = form.cleaned_data['profile_picture'].content_type
		profile.profile_picture = form.cleaned_data['profile_picture']
		form.save()
		context['message'] = 'Picture saved.'
		profile.save()
	context['form'] = ProfileForm()
	context['profile'] = profile
	if 'bio' in request.POST or request.POST['bio']:
		profile.bio = request.POST['bio']
		profile.save()
		context['bio'] = profile.bio
	context['user_id'] = profile.user_id
	context['first_name'] = profile.user.first_name
	context['last_name'] = profile.user.last_name
	context['bio'] = profile.bio
	context['length'] = len(profile.bio)
	context['creditrate'] = round(profile.creditrate,1)
	context['favorite'] = profile.favorite.count()
	context['posting'] = Item.objects.filter(owner = request.user,status=0).count()
	context['bought'] = Item.objects.filter(sold_to = request.user,status=1).count()
	context['sold'] = Item.objects.filter(owner = request.user,status=1).count()
	return render(request, 'onlinestore/userprofile.html', context)

@login_required
def user_profile(request,id):
	if Profile.objects.filter(user_id=id).exists():
		profile = Profile.objects.get(user_id=id)
	else:
		profile = Profile.objects.create(user_id=id)
	context = {}
	context['user_id'] = profile.user_id
	context['first_name'] = profile.user.first_name
	context['last_name'] = profile.user.last_name
	context['bio'] = profile.bio
	context['length'] = len(profile.bio)
	context['form']  = ProfileForm()
	context['profile'] = profile
	context['creditrate'] = round(profile.creditrate,1)
	context['favorite'] = profile.favorite.count()
	context['posting'] = Item.objects.filter(owner = request.user,status=0).count()
	context['bought'] = Item.objects.filter(sold_to = request.user,status=1).count()
	context['sold'] = Item.objects.filter(owner = request.user,status=1).count()
	context['cart_num'] = Item.objects.filter(status=0,requests__in=[profile]).count()
	#context['message'] = Message.objects.filter
	return render(request, 'onlinestore/userprofile.html', context)

@login_required
def get_self_avatar(request, id):
	profile = get_object_or_404(Profile, user_id=id)
	if profile.profile_picture:
		pic = profile.profile_picture
	else:
		pic = {}
	print('Picture #{} fetched from db: {} (type={})'.format(id, profile.profile_picture, type(profile.profile_picture)))
	return HttpResponse(pic, content_type='application/json')

def search(request):
	context = {}
	if request.user.is_authenticated:
		profile = get_object_or_404(Profile, user=request.user)
		context['profile'] = profile
		context['favorite'] = profile.favorite.count()
		context['cart_num'] = Item.objects.filter(status=0,requests__in=[profile]).count()
	else:
		context['profile'] = []
		context['favorite'] = 0
		context['cart_num'] = 0
	context['user'] = request.user
	context['items'] = Item.objects.all()
	if 'q' in request.GET or request.GET['q']:
		context['items']  = Item.objects.filter(name__icontains=request.GET['q'],status=0)
		context['num'] = context['items'].count()
	ad = Item.objects.filter(status=0).order_by("date_created").reverse()
	if context['num'] == 0:
		context['ad1'] = {'name':'BLANK','price':'12','original_price':'60'}
		context['ad2'] = {'name':'BLANK','price':'12','original_price':'60'}
	elif context['num'] == 1:
		context['ad1'] = ad[0]
		context['ad2'] = {'name':'BLANK','price':'12','original_price':'60'}
	else:
		context['ad1'] = ad[0]
		context['ad2'] = ad[1]
	return render(request, 'onlinestore/home.html', context)

def category(request, type):
	context = {}
	if type==0:
		type_value = 'Furniture'
	elif type==1:
		type_value = 'Electronics'
	elif type==2:
		type_value = 'Others'
	if request.user.is_authenticated:
		profile = get_object_or_404(Profile, user=request.user)
		context['profile'] = profile
		context['favorite'] = profile.favorite.count()
		context['cart_num'] = Item.objects.filter(status=0,requests__in=[profile]).count()
	else:
		context['profile'] = []
		context['favorite'] = 0
		context['cart_num'] = 0
	context['user'] = request.user
	context['items'] = Item.objects.filter(type_value=type_value,status=0).reverse()
	context['num'] = context['items'].count()
	ad = Item.objects.filter(status=0).order_by("date_created").reverse()
	if context['num'] == 0:
		context['ad1'] = {'name':'BLANK','price':'12','original_price':'60'}
		context['ad2'] = {'name':'BLANK','price':'12','original_price':'60'}
	elif context['num'] == 1:
		context['ad1'] = ad[0]
		context['ad2'] = {'name':'BLANK','price':'12','original_price':'60'}
	else:
		context['ad1'] = ad[0]
		context['ad2'] = ad[1]
	return render(request, 'onlinestore/home.html', context)

def get_sorted_data(request, type):
	sort_rule = type
	errors=''
	if sort_rule == 0:
		sort_type = ('price')
	elif sort_rule == 1:
		sort_type = ('-price')
	elif sort_rule == 2:
		sort_type = ('-date_created')
	elif sort_rule == 3:
		sort_type = ('date_created')
	context={}
	if request.user.is_authenticated:
		profile = get_object_or_404(Profile, user=request.user)
		context['profile'] = profile
		context['favorite'] = profile.favorite.count()
		context['cart_num'] = Item.objects.filter(status=0,requests__in=[profile]).count()
	else:
		context['profile'] = []
		context['favorite'] = 0
		context['cart_num'] = 0
	context['user'] = request.user
	item_list = Item.objects.order_by(sort_type).filter(status=0)
	context['items'] = item_list
	context['num'] = context['items'].count()
	context['errors'] = errors
	ad = Item.objects.filter(status=0).order_by("date_created").reverse()
	if context['num'] == 0:
		context['ad1'] = {'name':'BLANK','price':'12','original_price':'60'}
		context['ad2'] = {'name':'BLANK','price':'12','original_price':'60'}
	elif context['num'] == 1:
		context['ad1'] = ad[0]
		context['ad2'] = {'name':'BLANK','price':'12','original_price':'60'}
	else:
		context['ad1'] = ad[0]
		context['ad2'] = ad[1]
	return render(request, 'onlinestore/home.html', context)

def login_action(request):
	context = {}

	# Just display the registration form if this is a GET request.
	if request.method == 'GET':
		context['form'] = LoginForm()
		return render(request, 'onlinestore/login.html', context)

	# Creates a bound form from the request POST parameters and makes the
	# form available in the request context dictionary.
	form = LoginForm(request.POST)
	context['form'] = form

	# Validates the form.
	if not form.is_valid():
		print("invalid form!")
		print(str(request.POST))
		print(form)
		return render(request, 'onlinestore/login.html', context)

	new_user = authenticate(username=form.cleaned_data['username'],
							password=form.cleaned_data['password'])

	login(request, new_user)
	return redirect(reverse('home'))

def logout_action(request):
	logout(request)
	return redirect(reverse('home'))

@transaction.atomic
def register_action(request):
	context = {}

	# Just display the registration form if this is a GET request.
	if request.method == 'GET':
		context['form'] = RegistrationForm()
		return render(request, 'onlinestore/register.html', context)

	# Creates a bound form from the request POST parameters and makes the
	# form available in the request context dictionary.
	form = RegistrationForm(request.POST)
	context['form'] = form

	# Validates the form.
	if not form.is_valid():
		# print("invalid form!")
		# print(str(request.POST))
		# print(form)
		return render(request, 'onlinestore/register.html', context)

	# At this point, the form data is valid.  Register and login the user.
	new_user = User.objects.create_user(username=form.cleaned_data['username'],
	password=form.cleaned_data['password'],
	email=form.cleaned_data['email'],
	first_name=form.cleaned_data['first_name'],
	last_name=form.cleaned_data['last_name'])


	# Mark the user as inactive to prevent login before email confirmation.
	new_user.is_active = False
	new_user.save()

	profile = Profile(user=new_user, id=new_user.id)
	profile.save()


	# Generate a one-time use token and an email message body
	token = default_token_generator.make_token(new_user)
	email_body = """

Welcome to Pick Urs Second-hand Onlinestore. Hope you can enjoy your journey here!  Please click the link below to
verify your email address and complete the registration of your account:
  http://%s%s
""" % (request.get_host(),
	   reverse('confirm', args=(new_user.username, token)))
	send_mail(subject="Verify your email address",
			  message= email_body,
			  from_email="chenyuji@andrew.cmu.edu",
			  recipient_list=[new_user.email])
	context['email'] = form.cleaned_data['email']
	return render(request, 'onlinestore/email_confirmation.html', context)


@transaction.atomic
def confirm_action(request, username, token):
	new_user = get_object_or_404(User, username=username)
	# Send 404 error if token is invalid
	if not default_token_generator.check_token(new_user, token):
		raise Http404
	# Otherwise token was valid, activate the user.
	new_user.is_active = True
	new_user.save()
	return render(request, 'onlinestore/confirmed.html', {})

@login_required
def AddItemPost(request):
	context = {}
	errors=[]
	profile = Profile.objects.get(user = request.user)
	form = ProfileForm( instance = profile)
	if request.method != 'POST' :
		errors.append('You must use the POST method')
		context={}
		all_items = Item.objects.order_by("date_created").reverse()
		context['newpost'] = ItemPostForm()
		context['items'] = all_items
		context['user'] = request.user
		context['errors'] = errors
		context['form'] = form
		context['profile'] = profile
		return render(request,'onlinestore/release.html',context)
	item=Item()
	add_post = ItemPostForm(request.POST, request.FILES, instance=item)
	if not add_post.is_valid():
		print('formmmmmmmmmmmmm is not valid')
		print(request.POST)
		print(add_post.errors)

		context={}
		all_items = Item.objects.order_by("date_created").reverse()
		context['newpost'] = ItemPostForm()
		context['items'] = all_items
		context['user'] = request.user
		return render(request,'onlinestore/release.html',context)
	item.date_created=timezone.now()
	item.owner = request.user
	item.sold_to = request.user
	item.condition_value = request.POST.get('condition_value', "")
	item.type_value = request.POST.get('type_value', "")
	item.save()
	new_item = ItemPostForm(request.POST,request.FILES, instance = item)

	new_item.save()
	items = Item.objects.order_by("date_created").reverse()
	context['items']= items
	context['errors']=errors
	context['new_item'] = new_item
	return redirect(reverse('home'))

def get_photo(request, id):
	context = {}
	item = get_object_or_404(Item, id=id)
	#context['item'] = item
	print('Picture #{} fetched from db: {} (type={})'.format(id, item.picture, type(item.picture)))
	return HttpResponse(item.picture, content_type='application/json')

@login_required
def item_detail_action(request, id):
	profile = get_object_or_404(Profile, user = request.user)
	user = request.user
	item = get_object_or_404(Item, id=id)
	item.num_of_views += 1
	item.save()

	posts = Post.objects.filter(belong_item = item)
	comments = Comment.objects.filter(belong_item = item)

	context = {'profile': profile, 'user': user, 'item': item, 'posts': posts, 'comments': comments}
	if request.method == 'GET':
		return render(request, 'onlinestore/item_details.html', context)

@login_required
def add_to_favorite_action(request, id):
	item = get_object_or_404(Item, id=id)
	user = request.user
	profile = get_object_or_404(Profile, user = request.user)

	if item not in user.profile.favorite.all():
		user.profile.favorite.add(item)
	context = {'profile': profile, 'user': user, 'item': item}
	return render(request, 'onlinestore/item_details.html', context)

@login_required
def delete_from_favorite_action(request, id):
	item = get_object_or_404(Item, id=id)
	user = request.user
	profile = get_object_or_404(Profile, user = request.user)
	if item in user.profile.favorite.all():
		user.profile.favorite.remove(item)
	context = {'profile': profile, 'user': user, 'item': item}
	return render(request, 'onlinestore/item_details.html', context)

@login_required
def add_to_favorite_home_action(request):
	if request.GET.get('item_id') == None:
		raise Http404
	item_id=int(request.GET.get('item_id'))
	context={}
	item = get_object_or_404(Item, id=item_id)
	if item not in request.user.profile.favorite.all():
		request.user.profile.favorite.add(item)
	response_text = context
	return HttpResponse(response_text, content_type='application/json')

@login_required
def delete_from_favorite_home_action(request):
	if request.GET.get('item_id') == None:
		raise Http404
	item_id=int(request.GET.get('item_id'))
	context={}
	item = get_object_or_404(Item, id=item_id)
	if item in request.user.profile.favorite.all():
		request.user.profile.favorite.remove(item)
	response_text = context
	return HttpResponse(response_text, content_type='application/json')

@login_required
def request_for_trade_action(request, id):
	item = get_object_or_404(Item, id=id)
	user = request.user
	profile = get_object_or_404(Profile, user = request.user)

	if user.profile not in item.requests.all():
		item.requests.add(user.profile)

	context = {'profile': profile, 'user': user, 'item': item}
	return render(request, 'onlinestore/item_details.html', context)

@login_required
def cancel_trade_request_action(request, id):
	item = get_object_or_404(Item, id=id)
	user = request.user
	profile = get_object_or_404(Profile, user = request.user)

	if user.profile in item.requests.all():
		item.requests.remove(user.profile)

	context = {'profile': profile, 'user': user, 'item': item}
	return render(request, 'onlinestore/item_details.html', context)

@login_required
def accept_request_action(request, id, userid):
	item = get_object_or_404(Item, id=id)
	buyer = get_object_or_404(User, id=userid)

	user = request.user
	profile = get_object_or_404(Profile, user = request.user)

	error_message = None
	if item.status:
		error_message = "You've already chosen trade with another user. You can only accept one request."
	else:
		item.status = 1
		item.sold_to = buyer
	item.save()
	context = {'profile': profile, 'user': user, 'item': item, "error": error_message}
	return render(request, 'onlinestore/item_details.html', context)

@login_required
def delete_item_action(request, id):
	item = get_object_or_404(Item, id=id)
	item.delete()

	return redirect(reverse('home'))

@login_required
def favorites_page_action(request):
	errors=[]
	context={}
	context['errors'] = errors
	profile = get_object_or_404(Profile, user=request.user)
	favorites= profile.favorite.all()
	# items = Item.objects.filter(name__in=favorites)
	context['profile'] = profile
	context['user'] = request.user
	context['items'] = favorites
	context['errors'] = errors
	return render(request, 'onlinestore/favorites.html', context)

@login_required
def posting_items_action(request):
	errors=[]
	context={}
	context['errors'] = errors
	profile = get_object_or_404(Profile,id=request.user.id)
	posting_items= Item.objects.filter(owner = request.user,status=0)

	context['profile'] = profile
	context['user'] = request.user
	context['items'] = posting_items
	context['errors'] = errors
	return render(request, 'onlinestore/posting_items.html', context)

@login_required
def history_sells_action(request):
	errors=[]
	context={}
	context['errors'] = errors
	profile = get_object_or_404(Profile,id=request.user.id)
	history_sells = Item.objects.filter(owner = request.user,status=1)

	context['profile'] = profile
	context['user'] = request.user
	context['items'] = history_sells
	context['errors'] = errors
	return render(request, 'onlinestore/history_sells.html', context)

@login_required
def history_orders_action(request):
	errors=[]
	context={}
	context['errors'] = errors
	profile = get_object_or_404(Profile,id=request.user.id)
	history_orders= Item.objects.filter(sold_to = request.user, status = 1)

	context['profile'] = profile
	context['user'] = request.user
	context['items'] = history_orders
	context['errors'] = errors
	return render(request, 'onlinestore/history_orders.html', context)

@login_required
def get_list_json(request):
    if request.GET.get('last_refresh') == None:
        raise Http404
    items = []
    for p in Items.objects.filter(creation_time__gte = request.GET.get('last_refresh')):
        items.append({
            'id': p.id,
            'name': p.name,
            'condition_value': p.condition_value,
            'picture': p.picture,
            'time': p.date_created.isoformat()
        })
    response_text = json.dumps({'items': items})
    response = HttpResponse(response_text, content_type='application/json')
    #response['Access-Control-Allow-Origin'] = '*'
    return response 

@login_required
def rate_action(request, id):
	item = get_object_or_404(Item, id = id)

	if 'owner_rate' in request.POST:# buyer rate owner
		owner_rate = request.POST['owner_rate']
		owner_rate = int(owner_rate)
		#update rated user's profile
		rated_profile = item.owner.profile
		rated_profile.creditrate = (rated_profile.creditrate * rated_profile.rate_cnt + owner_rate) / (rated_profile.rate_cnt + 1)
		rated_profile.rate_cnt += 1
		rated_profile.save()

		#update item
		item.owner_rate = owner_rate
		item.have_buyer_rated = 1
		item.save()

	elif 'buyer_rate' in request.POST:
		buyer_rate = request.POST['buyer_rate']
		buyer_rate = int(buyer_rate)
		#update rated user's profile
		rated_profile = item.sold_to.profile
		rated_profile.creditrate = (rated_profile.creditrate * rated_profile.rate_cnt + buyer_rate) / (rated_profile.rate_cnt + 1)
		rated_profile.rate_cnt += 1
		rated_profile.save()

		#update item
		item.buyer_rate = buyer_rate
		item.have_owner_rated = 1
		item.save()
	
	profile = get_object_or_404(Profile, user = request.user)
	user = request.user

	context = {'profile': profile, 'user': user, 'item': item}

	return render(request, 'onlinestore/item_details.html', context)

# This method should return serialized new posts and comments 
# since last refresh time. To do so, we need use object filter
@login_required
def refresh_global_json(request): 
	if request.method != 'GET':
		raise Http404
	if 'last_refresh' not in request.GET:
		raise Http404

	last_refresh = parse_datetime(request.GET['last_refresh'])

	response_posts_text = serializers.serialize('json', 
							Post.objects.filter(creation_time__gte = last_refresh).order_by('creation_time'))
	response_comments_text = serializers.serialize('json', 
							Comment.objects.filter(creation_time__gte = last_refresh).order_by('creation_time'))

	response = {
		'new_posts': response_posts_text,
		'new_comments': response_comments_text,
	}

	return HttpResponse(json.dumps(response), content_type='application/json')

# This method should save the new post into database and return the all new posts and comments
@login_required
def add_post(request, ItemId):
	item = get_object_or_404(Item, id = ItemId)
	
	if request.method != 'POST':
		raise Http404

	if not 'new_post_text' in request.POST or not request.POST['new_post_text']:
		message = 'You must enter a post to add.'
		json_error = '{ "error": "'+message+'" }'
		return HttpResponse(json_error, content_type='application/json')

	if 'last_refresh' not in request.POST or not request.POST['last_refresh']:
		message = 'You must enter last refresh time.'
		json_error = '{ "error": "'+message+'" }'
		return HttpResponse(json_error, content_type='application/json')
	
	new_post = Post(created_by = request.user.profile, 
				post_input_text = request.POST['new_post_text'], 
				creation_time = timezone.now(),
				belong_item = item,
				first_name = request.user.first_name,
                last_name = request.user.last_name,
				)
	new_post.save()

	last_refresh = parse_datetime(request.POST['last_refresh'])

	response_posts_text = serializers.serialize('json', 
							Post.objects.filter(creation_time__gte = last_refresh, belong_item = item).order_by('creation_time'))
	response_comments_text = serializers.serialize('json', 
							Comment.objects.filter(creation_time__gte = last_refresh, belong_item = item).order_by('creation_time'))

	response = {
		'new_posts': response_posts_text,
		'new_comments': response_comments_text,
	}
	return HttpResponse(json.dumps(response), content_type='application/json')

# This method should save the new comment into database and return the new one
@login_required
def add_comment(request, PostId): 
	if request.method != 'POST':
		raise Http404

	if not 'new_comment_text' in request.POST or not request.POST['new_comment_text']:
		message = 'You must enter a comment to add.'
		json_error = '{ "error": "'+message+'" }'
		return HttpResponse(json_error, content_type='application/json')
	
	if 'last_refresh' not in request.POST or not request.POST['last_refresh']:
		message = 'You must enter last refresh time.'
		json_error = '{ "error": "'+message+'" }'
		return HttpResponse(json_error, content_type='application/json')

	belong_post = get_object_or_404(Post, pk = PostId) 
	item = belong_post.belong_item

	new_comment = Comment(created_by = request.user.profile, 
				belong_post = belong_post,
				content = request.POST['new_comment_text'], 
				creation_time = timezone.now(),
				belong_item = item,
				first_name = request.user.first_name,
                last_name = request.user.last_name,
				)
	new_comment.save()

	last_refresh = parse_datetime(request.POST['last_refresh'])

	response_posts_text = serializers.serialize('json', 
							Post.objects.filter(creation_time__gte = last_refresh, belong_item = item).order_by('creation_time'))
	response_comments_text = serializers.serialize('json', 
							Comment.objects.filter(creation_time__gte = last_refresh, belong_item = item).order_by('creation_time'))

	response = {
		'new_posts': response_posts_text,
		'new_comments': response_comments_text,
	}
	return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
def my_cart(request): 
	context = {}
	profile = get_object_or_404(Profile, user = request.user)
	cart = Item.objects.filter(status=0,requests__in=[profile])
	errors=[]
	context['errors'] = errors
	context['profile'] = profile
	context['user'] = request.user
	context['items'] = cart
	return render(request, 'onlinestore/cart.html', context)