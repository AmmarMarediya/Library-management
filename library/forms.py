from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import CATEGORY_CHOICES, PAYMENT_METHOD_CHOICES, Book, BorrowedBook, Member


class AddMemberForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter Member Name"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter Member Email"})
    )

    class Meta:
        model = Member
        fields = ["name", "email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if Member.objects.filter(email=email).exists():
            raise ValidationError(_("A member with that email already exists."))

        return email


class UpdateMemberForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter Member Name"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter Member Email"})
    )

    class Meta:
        model = Member
        fields = ["name", "email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if Member.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError(_("A member with that email already exists."))

        return email


class AddBookForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter Book Title"})
    )
    author = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter Book Author"})
    )

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES, widget=forms.Select(attrs={"class": "form-control form-control-lg"})
    )

    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter Book Quantity"})
    )

    borrowing_fee = forms.DecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter Book Fee"})
    )

    class Meta:
        model = Book
        fields = ["title", "author", "category", "quantity", "borrowing_fee"]


class LendBookForm(forms.ModelForm):
    book = forms.ModelChoiceField(
        label="Book / Books",
        queryset=Book.objects.none(),  # Initially empty, filtered in __init__
        empty_label=None,
        widget=forms.Select(
            attrs={"class": "form-control form-control-lg js-example-basic-multiple w-100", "multiple": "multiple"}
        ),
    )

    member = forms.ModelChoiceField(
        queryset=Member.objects.none(),  # Initially empty, filtered in __init__
        empty_label=None,
        widget=forms.Select(attrs={"class": "form-control form-control-lg js-example-basic-single w-100"}),
    )

    return_date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control form-control-lg", "type": "date", "id": "return-date"})
    )

    fine = forms.DecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter Fine"})
    )

    class Meta:
        model = BorrowedBook
        fields = ["book", "member", "return_date", "fine"]

    def __init__(self, *args, **kwargs):
        admin = kwargs.pop('admin', None)
        super().__init__(*args, **kwargs)

        if admin:
            self.fields['book'].queryset = Book.objects.filter(admin=admin, quantity__gt=0)
            self.fields['member'].queryset = Member.objects.filter(admin=admin)


class LendMemberBookForm(forms.ModelForm):
    book = forms.ModelChoiceField(
        queryset=Book.objects.none(),  # Initially empty, filtered in __init__
        empty_label=None,
        widget=forms.Select(
            attrs={"class": "form-control form-control-lg js-example-basic-multiple w-100", "multiple": "multiple"}
        ),
    )

    return_date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control form-control-lg", "type": "date", "id": "return-date"})
    )

    fine = forms.DecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter Fine"})
    )

    class Meta:
        model = BorrowedBook
        fields = ["book", "return_date", "fine"]

    def __init__(self, *args, **kwargs):
        admin = kwargs.pop('admin', None)
        super().__init__(*args, **kwargs)

        if admin:
            self.fields['book'].queryset = Book.objects.filter(admin=admin, quantity__gt=0)


class UpdateBorrowedBookForm(forms.ModelForm):
    return_date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control form-control-lg", "type": "date", "id": "return-date"})
    )

    fine = forms.DecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter Fine"})
    )

    class Meta:
        model = BorrowedBook
        fields = ["return_date", "fine"]


class PaymentForm(forms.Form):
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES, widget=forms.Select(attrs={"class": "form-control form-control-lg"})
    )

    class Meta:
        fields = ["payment_method"]
