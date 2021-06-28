import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from Achat.models import Responsable, User, Chantier, Modification, Phase
from datetime import datetime, timedelta, date
from . import forms, phaseApp
import calendar
from django.db import connection
from Achat.timeline import Timeline


def refreshSchedule(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            id_phase = request.POST.get("ID")
            id_phase = id_phase.split("-")[1]
            phase = Phase.objects.get(pk=id_phase)
            idRespEnd = request.POST.get('DataDrop')
            acheteurEnd = Responsable.objects.get(pk=idRespEnd)
            idRespStart = request.POST.get('DataDrag')
            acheteurStart = Responsable.objects.get(pk=idRespStart)
            colStart = request.POST.get('DGA').split("/")[1]
            colEnd = request.POST.get('GC').split("/")[0]
            delay = int(colEnd) - int(colStart)
            Debut = phase.Date_debut
            Fin = phase.Deadline
            phase.Date_debut = Debut + timedelta(days=delay * 7)
            phase.Deadline = Fin + timedelta(days=delay * 7)
            if(acheteurStart != acheteurEnd):
                phase.id_Responsable.add(acheteurEnd)
                phase.id_Responsable.remove(acheteurStart)
            phase.save()
            return JsonResponse({"success": True}, status=200)
        except KeyError:
            HttpResponseServerError("Malformed data!")

        return JsonResponse({"success": True}, status=200)

    else:
        return JsonResponse({"success": False}, status=400)

def chantierAcheteur(resp_id):
    with connection.cursor() as cursor:
        request = 'SELECT DISTINCT id_chantier_id FROM Achat_phase NATURAL JOIN (SELECT phase_id AS id FROM Achat_phase_id_Responsable WHERE responsable_id = ' + str(resp_id) + ' )'
        cursor.execute(request)
        row = cursor.fetchall()
    return row

def schedule(request, Year, Month, Day):
    if request.session.get('connected') == 'true':
        responsable_list = Responsable.objects.order_by('Name')
        acheteur = Responsable.objects.order_by('Name')
        acheteur_list = list()
        begin = date(int(Year), int(Month), int(Day))
        weekList = Timeline(begin).WeekList
        i = 0
        k = 2
        for resp in acheteur:
            chantier_list = list()
            chantiers = chantierAcheteur(resp.id)
            j=0
            for chant in chantiers:
                phases = Phase.objects.filter(id_Responsable=resp.id).filter(id_chantier=chant[0]).order_by('Name')
                Self = Chantier.objects.get(pk=chant[0])
                timeline = Timeline(begin)
                for phase in phases:
                    timeline.addTask(phase)
                chantier_list.append({"self": Self, "timeline": timeline,'num':j})
                j += 1

            if i%3 == 0:
                l = list()
                acheteur_list.append(l)
                k = 2

            if(len(chantier_list)>1):
                row = [k, (k + len(chantier_list))]
                k += len(chantier_list)

            else:
                row = [k, (k + 1)]
                k += 1
            acheteur_list[int(i / 3)].append({"self": resp, "chantierList": chantier_list, "row": row})
            i += 1
        context = {
            'WeekList': weekList,
            'acheteurList': acheteur_list,
            'connected': request.session.get('connected'),
            'responsableList': responsable_list,
            'form' : forms.PhaseForm
        }
        return render(request, 'timelineAcheteur.html', context)
    else:
        return redirect('/Home')

def addMonths(inputDate, month):
    tmpMonth = inputDate.month - 1 + month
    # Add floor((input month - 1 + k)/12) to input year component to get result year component
    resYr = inputDate.year + tmpMonth // 12
    # Result month component would be (input month - 1 + k)%12 + 1
    resMnth = tmpMonth % 12 + 1
    # Result day component would be minimum of input date component and max date of the result month (For example we cant have day component as 30 in February month)
    # Maximum date in a month can be found using the calendar module monthrange function as shown below
    resDay = min(inputDate.day, calendar.monthrange(resYr, resMnth)[1])
    # construct result datetime with the components derived above
    resDate = date(resYr, resMnth, resDay)

    return resDate

def setDateTimeline(request, Data):

    Data = int(Data)
    if Data == 0:
        request.session['year'] = str(date.today().year)
        request.session['month'] = str(date.today().month)
        request.session['day'] = str(date.today().day)

    else:
        actualDate = date(int(request.session['year']), int(request.session['month']), int(request.session['day']))
        newDate = addMonths(actualDate,Data)
        request.session['year'] = str(newDate .year)
        request.session['month'] = str(newDate .month)
        request.session['day'] = str(newDate .day)

    return redirect("/TimelineAcheteur/" + request.session['year'] + "/" + request.session['month'] + "/" + request.session['day'])