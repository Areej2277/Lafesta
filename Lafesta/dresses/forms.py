from django import forms
from .models import Dress
from .models import Review
from .models import Rental



class DressForm(forms.ModelForm):
    class Meta:
        model = Dress
        fields = ['name', 'color', 'size', 'price_per_day', 'category', 'description', 'image', 'video', 'status']



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your thoughts...'}),
        }



class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'start_date': 'Start Date',
            'end_date': 'End Date',
        }
       