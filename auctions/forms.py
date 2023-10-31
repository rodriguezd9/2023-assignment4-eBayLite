from django import forms

from auctions.models import Category


class ListingForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Title"}
        ),
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Description"}
        ),
    )
    bidPrice = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "5.00"}
        ),
    )
    imageLink = forms.URLField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Image URL"}
        ),
    )
    category = forms.ModelChoiceField(
        required=False,
        widget=forms.Select(
            attrs={"class": "form-control"},
        ),
        queryset=Category.objects.all()
    )


class BidForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "10.00"}
        ),
    )


class CommentForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Leave a comment!"}
        )
    )
