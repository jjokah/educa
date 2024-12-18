from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import CouponApplyForm
from .models import Coupon


@require_POST
def coupon_apply(request):
    """
    View to handle coupon application - validates the submitted coupon.
    """
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            # Attempt to get valid coupon matching the code
            coupon = Coupon.objects.get(
                code__iexact=code,  # Case-insensitive code matching
                valid_from__lte=now,  # Coupon period has started
                valid_to__gte=now,  # Coupon hasn't expired
                active=True  # Coupon is active
            )
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            # Clear coupon from session if invalid
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')
