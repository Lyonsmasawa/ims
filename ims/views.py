from .models import Stock
from django.shortcuts import render
from django.shortcuts import render, redirect
import csv
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import plotly.graph_objs as go

# Create your views here.


def home(request):
    title = "Mini Inventory Stcok Management"
    context = {"title": title}
    return render(request, 'home.html', context)


@login_required
def list_items(request):
    header = 'list of items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()

    if request.method == 'POST':
        queryset = Stock.objects.filter(  # category__icontains=form['category'].value(),
            item_name__icontains=form['item_name'].value())
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Desposition'] = 'attachmnet; filename = "List of stocks.csv'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM_NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow(
                    {stock.category, stock.item_name, stock.quantity})
            return response
    context = {
        "header": header,
        'form': form,
        "queryset": queryset
    }

    return render(request, "list_items.html",  context)


@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully added')
        return redirect('/list_items')
    context = {
        "form": form,
        "title": "Add item",
    }
    return render(request, "add_items.html", context)


@login_required
def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated')
            return redirect('/list_items')
    context = {
        "form": form,
    }
    return render(request, "add_items.html", context)


@login_required
def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully deleted')
        return redirect('/list_items')

    return render(request, "delete.html")


@login_required
def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)

    context = {
        "queryset": queryset,
    }
    return render(request, "stock_detail.html", context)


@login_required
def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity -= instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request, 'Issued successfully.' + str(instance.quantity) +
                         " " + str(instance.item_name) + "s now left in store")
        return redirect('/stock_detail/' + str(instance.id))
    context = {
        "form": form,
        "queryset": queryset,
        "title": "Issue " + str(queryset.item_name),
        "username": "Issue By: " + str(request.user)
    }
    return render(request, "add_items.html", context)


@login_required
def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity += instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request, 'Received successfully.' + str(instance.quantity) +
                         " " + str(instance.item_name) + "s now left in store")
        return redirect('/stock_detail/' + str(instance.id))
    context = {
        "form": form,
        "queryset": queryset,
        "title": "Receive " + str(queryset.item_name),
        "username": "Receive By: " + str(request.user)
    }
    return render(request, "add_items.html", context)


@login_required
def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Reorder level for' + " " +
                         str(instance.item_name) + " is updated to " + str(instance.reorder_level))
        return redirect('/list_items')
    context = {
        "form": form,
        "instance": queryset
    }
    return render(request, "add_items.html", context)


@login_required
def list_history(request):
    header = 'list of items'
    form = StockHistorySearchForm(request.POST or None)
    queryset = StockHistory.objects.all()

    if request.method == 'POST':
        queryset = StockHistory.objects.filter(  # category__icontains=form['category'].value(),
            item_name__icontains=form['item_name'].value(),
            last_updated__range=[
                form['start_date'].value(),
                form['end_date'].value(),
            ]
        )
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Desposition'] = 'attachmnet; filename = "List of stocks.csv'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM_NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow(
                    {stock.category, stock.item_name, stock.quantity})
            return response
    context = {
        "header": header,
        'form': form,
        "queryset": queryset
    }

    return render(request, "list_history.html",  context)


def inventory_overview(request):
    # Fetch inventory data
    stocks = Stock.objects.all()

    # Extract relevant data for visualization
    item_names = [stock.item_name for stock in stocks]
    quantities = [stock.quantity for stock in stocks]

    # Create bar chart
    bar_chart = go.Bar(x=item_names, y=quantities)

    # Create layout for the chart
    layout = go.Layout(title='Inventory Overview',
                       xaxis=dict(title='Item Name'),
                       yaxis=dict(title='Quantity'))

    # Create figure and add chart and layout
    figure = go.Figure(data=[bar_chart], layout=layout)

    # Convert figure to HTML
    chart_div = figure.to_html(full_html=False)

    return render(request, 'reports/inventory_overview.html', {'chart_div': chart_div})


def inventory_trend_analysis(request):
    stock_history = StockHistory.objects.all()

    item_names = set()
    data = {}

    for record in stock_history:
        item_names.add(record.item_name)
        if record.item_name not in data:
            data[record.item_name] = {'dates': [], 'quantities': []}
        data[record.item_name]['dates'].append(record.timestamp)
        data[record.item_name]['quantities'].append(record.quantity)

    line_charts = []

    for item_name in item_names:
        line_chart = go.Scatter(
            x=data[item_name]['dates'], y=data[item_name]['quantities'], mode='lines', name=item_name)
        line_charts.append(line_chart)

    layout = go.Layout(title='Inventory Trend Analysis', xaxis=dict(
        title='Date'), yaxis=dict(title='Quantity'))
    figure = go.Figure(data=line_charts, layout=layout)
    chart_div = figure.to_html(full_html=False)

    return render(request, 'reports/inventory_trend_analysis.html', {'chart_div': chart_div})


def category_analysis(request):
    stocks = Stock.objects.all()

    category_quantities = {}
    for stock in stocks:
        category_name = stock.category.name
        quantity = stock.quantity
        if category_name in category_quantities:
            category_quantities[category_name] += quantity
        else:
            category_quantities[category_name] = quantity

    categories = list(category_quantities.keys())
    quantities = list(category_quantities.values())

    pie_chart = go.Pie(labels=categories, values=quantities)
    layout = go.Layout(title='Category-wise Analysis')
    figure = go.Figure(data=[pie_chart], layout=layout)
    chart_div = figure.to_html(full_html=False)

    return render(request, 'reports/category_analysis.html', {'chart_div': chart_div})


def stock_movement_analysis(request):
    # Fetch stock data
    stocks = Stock.objects.all()

    timestamps = [stock.timestamp for stock in stocks]
    receive_quantities = [stock.receive_quantity for stock in stocks]
    issue_quantities = [stock.issue_quantity for stock in stocks]

    receive_chart = go.Scatter(
        x=timestamps, y=receive_quantities, mode='lines', name='Received Quantity')
    issue_chart = go.Scatter(
        x=timestamps, y=issue_quantities, mode='lines', name='Issued Quantity')

    layout = go.Layout(title='Stock Movement Analysis',
                       xaxis=dict(title='Timestamp'),
                       yaxis=dict(title='Quantity'))

    figure = go.Figure(data=[receive_chart, issue_chart], layout=layout)

    chart_div = figure.to_html(full_html=False)

    return render(request, 'reports/stock_movement_analysis.html', {'chart_div': chart_div})


def combined_reports(request):
    # Inventory Overview Report
    stocks = Stock.objects.all()
    item_names = [stock.item_name for stock in stocks]
    quantities = [stock.quantity for stock in stocks]
    bar_chart = go.Bar(x=item_names, y=quantities)
    inventory_overview_chart = go.Figure(data=[bar_chart])

    # Inventory Trend Analysis Report
    timestamps = [stock.timestamp for stock in stocks]
    inventory_trend_chart = go.Figure(
        data=[go.Scatter(x=timestamps, y=quantities, mode='lines')])

    # Category-wise Analysis Report
    categories = Category.objects.all()
    category_names = [category.name for category in categories]
    category_quantities = [sum(stock.quantity for stock in Stock.objects.filter(
        category=category)) for category in categories]
    category_analysis_chart = go.Figure(
        data=[go.Pie(labels=category_names, values=category_quantities, hole=0.3)])

    # Stock Movement Analysis Report
    receive_quantities = [stock.receive_quantity for stock in stocks]
    issue_quantities = [stock.issue_quantity for stock in stocks]
    stock_movement_analysis_chart = go.Figure(data=[go.Scatter(x=timestamps, y=receive_quantities, mode='lines', name='Received Quantity'),
                                                    go.Scatter(x=timestamps, y=issue_quantities, mode='lines', name='Issued Quantity')])

    # Reorder Level Monitoring Report
    low_stock_items = [
        stock for stock in stocks if stock.quantity < stock.reorder_level]
    if low_stock_items:
        reorder_level_monitoring_alert = '<div style="background-color:red; padding: 10px; border-radius: 5px;">Some items are below the reorder level!</div>'
    else:
        reorder_level_monitoring_alert = '<div style="background-color:green; padding: 10px; border-radius: 5px;">All items are above the reorder level.</div>'

    return render(request, 'reports/combined_reports.html', {'inventory_overview_chart': inventory_overview_chart.to_html(full_html=False),
                                                             'inventory_trend_chart': inventory_trend_chart.to_html(full_html=False),
                                                             'category_analysis_chart': category_analysis_chart.to_html(full_html=False),
                                                             'stock_movement_analysis_chart': stock_movement_analysis_chart.to_html(full_html=False),
                                                             'reorder_level_monitoring_alert': reorder_level_monitoring_alert})


def download_inventory_data(request):
    stocks = Stock.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Item Name', 'Quantity'])
    for stock in stocks:
        writer.writerow([stock.item_name, stock.quantity])

    return response
