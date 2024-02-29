from django import forms
from .models import *


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('This field is required')
        return category

    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This field is required')
        for instance in Stock.objects.all():
            if instance.item_name == item_name:
                raise forms.ValidationError(
                    str(item_name) + ' is already created')
        return item_name


class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)

    class Meta:
        model = Stock
        fields = ['category', 'item_name']


class StockHistorySearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)

    class Meta:
        model = StockHistory
        fields = ['category', 'item_name', 'start_date', 'end_date']


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than 0.")
        return quantity


class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['issue_quantity', 'issue_to']

    def clean_issue_quantity(self):
        issue_quantity = self.cleaned_data['issue_quantity']
        stock_instance = self.instance

        # Check if the issue quantity is greater than the available quantity in stock
        if issue_quantity > stock_instance.quantity:
            raise forms.ValidationError(
                "Issue quantity cannot be greater than the available quantity in stock.")

        return issue_quantity


class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['receive_quantity', 'receive_by']

    def clean_receive_quantity(self):
        receive_quantity = self.cleaned_data['receive_quantity']
        if receive_quantity <= 0:
            raise forms.ValidationError(
                "Receive quantity must be greater than 0.")
        return receive_quantity


class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']

    def clean_reorder_level(self):
        reorder_level = self.cleaned_data['reorder_level']
        if reorder_level <= 0:
            raise forms.ValidationError(
                "Reorder level must be greater than 0.")
        return reorder_level
