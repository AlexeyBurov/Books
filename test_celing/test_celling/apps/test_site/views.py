import datetime
import json
import os
import random

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView
from django.conf import settings as settings_file

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
        context = {}
        return render(request, 'index.html', context=context)
    else:
        return HttpResponseRedirect("./login")


@group_required('manager', 'dealer')
def orders(request):
    if request.user.is_authenticated:
        context = {
            'material_group': MaterialGroup.objects.all(),
            'dealers': Dealer.objects.all()
        }
        return render(request, 'orders.html', context=context)
    else:
        return HttpResponseRedirect('./login')


@group_required('manager')
def dealers(request):
    if request.user.is_authenticated:
        context = {'material_groups': MaterialGroup.objects.all()}
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


@group_required('manager')
def get_discounts_for_dealer(request):
    dealer_id = request.GET.get('dealer_id')
    dealer = Dealer.objects.get(id=dealer_id)
    dealer_discounts = MaterialDealerPrice.objects.filter(dealer=dealer)
    discounts = list()
    for discount in dealer_discounts:
        discounts.append(discount.to_json())
    return HttpResponse(json.dumps(discounts))


@group_required('manager', 'dealer')
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
        celling_model = Celling(
            name=celling_name,
            material_group=material_group,
            celling_width=celling_width,
            count_meters_pagon=celling_count
        )
        result = celling_model.save()
        return HttpResponse(result)
    else:
        return HttpResponse(status=405)


@group_required('manager', 'dealer')
def save_file(request):
    file_content = ''
    content = {}
    hash_str = random.getrandbits(128)
    chunks = request.FILES['file'].chunks()
    while os.path.exists(settings_file.MEDIA_ROOT+str(hash_str)+'.ec'):
        hash_str = random.getrandbits(128)
    f = open(settings_file.MEDIA_ROOT+str(hash_str)+'.ec', 'wb')
    for chunk in chunks:
        f.write(chunk)
        file_content += chunk.decode('utf-16', 'ignore')
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
    content['path_to_file'] = os.path.basename(f.name)
    f.close()

    return render(request, 'add_order_template.html', context=content)


@group_required('manager')
def materials_list_tmpl(request):
    return render(request, 'materials_list.html', context={'material_groups': MaterialGroup.objects.all()})


@group_required('manager')
def materials_group_tmpl(request):
    return render(request, 'materials_group.html', context={'colors': MaterialColor.objects.all()})


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
            dealer = Dealer.objects.get(id=dealer_id)
            celling = Celling.objects.get(id=material_id)
        except Exception:
            pass
        material_color = MaterialColor.objects.get(id=request.POST.get('material_color'))
        celling_s = float(request.POST.get('celling_s').replace(',', '.'))
        celling_p = float(request.POST.get('celling_p').replace(',', '.'))
        garpun_p = float(request.POST.get('garpun_p').replace(',', '.'))
        p_curve = float(request.POST.get('p_curve').replace(',', '.'))
        material_group_id = request.POST.get('material_group')
        material_group = MaterialGroup.objects.get(id=material_group_id)
        s_material = float(request.POST.get('s_material').replace(',', '.'))
        material_long_m = 0.0
        path_to_file = request.POST.get('path_to_file')
        if bool(request.user.groups.filter(name__in='dealer')):
            material_long_m = float(request.POST.get('material_long_m').replace(',', '.'))
        balance_model = None
        balance = 0.0
        order_price = 0.0
        celling_price = 0.0
        discount = 0.0
        try:
            discount_model = MaterialDealerPrice.objects.get(dealer=dealer, material=material_group)
            discount = discount_model.discount
        except:
            discount = 0.0
        if celling is not None:
            balance = float(celling.celling_width * material_long_m - s_material)
            celling_price = (material_group.default_price - discount) * celling_s
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
                            celling_price=celling_price,
                            color_model=material_color,
                            file_name=path_to_file,
                            for_remove=False
                            )
        order_model.save()
        return HttpResponse('{"error":false,"Заказ добавлен","celling_price":'+str(celling_price)+
                            ',"celing_price_with_discount:'+str(celling_price-discount)+'"}')

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
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "register.html"

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name='manager')
        group.user_set.add(user)
        user.groups.add(group)
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
        user = User.objects.get(id=dealer.user_id)
        user.delete()
        return HttpResponse(dealer.delete())


@group_required('manager')
def add_material_api(request):
    material_group_id = request.POST.get('material_group')
    material_group = MaterialGroup.objects.get(id=material_group_id)
    material_name = request.POST.get('celling_name')
    material_width = request.POST.get('celling_width')
    material_count = request.POST.get('material_count')
    material_price = float(request.POST.get('material_price').replace(',', '.'))
    material_model = Celling(
        material_group=material_group,
        name=material_name,
        celling_width=material_width,
        count_meters_pagon=material_count,
        price=material_price
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
def get_material_json(request):
    material_id = request.GET.get('material_id')
    material_model = Celling.objects.get(id=material_id)
    return HttpResponse(json.dumps(material_model.to_json()))


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


@group_required('manager')
def edit_discount(request):
    discount_id = request.POST.get('discount_id')
    discount_price = request.POST.get('discount_price')
    discount_model = MaterialDealerPrice.objects.get(id=discount_id)
    discount_model.discount = discount_price
    discount_model.save()
    return HttpResponse(json.dumps(discount_model.to_json()))


@group_required('manager')
def add_discount(request):
    dealer_id = request.POST.get('dealer_id')
    material_id = request.POST.get('material_group_id')
    discount = request.POST.get('payment_sum')
    material = MaterialGroup.objects.get(id=material_id)
    dealer = Dealer.objects.get(id=dealer_id)
    material_dealer_price = MaterialDealerPrice(dealer=dealer, material=material, discount=discount)
    material_dealer_price.save()
    return HttpResponse(json.dumps(material_dealer_price.to_json()))


@group_required('manager')
def delete_color(request):
    color_id = request.POST.get('color_id')
    color_model = MaterialColor.objects.get(id=color_id)
    if request.user.groups.filter(name='manager').exists():
        color_model.for_remove = True
        return HttpResponse(color_model.save())
    else:
        color_model.delete()
    return HttpResponse(json.dumps(color_model.to_json()))


@group_required('manager')
def delete_material_group(request):
    material_group_id = request.POST.get('material_group')
    material_group_model = MaterialGroup.objects.get(id=material_group_id)
    material_group_model.colors = list()
    material_group_model.delete()
    return HttpResponse(material_group_model.to_json())


@group_required('manager')
def material_group_info(request):
    material_group_id = request.GET.get('material_group_id')
    material_group_model = MaterialGroup.objects.get(id=material_group_id)
    return HttpResponse(json.dumps(material_group_model.to_json()))


@group_required('manager')
def delete_material(request):
    material_id = request.POST.get('material_id')
    material_model = Celling.objects.get(id=material_id)
    if request.user.groups.filter(name='manager').exists():
        material_model.for_remove = True
        return HttpResponse(material_model.save())
    else:
        material_model.delete()
    return HttpResponse(json.dumps(material_model.to_json()))


@group_required('manager')
def edit_material_group(request):
    material_group_id = request.POST.get('material_group_id')
    material_group_name = request.POST.get('material_group_name')
    default_price = request.POST.get('default_price')
    colors_req = request.POST.getlist('colors')
    colors = MaterialColor.objects.filter(id__in=colors_req)
    material_group_model = MaterialGroup.objects.get(id=material_group_id)
    material_group_model.name = material_group_name
    material_group_model.default_price = default_price
    material_group_model.for_remove = False
    material_group_model.colors = colors
    material_group_model.save()
    return HttpResponse(json.dumps(material_group_model.to_json()))


@group_required('manager')
def edit_material(request):
    material_id = request.POST.get('material_id')
    material_name = request.POST.get('material_name')
    celling_width = request.POST.get('celling_width')
    material_price = request.POST.get('material_price')
    material_group_id = request.POST.get('material_group')
    count_material = request.POST.get('count_meters_pagon')
    material_model = Celling.objects.get(id=material_id)
    material_group_model = MaterialGroup.objects.get(id=material_group_id)
    material_model.name = material_name
    material_model.celling_width = celling_width
    material_model.price = material_price
    material_model.material_group = material_group_model
    material_model.for_remove = False
    material_model.count_meters_pagon = count_material
    material_model.save()
    return HttpResponse(json.dumps(material_model.to_json()))


@group_required('manager')
def delete_order(request):
    order_id = request.POST.get('order_id')
    order_model = Order.objects.get(id=order_id)
    order_model.delete()
    return HttpResponse(json.dumps(order_model.to_json()))


@group_required('manager')
def order_info(request):
    order_id = request.GET.get('order_id')
    order_model = Order.objects.get(id=order_id)
    result = order_model.to_json()
    discount = 0.0
    try:
        discount = MaterialDealerPrice.objects.filter(dealer=order_model.dealer).get(material=order_model.material_group).discount
    except Exception:
        pass
    result['discount'] = discount
    return HttpResponse(json.dumps(result))


@group_required('manager')
def edit_order(request):
    order_id = request.POST.get('order_id')
    material_id = request.POST.get('material_id')
    dealer_id = request.POST.get('dealer_id')
    material_group_id = request.POST.get('material_group')
    material_group = MaterialGroup.objects.get(id=material_group_id)
    material_color_id = request.POST.get('material_color')
    material_color = MaterialColor.objects.get(id=material_color_id)
    material_long_m = float(request.POST.get('material_long_m').replace(',', '.'))
    celling_s = float(request.POST.get('celling_s').replace(',', '.'))
    celling_p = float(request.POST.get('celling_p').replace(',', '.'))
    garpun_p = float(request.POST.get('garpun_p').replace(',', '.'))
    p_curve = float(request.POST.get('p_curve').replace(',', '.'))
    s_material = float(request.POST.get('s_material').replace(',', '.'))
    order_status = request.POST.get('order_status')
    order_model = Order.objects.get(id=order_id)
    order_model.material_long = material_long_m
    order_model.s_celling = celling_s
    order_model.p_celling = celling_p
    order_model.p_garpun = garpun_p
    order_model.p_curve = p_curve
    order_model.s_material = s_material
    order_model.order_status = order_status
    order_model.color_model = material_color
    order_model.material_group = material_group
    material = None
    dealer = None
    try:
        dealer = Dealer.objects.get(id=dealer_id)
        material = Celling.objects.get(id=material_id)
    except Exception:
        pass
    order_model.dealer_obj = dealer
    order_model.celling = material
    order_model.save()
    return HttpResponse(json.dumps(order_model.to_json()))
