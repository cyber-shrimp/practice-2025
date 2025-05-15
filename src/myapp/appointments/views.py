from datetime import datetime
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.duration import duration_string
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from appointments.models import Appointment
from django.forms import model_to_dict
import sqlite3 as sl





class AppointmentsApiView(APIView):
    def get(self, request):
        try:
            if request.data['id']:
                return Response([x for x in Appointment.objects.all().values() if x['id'] == request.data['id']])
        except KeyError:
            return Response(Appointment.objects.all().values())

    def post(self, request):
        print(request.data)
        post_new = Appointment.objects.create(
            place=request.data['place'],
            initiator=request.data['initiator'],
            guest=request.data['guest'],
            date=datetime.strptime(request.data['date'], "%Y-%m-%dT%H:%M:%SZ"),
        )
        return Response({'post': model_to_dict(post_new)})

    def delete(self, request):
        conn = sl.connect('db.sqlite3')
        delete_post = [x for x in Appointment.objects.all().values() if x['id'] == request.data['id']]
        conn.execute(f'DELETE FROM appointments_appointment WHERE id = {data["id"]}')
        conn.commit()
        conn.close()

        return Response({'delete': delete_post})

    def put(self, request):
        conn = sl.connect('db.sqlite3')
        # delete_post = conn.execute('SELECT place, initiator, guest, date FROM appointments_appointment WHERE id = ?', (request.data['id'], ))
        conn.execute('UPDATE appointments_appointment SET place = ?, initiator = ?, guest = ?, date = ? WHERE id = ?', (request.data['place'], request.data['initiator'], request.data['guest'], datetime.strptime(request.data['date'], "%Y-%m-%dT%H:%M:%SZ"), request.data['id']))
        conn.commit()
        conn.close()
        return Response({'put': request.data})


# Create your views here.
