# coding: utf-8

import os
from datetime import datetime

from rest_framework.views import APIView, Response
from django.core.files.storage import FileSystemStorage

from .models import Pet, Image
from .serializers import PetCreationSerializer, ImagePath, PetSerializer


class PetsView(APIView):
    def get(self, request, id):
        """
        Get single pet.

        $ curl http://127.0.0.1:8000/api/v1/pets/53994ea5412d96961fc85e53
        """
        return Response(
            PetSerializer(Pet.objects.get(id=id), many=False).data
        )


class PetsListView(APIView):

    def get(self, request):
        """
        List pets

        > curl -v http://127.0.0.1:8000/api/v1/pets/

        < HTTP/1.0 200 OK
        < Content-Type: application/json
        < X-Frame-Options: SAMEORIGIN
        < x-next: 5399385f412d968e56078024
        < Allow: GET, POST, HEAD, OPTIONS

        [
            {
            "self": "/api/v1/pets/5399385f412d968e56078024/",
            "id": "5399385f412d968e56078024",
            "images": [],
            "user_description": null,
            "breed_by_user": "1",
            "created_at": "2014-06-12T05:19:27.288"}
        ]

        You get X-Next to paginate from previous request. If no "X-Next" in response,
        no more pages.

        curl -H"X-Next: 5399433e412d969239ee17a5" \
        http://127.0.0.1:8000/api/v1/pets/

        """
        # last element seen on previous page
        last_seen_element = request.META.get('HTTP_X_NEXT')
        page_size = 1  # how many on page
        qs = Pet.objects.order_by('id').limit(page_size + 1)
        if last_seen_element:
            qs = qs.filter(id__gt=last_seen_element)
        pets = list(qs)
        headers = {}
        if len(pets) > page_size:
            # got more to paginate
            pets.pop()
            headers['x-next'] = str(pets[-1].id)
        return Response(PetSerializer(pets).data, headers=headers)

    def _images(self, images_paths):
        """

        :type images_paths: list
        :rtype: list
        """
        return (
            Image(path=path_to_image)
            for path_to_image in images_paths
        )

    def post(self, request):
        """
        Create a record about a pet.

        $ curl -XPOST \
        -H"Content-Type: application/json" \
        -d'{"breed_by_user": 1, "position": {"lat": 10, "lon": "10"}, "phone_number": "12", "user_description": ""}' \
        http://127.0.0.1:8000/api/v1/pets/

        {
            "self": "/api/v1/pets/53994ea5412d96961fc85e53/",
            "id": "53994ea5412d96961fc85e53",
            "images": [],
            "user_description": "",
            "breed_by_user": "1",
            "created_at": "2014-06-12T06:54:29.372"
        }
        """
        data = request.DATA
        if 'images' in data:
            data['images'] = self._images(data['images'])
        serializer = PetCreationSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        pet_data = serializer.data
        pet_data['created_at'] = datetime.now()
        pet_data['position'] = (
            pet_data['position']['lat'], pet_data['position']['lon']
        )
        pet = Pet(**pet_data)
        pet.save()
        try:
            return Response(PetSerializer(pet, many=False).data)
        except:
            import traceback
            traceback.format_exc()


class ImageUploadView(APIView):
    def post(self, request):
        """
        Upload single image to yandex disk.
        """
        filename = list(request.FILES.keys())[0]
        uploaded_file = request.FILES[filename]
        result = FileSystemStorage().save(uploaded_file.name, uploaded_file)
        return Response(ImagePath({'path': 'file/1/' + result}).data)
