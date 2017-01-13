
from django.conf.urls import url,include

from elastic.views import *


urlpatterns = [
    

    url(r'^api/func_hello/?$', func_hello ),
    url(r'^api/elastic/?$', elastic ),
    url(r'^api/deleteInput/?$', deleteInput ),
    url(r'^api/oneByOneInput/?$', oneByOneInput ),
    url(r'^api/addingToDb/?$', addingToDb ),
    url(r'^api/retrieve/?$', retrieve ),
    url(r'ui/index.html/?$',indexUI),
    url(r'ui/deleteIndex.html/?$',deleteIndex),
    url(r'ui/oneByOne.html/?$',oneByOne),
    url(r'ui/dbInput.html/?$',dbin),
    url(r'ui/retrieve.html/?$',retrievehtml),
    

]
