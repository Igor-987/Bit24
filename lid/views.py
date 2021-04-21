from django.shortcuts import render
import requests
from dadata import Dadata


# Create your views here.
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """

    name = request.GET.get('fio')
    # sname = request.GET.get('fio')
    # lname = request.GET.get('fio')
    phone = request.GET.get('phone')
    addr = request.GET.get('adr')

    token = "a47b1aee73b17dd7ba087adc76b6db067ca725e2"
    secret = "0df1d0a5d779dfb9e16ca9beeeec1844053f0cad"
    dadata = Dadata(token, secret)
    result = dadata.clean("name", name)

    name = result[name]
    sname = result[patronymic]
    lname = result[surname]



    load = {'FIELDS[NAME]': name,
            'FIELDS[SECOND_NAME]': sname,
            'FIELDS[LAST_NAME]': lname,
            'FIELDS[PHONE][0][VALUE]': phone,
            'FIELDS[ADDRESS]': addr,
            }

    r = requests.post('https://b24-ordgbr.bitrix24.ru/rest/1/ehkb815cbixn3h64/crm.lead.add.json', data=load)
    return render(
        request,
        'index.html',
    )