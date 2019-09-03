from rest_framework import serializers
from ..db_models.banks import Bank
from ..db_models.branches import Branches


class BankSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Bank
        fields = ('__all__')


class BranchesReadSerializer(serializers.ModelSerializer):
    bank_id = BankSerializer(read_only=True)

    class Meta(object):
        model = Branches
        fields = '__all__'


class BranchesWriteSerializer(serializers.ModelSerializer):

    # bank = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta(object):
        model = Branches
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['bank'] = BankSerializer(instance.bank_id).data
        return response
