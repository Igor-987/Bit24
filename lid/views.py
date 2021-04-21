from django.shortcuts import render
import requests
from dadata import Dadata


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """

    fio = request.GET.get('fio')
    phone = request.GET.get('phone')
    adr = request.GET.get('adr')
    number = 0

    if fio or phone or adr:
        if not fio:
            fio = ' '
        if not adr:
            adr = ' '
        token = "a47b1aee73b17dd7ba087adc76b6db067ca725e2"
        with open('secret_key.txt') as f:
            secret = f.read().strip()
        with Dadata(token, secret) as dadata:
            res_fio = dadata.clean(name="name", source=fio)
            name = res_fio['name']
            sname = res_fio['patronymic']
            lname = res_fio['surname']
            res_addr = dadata.clean(name="address", source=adr)
            addr = res_addr['result']

        load = {'FIELDS[NAME]': name,
                'FIELDS[SECOND_NAME]': sname,
                'FIELDS[LAST_NAME]': lname,
                'FIELDS[PHONE][0][VALUE]': phone,
                'FIELDS[ADDRESS]': addr,
                }

        r = requests.post('https://b24-ordgbr.bitrix24.ru/rest/1/ehkb815cbixn3h64/crm.lead.add.json', data=load)
        number = r.json()['result']



    return render(
        request,
        'index.html',
        context={'r': number},
    )
