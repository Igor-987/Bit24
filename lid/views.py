from django.shortcuts import render
import requests
from dadata import Dadata


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """

    fio = request.GET.get('fio') # получаем данные из формы в HTML
    phone = request.GET.get('phone')
    adr = request.GET.get('adr')
    number1 = 0
    number2 = 0
    comp_id = 0
    cont_id = 0
    count_cont = 0
    contacts = 0
    cont_name = 0
    comp_name = 0

    if fio or phone or adr: # если заполнено хотябы одно поле
        if not fio:
            fio = ' '
        if not adr:
            adr = ' '
        token = "a47b1aee73b17dd7ba087adc76b6db067ca725e2" # стандартизируем ФИО и адрес через DADATA
        with open('secret_key.txt') as f:
            secret = f.read().strip()
        with Dadata(token, secret) as dadata:
            res_fio = dadata.clean(name="name", source=fio)
            name = res_fio['name']
            sname = res_fio['patronymic']
            lname = res_fio['surname']
            res_addr = dadata.clean(name="address", source=adr)
            addr = res_addr['result']

        # данные для фильтрации списка контактов
        filt = {}
        if name:
            filt["filter[NAME]"] = name
        if sname:
            filt["filter[SECOND_NAME]"] = sname
        if lname:
            filt["filter[LAST_NAME]"] = lname
        # получаем отфильтрованный список контактов
        list_cont = requests.post('https://b24-ordgbr.bitrix24.ru/rest/1/ehkb815cbixn3h64/crm.contact.list', data=filt)
        count_cont = list_cont.json()['total'] # всего контактов в списке
        contacts = list_cont.json()

        if count_cont == 1: # если найден всего один контакт
            cont_id = list_cont.json()['result'][0]['ID'] # получаем его id
            comp_id = list_cont.json()['result'][0]['COMPANY_ID']  # получаем id компании, к которой он прикреплен

            cont_n = requests.post('https://b24-ordgbr.bitrix24.ru/rest/1/ehkb815cbixn3h64/crm.contact.get', {'id': cont_id})
            cont_name = cont_n.json()['result']['NAME'] + ' ' + cont_n.json()['result']['LAST_NAME']

            if comp_id:
                load1 = {'FIELDS[CONTACT_ID]': cont_id,
                         'FIELDS[COMPANY_ID]': comp_id,
                         'FIELDS[PHONE][0][VALUE]': phone,
                         'FIELDS[ADDRESS]': addr,
                         }
                comp_n = requests.post('https://b24-ordgbr.bitrix24.ru/rest/1/ehkb815cbixn3h64/crm.company.get', {'id': comp_id})
                comp_name = '"' + comp_n.json()['result']['TITLE'] + '"'

            else:
                load1 = {'FIELDS[CONTACT_ID]': cont_id,
                         'FIELDS[PHONE][0][VALUE]': phone,
                         'FIELDS[ADDRESS]': addr,
                         }

            new_lid = requests.post('https://b24-ordgbr.bitrix24.ru/rest/1/ehkb815cbixn3h64/crm.lead.add.json', data=load1)
            number1 = new_lid.json()['result'] # номер лида, если он привязан к контакту


        else: # если найдено 0 контактов или несколько, загружаем лид без привязки к контакту
            load2 = {'FIELDS[NAME]': name,
                    'FIELDS[SECOND_NAME]': sname,
                    'FIELDS[LAST_NAME]': lname,
                    'FIELDS[PHONE][0][VALUE]': phone,
                    'FIELDS[ADDRESS]': addr,
                    }

            new_lid = requests.post('https://b24-ordgbr.bitrix24.ru/rest/1/ehkb815cbixn3h64/crm.lead.add.json', data=load2)
            number2 = new_lid.json()['result'] # номер лида, если он НЕ привязан к контакту

    return render(
        request,
        'index.html',
        context={'number1': number1, 'number2': number2, 'cont_name': cont_name, 'comp_name': comp_name, 'count_cont': count_cont}
    )
