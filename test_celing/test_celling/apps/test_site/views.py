import datetime
import json

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView

from test_celling.apps.test_site.models import Celling, MaterialDealerPrice, Payment, MaterialGroup, MaterialColor, \
    Balance
from test_celling.apps.test_site.models import Dealer
from test_celling.apps.test_site.models import Order


# Create your views here.

def group_required(*group_names):
    def in_groups(user):
        if user.is_authenticated():
            if user.is_superuser or bool(user.groups.filter(name__in=group_names)):
                return True
        return False

    return user_passes_test(in_groups, login_url='./login')


@group_required('manager', 'dealer')
def index(request):
    if request.user.is_authenticated:

        context = {

        }
        return render(request, 'index.html', context=context)
    else:
        return HttpResponseRedirect("./login")


@group_required('manager', 'dealer')
def orders(request):
    if request.user.is_authenticated:
        context = {}
        return render(request, 'orders.html', context=context)
    else:
        return HttpResponseRedirect('./login')


@group_required('manager')
def dealers(request):
    if request.user.is_authenticated:
        context = {}
        return render(request, 'dealers.html', context=context)
    else:
        return HttpResponseRedirect('./login')


@group_required('manager')
def finance(request):
    if request.user.is_authenticated:
        context = {}
        return render(request, 'finance.html', context=context)
    else:
        return HttpResponseRedirect('./login')


@group_required('admin')
def settings(request):
    if request.user.is_authenticated:
        context = {}
        return render(request, 'settings.html', context=context)
    else:
        return HttpResponseRedirect('./login')


def file_upload_template(request):
    if request.user.is_authenticated:
        context = {}
        return render(request, 'file_upload.html', context=context)
    else:
        return HttpResponseRedirect('./login')


@group_required('manager')
def add_dealer_form(request):
    if request.user.is_authenticated:
        context = {}
        return render(request, 'dealer_add.html', context=context)
    else:
        return HttpResponseRedirect('./login')


@group_required('manager')
def add_dealer(request):
    if request.method == 'POST':
        dealer_name = request.POST.get('dealer_name')
        dealer_email = request.POST.get('dealer_email')
        dealer_phone = request.POST.get('dealer_phone')
        dealer_address = request.POST.get('dealer_address')
        dealer_firm_name = request.POST.get('dealer_firm_name')
        dealer_unp = request.POST.get('dealer_unp')
        dealer_max_deposit = request.POST.get('max_deposit').replace(',', '.')
        password_for_dealer = request.POST.get('dealer_password')
        group = Group.objects.get(name='dealer')
        user = User.objects.create_user(username=dealer_email, email=dealer_email, password=password_for_dealer)
        user.save()
        group.user_set.add(user)
        user.groups.add(group)
        dealer_model = Dealer(
            dealer_name=dealer_name,
            dealer_phone=dealer_phone,
            dealer_email=dealer_email,
            dealer_address=dealer_address,
            dealer_firm_name=dealer_firm_name,
            max_deposit=dealer_max_deposit,
            dealer_unp=dealer_unp,
            user_id=user.id
        )
        return HttpResponse(dealer_model.save())
    else:
        return HttpResponse(status=405)


@group_required('manager')
def add_celling_material(request):
    if request.method == 'POST':
        material_group = MaterialGroup.objects.get(request.POST.get('material_group'))
        celling_name = request.POST.get('celling_name')
        celling_count = request.POST.get('material_count')
        celling_width = request.POST.get('celling_width')
        celling_model = Celling(name=celling_name, material_group=material_group, celling_width=celling_width,
                                count_meters_pagon=celling_count)
        result = celling_model.save()
        return HttpResponse(result)
    else:
        return HttpResponse(status=405)


@group_required('manager', 'dealer')
def save_file(request):
    file_content = ''
    content = {}
    for chunk in request.FILES['file'].chunks():
        file_content += chunk.decode('utf-16')
    lines = file_content.split('\n')
    list_length = len(lines)
    s_celling = float(lines[list_length - 7])
    p_celling = float(lines[list_length - 6])
    p_garpun = float(lines[list_length - 5])
    p_curves = float(lines[list_length - 2])
    material_name = lines[35]
    material_width = lines[36]

    client_name = lines[13]
    client_address = lines[14]
    client_phone = lines[15]
    order = Order(s_celling=s_celling, p_celling=p_celling, p_garpun=p_garpun, p_curve=p_curves, celling_id=1)
    dealers_list = Dealer.objects.all()
    dealer = None
    if dealers_list.filter(user_id=request.user.pk):
        dealer = dealers_list.get(user_id=request.user.pk)
    celling = Celling.objects.exclude(name=material_name, celling_width=material_width)
    if len(celling) > 0:
        content['material'] = celling
    content['materials'] = Celling.objects.all()
    content['material_group'] = list(MaterialGroup.objects.all())
    content['order'] = order
    if bool(dealer) > 0:
        content['dealer'] = dealer
        content['discount'] = MaterialDealerPrice.objects.filter(dealer_id=dealer.id)
    content['dealers'] = dealers_list
    content['dialer'] = Dealer(dealer_name=client_name, dealer_address=client_address, dealer_phone=client_phone)

    return render(request, 'add_order_template.html', context=content)


@group_required('manager')
def materials_list_tmpl(request):
    return render(request, 'materials_list.html', context={})


@group_required('manager')
def materials_group_tmpl(request):
    return render(request, 'materials_group.html', context={})


@group_required('manager')
def add_material_color(request):
    return render(request, 'add_color.html', context={})


@group_required('manager')
def colors_list_tmpl(request):
    return render(request, 'colors_list.html', context={})


@group_required('manager', 'dealer')
def add_order(request):
    if request.method == 'POST':
        dealer = None
        celling = None
        try:
            material_id = request.POST.get('material_id')
            dealer_id = request.POST.get('dealer_id')
            celling = Celling.objects.get(id=material_id)
            dealer = Dealer.objects.get(id=dealer_id)
        except Exception:
            pass
        celling_s = float(request.POST.get('celling_s').replace(',', '.'))
        celling_p = float(request.POST.get('celling_p').replace(',', '.'))
        garpun_p = float(request.POST.get('garpun_p').replace(',', '.'))
        p_curve = float(request.POST.get('p_curve').replace(',', '.'))
        material_group_id = request.POST.get('material_group')
        material_group = MaterialGroup.objects.get(id=material_group_id)
        s_material = float(request.POST.get('s_material').replace(',', '.'))
        material_long_m = 0.0
        if  bool(request.user.groups.filter(name__in='dealer')):
            material_long_m = float(request.POST.get('material_long_m').replace(',', '.'))
        balance_model = None
        balance = 0.0
        order_price = 0.0
        celling_price = 0.0
        if celling is not None:
            balance = float(celling.celling_width * material_long_m - s_material)
            celling_price = material_group.default_price * celling_s
            order_price = celling_s * material_group.default_price
        if dealer is not None:
            dealer.dealer_amount -= order_price
            dealer.save()
            balance_model = Balance(dealer=dealer, count=balance)
            balance_model.save()

        order_model = Order(celling=celling,
                            dealer_obj=dealer,
                            s_celling=celling_s,
                            p_celling=celling_p,
                            p_garpun=garpun_p,
                            p_curve=p_curve,
                            material_long=material_long_m,
                            material_group=material_group,
                            celling_price=celling_price
                            )
        order_model.save()
        return HttpResponse('{"error":false,"Заказ добавлен"}')

    else:
        return HttpResponse(status=405)


@group_required('manager')
def get_dealers(request):
    if request.user.is_authenticated:
        for_map = []
        for dealer in Dealer.objects.all():
            for_map.append(dealer.to_json())
        return HttpResponse(json.dumps({'data': for_map}), content_type='application/json')
    else:
        return HttpResponseRedirect('./login')


class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        user = form.save()
        group = Group.objects.get(name='manager')
        group.user_set.add(user)
        user.groups.add(group)

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("./")


@group_required('manager')
def dealer_info(request):
    dealer_id = request.GET.get('dealer_id')
    if dealer_id is not None:
        dealer = Dealer.objects.get(id=dealer_id)
        orders_tab = Order.objects.filter(dealer_obj=dealer)
        orders_res = list()
        for order in orders_tab:
            orders_res.append(order.to_json())
        return HttpResponse(json.dumps({'dealer': json.dumps(dealer.to_json()), 'orders': orders_res}),
                            content_type="application/json")
    else:
        return HttpResponse(status=403, body='Bad request')


@group_required('manager', 'dealer')
def get_orders(request):
    dealer_id = request.GET.get('dealer_id')
    if (not bool(Dealer.objects.filter(id=dealer_id))) and bool(request.user.groups.filter(name__in='dealer')):
        return HttpResponse(status=403)
    dealers = list(Dealer.objects.all())
    orders = None
    orders_res = list()

    if dealer_id is not None:
        dealer = Dealer.objects.get(user_id=dealer_id)
        orders = Order.objects.filter(dealer_obj=dealer)
        for order in orders:
            orders_res.append(order.to_json())
    else:
        orders = Order.objects.all()
        for order in orders:
            orders_res.append(order.to_json())

    return HttpResponse(json.dumps({'data': orders_res}))


@group_required('manager')
def dealer_add_payment(request):
    dealer = Dealer.objects.get(id=request.POST.get('dealer_id'))
    payment = Payment(dealer=dealer, sum=request.POST.get('payment_sum'))
    payment.save()
    dealer.dealer_amount += float(payment.sum)
    dealer.save()
    return HttpResponse(payment)


@group_required('manager', 'dealer')
def get_available_colors(request):
    material_group_id = request.GET.get('material_group_id')
    material_group = MaterialGroup.objects.get(id=material_group_id)
    materials_res = Celling.objects.filter(material_group=material_group)
    materials = list()
    for material in materials_res:
        materials.append(material.to_json())
    return HttpResponse(json.dumps({'material_group': material_group.to_json(), 'materials': materials}))


@group_required('manager')
def expense_page(request):
    return render(request, 'material_expense.html', context={})


@group_required('manager')
def materials_json(request):
    materials = Celling.objects.all()
    materials_result = list()


@group_required('manager')
def materials_expense(request):
    materials = Celling.objects.all()
    materials_res = dict()
    for material in materials:
        materials_res[material.id] = {
            'material_id': material.id,
            'material_name': material.material_group.name + ' ' + material.name + ' ' + str(material.celling_width),
            'material_expense': 0.0,
            'material_count': material.count_meters_pagon
        }

    orders_l = list(Order.objects.filter(order_status=3))
    for order in orders_l:
        materials_res[order.celling.id]['material_expense'] += order.material_long
        materials_res[order.celling.id]['material_count'] -= order.material_long
    return HttpResponse(json.dumps({'data': list(materials_res.values())}), content_type='application/json')


@group_required('manager')
def add_material_tmpl(request):
    materials_group = MaterialGroup.objects.all()
    return render(request, 'add_material.html', context={'material_groups': materials_group})


@group_required('manager')
def add_material_group_tmpl(request):
    colors = MaterialColor.objects.all()
    context = {'colors': colors}
    return render(request, 'material_group_add.html', context=context)


@group_required('manager')
def add_material_api(request):
    name = request.POST.get('color_name')
    material_color = MaterialColor(name=name)
    return HttpResponse(material_color.save())


@group_required('manager')
def get_colors_table(request):
    colors_set = MaterialColor.objects.all()
    colors = list()
    for color in colors_set:
        colors.append(color.to_json())
    return HttpResponse(json.dumps({'data': colors}))


@group_required('manager')
def groups_json(request):
    groups_rez = MaterialGroup.objects.all()
    groups = list()
    for group in groups_rez:
        groups.append(group.to_json())
    return HttpResponse(json.dumps({'data': groups}))


@group_required('manager')
def delete_dealer(request):
    dealer_id = request.POST.get('dealer_id')
    dealer = Dealer.objects.get(id=dealer_id)
    if request.user.groups.filter(name='manager').exists():
        dealer.for_remove = True
        return HttpResponse(dealer.save())
    else:
        return HttpResponse(dealer.delete())


@group_required('manager')
def add_material_api(request):
    material_group_id = request.POST.get('material_group')
    material_group = MaterialGroup.objects.get(id=material_group_id)
    material_name = request.POST.get('celling_name')
    material_width = request.POST.get('celling_width')
    material_count = request.POST.get('material_count')
    material_model = Celling(
        material_group=material_group,
        name=material_name,
        celling_width=material_width,
        count_meters_pagon=material_count
    )
    return HttpResponse(material_model.save())


@group_required('manager')
def finance_orders(request):
    date_str = request.GET.get('date')
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    orders_res = Order.objects.filter(order_date__year=date.year, order_date__month=date.month,
                                      order_date__day=date.day)
    count_orders = orders_res.count()
    orders_map = list()
    sum_orders = 0.0
    celling_s = 0.0
    p_garpun = 0.0
    for order in orders_res:
        sum_orders += order.celling_price
        celling_s += order.s_celling
        p_garpun += order.p_garpun
        orders_map.append(order.to_json())
    return HttpResponse(json.dumps({
        'count_orders': count_orders,
        'sum_orders': sum_orders,
        'p_garpun': p_garpun,
        'celling_s': celling_s,
        'orders': json.dumps(orders_map)
    }))


@group_required('manager')
def add_color_api(request):
    color_code = request.POST.get('color_name')
    color_model = MaterialColor(name=color_code)
    color_model.save()
    return HttpResponse(json.dumps({'error': 'false'}))


@group_required('manager')
def add_material_group_api(request):
    colors = request.POST.getlist('colors')
    colors_res = MaterialColor.objects.filter(id__in=colors)
    group_name = request.POST.get('material_group_name')
    default_price = request.POST.get('default_price')
    group_model = MaterialGroup(name=group_name, default_price=default_price)
    group_model.save()
    group_model.colors = colors_res

    return HttpResponse(json.dumps(group_model.to_json()))


@group_required('manager')
def get_materials_json(request):
    materials = list(Celling.objects.all())
    materials_res = list(map(lambda material: material.to_json(), materials))
    return HttpResponse(json.dumps({'data': materials_res}))


@group_required('manager')
def dealer_edit_api(request):
    dealer_id = request.POST.get('dealer_id')
    dealer_name = request.POST.get('dealer_name')
    dealer_phone = request.POST.get('dealer_phone')
    dealer_email = request.POST.get('dealer_email')
    dealer_address = request.POST.get('dealer_address')
    dealer_firm_name = request.POST.get('dealer_firm')
    dealer_unp = request.POST.get('dealer_unp')
    dealer_amount = request.POST.get('dealer_amount')
    dealer_max_deposit = request.POST.get('dealer_max_depozit')
    for_remove = request.POST.get('for_remove')
    if for_remove == 'on':
        for_remove = True
    else:
        for_remove = False
    dealer_model = Dealer.objects.get(id=dealer_id)
    dealer_model.id = dealer_id
    dealer_model.dealer_name = dealer_name
    dealer_model.dealer_phone = dealer_phone
    dealer_model.dealer_email = dealer_email
    dealer_model.dealer_address = dealer_address
    dealer_model.dealer_firm_name = dealer_firm_name
    dealer_model.dealer_unp = dealer_unp
    dealer_model.dealer_amount = dealer_amount
    dealer_model.max_deposit = dealer_max_deposit
    dealer_model.for_remove = for_remove
    dealer_model.save()
    return HttpResponse(dealer_model)
