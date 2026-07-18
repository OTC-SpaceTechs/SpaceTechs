from rest_framework import serializers

from .models import Component, Document, Project, Tip


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'project', 'title', 'image', 'created_at', 'file', 'content', 'doc_type']


class TipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = ['id', 'project', 'title', 'image', 'created_at', 'question', 'short_answer', 'content', 'category']


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ['id', 'project', 'name', 'quantity', 'cost', 'supplier', 'notes']


class ProjectSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    tips = TipSerializer(many=True, read_only=True)
    components = ComponentSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'status', 'start_date', 'documents', 'tips', 'components']
