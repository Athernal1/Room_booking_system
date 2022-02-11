import datetime

from django.shortcuts import render, redirect
from django.views import View

from .models import Room, Reservation


class HomePage(View):
    template_name = 'main_app/home_page.html'
    ctx = {}

    def get(self, request):
        rooms = Room.objects.all()
        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.reservation_set.all()]
            room.reserved = datetime.date.today() not in reservation_dates
        self.ctx['rooms'] = rooms
        return render(request, self.template_name, self.ctx)


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

        return redirect('home-page')


class DeleteRoom(View):

    def get(self, request, pk):
        room = Room.objects.get(pk=pk)
        room.delete()
        return redirect('home-page')


class ModifyRoom(View):
    template_name = 'main_app/modify_room.html'
    ctx ={}

    def get(self, request, pk):
        room = Room.objects.get(pk=pk)
        self.ctx['room'] = room
        return render(request, self.template_name, self.ctx)

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
                self.ctx['error'] = error
                return render(request, self.template_name, self.ctx)
        if not name or name == '':
            error = 'Room name can\'t be empty'
            self.ctx['error'] = error
            return render(request, self.template_name, self.ctx)
        if capacity <= 0:
            error = 'Capacity can\'t be so low'
            self.ctx['error'] = error
            return render(request, self.template_name, self.ctx)

        room.name = name
        room.capacity = capacity
        room.projector = projector
        room.save()

        return redirect('home-page')


class MakeReservation(View):
    template_name = 'main_app/reservation.html'
    ctx = {}

    def get(self, request, pk):
        room = Room.objects.get(pk=pk)
        reservations = room.reservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')

        self.ctx['room'] = room
        self.ctx['reservations'] = reservations

        return render(request, self.template_name, self.ctx)

    def post(self, request, pk):
        room = Room.objects.get(pk=pk)
        self.ctx['room'] = room
        reservation_date = request.POST.get('reservation-date')
        note = request.POST.get('comment')

        if reservation_date < str(datetime.date.today()-datetime.timedelta(days=1)):
            self.ctx['error'] = "The reservation date is in the past!"
            return render(request, self.template_name, self.ctx)
        if Reservation.objects.filter(room=room.id, date=reservation_date):
            self.ctx['error'] = "This room is already reserved."
            return render(request, self.template_name, self.ctx)

        Reservation.objects.create(date=reservation_date, note=note, room=room)
        return redirect('home-page')


class RoomDetails(View):
    template_name = 'main_app/room_details.html'
    ctx = {}

    def get(self, request, pk):
        room = Room.objects.get(pk=pk)
        reservations = room.reservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')
        self.ctx['room'] = room
        self.ctx['reservations'] = reservations

        return render(request, self.template_name, self.ctx)


class Search(View):
    template_name = 'main_app/home_page.html'
    ctx = {}

    def get(self, request):
        name = request.GET.get('room-name')
        capacity = request.GET.get('capacity')
        capacity = int(capacity) if capacity else 0
        projector = request.GET.get('projector')

        if projector:
            projector = True
        else:
            projector = False

        rooms = Room.objects.all()

        if projector:
            rooms = rooms.filter(projector=projector)
        if capacity:
            rooms = rooms.filter(capacity__gte=capacity)
        if name:
            rooms.filter(name__contains=name)

        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.reservation_set.all()]
            room.reserved = str(datetime.date.today()) not in reservation_dates

        self.ctx['rooms'] = rooms
        self.ctx['date'] = datetime.date.today()

        return render(request, self.template_name, self.ctx)
