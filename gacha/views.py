from django.shortcuts import render
from django.views.generic import TemplateView
from gacha.models import Characters
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
import random
import json
# Create your views here.
class gacha(TemplateView):
    template_name = 'gacha/gacha.html'

    def randomStar(self):
        selection = [5,4,3]
        probability = [0.03, 0.15, 0.82]
        star = random.choices(selection, probability)
        return star[0]

    '''def get_context_data(self, **kwargs):
        context = super(gacha, self).get_context_data(**kwargs)
        multi = []
        characters = []
        for x in range(5):
            star = self.randomStar()
            multi.append(star)

        for star in multi:
            character = Characters.objects.filter(stars=star).order_by('?')[:1]
            for obj in character:
                characters.append(obj)

        context['characters'] = characters
        context['multi'] = multi
        return context'''


class singlePull(TemplateView):
    template_name = 'gacha/singlepull.html'

    def randomStar(self):
        choice = [5,4,3]
        probability = [0.06, 0.2, 0.80]
        star = random.choices(choice, probability)
        return star


    def post(self, request):
        result = self.randomStar()
        for key in result:
            character = Characters.objects.filter(stars=key).order_by('?')[:1]
            for obj in character:
                name = obj.name
                stars = obj.stars
                series = obj.series
                image = obj.image
        return JsonResponse({'name': name, 'stars': stars, 'series': series, 'image': image}, safe=False)


class multiplePull(TemplateView):
    template_name = 'gacha/multiplePull.html'

    def randomStar(self):
        selection = [5,4,3]
        probability = [0.1, 0.2, 0.7]
        star = random.choices(selection, probability)
        return star[0]

    def post(self, request):
        multi = []
        characters = []
        for x in range(8):
            star = self.randomStar()
            multi.append(star)

        for star in multi:
            charData = {}
            character = Characters.objects.filter(stars=star).order_by('?')[:1]
            for obj in character:
                charData['name'] = obj.name
                charData['series'] = obj.series
                charData['image'] = obj.image
                charData['stars'] = obj.stars
            characters.append(charData)
        return JsonResponse(json.dumps(characters), safe=False)


#Script to add characters to DB
'''image = "no image"
characters = {
    "Auron": {'name': "Auron",
               'stars': 4,
               'image': image,
               'series': "FF10"},
    "Barret": {'name': "Barret",
               'stars': 3,
               'image': image,
               'series': "FF7"},
    "Fran":  {'name': "Fran",
               'stars': 3,
               'image': image,
               'series': "FF12"},
    "Noctis":  {'name': "Noctis",
               'stars': 5,
               'image': image,
               'series': "FF15"},
    "Orlandu":  {'name': "Orlandu",
               'stars': 4,
               'image': image,
               'series': "FFT"},
    "Ramza":  {'name': "Ramza",
               'stars': 5,
               'image': image,
               'series': "FFT"},
    "Rikku":  {'name': "Rikku",
               'stars': 3,
               'image': image,
               'series': "FF10"},
    "Sephiroth":  {'name': "Sephiroth",
               'stars': 4,
               'image': image,
               'series': "FF7"},
    "Terra":  {'name': "Terra",
               'stars': 5,
               'image': image,
               'series': "FF6"},
    "Tidus":  {'name': "Tidus",
               'stars': 5,
               'image': image,
               'series': "FF10"},
    "Tifa":  {'name': "Tifa",
               'stars': 4,
               'image': image,
               'series': "FF7"},
    "Vivi":  {'name': "Vivi",
               'stars': 3,
               'image': image,
               'series': "FF9"},
    "Wakka":  {'name': "Wakka",
               'stars': 3,
               'image': image,
               'series': "FF10"},
    "Yuffie":  {'name': "Yuffie",
               'stars': 3,
               'image': image,
               'series': "FF7"},
    "Zidane":  {'name': "Zidane",
               'stars': 5,
               'image': image,
               'series': "FF9"}
}
for key, value in characters.items():
    number = 3
    name = value['name']
    stars = value['stars']
    image = value['image']
    series = value['series']
    Characters.objects.create(id=number,name=name,stars=stars,image=image,series=series)
    number += 1
'''
