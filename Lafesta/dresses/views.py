
# Create your views here.
from django.shortcuts import render, redirect , get_object_or_404
from .forms import DressForm , ReviewForm
from .models import Dress , Review
from django.db.models import Q  # تأكدي أنه مضاف بأعلى الملف
from .forms import RentalForm
from .models import Rental
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from customer.models import Bookmark  # ✅ تأكدي تستوردين Bookmark فوق!
from django.core.paginator import Paginator
from django.db.models import Avg
from shipping.models import Shipment, Payment

from django.utils.safestring import mark_safe
from django.urls import reverse









def add_dress(request):
    if request.method == 'POST':
        form = DressForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.owner = request.user  # ✅ هنا الربط
            form.save()
            #return redirect('my_dresses')
            return redirect('dresses:my_dresses')

    else:
        form = DressForm()
    
    return render(request, 'dresses/add_dress.html', {'form': form})

def edit_dress(request, dress_id):
    dress = get_object_or_404(Dress, id=dress_id)
    if request.user != dress.owner:
       # return redirect('my_dresses')
        return redirect('dresses:my_dresses')


    if request.method == 'POST':
        form = DressForm(request.POST, request.FILES, instance=dress)
        if form.is_valid():
            form.save()
           # return redirect('dress_detail', dress_id=dress.id)
            return redirect('dresses:dress_detail', dress_id=dress.id)

    else:
        form = DressForm(instance=dress)

    return render(request, 'dresses/edit_dress.html', {'form': form, 'dress': dress})

def delete_dress(request, dress_id):
    dress = get_object_or_404(Dress, id=dress_id)
    if request.user == dress.owner:
        dress.delete()
   # return redirect('my_dresses')
    return redirect('dresses:my_dresses')




# def my_dresses(request):
#     dresses = Dress.objects.all()
#     return render(request, 'dresses/dresses.html', {'dresses': dresses})

def my_dresses(request):
    dresses = Dress.objects.all()

    # 🔍 البحث بالاسم أو الوصف
    query = request.GET.get('search')
    if query:
       dresses = dresses.filter(
           Q(name__icontains=query) |
           Q(description__icontains=query)
    )
    # 🎯 الفلترة حسب المقاس
    size = request.GET.get('size')
    if size and size != 'all':
        dresses = dresses.filter(size=size)

    # 🎯 الفلترة حسب الفئة
    category = request.GET.get('category')
    if category and category != 'all':
        dresses = dresses.filter(category=category)

    # 🎯 الفلترة حسب المدينة (من ملف المستخدم)
    city = request.GET.get('city')
    if city and city != 'all':
        dresses = dresses.filter(owner__profile__city=city)

        
    # ✅ إضافة البيجينيشن هنا
    paginator = Paginator(dresses, 6)  # 6 فساتين لكل صفحة
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'dresses/dresses.html', {'dresses': dresses})



# def dress_detail(request, dress_id):
#     dress = get_object_or_404(Dress, id=dress_id)
#     reviews = dress.reviews.all().order_by('-created_at')  # عرض التقييمات من الأحدث إلى الأقدم

#     is_bookmarked = Bookmark.objects.filter(user=request.user, dress=dress).exists() if request.user.is_authenticated else False


#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.dress = dress
#             review.user = request.user
#             review.save()
#            # return redirect('dress_detail', dress_id=dress.id)
#             return redirect('dresses:dress_detail', dress_id=dress.id)

#     else:
#         form = ReviewForm()

#     return render(request, 'dresses/dress_detail.html', {
#         'dress': dress,
#         'form': form,
#         'reviews': reviews,
#         'is_bookmarked': is_bookmarked,  # ✅ أضف هذا السطر

#     })


def dress_detail(request, dress_id):
    dress = get_object_or_404(Dress, id=dress_id)
    reviews = dress.reviews.all().order_by('-created_at')  # عرض التقييمات من الأحدث إلى الأقدم
    average_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    average_rating = round(average_rating, 1)

    is_bookmarked = Bookmark.objects.filter(user=request.user, dress=dress).exists() if request.user.is_authenticated else False

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.dress = dress
            review.user = request.user
            review.save()
            return redirect('dresses:dress_detail', dress_id=dress.id)
    else:
        form = ReviewForm()

    return render(request, 'dresses/dress_detail.html', {
        'dress': dress,
        'form': form,
        'reviews': reviews,
        'average_rating': average_rating,
        'is_bookmarked': is_bookmarked,
    })




# def rent_dress(request, dress_id):
#     dress = get_object_or_404(Dress, id=dress_id)

#     if request.method == 'POST':
#         form = RentalForm(request.POST)
#         if form.is_valid():
#             rental = form.save(commit=False) 
#             rental.dress = dress
#             rental.customer = request.user
#             rental.save()
#             messages.success(request, 'Rental request submitted successfully!')  # ✅ رسالة النجاح
#            # return redirect('dress_detail', dress_id=dress.id)
#             #return redirect('customer:add_adress', dress_id=dress.id)
#             #تم التعديل لتمرير الاي دي الخاه بالريكويست بدل من الاي دي الخاص بالفستان الى صفحة العنوان 
#             return redirect('customer:adress_choice', rental_id=rental.id)

#     else:
#         form = RentalForm()

#     return render(request, 'dresses/rent_dress.html', {
#         'form': form,
#         'dress': dress,
#         'daily_price': dress.price_per_day,  # تأكد هذا موجود
#     })


#from django.utils.translation import gettext as _  # لو حابة تدعمي الترجمة مستقبلاً
#//////////////////////////////////////////////////////////////////////////////////////

# @login_required
# def rent_dress(request, dress_id):
#     dress = get_object_or_404(Dress, id=dress_id)

#     if request.method == 'POST':
#         form = RentalForm(request.POST)
#         if form.is_valid():
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']

#             # 🔍 Check for existing conflicting rentals
#             conflicting_rentals = Rental.objects.filter(
#                 dress=dress,
#                 start_date__lte=end_date,
#                 end_date__gte=start_date
#             )

#             if conflicting_rentals.exists():
#                 if conflicting_rentals.filter(customer=request.user).exists():
#                     messages.warning(request, "You already have a rental request for this dress during the selected dates. Please edit your previous request instead.")
#                 else:
#                     messages.error(request, "This dress is already booked during the selected dates. Please choose different dates.")
#                 return redirect('dresses:rent_dress', dress_id=dress.id)

#             rental = form.save(commit=False)
#             rental.dress = dress
#             rental.customer = request.user
#             rental.save()
#             messages.success(request, 'Your rental request has been submitted successfully. ✅')
#             return redirect('customer:adress_choice', rental_id=rental.id)

#     else:
#         form = RentalForm()

#     return render(request, 'dresses/rent_dress.html', {
#         'form': form,
#         'dress': dress,
#         'daily_price': dress.price_per_day,
#     })

@login_required
def rent_dress(request, dress_id):
    dress = get_object_or_404(Dress, id=dress_id)

    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # 🔍 Check for existing conflicting rentals
            conflicting_rentals = Rental.objects.filter(
                dress=dress,
                start_date__lte=end_date,
                end_date__gte=start_date
            )

            if conflicting_rentals.exists():
                if conflicting_rentals.filter(customer=request.user).exists():
                    existing_rental = conflicting_rentals.filter(customer=request.user).first()
                    messages.warning(
                        request,
                        mark_safe(
                            f'You already have a booking for this dress during the selected dates. '
                            f'<a href="{reverse("dresses:edit_rental_customer", args=[existing_rental.id])}">Click here to edit it.</a>'
                        )
                    )
                else:
                    messages.error(request, "This dress is already booked during the selected dates. Please choose different dates.")
                return redirect('dresses:rent_dress', dress_id=dress.id)

            rental = form.save(commit=False)
            rental.dress = dress
            rental.customer = request.user
            rental.save()
            messages.success(request, 'Your rental request has been submitted successfully. ✅')
            return redirect('customer:adress_choice', rental_id=rental.id)

    else:
        form = RentalForm()

    return render(request, 'dresses/rent_dress.html', {
        'form': form,
        'dress': dress,
        'daily_price': dress.price_per_day,
    })



@login_required
def rental_requests(request):
    user = request.user
    # جلب جميع الطلبات للفستاتين اللي يملكها المستخدم
    requests = Rental.objects.filter(dress__owner=user).order_by('-created_at')
   # return render(request, 'dresses/rental_requests.html', {'requests': requests})
    return render(request, 'dresses/rental_requests.html', {'rentals': requests})




@login_required
def rental_action(request, rental_id, action):
    rental = get_object_or_404(Rental, id=rental_id, dress__owner=request.user)

    if action == 'confirm':
        rental.status = 'confirmed'
        messages.success(request, 'Rental request confirmed successfully! ✅')
    elif action == 'cancel':
        rental.status = 'cancelled'
        messages.error(request, 'Rental request cancelled. ❌')

    rental.save()
   # return redirect('rental_requests')
    return redirect('dresses:rental_requests')



@login_required
def my_orders(request):
    user = request.user

    # جلب كل الطلبات اللي سواها المستخدم الحالي

    orders = Rental.objects.filter(customer=user).order_by('-created_at')
    return render(request, 'dresses/orders.html', {'rentals': orders})


# @login_required
# def my_orders(request):
#     user = request.user
#     rentals = Rental.objects.filter(customer=user).order_by('-created_at')

#     orders_info = []

#     for rental in rentals:
#         has_address = Shipment.objects.filter(rental=rental).exists()
#         payment = Payment.objects.filter(rental=rental).first()
#         has_payment = payment and payment.status == 'Paid'

#         orders_info.append({
#             'rental': rental,
#             'has_address': has_address,
#             'has_payment': has_payment,
#         })

#     return render(request, 'dresses/orders.html', {'orders_info': orders_info})

@login_required
def edit_rental_customer(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, customer=request.user)

    # لا يمكن التعديل إذا الدفع تم
    if rental.payment.exists() and rental.payment.first().status == 'Paid':

        messages.error(request, "You cannot edit this rental because it has already been paid.")
        return redirect('dresses:my_orders')

    if request.method == 'POST':
        form = RentalForm(request.POST, instance=rental)
        if form.is_valid():
            form.save()
            messages.success(request, "Rental updated successfully.")
            return redirect('dresses:my_orders')
    else:
        form = RentalForm(instance=rental)

    return render(request, 'dresses/edit_rental_customer.html', {'form': form, 'rental': rental})
