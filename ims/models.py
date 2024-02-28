from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
# category_choice = (
#     ('Furniture', 'Furniture'),
#     ('IT Equipment', 'IT Equipment'),
#     ('Phone', 'Phone'),
#     ('Electronics', 'Electronics'),
# )


class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Stock(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default="0", blank=True, null=True)
    receive_quantity = models.IntegerField(default="0", blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default="0", blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default="0", blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    # date = models.DateTimeField(auto_now_add=False, auto_now=False)

    def __str__(self) -> str:
        return self.item_name + " " + str(self.quantity)


class StockHistory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default="0", blank=True, null=True)
    receive_quantity = models.IntegerField(default="0", blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default="0", blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default="0", blank=True, null=True)
    last_updated = models.DateTimeField(
        auto_now_add=False, auto_now=False, null=True)
    timestamp = models.DateTimeField(
        auto_now_add=False, auto_now=False, null=True)

    def __str__(self) -> str:
        return self.item_name + " " + str(self.quantity)


@receiver(post_save, sender=Stock)
def track_stock_changes(sender, instance, created, **kwargs):
    if created:
        # If a new Stock object is created, create a corresponding StockHistory entry
        StockHistory.objects.create(
            category=instance.category,
            item_name=instance.item_name,
            quantity=instance.quantity,
            receive_quantity=instance.receive_quantity,
            receive_by=instance.receive_by,
            issue_quantity=instance.issue_quantity,
            issue_by=instance.issue_by,
            issue_to=instance.issue_to,
            phone_number=instance.phone_number,
            created_by=instance.created_by,
            reorder_level=instance.reorder_level,
            last_updated=instance.last_updated,
            timestamp=instance.timestamp
        )
    else:
        # If an existing Stock object is updated, create a new StockHistory entry
        # to capture the changes
        StockHistory.objects.create(
            category=instance.category,
            item_name=instance.item_name,
            quantity=instance.quantity,
            receive_quantity=instance.receive_quantity,
            receive_by=instance.receive_by,
            issue_quantity=instance.issue_quantity,
            issue_by=instance.issue_by,
            issue_to=instance.issue_to,
            phone_number=instance.phone_number,
            created_by=instance.created_by,
            reorder_level=instance.reorder_level,
            last_updated=instance.last_updated,
            timestamp=instance.timestamp
        )
