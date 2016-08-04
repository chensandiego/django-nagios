from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from data_collector.models import DataPoint,Alert 
from django.core.urlresolvers import reverse
from django.views.generic import CreateView,UpdateView,DeleteView

class StatusView(TemplateView):
	template_name='status.html'

	def get_context_data(self,**kwargs):
		ctx = super(StatusView,self).get_context_data(**kwargs)

		nodes_and_data_types = DataPoint.objects.all().values('node_name','data_type').distinct()

		status_data_dict = dict()
		for nodes_and_data_type_pair in nodes_and_data_types:
			node_name=nodes_and_data_type_pair['node_name']
			data_type=nodes_and_data_type_pair['data_type']

			data_point_map=status_data_dict.setdefault(node_name,dict())
			data_point_map[data_type] = DataPoint.objects.filter(node_name=node_name,data_type=data_type).latest('datetime')

			ctx['status_data_dict']=status_data_dict
			return ctx 


class AlertListView(ListView):
	template_name='alerts_list.html'
	model =Alert 

class NewAlertView(CreateView):
	template_name='create_or_update_alert.html'
	model=Alert 
	fields=[
		'data_type','min_value','max_value','node_name','is_active'
	]
	def get_success_url(self):
		return reverse('alerts-list')


class EditAlertView(UpdateView):
	template_name='create_or_update_alert.html'
	model=Alert 
	fields=[
		'data_type','min_value','max_value','node_name','is_active'
	]

	def get_success_url(self):
		return reverse('alerts-list')

class DeleteAlertView(DeleteView):
	template_name='delete_alert.html'
	model=Alert 

	def get_success_url(self):
		return reverse('alerts-list')