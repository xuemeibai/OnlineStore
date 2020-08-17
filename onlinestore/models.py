from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
# from django.contrib.gis.db.models.fields import PointField

# For users to release products to sell
class Item(models.Model):
    name = models.CharField(max_length=50) #item_name --> name
    picture = models.FileField(blank=True) #item_picture --> picture
    content_type = models.CharField(max_length=50)
    description = models.CharField(max_length=200) #product_introduction --> description
    date_created = models.DateTimeField(default=timezone.now, blank=True)
    owner = models.ForeignKey(User, related_name="posted_items", on_delete=models.PROTECT)
    CONDITION = (
                ('Brand New', 'BrandNew'),
                ('80% New', '80%'),
                ('60% New', '60%'),
                ('40% New', '40%'),
                ('Old', 'Old'),
        )
    condition_value = models.CharField(max_length=20, choices=CONDITION)
    # tags = TagField(max_count=10, force_lowercase=True, space_delimiter=False, blank=True)
    TYPE=(
                ('Furniture', 'Furniture'),
                ('Electronics', 'Electronics'),
                ('Others', 'Others'),
        )
    type_value= models.CharField(max_length=20, choices=TYPE)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    unit = models.CharField(max_length=80, default='each')
    # location = PointField()
    num_of_views=models.IntegerField(default=0)

    status = models.BooleanField(default=0) #0 for In stock, 1 for traded
    requests = models.ManyToManyField('Profile', related_name="requested_items")
    sold_to = models.ForeignKey(User, related_name="purchased_items", on_delete=models.PROTECT)

    lat = models.DecimalField(max_digits=20, decimal_places=15, default=0)
    lng = models.DecimalField(max_digits=20, decimal_places=15, default=0)

    SCORE_CHOICES = [
                    (1, '1'),
                    (2, '2'),
                    (3, '3'),
                    (4, '4'),
                    (5, '5'),
        ]
    buyer_rate = models.IntegerField(choices=SCORE_CHOICES, default=4)
    owner_rate = models.IntegerField(choices=SCORE_CHOICES, default=4)

    have_buyer_rated = models.BooleanField(default=0) #0 for haven't rated, 1 for rated
    have_owner_rated = models.BooleanField(default=0) #0 for haven't rated, 1 for rated   
    
    class Meta:
        ordering=['date_created']

class Profile(models.Model):
    profile_picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    # Users have a list of users in  the recent conservation
    # friends = models.ManyToManyField(User, related_name="friends", blank = True)
    user = models.OneToOneField(User, related_name="profile", on_delete=models.PROTECT)

    bio = models.TextField(max_length=2000, blank=True)
    # location = PointField()
    creditrate = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    rate_cnt = models.IntegerField(default=0)
    
    favorite = models.ManyToManyField(Item, related_name="favorite", blank = True)

class Post(models.Model):
    created_by = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="created_posts")
    post_input_text = models.CharField(max_length=300)
    creation_time = models.DateTimeField()
    belong_item =models.ForeignKey(Item,on_delete=models.PROTECT, related_name="posts")

    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    class Meta:
        ordering=['creation_time']

    def __str__(self):
        return 'Posts(USER =' + str(self.created_by) + 'content = ' + str(self.post_input_text) + 'Create Time = ' + str(self.creation_time) + ')'

class Comment(models.Model):
    created_by = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="created_comments")
    belong_post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name="comments")
    
    belong_item =models.ForeignKey(Item,on_delete=models.PROTECT, related_name="items_comments")
    
    content = models.CharField(max_length=300)
    creation_time = models.DateTimeField()

    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    class Meta:
        ordering=['creation_time']

    def __str__(self):
        return 'id = ' + str(self.id) + 'content = ' + str(self.content)

# Messages for seller and buyer to communicate
class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(Profile, default=1, on_delete=models.CASCADE, related_name='recipient')
    subject = models.CharField(max_length=128)
    referenced_product = models.ForeignKey(Item, on_delete=models.CASCADE)
    body = models.TextField(max_length=5000)

# Reviews for every transaction
class Review(models.Model):
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviewer')
    reviewee = models.ForeignKey(Profile, default=1, on_delete=models.CASCADE, related_name='reviewee')
    title = models.CharField(max_length=128)
    SCORE_CHOICES = [
                    (1, '1'),
                    (2, '2'),
                    (3, '3'),
                    (4, '4'),
                    (5, '5'),
        ]
    score = models.IntegerField(choices=SCORE_CHOICES, default=4)
    review = models.TextField(max_length=5000)
