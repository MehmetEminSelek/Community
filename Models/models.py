from django.db import models
import uuid
# import qrcode
from io import BytesIO
from django.core.files import File
# from PIL import Image, ImageDraw
# ALL PROGS SHOULD BE PRIMARY KEY
# USER PRESENTERID SHOULD BE CHARFIELD WITH 16 CHARACTERS
# NO AUTOFIELDS INSTED OF THAT WE ARE GOING TO USE INTEGERFIELD WITH PRIMARY KEY


class UserModel(models.Model):
    user_Prog = models.AutoField(primary_key=True)
    user_Mail = models.CharField(max_length=50, unique=True)
    user_CountryCode = models.CharField(max_length=2)
    user_Language = models.CharField(max_length=2)
    user_PresenterID = models.IntegerField(default=0, blank=True, null=True)
    user_mailStatus = models.CharField(max_length=1, default='N')
    user_Status = models.IntegerField(null=True, blank=True)
    user_phonePrefix = models.CharField(max_length=7, blank=True, null=True)
    user_Language = models.CharField(max_length=2, blank=True, null=True)
    user_phoneNumber = models.CharField(max_length=15, blank=True, null=True)
    user_acceptTermsCondition = models.CharField(
        max_length=1, blank=True, default='N')
    user_acceptPrivacy = models.CharField(
        max_length=1, blank=True, default='N')
    user_acceptStatistics = models.CharField(
        max_length=1, blank=True, default='N')
    user_promoCode = models.CharField(max_length=10, blank=True, default='N')
    user_userID = models.CharField(blank=True, null=True, max_length=50)
    user_Type = models.CharField(max_length=2, blank=True, null=True)
    user_mail2 = models.CharField(max_length=50, blank=True, null=True)
    user_maildelegat = models.CharField(max_length=50, blank=True, null=True)
    user_phonenumber2 = models.IntegerField(
        null=True, blank=True)
    user_username = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'

    def __str__(self):
        return str(self.user_Mail)


class CountryModel(models.Model):
    country_countrycode = models.CharField(max_length=2)
    country_name = models.CharField(max_length=14)
    country_phoneprefix = models.CharField(max_length=4)

    class Meta:
        db_table = 'country'

    def __str__(self) -> str:
        return self.country_countrycode


class CommunityModel(models.Model):
    cmty_ownerid = models.IntegerField(default=0, blank=True, null=True)
    cmty_country = models.CharField(max_length=2)
    cmty_memberid = models.IntegerField(default=0, blank=True, null=True)
    cmty_cmtylevel = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    cmty_status = models.CharField(max_length=1, choices=[(
        'P', 'Pending'), ('A', 'Approved'), ('C', 'Cancelled')])
    cmty_insertdate = models.DateTimeField(auto_now_add=True)
    cmty_lastupdate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'community'

    def __str__(self) -> str:
        return str(self.cmty_ownerid)


class RewardsModel(models.Model):
    hrew_userid = models.IntegerField(
        default=0, blank=True, null=True)  # populate by hand
    hrew_period = models.CharField(max_length=7, null=True, blank=True)
    hrew_country = models.CharField(max_length=2, null=True, blank=True)
    hrew_friendscount = models.IntegerField(default=0, null=True, blank=True)
    hrew_cmtycount = models.IntegerField(default=0, null=True, blank=True)
    hrew_userrp = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True, default=0)
    hrew_cmtyrp = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True, default=0)
    hrew_userlevel = models.DecimalField(
        max_digits=2, decimal_places=0, null=True, blank=True, default=0)
    hrew_levelperc = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    hrew_userearn = models.DecimalField(
        max_digits=11, decimal_places=2, null=True, blank=True, default=0)
    hrew_cmtyearn = models.DecimalField(
        max_digits=11, decimal_places=2, null=True, blank=True, default=0)
    hrew_userwin = models.DecimalField(
        max_digits=11, decimal_places=2, null=True, blank=True, default=0)
    hrew_insertdate = models.DateTimeField(auto_now_add=True)
    hrew_lastupdate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'histrewpoints'


class Comlevel(models.Model):
    com_countryid = models.CharField(max_length=2)
    com_level = models.IntegerField()
    com_level_from = models.IntegerField(name='Comlevel_from')
    com_level_to = models.IntegerField(name='Comlevel_to')
    com_perc = models.DecimalField(
        max_digits=6, decimal_places=2, name='Comlevel_perc')

    class Meta:
        db_table = 'comlevel'


class ErrorCode(models.Model):
    error_id = models.AutoField(primary_key=True)
    error_code = models.IntegerField()
    error_message = models.TextField()
    error_language = models.CharField(max_length=2)

    class Meta:
        db_table = 'error_codes'

    def __str__(self):
        return f"{self.error_code}: {self.error_message} ({self.error_language})"
