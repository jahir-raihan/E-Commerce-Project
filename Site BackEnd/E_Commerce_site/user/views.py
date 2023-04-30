from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from order.models import *
from .forms import UserRegisterForm
from django.middleware.csrf import get_token
from .algorithms import *
from products.models import *
from django.db.models import Q
from django.utils import timezone
from django.db.models import Sum
import json
User = get_user_model()


# Register view
def register_user(request):

    """Registers a user if user is not registered or logged in"""

    # Checking if user is already logged in or not
    if request.user.is_authenticated and request.method == 'POST':
        return JsonResponse({'redirect': False})
    if request.user.is_authenticated:
        return redirect('redirect_origin')

    # If request is post and user is not registered or logged in
    if request.method == 'POST' and not request.user.is_authenticated:

        # Verify the request data and register the user
        form = UserRegisterForm(request.POST)
        if form.is_valid:
            form.save()
            user = authenticate(request, email=form.cleaned_data['email'], password=request.POST['password1'])
            login(request, user)
            if 'redirect_url' in request.POST:
                return JsonResponse({'success': True, 'redirect': f'{request.POST["redirect_url"]}'})
            else:
                return JsonResponse({'success': True, 'redirect': '/'})
        else:
            return JsonResponse({'error': True})

    return render(request, 'account/register.html')


# Login view
def login_user(request):

    """Logs in a user if user is registered and logged out"""

    # If user is logged in redirect him or return a bad request
    if request.user.is_authenticated and request.method == 'POST':
        return JsonResponse({'redirect': False}, status=403)
    if request.user.is_authenticated:
        return redirect('redirect_origin')

    # If user is not logged in then initiate login and redirect the user to base location where he came from
    if request.method == 'POST' and not request.user.is_authenticated:
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
        if user:
            login(request, user)
            if 'redirect_url' in request.POST:
                return JsonResponse({'success': True, 'redirect': f'{request.POST["redirect_url"]}'})
            else:
                return JsonResponse({'success': True, 'redirect': '/'})
        else:
            return JsonResponse({'error': True})
    return render(request, 'account/login.html')


# Logout view
@login_required
def logout_user(request):

    """Logs out a user and redirects to login page"""
    if not request.user.is_authenticated:
        return redirect('login')

    logout(request)
    return redirect('login')


# Redirect Origin view
def redirect_origin(request):

    """Responsible for redirecting a user to base url where he came from before registering or logging in """

    return render(request, 'redirect_user_base_url.html')


# Staff panel


# Staff Order Handler panel view
def staff_main1(request):

    """Product Handler Account main page, -> If the request is made for query then filter out the Orders and return
        filtered orders to frontEnd"""

    # Router definition -> It determines user type and tells if the user is authenticated for accessing this page
    request_action = router(request, {'is_order_handler': True, 'is_product_adder': False, 'is_admin': False,
                                      'is_user': False})
    if not request_action[0]:
        return redirect(request_action[1])

    # Checking if the request is a query request
    if request.method == 'POST':

        # If query then filter out orders according to query
        query = request.POST['query']
        orders = Order.objects.filter(
            Q(order_id__icontains=query) | Q(order_person_name__icontains=query) | Q(
                order_person_email__icontains=query)
            | Q(order_person_phone__icontains=query) | Q(order_payment_method__icontains=query)
        )
    else:
        # Else return orders, ordered by date
        orders = Order.objects.filter(order_handled_by=request.user.id).order_by('order_handle_date')

    real_orders = []

    # Parsing products data from order data, Because we compressed these data when we saved the order in first place
    for order in orders:
        o_items = json.loads(order.order_items)
        items = []
        for idx in range(len(o_items['ids'])):
            tmp = {
                'item': Product.objects.get(pk=o_items['ids'][idx]),
                'quantity': o_items['quantities'][idx],
                'size': o_items['sizes'][idx],
                'price': o_items['prices'][idx]
            }
            items.append(tmp)

        real_orders.append(
            {
                "order": order,
                "items": items
            }
        )

    # Getting length of confirmed orders
    confirmed_orders = len(orders.filter(
        Q(order_is_confirmed=True) | Q(order_is_delivered=True)
    ))

    # Getting length of cancelled orders
    cancelled_orders = len(orders.filter(order_is_cancelled=True))

    # New csrf token
    token = get_token(request)

    context = {
        'orders': real_orders,
        'token': token,
        'confirmed_orders': confirmed_orders,
        'cancelled_orders': cancelled_orders
    }
    if request.method == 'POST':
        template = render_to_string('pending_orders_template.html', request=request, context=context)

        return JsonResponse({'template': template, 'token': token})

    return render(request, 'staff_main.html', context)


# Staff Product adder panel view
def staff_main2(request):

    """Product adder Account main page"""

    # Router definition -> It determines user type and tells if the user is authenticated for accessing this page
    request_action = router(request, {'is_order_handler': False, 'is_product_adder': True, 'is_admin': False,
                                      'is_user': False})
    if not request_action[0]:
        return redirect(request_action[1])

    products = Product.objects.filter(product_added_by=request.user)

    return render(request, 'staff2_main.html', {'products': products})


# Staff Pending Order (Order Handler) view
def pending_orders(request):

    """Returns list of pending orders only for Order Handler staff view,
        There's a functionality for querying the orders by get or post request. It depends on the request type"""

    # Router definition -> It determines user type and tells if the user is authenticated for accessing this page
    request_action = router(request, {'is_order_handler': True, 'is_product_adder': False, 'is_admin': False,
                                      'is_user': False})
    if not request_action[0]:
        return redirect(request_action[1])

    # If request is for query or there is a search string in request GET
    if request.method == 'POST' or 's' in request.GET:
        try:
            query = request.POST['query']
        except:
            if 's' in request.GET:
                query = request.GET['s']

        # Filter out orders according to query
        orders = Order.objects.filter(
            Q(order_id__icontains=query) | Q(order_person_name__icontains=query) | Q(
                order_person_email__icontains=query)
            | Q(order_person_phone__icontains=query) | Q(order_payment_method__icontains=query)
        )
    else:
        orders = Order.objects.filter(order_is_pending=True).order_by('order_date')

    real_orders = []

    # Same as staff main 1 view functionality , parsing products data from order data which was compressed in the first
    #  place while saving order after checkout
    for order in orders:
        o_items = json.loads(order.order_items)
        items = []
        for idx in range(len(o_items['ids'])):
            tmp = {
                'item': Product.objects.get(pk=o_items['ids'][idx]),
                'quantity': o_items['quantities'][idx],
                'size': o_items['sizes'][idx],
                'price': o_items['prices'][idx]
            }
            items.append(tmp)

        real_orders.append(
            {
                "order": order,
                "items": items
            }
        )

    token = get_token(request)
    context = {
        'orders': real_orders,
        'token': token
    }
    if request.method == 'POST' or 's' in request.GET:
        template = render_to_string('pending_orders_template.html', request=request, context=context)

        return JsonResponse({'template': template, 'token': token})

    return render(request, 'staff_pending_orders.html', context)


# Pending order action (Order Handler) view
def pending_order_action(request):

    """Accept or cancel an order, -> Depends on action data from post request, Only admin and order_handler"""

    # # Router definition -> It determines user type and tells if the user is authenticated for accessing this page
    # request_action = router(request, {'is_order_handler': True, 'is_product_adder': False, 'is_admin': False,
    #                                   'is_user': False})
    # if not request_action[0]:
    #     return redirect(request_action[1])

    action = request.POST['action']

    # Getting the order
    order = Order.objects.get(pk=request.POST['order_id'])

    # If, confirm then mark it confirm and remove pending
    if action == 'confirm':
        order.order_is_confirmed = True
        order.order_is_pending = False
    else:
        # Mark it cancelled and remove pending
        order.order_is_cancelled = True
        order.order_is_pending = False

    # Saving order handle data and who handled it
    order.order_handle_date = timezone.now()
    order.order_handled_by = request.user.id
    order.save()

    # New token
    token = get_token(request)

    return JsonResponse({'success': True, 'token': token, 'cancelled': order.order_is_cancelled,
                         'confirmed': order.order_is_confirmed})


# Add new product (Product Adder) view
def add_products(request):

    """Add a new product to the database with images and information """

    # Router definition -> It determines user type and tells if the user is authenticated for accessing this page
    request_action = router(request, {'is_order_handler': False, 'is_product_adder': True, 'is_admin': False,
                                      'is_user': False})
    if not request_action[0]:
        return redirect(request_action[1])

    # Product add reqeust
    if request.method == 'POST':
        data = request.POST

        # If category is empty then create a new category from new_category data included in request data
        if data['category'] == '':
            category = Category(category_name=data['category_new'])
            category.save()
        else:
            category = Category.objects.get(pk=data['category'])

        # Creating product
        product = Product(
            product_title=data['title'].lower(),
            product_code=data['product_code'],
            product_price=data['price'],
            product_category=category,
            color_type=data['color_type'],
            yarn_type=data['yarn_type'],
            yarn_count=data['yarn_count'],
            brand=data['brand'],
            product_in_stock=bool(data['status']),
            product_tags=data['tags'].lower(),
            product_primary_image=request.FILES['primary_image'],
            product_more_information=data['more_info'].lower(),
            product_search_keyword=data['search_keywords'].lower(),
        )

        # If the product is on discount call on_discount function from user.algorithms
        if 'on_discount' in data:
            on_discount(data, product)
        product.save()

        #  Save all images
        alt_texts = request.POST['image_alt_texts']
        images = request.FILES.getlist('images')
        save_product_images(product, alt_texts.split(','), images)

        # new csrf token
        new_token = get_token(request)

        return JsonResponse({'success': True, 'token': new_token, 'edit': False})

    categories = Category.objects.all()
    discount_reasons = DiscountReason.objects.all()

    context = {
        'categories': categories,
        'discount_reasons': discount_reasons
    }
    return render(request, 'add_a_product.html', context)


# Edit existing product (Product adder view)
def edit_products(request, pk):

    """Edits a product details and images"""

    # Router definition -> It determines user type and tells if the user is authenticated for accessing this page
    request_action = router(request, {'is_order_handler': False, 'is_product_adder': True, 'is_admin': False,
                                      'is_user': False})
    if not request_action[0]:
        return redirect(request_action[1])

    # If edit product reqeust
    if request.method == 'POST':

        # Get the product and call out edit function to save the edited contents of the product
        product = Product.objects.get(pk=pk)
        save_edited_product(product, request)

        # New csrf token
        new_token = get_token(request)

        return JsonResponse({'success': True, 'token': new_token, 'edit': True})

    product = Product.objects.get(pk=pk)
    product_images = product.productimages_set.all()
    context = {
        'product': product,
        'product_images': product_images
    }

    return render(request, 'add_a_product.html', context)


# User Section

# User account page -> Registered or Unregistered
@csrf_exempt
def account(request):

    """Account main page for users (Registered or Unregistered)"""

    # Router definition -> It determines user type and tells if the user is authenticated for accessing this page
    request_action = router(request, {'is_order_handler': False, 'is_product_adder': False, 'is_admin': False,
                                      'is_user': True})
    if not request_action[0] and len(request_action) < 3:
        return redirect(request_action[1])

    # If registered filter out recent orders by user
    if request.user.is_authenticated:

        orders = Order.objects.filter(order_person=request.user).order_by('-order_date')
    else:
        # Else filter out by IP Address
        orders = Order.objects.filter(order_person_ip=get_client_ip(request)).order_by('-order_date')
    real_orders = []

    # Parsing order products details, this details was compressed in the first place to save storage and complexity
    for order in orders:
        o_items = json.loads(order.order_items)
        items = []
        for idx in range(len(o_items['ids'])):
            tmp = {
                'item': Product.objects.get(pk=o_items['ids'][idx]),
                'quantity': o_items['quantities'][idx],
                'size': o_items['sizes'][idx],
                'price': o_items['prices'][idx]
            }
            items.append(tmp)

        real_orders.append(
            {
                "order": order,
                "items": items
            }
        )

    context = {
        'orders': real_orders
    }

    return render(request, 'page_profile.html', context)


# User order history view -> registered or unregistered -> If unregistered track by ip address
@csrf_exempt
def order_history(request):

    """This view is like a multipurpose kind, we're using it as order history of a user, also using it
        as return request or redirect request which is POST, from online payment service"""

    # Router definition -> It determines user type and tells if the user is authenticated for accessing this page
    request_action = router(request, {'is_order_handler': False, 'is_product_adder': False, 'is_admin': False,
                                      'is_user': True})
    if not request_action[0] and len(request_action) < 3:
        return redirect(request_action[1])

    # If the request is from online payment gateway
    if request.method == 'POST':

        # Response from sslcommerze payment system
        data = request.POST

        # Getting the order
        order_id = data['value_a']
        order = Order.objects.get(pk=order_id)

        # Determining transactions method
        transaction_method = 'sslcom'
        if data['card_issuer'] == 'Bkash Mobile Banking':
            transaction_method = 'bkash'

        # Saving transaction data
        tran = Transaction(
            transaction_id=data['tran_id'],
            transaction_amount=float(data['amount']),
            transaction_method=transaction_method,
            bank_tran_id=data['bank_tran_id'],
            transaction_person=order.order_person,
            transaction_person_name=order.order_person_name,
            transaction_person_phone=order.order_person_phone,
            transaction_person_email=order.order_person_email,
            transaction_person_ip=order.order_person_ip,
            order=order
        )
        tran.save()
        order.order_is_pending = False
        order.order_is_confirmed = True
        order.save()

    # If not a request from any payment gateway then just return orders of user (Registered or Unregistered)
    # I've always used ip tracking for this kind of purpose to verify a user. Like isolated multi tenet database
    if request.user.is_authenticated:
        orders = Order.objects.filter(order_person=request.user).order_by('-order_date')
    else:
        orders = Order.objects.filter(order_person_ip=get_client_ip(request)).order_by('-order_date')
    real_orders = []

    # Parsing Ordered products details, which was compressed in the first place.
    for order in orders:
        o_items = json.loads(order.order_items)
        items = []
        for idx in range(len(o_items['ids'])):
            tmp = {
                'item': Product.objects.get(pk=o_items['ids'][idx]),
                'quantity': o_items['quantities'][idx],
                'size': o_items['sizes'][idx],
                'price': o_items['prices'][idx]
            }
            items.append(tmp)

        real_orders.append(
            {
                "order": order,
                "items": items
            }
        )

    # New csrf_token
    token = get_token(request)
    context = {
        'orders': real_orders,
        'token': token
    }

    return render(request, 'order_history.html', context)


# Query order history by user or ip address -> Depends on authentications
def query_order_history(request):

    """The reason why we are using separate view for querying order history of users is because, we've already
        used the post request of order history page for payment request"""

    # Getting query data
    if 's' in request.GET:
        query = request.GET['s']
    else:
        query = request.POST['query']

    # First of all filtering orders according to user -> Isolated purpose
    if request.user.is_authenticated:
        orders = Order.objects.filter(order_person=request.user)
    else:
        orders = Order.objects.filter(order_person_ip=get_client_ip(request))

    # Then filtering by query data
    orders = orders.filter(
        Q(order_id__icontains=query) | Q(order_person_name__icontains=query) | Q(order_person_email__icontains=query)
        | Q(order_person_phone__icontains=query) | Q(order_payment_method__icontains=query) |
        Q(id__icontains=query)
    )
    real_orders = []

    # Parsing Order products data, compressed in the first place to save storage and load time
    for order in orders:
        o_items = json.loads(order.order_items)
        items = []
        for idx in range(len(o_items['ids'])):
            tmp = {
                'item': Product.objects.get(pk=o_items['ids'][idx]),
                'quantity': o_items['quantities'][idx],
                'size': o_items['sizes'][idx],
                'price': o_items['prices'][idx]
            }
            items.append(tmp)

        real_orders.append(
            {
                "order": order,
                "items": items
            }
        )

    # new token
    token = get_token(request)

    context = {
        'orders': real_orders,
        'token': token
    }
    template = render_to_string('order_history_search_template.html', request=request, context=context)

    if request.method == 'POST':
        return JsonResponse({'template': template, 'token': token})
    else:
        return render(request, 'order_history.html', context)


# Wishlist section

# Save a product to wishlist -> only for registered users
def save_wishlist_item(request):

    """Saves a product to a registered user wishlist"""

    # Getting the product and updating it's wished count -> can be useful for Analysis
    product = Product.objects.get(pk=request.POST['product_id'])
    product.wish_count += 1
    product.save()

    # Getting or creating wishlist instance for the user, and saving the product to wishlist.
    try:
        wishlist_obj = WishList.objects.get(wisher_person=request.user)
        items = json.loads(wishlist_obj.wishlist_items)
        items.append(product.id)
        wishlist_obj.wishlist_items = f'{items}'
        wishlist_obj.save()
    except:
        wishlist_obj = WishList(wishlist_items=f'[{product.id}]', wisher_person=request.user,
                                wisher_person_ip=get_client_ip(request))
        wishlist_obj.save()

    # New csrf token
    token = get_token(request)

    return JsonResponse({'success': True, 'token': token})


# Remove a product from wishlist -> Only for Registered users
def remove_wishlist_item(request):

    """Removes a product from user wishlist instance and decreases the count of wished for that particular
        Product"""

    # Getting product and decreasing it's wished count
    product = Product.objects.get(pk=request.GET['product_id'])
    product.wish_count -= 1
    product.save()

    # Removing the product from wishlist instance ,
    wishlist_obj = WishList.objects.get(wisher_person=request.user)
    items = json.loads(wishlist_obj.wishlist_items)
    items.remove(product.id)
    wishlist_obj.wishlist_items = f'{items}'
    wishlist_obj.save()

    return JsonResponse({'success': True, 'items_count': len(items)})


# Wishlist page -> If user is registered return wishlist items of the user from database else just render the template
def wishlist(request):

    """Returns wishlist items if user is registered , else just renders out the template, and the whole work
        is done on front end"""

    # Router definition -> It determines user type and tells if the user is authenticated for accessing this page
    request_action = router(request, {'is_order_handler': False, 'is_product_adder': False, 'is_admin': False,
                                      'is_user': True})
    if not request_action[0] and len(request_action) < 3:
        return redirect(request_action[1])

    items = []
    try:
        # Getting wishlist instance
        wishlist_itm = WishList.objects.get(wisher_person=request.user)

        # Appending them in items list
        for p_id in json.loads(wishlist_itm.wishlist_items):
            product = Product.objects.get(pk=p_id)
            items.append(product)
    except:pass

    context = {
        'items': items
    }
    return render(request, 'wishlist.html', context)


# Responsible for checking a product availability -> Simultaneous request
def check_product_availability(request):

    """Responsible for checking a product availability"""

    # Getting the product
    product = Product.objects.get(pk=request.GET['p_id'])

    # And returning its current status
    context = {
        'status': True if product.product_in_stock else False
    }
    return JsonResponse(context)


# Transactions view for Registered or Unregistered users
def transactions(request):

    """Returns transaction list of a user"""

    # Router definition -> It determines user type and tells if the user is authenticated for accessing this page
    request_action = router(request, {'is_order_handler': False, 'is_product_adder': False, 'is_admin': False,
                                      'is_user': True})
    if not request_action[0] and len(request_action) < 3:
        return redirect(request_action[1])

    # If registered then filter by user
    if request.user.is_authenticated:
        user = request.user
        trans = Transaction.objects.filter(transaction_person=user)
    else:
        # Else filter by IP Address
        user_ip = get_client_ip(request)
        trans = Transaction.objects.filter(transaction_person_ip=user_ip)

    context = {
        'transactions': trans
    }
    return render(request, 'transactions.html', context)

# Admin section


# Admin Dashboard

def dashboard(request):

    """Dashboard of admin, includes total earning , orders, products, Earning change log graph, and visiting traffic
        . Yah I know I haven't implemented all of them , but I will do them shortly """

    # Router definition -> It determines user type and tells if the user is authenticated for accessing this page
    request_action = router(request, {'is_order_handler': False, 'is_product_adder': False, 'is_admin': True,
                                      'is_user': False})
    if not request_action[0]:
        return redirect(request_action[1])

    total_earnings = Order.objects.filter(order_is_confirmed=True).aggregate(Sum('order_total_price'))['order_total_price__sum']
    total_orders = Order.objects.filter(order_is_confirmed=True).count()
    total_products = Product.objects.all().count()

    orders = Order.objects.all().order_by('-order_date')[:50]

    context = {
        'total_earnings': total_earnings,
        'total_orders': total_orders,
        'total_products': total_products,
        'orders': orders
    }
    return render(request, 'admin/dashboard.html', context)


# Admin products list view
def admin_product_list(request):

    """Admin products list, here admin can view query and edit a product details just as Product Adder functionality"""

    # Router definition -> It determines user type and tells if the user is authenticated for accessing this page
    request_action = router(request, {'is_order_handler': False, 'is_product_adder': False, 'is_admin': True,
                                      'is_user': False})
    if not request_action[0]:
        return redirect(request_action[1])

    # Query through products
    if request.method == 'POST':

        query = request.POST['query']
        category = Category.objects.filter(category_name__icontains=query)
        reasons = DiscountReason.objects.filter(discount_reason__icontains=query)

        products_list = Product.objects.filter(
            Q(product_title__icontains=query) | Q(brand__icontains=query) | Q(product_tags__icontains=query) |
            Q(product_search_keyword__icontains=query) | Q(product_more_information__icontains=query) |
            Q(product_category__in=category) | Q(discount_reason__in=reasons)

        )

        # New csrf token -> For simultaneous request
        token = get_token(request)

        context = {
            'products': products_list,
        }
        template = render_to_string('admin/product_list_template.html', context=context, request=request)

        return JsonResponse({'template': template, 'token': token})

    # if no query request, just return all products , ordered by adding date
    products = Product.objects.all().order_by('-product_last_update')
    context = {
        'products': products
    }
    return render(request, 'admin/products_list.html', context)


# Admin add product view
def admin_add_product(request):

    """Admin add a product view, from here admin can add a new product."""

    # Router definition -> It determines user type and tells if the user is authenticated for accessing this page
    request_action = router(request, {'is_order_handler': False, 'is_product_adder': False, 'is_admin': True,
                                      'is_user': False})
    if not request_action[0]:
        return redirect(request_action[1])

    # Adding reqeust
    if request.method == 'POST':
        data = request.POST

        # If category is empty and new_category is in request data then create new category for the product
        if data['category'] == '':
            category = Category(category_name=data['category_new'])
            category.save()
        else:
            category = Category.objects.get(pk=data['category'])

        # Creating product
        product = Product(
            product_title=data['title'].lower(),
            product_code=data['product_code'],
            product_price=data['price'],
            product_category=category,
            color_type=data['color_type'],
            yarn_type=data['yarn_type'],
            yarn_count=data['yarn_count'],
            brand=data['brand'],
            product_in_stock=bool(data['status']),
            product_tags=data['tags'].lower(),
            product_primary_image=request.FILES['primary_image'],
            product_more_information=data['more_info'].lower(),
            product_search_keyword=data['search_keywords'].lower(),
        )

        # If the product is on discount call out on_discount function from user.algorithms
        if 'on_discount' in data:
            on_discount(data, product)
        product.save()

        #  Save all images
        alt_texts = request.POST['image_alt_texts']
        images = request.FILES.getlist('images')
        save_product_images(product, alt_texts.split(','), images)

        # New csrf token
        new_token = get_token(request)

        return JsonResponse({'success': True, 'token': new_token, 'edit': False})

    categories = Category.objects.all()
    discount_reasons = DiscountReason.objects.all()

    context = {
        'categories': categories,
        'discount_reasons': discount_reasons
    }
    return render(request, 'admin/add_edit_products.html', context)


# Admin edit a product view
def admin_edit_product(request, pk):

    """Admin edit a product, functionality is same as Product adder"""

    # Router definition -> It determines user type and tells if the user is authenticated for accessing this page
    request_action = router(request, {'is_order_handler': False, 'is_product_adder': False, 'is_admin': True,
                                      'is_user': False})
    if not request_action[0]:
        return redirect(request_action[1])

    # Edit request
    if request.method == 'POST':

        # Getting the product to be edited
        product = Product.objects.get(pk=pk)

        # Editing by calling edit function from user.algorithms
        save_edited_product(product, request)

        # New csrf token
        new_token = get_token(request)

        return JsonResponse({'success': True, 'token': new_token, 'edit': True})

    product = Product.objects.get(pk=pk)
    product_images = product.productimages_set.all()
    context = {
        'product': product,
        'product_images': product_images
    }

    return render(request, 'admin/add_edit_products.html', context)


# Admin all orders list view
def admin_orders(request):

    """Admin orders page, can view query or take actions to orders that are in pending status"""

    # Router definition -> It determines user type and tells if the user is authenticated for accessing this page
    request_action = router(request, {'is_order_handler': False, 'is_product_adder': False, 'is_admin': True,
                                      'is_user': False})
    if not request_action[0]:
        return redirect(request_action[1])

    # Query request
    if request.method == 'POST' or 's' in request.GET:
        try:
            query = request.POST['query']
        except:
            if 's' in request.GET:
                query = request.GET['s']

        # Filtering by query data
        orders = Order.objects.filter(
            Q(order_id__icontains=query) | Q(order_person_name__icontains=query) | Q(
                order_person_email__icontains=query)
            | Q(order_person_phone__icontains=query) | Q(order_payment_method__icontains=query) |
            Q(id__icontains=query)
        )
    else:
        orders = Order.objects.filter(order_is_pending=True).order_by('order_date')

    real_orders = []

    # Parsing order product data, which was compressed in the first place to save storage
    for order in orders:
        o_items = json.loads(order.order_items)
        items = []
        for idx in range(len(o_items['ids'])):
            tmp = {
                'item': Product.objects.get(pk=o_items['ids'][idx]),
                'quantity': o_items['quantities'][idx],
                'size': o_items['sizes'][idx],
                'price': o_items['prices'][idx]
            }
            items.append(tmp)

        real_orders.append(
            {
                "order": order,
                "items": items
            }
        )

    # New csrf token
    token = get_token(request)
    context = {
        'orders': real_orders,
        'token': token
    }
    if request.method == 'POST':
        template = render_to_string('pending_orders_template.html', request=request, context=context)

        return JsonResponse({'template': template, 'token': token})

    return render(request, 'admin/orders.html', context)


# Admin all transactions list view
def admin_transactions(request):

    """Admin transactions page, admin can view transaction order, user, amount and can query through all of them"""

    # Router definition -> It determines user type and tells if the user is authenticated for accessing this page
    request_action = router(request, {'is_order_handler': False, 'is_product_adder': False, 'is_admin': True,
                                      'is_user': False})
    if not request_action[0]:
        return redirect(request_action[1])

    # Querying transactions
    if request.method == 'POST':
        query = request.POST['query']

        # Filtering out transactions by query data
        transactions = Transaction.objects.filter(
            Q(transaction_person_name__icontains=query) | Q(transaction_person_phone__icontains=query) |
            Q(transaction_person_email__icontains=query) | Q(transaction_id__icontains=query) |
            Q(transaction_person_ip__icontains=query)
        )
        context = {
            'transactions': transactions,
        }

        # New csrf token
        token = get_token(request)

        # Rendering template as string
        template = render_to_string('admin/transactions_template.html', context, request)

        return JsonResponse({'template': template, 'token': token})

    transactions = Transaction.objects.all()
    return render(request, 'admin/transactions.html', {'transactions': transactions})