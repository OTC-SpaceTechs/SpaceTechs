from rest_framework import serializers

from .models import Document, Project, Tip


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'project', 'title', 'image', 'created_at', 'file', 'content', 'doc_type']


class TipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = ['id', 'project', 'title', 'image', 'created_at', 'question', 'short_answer', 'content', 'category']


class ProjectSerializer(serializers.ModelSerializer):
    """Public showcase representation — full docs/tips live behind their own officer-only endpoints."""

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'status', 'start_date']
