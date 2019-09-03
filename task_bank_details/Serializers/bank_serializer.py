from rest_framework import serializers
from ..db_models.banks import Bank
from ..db_models.branches import Branches


class BankSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Bank
        fields = ('id', 'bank_name')


class BankDetailsReadSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Branches
        fields = '__all__'