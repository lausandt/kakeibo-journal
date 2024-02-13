"""
Class containing the models which will be used by Tortoise and Aerich to create the database tables
& by pandatic to create the schemas.

The use of the Meta classes allows us to name that tables seperately from the model class names, 
allowing those to change while keeping the schemas intact.
"""
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Any

from tortoise import fields, models


class Interval(str, Enum):
    Weekly: str = 'Weekly'
    Monthly: str = 'Monthly'
    Yearly: str = 'Yearly'


class Qualification(str, Enum):
    Need: str = 'Need'
    Want: str = 'Want'
    Leisure: str = 'Leasure'
    Unexpected: str = 'Unexpected'


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    full_name = fields.CharField(max_length=50, null=False)
    password = fields.CharField(max_length=128, null=False)
    active = fields.BooleanField(default=True)
    superuser = fields.BooleanField(default=False)

    def __str__(self):
        return f'user: {self.username}'

    class Meta:
        table = 'users'


class Period(models.Model):
    id = fields.IntField(pk=True)
    nr = fields.IntField(pk=False, unique=True)
    start_date: date = fields.DateField(unique=True)
    end_date: date = fields.DateField(unique=True)

    class Meta:
        table = 'periods'


class Entry(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=225)
    amount: Decimal = fields.DecimalField(max_digits=10, decimal_places=2)
    supplier = fields.CharField(max_length=225)
    qualification: Qualification = fields.CharEnumField(
        Qualification, default=Qualification.Want
    )
    note = fields.TextField()
    author: User = fields.ForeignKeyField('models.User', related_name='entries')
    created_at: date = fields.DateField()

    def __str__(self) -> str:
        return f'{self.title} {self.author.id} {self.created_at}'

    class Meta:
        table = 'variable_entries'


class FixedEntry(Entry):
    title = fields.CharField(max_length=225, unique=True)
    author: User = fields.ForeignKeyField('models.User', related_name='fixeds')
    qualification: Qualification = fields.CharEnumField(
        Qualification, default=Qualification.Need
    )
    interval: Interval = fields.CharEnumField(Interval, default=Interval.Monthly)

    def __str__(self) -> str:
        return f'{self.title} {self.author.id} {self.created_at}'

    class Meta:
        table = 'fixed_entries'


class Budget(models.Model):
    id = fields.IntField(pk=True)
    amount: Decimal = fields.DecimalField(max_digits=10, decimal_places=2)
    created_at: date = fields.DateField()
    source_one: Any = fields.CharField(max_length=225, unique=True)
    source_two: Any = fields.CharField(max_length=225, unique=True)
    source_three: Any = fields.CharField(max_length=225, unique=True)


class SavingsGoal(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=225)
    amount: Decimal = fields.DecimalField(max_digits=10, decimal_places=2)
    description = fields.TextField()
    active = fields.BooleanField
    author: User = fields.ForeignKeyField('models.User', related_name='savings_goal')
