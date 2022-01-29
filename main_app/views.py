from django.shortcuts import render
from django.views import View
from .models import Room

class HomePage(View):
    template_name = 'main_app/home_page.html'

    def get(self, request):
        return render(request, self.template_name)


class AddRoom(View):
    template_name = 'main_app/add_room.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('room-name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')

        if projector:
            projector = True
        else:
            projector = False

        all_rooms = Room.objects.all()
        all_rooms_names = []

        for room in all_rooms:
            all_rooms_names.append(room.name)

        message_error = ''
        if name in all_rooms_names:
            message_error += 'This name is already in use. Choose other name.\n'
        if not name:
            message_error += 'Name of room can\'t be empty'

