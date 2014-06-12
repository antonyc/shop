from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView


class PaginatedView(GenericAPIView):
    def get_paginate_by(self, queryset=None):
        pass
