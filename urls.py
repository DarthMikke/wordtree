import wordtree.views as views
from django.urls import include, path

urlpatterns = [
	path('image/<str:word_pks>.png', views.image),
	path('index.html', views.index),
	path('tree.html', views.tree, name='word_tree'),
	path('api/autofill', views.search),
]
