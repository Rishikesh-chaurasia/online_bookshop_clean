from django.urls import path
from .import views
urlpatterns =[
   path('userdash/',views.userdash,name='userdash'),
   path('userlogout/',views.userlogout,name='userlogout'),
   path('userprofile/',views.userprofile,name='userprofile'),
   path('editprofile/',views.editprofile,name='editprofile'),
   path('cart/',views.cart,name='cart'),
   path('order/',views.order,name='order'),
   path('change_password/',views.change_password,name='change_password'),
   path('addtocart/<bid>',views.addtocart,name='addtocart'),
   path('updateitem/<id><operator>',views.updateitem,name='updateitem'),
   path('checkout/',views.checkout,name='checkout'),
   path('payment-success/',views.payment_success,name='payment_success'),
   path('removeitem/<id>',views.removeitem,name='removeitem'),
   path("create-admin/", views.create_admin),
]