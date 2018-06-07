from carpark import views
from taxi.decorators import group_required


from django.conf.urls import url

urlpatterns = [
    url("^create", group_required('Manager')(views.CarFormView.as_view()), name="create_car"),
    url("^add-driver", group_required('Manager')(views.AddDriverFormView.as_view()), name="add_driver"),
    url("^add-trip", group_required('Client')(views.AddTripFormView.as_view()), name="add_trip"),
    url("^non-accepted-trips", group_required('Driver')(views.NonAcceptedTripsView.as_view()), name="non_trip"),
    url("^accept-trip/(?P<trip_id>\d+)", group_required('Driver')(views.AcceptTripView.as_view()), name="accept"),
    url("^close-trip/(?P<trip_id>\d+)", group_required('Driver')(views.CloseTripView.as_view()), name="close"),
     url("^non-closed-trips", group_required('Driver')(views.NonClosedTripsView.as_view()), name="nonclosed_trips")
]
