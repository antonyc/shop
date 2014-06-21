from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response


class PaginatedView(GenericAPIView):
    def get_paginate_by(self, queryset=None):
        pass


class AppView(APIView):
    def handle_exception(self, exc):
        print(exc)
        return Response({
            'error': 'unhandled exception',
            'message': repr(exc),
        })
