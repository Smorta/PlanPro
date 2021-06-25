import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from Achat.models import Responsable, User, Chantier, Modification, Phase
from datetime import datetime, timedelta, date
from django.db import connection
from Achat.timeline import Timeline

def refreshSchedule(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            id_phase = request.POST.get("ID")
            id_phase = id_phase.split("-")[1]
            phase = Phase.objects.get(pk=id_phase)
            id_chantier = request.POST.get('GR')
            chantier = Chantier.objects.get(pk=id_chantier)
            colStart = request.POST.get('DGA').split("/")[1]
            colEnd = request.POST.get('GC').split("/")[0]
            delay = int(colEnd) - int(colStart)
            Debut = phase.Date_debut
            Fin = phase.Deadline
            phase.Date_debut = Debut + timedelta(days=delay * 7)
            phase.Deadline = Fin + timedelta(days=delay * 7)
            phase.id_chantier = chantier
            phase.save()
            return JsonResponse({"success": True}, status=200)
        except KeyError:
            HttpResponseServerError("Malformed data!")

        return JsonResponse({"success": True}, status=200)

    else:
        return JsonResponse({"success": False}, status=400)

def acheteursChantier(chantier):
    with connection.cursor() as cursor:
        cursor.execute('SELECT DISTINCT id FROM Achat_responsable NATURAL JOIN (SELECT DISTINCT responsable_id As id FROM  Achat_phase NATURAL JOIN (SELECT phase_id AS id , responsable_id FROM Achat_phase_id_Responsable) WHERE id_chantier_id = '+str(chantier.id)+')')
        row = cursor.fetchall()
    return row

def schedule(request,Year,Month,Day):
    if request.session.get('connected') == 'true':

        chantiers = Chantier.objects.order_by('Name')
        i = 0
        chantier_list = list()
        begin = date(int(Year), int(Month), int(Day))
        weekList = Timeline(begin).WeekList
        for chant in chantiers:
            acheteurList = list()
            acheteur = acheteursChantier(chant)
            j = 0
            for A in acheteur:
                phases = Phase.objects.filter(id_chantier=chant.id).filter(id_Responsable=A[0]).exclude(Date_debut=None).order_by('Name')
                Self = Responsable.objects.get(pk=A[0])
                timeline = Timeline(begin)
                for phase in phases:
                    timeline.addTask(phase)
                acheteurList.append({"self": Self, "timeline": timeline, "num": j})
                j += 1

            if i%3 == 0:
                l = list()
                chantier_list.append(l)
                k=2

            if (len(acheteurList) > 1):
                row = [k, (k + len(acheteurList))]
                k += len(acheteurList)

            else:
                row = [k, (k + 1)]
                k += 1

            chantier_list[int(i/3)].append({"self": chant, "acheteurList": acheteurList, "row": row})
            i += 1

        context = {
            'WeekList': weekList,
            'chantier_list': chantier_list,
            'connected': request.session.get('connected'),
        }
        return render(request, 'timeline.html', context)
    else:
        return redirect('/Home')