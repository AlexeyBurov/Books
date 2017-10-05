import datetime

from django.core import serializers
from django.db import models


# Create your models here.
class MaterialColor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def to_json(self):
        return dict(id=self.id, name=self.name)


class MaterialGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    default_price = models.FloatField(null=False, default=0.0)
    colors = models.ManyToManyField(MaterialColor, default=None)

    def to_json(self):
        return dict(id=self.id, name=self.name, default_price=self.default_price,
                    colors=serializers.serialize('json', self.colors.all()))


class Celling(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    celling_width = models.IntegerField()
    price = models.BigIntegerField(default=0)
    material_group = models.ForeignKey(MaterialGroup)
    for_remove = models.BooleanField(null=False, default=False)
    count_meters_pagon = models.FloatField(null=False, default=0.0)

    def __str__(self):
        return str(self.id) + '_' + self.name + '_' + str(self.celling_width)

    def to_json(self):
        return dict(
            id=self.id,
            name=self.name,
            celling_width=self.celling_width,
            price=self.price,
            material_group=self.material_group.to_json(),
            count_meters_pagon=self.count_meters_pagon,
            for_remove=self.for_remove
        )


class Dealer(models.Model):
    id = models.AutoField(primary_key=True)
    dealer_name = models.CharField(max_length=100)
    dealer_phone = models.CharField(max_length=13, unique=True)
    dealer_email = models.CharField(max_length=150, null=False, unique=True)
    dealer_firm_name = models.CharField(max_length=100, null=True)
    dealer_address = models.CharField(max_length=100, null=True)
    dealer_unp = models.CharField(max_length=9, null=True)
    dealer_amount = models.FloatField(default=0.0)
    user_id = models.BigIntegerField(unique=False)
    max_deposit = models.FloatField(null=False, default=500.0)
    for_remove = models.BooleanField(null=False, default=False)

    def __str__(self):
        return str(self.dealer_name) + '_' + str(self.dealer_phone)

    def to_json(self):
        return dict(
            id=self.id,
            dealer_name=self.dealer_name,
            dealer_phone=self.dealer_phone,
            dealer_email=self.dealer_email,
            dealer_firm_name=self.dealer_firm_name,
            dealer_address=self.dealer_address,
            dealer_unp=self.dealer_unp,
            max_depozit=self.max_deposit,
            dealer_amount=self.dealer_amount,
            user_id=self.user_id,
            for_remove=self.for_remove
        )


class Balance(models.Model):
    id = models.AutoField(primary_key=True)
    dealer = models.ForeignKey(Dealer, null=False)
    count = models.FloatField(null=False, default=0.0)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    celling = models.ForeignKey(Celling, null=True)
    material_group = models.ForeignKey(MaterialGroup, null=True)
    dealer_obj = models.ForeignKey(Dealer, default=None, null=True)
    s_celling = models.FloatField(null=True)
    p_celling = models.FloatField(null=True)
    p_garpun = models.FloatField(null=True)
    p_curve = models.FloatField(null=True)
    material_long = models.FloatField(null=True, default=0.0)
    celling_price = models.FloatField(null=True)
    order_status = models.IntegerField(null=False, default=1)
    order_date = models.DateField(default=datetime.datetime.now, blank=False)
    for_remove = models.BooleanField(null=False, default=False)

    def to_json(self):
        result = dict(
            id=self.id,
            s_celling=self.s_celling,
            p_celling=self.p_celling,
            p_garpun=self.p_garpun,
            p_curve=self.p_curve,
            material_long=self.material_long,
            celling_price=self.celling_price,
            order_status=self.order_status,
            order_date=str(self.order_date),
            for_remove=self.for_remove
        )
        if self.dealer_obj is not None:
            result['dealer'] = self.dealer_obj.to_json()
        else:
            result['dealer'] = {'dealer_firm_name': 'None'}
        if self.celling is not None:
            result['celling'] = self.celling.to_json()
        else:
            result['celling'] = {'name': 'None'}
        return result


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    dealer = models.ForeignKey(Dealer, null=True)
    sum = models.FloatField(null=False, default=0.0)

    def to_json(self):
        return dict(
            id=self.id,
            dealer=self.dealer.to_json(),
            sum=self.sum
        )


class MaterialDealerPrice(models.Model):
    id = models.AutoField(primary_key=True)
    dealer_id = models.BigIntegerField(null=False)
    material_id = models.BigIntegerField(null=False)
    discount = models.FloatField(null=True, default=0.0)

    def to_json(self):
        return dict(id=self.id,
                    dealer_id=self.dealer_id,
                    material_id=self.material_id,
                    discount=self.discount)


class Setting(models.Model):
    id = models.AutoField(primary_key=True)
    property_name = models.CharField(null=False, max_length=256)
    property_value = models.CharField(null=False, max_length=256)
