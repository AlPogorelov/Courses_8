from rest_framework import serializers
from django.core.exceptions import ValidationError

from habit.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        try:
            instance = Habit(**data)
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return data
