from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import SalesSearch
import pandas as pd
from .utils import get_salesman_from_id, get_customer_from_id, get_chart
from reports.forms import ReportForm


from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def home_view(request):
	search_form = SalesSearch(request.POST or None)
	report_form = ReportForm()
	sales_df = None
	position_df = None
	merged_df = None
	chart = None
	df = None
	no_data = None
	if request.method == 'POST':
		date_from = request.POST.get('date_from')
		date_to = request.POST.get('date_to')
		chart_type = request.POST.get('chart_type')
		results_by = request.POST.get('results_by')

		# print(date_from, date_to, char`t_type)

		sale_qs = Sale.objects.filter(created_date__date__lte =date_to, created_date__date__gte=date_from)
		if len(sale_qs)>0:
			sales_df = pd.DataFrame(sale_qs.values())
			sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
			sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)

			sales_df['created_date'] = sales_df['created_date'].apply(lambda x: x.strftime('%d-%m-%y'))
			sales_df['updated_date'] = sales_df['updated_date'].apply(lambda x: x.strftime('%d-%m-%y'))
			sales_df.rename({'created_date':'created'}, axis=1, inplace=True)
			sales_df.rename({'updated_date':'updated'}, axis=1, inplace=True)

			sales_df.rename({'customer_id':'customer', 'salesman_id':'salesman', 'id':'sales_id'}, axis=1, inplace=True)
			# sales_df['sales_id'] = sales_df['id']
			position_data = []
			for sale in sale_qs:
				for pos in sale.get_positions():
					obj = {
						'position_id':pos.id,
						'product':pos.product.name,
						'quantity':pos.quantity,
						'price': pos.price,
						'sales_id':pos.get_sales_id(),

					}
					position_data.append(obj)

			position_df = pd.DataFrame(position_data)
			merged_df = pd.merge(sales_df, position_df, on='sales_id')

			df = merged_df.groupby('transaction_id', as_index=False)['price'].agg('sum')

			chart = get_chart(chart_type, sales_df, results_by)
			print('Chart', chart)

			position_df = position_df.to_html()


			sales_df = sales_df.to_html()
			merged_df = merged_df.to_html()
			df = df.to_html()
		else:
			no_data = 'Here has no selling data available.'

	context = {
		'sales_df': sales_df,
		'search_form':search_form,
		'report_form':report_form,
		'position_df':position_df,
		'merged_df':merged_df,
		'df':df,
		'chart':chart,
		'no_data':no_data,
	}
	return render(request, 'sales/home.html', context)


class SalesListView(LoginRequiredMixin,ListView):

	model = Sale
	template = 'sales/sale_list.html'

class SalesDetailView(LoginRequiredMixin, DetailView):
	model = Sale
	template_name = 'sales/model_detail.html'