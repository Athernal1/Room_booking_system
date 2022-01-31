from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from .models import Room


class HomePage(View):
    template_name = 'main_app/home_page.html'

    def get(self, request):
        rooms = Room.objects.all()
        return render(request, self.template_name, context = {'rooms': rooms})


class AddRoom(View):
    template_name = 'main_app/add_room.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('room-name')
        capacity = request.POST.get('capacity')
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get('projector')

        if projector:
            projector = True
        else:
            projector = False

        all_rooms = Room.objects.all()
        all_rooms_names = []

        for room in all_rooms:
            all_rooms_names.append(room.name)

        if name in all_rooms_names:
            error = 'This name is already in use. Choose other name.'
            return render(request, self.template_name, context = {'error': error})
        if not name or name == '':
            error = 'Room name can\'t be empty'
            return render(request, self.template_name, context={'error': error})
        if capacity <= 0:
            error = 'Capacity can\'t be so low'
            return render(request, self.template_name, context={'error': error})

        Room.objects.create(name=name, capacity=capacity, projector=projector)

        return redirect('/')


class DeleteRoom(View):
    def get(self, request, pk):
        room = Room.objects.get(pk=pk)
        room.delete()
        return redirect('/')


class ModifyRoom(View):
    template_name = 'main_app/modify_room.html'

    def get(self, request, pk):
        room = Room.objects.get(pk=pk)
        return render(request, self.template_name, context={'room': room})

    def post(self, request, pk):
        room = Room.objects.get(pk=pk)

        name = request.POST.get('room-name')
        capacity = request.POST.get('capacity')
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get('projector')

        if projector:
            projector = True
        else:
            projector = False

        all_rooms = Room.objects.all()
        all_rooms_names = []
        for room in all_rooms:
            all_rooms_names.append(room.name)

        if name != room.name:
            if name in all_rooms_names:
                error = 'This name is already in use. Choose other name.'
                return render(request, self.template_name, context = {'error': error})
        if not name or name == '':
            error = 'Room name can\'t be empty'
            return render(request, self.template_name, context={'error': error})
        if capacity <= 0:
            error = 'Capacity can\'t be so low'
            return render(request, self.template_name, context={'error': error})

        room.name = name
        room.capacity = capacity
        room.projector = projector
        room.save()

        return redirect('/')
