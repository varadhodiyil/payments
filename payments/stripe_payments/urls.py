from django.urls import path
from payments.stripe_payments import views

urlpatterns = [
	path('add_card/', views.CreatePaymentMethod.as_view() , name="create_card"),
	path('cards/', views.CardDetails.as_view() , name="get_cards"),
	path('set_default/', views.SetDefaultCard.as_view() , name="set_default"),
]