from django import forms


# Create choices for product quantity dropdown (1-20)
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """
    Form for adding products to the shopping cart.
    Allows selecting quantity and handles quantity override functionality.
    """
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int  # Convert selected value to integer
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput  # Hidden field to determine if quantity should be updated or added
    )
