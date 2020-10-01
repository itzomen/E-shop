from django import forms

QUANTITY_CHOICES = [ (i, str(i)) for i in range(1,51)]
# quantity between 1 to 50

class AddItemForm(forms.Form):
    """AddItemForm definition."""

    quantity = forms.TypedChoiceField( choices=QUANTITY_CHOICES, coerce=int)
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)

    