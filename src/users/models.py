from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.
from django.utils.simplejson import loads
from orders.models import Order

def resolve_first_name(identity):
    data = loads(identity.data or '{}')
    return data.get('name', {}).get('first_name', '')

def resolve_last_name(identity):
    data = loads(identity.data or '{}')
    return data.get('name', {}).get('last_name', '')

def resolve_ui_lang(identity):
    data = loads(identity.data or '{}')
    return data.get('language', 'ru')[:2]

resolver_map = {'first_name': resolve_first_name,
                'last_name': resolve_last_name}

class LoginzaDataResolution(object):
    def __init__(self, property, *args, **kwargs):
        self.property = property
        super(LoginzaDataResolution, self).__init__(*args, **kwargs)
        
    def __get__(self, profile, cls=None):
        if getattr(profile, self.property, None) is None:
            value = ''
            user_maps = profile.user.usermap_set.all().select_related('identity')[:1]
            if user_maps:
                mp = user_maps[0]
                resolver = resolver_map.get(self.property)
                value = resolver(mp.identity)
            setattr(profile, self.property, value)
            profile.save()
        return getattr(profile, self.property, None)


def orders(user):
    return Order.public_objects.filter(user=user)


def has_orders(user):
    return orders(user).exists()

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)

    res_first_name = LoginzaDataResolution('first_name')
    res_last_name = LoginzaDataResolution('last_name')
    res_ui_lang = LoginzaDataResolution('ui_lang')

    ui_lang = models.CharField(max_length=2, default="ru")
    phone_number = models.CharField(max_length=16, null=True)

    @property
    def full_name(self):
        return u"%s %s" % (self.res_first_name, self.res_last_name)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)