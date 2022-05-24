from rest_framework import serializers


class ResultSerializer(serializers.Serializer):
    exam = serializers.CharField(max_length=100, required=True)
    board = serializers.CharField(max_length=100, required=True)
    year = serializers.CharField(max_length=100, required=True)
    roll = serializers.CharField(max_length=100, required=True)
    reg = serializers.CharField(max_length=100, required=True)
