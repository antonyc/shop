# coding: utf-8

import random
import hashlib
from urllib.parse import quote
from datetime import datetime

import requests
from rest_framework.views import APIView, Response
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from .models import Pet, Image
from .serializers import PetCreationSerializer, ImagePath, PetSerializer
from pets_core.views import AppView


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


class ImageUploadView(AppView):
    def post(self, request):
        """
        Upload single image to yandex disk.
        """
        filename = list(request.FILES.keys())[0]
        uploaded_file = request.FILES[filename]
        fileid = upload_to_yadisk(uploaded_file)
        return Response(ImagePath({'path': fileid}).data)


class YaDiskUnexpectedError(Exception):
    pass


def check_folder_exists(folder_name):
    url = 'https://cloud-api.yandex.net/v1/disk/resources?path={0}'.format(
        quote(folder_name, safe='')
    )
    response = requests.get(url, timeout=3, headers=dict(
        Authorization='OAuth ' + settings.YADISK_API_TOKEN
    ))
    if response.status_code == 404:
        return False
    elif response.status_code == 200:
        return True
    else:
        raise YaDiskUnexpectedError('not ready for such status code', response.status_code)


def create_folder(folder_name):
    url = 'https://cloud-api.yandex.net/v1/disk/resources/?path={0}'.format(
        quote(folder_name, safe='')
    )
    response = requests.put(url, timeout=3, headers=dict(
        Authorization='OAuth ' + settings.YADISK_API_TOKEN
    ))
    if response.status_code != 201:
        raise YaDiskUnexpectedError('Not created folder', response.status_code)


def ensure_folder_exists(folder_name):
    parts = folder_name.strip('/').split('/')
    for i in range(len(parts)):
        name = '/' + '/'.join(parts[:i + 1])
        if not check_folder_exists(name):
            create_folder(name)


def upload_to_yadisk(uploaded_file):
    folder = '/pets/photos/'
    # TODO: do this only once
    # ensure_folder_exists(folder)
    # 40 is because YaDisk has limit on file length (I don't know exact value)
    file_id = '{filename}_{date_uploaded}_{seed}'.format(
        filename=uploaded_file.name,
        date_uploaded=str(datetime.now().isoformat()),
        seed=str(random.randint(1000, 9999)),
    )[:40]
    url = (
        'https://cloud-api.yandex.net/v1/disk/'
        'resources/upload?path={0}&overwrite=true'
    ).format(quote(folder + 'sample'))
    response = requests.get(url, timeout=3, headers=dict(
        Authorization='OAuth ' + settings.YADISK_API_TOKEN
    ))
    if response.status_code != 200:
        raise YaDiskUnexpectedError('failed to upload to YaDisk', response.status_code)
    url = response.json()['href']
    # тут имя файла некорректное
    response = requests.put(url, timeout=10, files={
        'file': (file_id, uploaded_file.file),
    }, headers={
        'Content-Type': 'application/octet-stream'
    })
    if response.status_code != 201:
        raise YaDiskUnexpectedError('failed to upload to YaDisk', response.status_code)
    return folder + file_id
