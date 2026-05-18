from rest_framework import serializers
from .models import Contact, ContactLabel, ContactActivity, ContactSegment, ContactLabelAssignment


class ContactLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactLabel
        fields = ['id', 'name', 'description', 'color', 'created_at']
        read_only_fields = ['id', 'created_at']


class ContactActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactActivity
        fields = ['id', 'activity_type', 'title', 'description', 'metadata', 'created_at', 'created_by']
        read_only_fields = ['id', 'created_at']


class ContactSerializer(serializers.ModelSerializer):
    labels = ContactLabelSerializer(many=True, read_only=True)
    activities = ContactActivitySerializer(many=True, read_only=True)

    class Meta:
        model = Contact
        fields = ['id', 'email', 'phone', 'name', 'avatar', 'status', 'description',
                  'company', 'location', 'custom_attributes', 'labels', 'activities',
                  'last_activity', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ContactListSerializer(serializers.ModelSerializer):
    labels_count = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'phone', 'status', 'company', 'avatar',
                  'last_activity', 'labels_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_labels_count(self, obj):
        return obj.labels.count()


class ContactSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSegment
        fields = ['id', 'name', 'description', 'query', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
