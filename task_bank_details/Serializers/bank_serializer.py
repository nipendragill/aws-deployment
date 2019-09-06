from rest_framework import serializers
from ..db_models.banks import Bank
from ..db_models.branches import Branches


class BankSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Bank
        fields = ('__all__')

    def create(self, validated_data):
        validated_data['name'] = validated_data.get('name').strip().upper()
        bank = Bank.objects.create(**validated_data)
        return bank


class BranchesReadSerializer(serializers.ModelSerializer):
    bank = BankSerializer(read_only=True)

    class Meta(object):
        model = Branches
        fields = '__all__'


class BranchesWriteSerializer(serializers.ModelSerializer):

    # bank = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta(object):
        model = Branches
        fields = ('__all__')

    def create(self, validated_data):
        validated_data['city'] = validated_data.get('city').strip().upper()
        branches_detail = Branches.objects.create(**validated_data)
        return branches_detail

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['bank'] = BankSerializer(instance.bank).data
        return response
