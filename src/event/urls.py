from django.urls import path
import event.views as v_

app_name = 'event'

urlpatterns = [
    path('', v_.EventListView.as_view(), name='event_list'),
#   Managers
    path('management/', v_.ManagerOptions.as_view(), name='manager_options'),
#   Event
    path('create/', v_.EventCreateView.as_view(), name='create_event'),
    path('<slug:slug>/', v_.EventDetailView.as_view(), name='dashboard'),
    path('<slug:slug>/assign-supplier/', v_.EventAssignSupplier.as_view(), name='assign_supplier'),
    path('<slug:slug>/assign-logistics-user/', v_.EventAssignLogisticsStaff.as_view(), name='assign_logistics_user'),
    path('<slug:slug>/close-event/', v_.EventCloseView.as_view(), name='close_event'),
#   Worker urls below this line
    path('<slug:slug>/worker/', v_.WorkerSearch.as_view(), name='worker_search'),
    path('<slug:slug>/worker/create/', v_.WorkerCreate.as_view(), name='worker_create'),
    path('<slug:slug>/worker/bulk-create/', v_.WorkerBulkCreate.as_view(), name='worker_bulk_create'),
    path('<slug:slug>/worker/<int:id>/', v_.WorkerDetail.as_view(), name='worker_detail'),
    path('<slug:slug>/worker/<int:id>/edit/', v_.WorkerUpdate.as_view(), name='worker_update'),
    path('<slug:slug>/worker/<int:id>/accredit/', v_.WorkerAccredit.as_view(), name='worker_accredit'),
]