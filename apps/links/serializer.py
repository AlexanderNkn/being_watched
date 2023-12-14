from datetime import datetime

from rest_framework import serializers


class VisitedLinkSerializer(serializers.Serializer):
    links = serializers.ListSerializer(
        child=serializers.URLField(),
    )


class DateTimeFromTimestampField(serializers.IntegerField):
    def to_internal_value(self, value):
        timestamp = super().to_internal_value(value)
        try:
            return datetime.fromtimestamp(float(timestamp))
        except ValueError as error:
            raise serializers.ValidationError(error)


class TimeStampSerializer(serializers.Serializer):
    date = DateTimeFromTimestampField()
