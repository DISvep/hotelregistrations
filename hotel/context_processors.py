from .forms import RoomFilterForm


def search_form_processor(request):
    return {'filter_form': RoomFilterForm()}
