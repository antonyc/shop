# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
import administration
import os
from django.test import TestCase
from pages.models import Page, PageImage
from django.contrib.auth.models import User

add_url = '/administration/pages/%d/images/add/'


class PageImageDeleteTest(TestCase):
    fixtures = ['categories.json']
    def setUp(self):
        self.user = User.objects.create_superuser('chapson', 'mrdark@list.ru', '1')
        self.page = Page(title="a page",
             body="",
             url="a-cosmic-ship",
             author=self.user)
        self.page.save()
        self.file_path = os.path.join(os.path.dirname(administration.__file__), 'fixtures')
        self.user1 = User.objects.create_superuser('zver', 'anton@list.ru', '1')
        self.client.login(username='chapson', password='1')

    def test_delete(self):
        # upload
        fp = open(os.path.join(self.file_path, '1.jpg'))
        images = PageImage.objects.filter(page=self.page)
        before_images = images.count()
        alt = u'Мишка на севере'
        post = {'image': fp, 'alt': alt,}
        result = self.client.post(add_url % self.page.id, post)
        self.assertEqual(before_images, images.count() - 1, "Must have added")
        fp.close()
        before_images = images.count()
        response = self.client.post(reverse('delete_page_image', args=(images[0].id,)))
        self.assertEqual(before_images, images.count() + 1, "Must have deleted")
        self.assertEqual(response.status_code, 302)