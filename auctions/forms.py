from datetime import datetime, timedelta

from django import forms
from django.core.exceptions import ValidationError


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
    close_on = forms.DateTimeField(
        initial=datetime.now() + timedelta(weeks=1),
        widget=forms.DateTimeInput(
            attrs={"class": "form-control"}
        ),
    )
    imageLink = forms.URLField(
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Image URL"}
        ),
    )

    # TODO: Figure out how to add categories

    def clean_close_on(self):
        close_on = self.cleaned_data['close_on']
        if close_on <= datetime.now():
            raise ValidationError("The date and time must be in the future.")
        return close_on


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
