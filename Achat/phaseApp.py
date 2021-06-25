import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from Achat.models import Responsable, User, Chantier, Modification, Phase
from . import forms, chantierApp
from datetime import datetime, timedelta, date
from django.db import connection
from decimal import Decimal
from Achat.timeline import Timeline

def New(request, chant_id, typePhase):
    if request.session.get('connected') == 'true':
        responsable_list = Responsable.objects.order_by('Name')
        if request.method == 'POST':
            form = forms.PhaseForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['inputName']
                type = form.cleaned_data['inputType']
                debut = form.cleaned_data['inputDebut']
                objectif = form.cleaned_data['inputObjectif']
                state = form.cleaned_data['inputState']
                chantier = Chantier.objects.get(pk=chant_id)
                phase = Phase.objects.get_or_create(
                    Name=name,
                    Type=type,
                    State=state,
                    num=0,
                    Date_debut=debut,
                    Deadline=objectif,
                    id_chantier=chantier)[0]
                Acheteurs = request.POST.getlist("Resp")
                for A in Acheteurs:
                    Resp = Responsable.objects.get(pk=A)
                    phase.id_Responsable.add(Resp)
                phase.save()
                return redirect('/Chantier/Modif/' + chant_id)
            else:
                print(form.errors.items())

        form_list = forms.PhaseForm()

        context = {
            'form': form_list,
            'typePhase': typePhase,
            'responsableList': responsable_list,
            'id_chant': chant_id,
            'connected': request.session.get('connected'),
        }
        return render(request, 'PhaseNew.html', context)
    else:
        return redirect('/Home')


def Modif(request, phase_id):
    if request.session.get('connected') == 'true':
        phase = Phase.objects.get(pk=phase_id)
        Name = phase.Name
        Type = phase.Type
        Debut = phase.Date_debut
        Objectif = phase.Deadline
        State = phase.State
        chant_id = phase.id_chantier.id
        responsable_list = Responsable.objects.order_by('Name')
        phaseRespList = phase.id_Responsable.all()
        year = request.session['year']
        month = request.session['month']
        day = request.session['day']
        begin = date(int(year), int(month), int(day))
        weekList = Timeline(begin).WeekList

        if request.method == 'POST':
            form = forms.PhaseForm(request.POST)
            print('hello world')
            if form.is_valid():
                print('coucou')
                Name = form.cleaned_data['inputName']
                Type = form.cleaned_data['inputType']
                Debut = form.cleaned_data['inputDebut']
                Objectif = form.cleaned_data['inputObjectif']
                State = form.cleaned_data['inputState']
                Acheteurs = request.POST.getlist("Resp")
                phase.Name = Name
                phase.Type = Type
                phase.Date_debut = Debut
                phase.Deadline = Objectif
                phase.State = State
                for phaseResp in phaseRespList:
                    if phaseResp.id not in Acheteurs:
                        phase.id_Responsable.remove(phaseResp)
                for A in Acheteurs:
                    Resp = Responsable.objects.get(pk=A)
                    phase.id_Responsable.add(Resp)
                chantierRespList = phase.id_Responsable.all()
                phase.save()
                return redirect('../../Chantier/Modif/' + str(phase.id_chantier.id))
            else:
                print(form.errors.items())

        form_list = forms.PhaseForm(initial={
            'inputName': Name,
            'inputType': Type,
            'inputDebut': Debut,
            'inputObjectif': Objectif,
            'inputState': State,
        })

        context = {
            'form': form_list,
            'phase': phase,
            'id_chant': chant_id,
            'typePhase': phase.Type,
            'connected': request.session.get('connected'),
            'responsableList': responsable_list,
            'phaseRespList': phaseRespList,
            'WeekList': weekList,
            'schedule': chantierApp.Getschedule(begin, phase.id_chantier),
        }
        return render(request, 'Phase.html', context)
    else:
        return redirect('/Home')

def Delete(request, phase_id):
    if request.session.get('connected') == 'true':
        phase = Phase.objects.get(pk=phase_id)
        chant_id = phase.id_chantier
        context = {
            "id_chant": chant_id,
            "id_phase": phase_id
        }
        if request.method == 'POST':
            phase.delete()
            return redirect('/Chantier/Modif/' + str(chant_id.id))
        return render(request, 'DeletePhase.html', context)
    else:
        return redirect('/Home')