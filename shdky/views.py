from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.http import HttpResponse #,HttpResponseRedirect
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
#from demoweb.views import HomePageView
from django.views.generic import TemplateView

import numpy as np
import pandas as pd
import keras
from keras.models import load_model
import matplotlib.pyplot as plt

from license_check.license_chk import license_check, lic_loc_chk
#@login_required
#def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")
#    return HttpResponseRedirect("https://www.avarun.cn/stocksdemo")

class IndexView(TemplateView):
    template_name='shdky/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['license_chk_message'] = license_check()
        context['lic_loc_chk_msg'] = lic_loc_chk()
        return context


class VTrainSimuView(TemplateView):
    template_name='shdky/v_train_simu.html'
#    template_name='shdky/v_train_simu.html'
    from bokeh.layouts import column
    from bokeh.models import CustomJS, ColumnDataSource, Slider, CDSView, IndexFilter, HoverTool
    from bokeh.plotting import Figure, output_file, show
    from bokeh.embed import components

    R=pd.read_csv('/home/techstar/demoweb/shdky/static/shdky/V_test.csv',index_col=0)
    shuffler= np.random.permutation(len(R))
    R=R.take(shuffler)
#    df = R.iloc[:100,:]
    df = R.reset_index()
    source = ColumnDataSource(data=df)
#    view = CDSView(source=source, filters=[IndexFilter(list(range(100)))])
    hover = HoverTool(tooltips=[
        ("index", "$index"),
        ("date", "@time"),
        ("(V_True,V_Pred)", "(@V_true, @V_pred)")
    ])

    tools = ["box_select", hover, "reset"]
    plot = Figure(plot_width=800, plot_height=300, tools=tools, x_range=(0,100))
#    plot.line('index', 'V_true', source=source, view = view, line_width=2, line_alpha=0.3, line_color="red")
    plot.line('index', 'V_true', source=source, line_width=2, line_alpha=0.3, line_color="red")
    plot.line('index', 'V_pred', source=source, line_width=2, line_alpha=0.3, line_color="blue")
    
    callback = CustomJS(args=dict(xr=plot.x_range), code="""
        var a = 0 + cb_obj.value;
        var b = 100 + cb_obj.value;
        xr.start = a;
        xr.end = b;
    """)
    
    slider = Slider(start=0, end=399, value=1, step=1, title="power")
    slider.js_on_change('value', callback)

    layout = column(slider, plot)
    #show(layout)

    script,div = components(layout)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['script'] = self.script
        context['div'] = self.div
        return context


'''
    def get(self, request, *args, **kwargs):
        model = load_model('wanke1V.h5')
        R=pd.read_csv('V_test.csv',index_col=0)
        fig = plt.figure()

        return render (request,self.template_name,self.get_context_data())

'''

class VSimuView(TemplateView):
    template_name='shdky/v_simu.html'


class PGMonitor(TemplateView):
    template_name='shdky/pg_monitor.html'
    from bokeh.layouts import column
    from bokeh.models import CustomJS, ColumnDataSource, Slider, CDSView, IndexFilter, HoverTool
    from bokeh.plotting import Figure, output_file, show
    from bokeh.embed import components
    from bokeh.models.sources import AjaxDataSource
    #source = AjaxDataSource(data_url='https://182.150.63.68:10443/static/test.json',method='GET') # failed
    #source = AjaxDataSource(data_url='http://localhost:9090/static/test.json',method='GET') # failed, it seems unsuccessful when serving files directly
    source = AjaxDataSource(data_url='https://182.150.63.68:10443/shdky/pg_ajax',method="GET",polling_interval=5000)
    #data = {
    #    'x' : [1, 2, 3],
    #    'y' : [9, 3, 2]
    #    }
    #source = ColumnDataSource(data=data)    
    p = Figure(plot_width=800, plot_height=300,x_axis_type="datetime")
    p.line('time', 'AMBIENT_TEMPERATURE', source=source, line_width=2, line_alpha=0.3, line_color="red")
    layout = column(p)
    script,div = components(layout)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['script'] = self.script
        context['div'] = self.div
        return context





def upload_ajax(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        import os
        f = open("/home/techstar/demoweb/static/shdky/"+ file_obj.name , 'wb')
#        print(file_obj,type(file_obj))
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
#        print('11111')
        return HttpResponse('OK')
    return HttpResponse('Get method used or somthing wrong')




def v_simu_table(request):
    from io import StringIO
    tb = StringIO()
    df = pd.read_csv('/home/techstar/demoweb/shdky/static/shdky/V_test.csv',index_col=0)
    df = df[:10]
    df.to_html(tb)
    return HttpResponse(tb.getvalue())

def pg_ajax(request):
#    if request.method == 'POST':
    import json
#    J={ 'x' : [np.random.randint(5), np.random.randint(5), np.random.randint(5)],
#        'y' : [np.random.randint(3), np.random.randint(3), np.random.randint(3)]}
#    J={'x' : [1, 2, 3],'y' : [9, 3, 2]}
    df = pd.read_csv('/home/techstar/demoweb/static/powerplant.csv',index_col=0)
    df.index=pd.to_datetime(df.index)
    df['time']=pd.to_datetime(df.index)
    df['time']=df['time'].apply(lambda x: x.value/1000000)
    J = {S: list(df[S].values) for S in df}
    return HttpResponse(json.dumps(J))
#    return HttpResponse('Get method used or somthing wrong')
 

