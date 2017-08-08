# -*- coding: UTF-8 -*-

from django.http import JsonResponse
from django.http.response import HttpResponse, HttpResponseRedirectBase, HttpResponseNotFound
from django.utils import timezone
from django.contrib.auth.models import User
from models import Annotation
import json

class HttpResponseSeeOtherRedirect(HttpResponseRedirectBase):
  status_code = 303

def root(request):
  return JsonResponse({
    "name":"Annotation Store API",
    "version": "0.1",
  }, safe=False)

def annotations(request):
  if request.method == "POST":
    received_annotation = json.loads(request.body)
    findex = received_annotation['findex']
    stuid = received_annotation['stuid']
    del received_annotation['findex']
    del received_annotation['stuid']
    annotation = Annotation(user_id=request.user.id, findex=findex, stuid=stuid, annotation=json.dumps(received_annotation))
    annotation.save()
    return HttpResponseSeeOtherRedirect('/annotate/annotations/'+str(annotation.id))

  # 取得目前使用者所有標註資料。(理論上不會執行到這邊，應該會從 search 僅取得目前頁面的標註資料)
  annotations = [a for a in Annotation.objects.filter(user_id=request.user.id).order_by('id')]
  rows = []
  for annotation in annotations:
    rows.append(json.loads(annotation.annotation))
  return JsonResponse(rows, safe=False)

#
#
#
def single_annotation(request, annotation_id):
  try: 
    annotation = Annotation.objects.get(id=annotation_id, user_id=request.user.id)
    if request.method == "DELETE":
      result = annotation
      annotation.delete()
      response = HttpResponse(status=204)
    elif request.method == "PUT":
      received_annotation = json.loads(request.body)
      findex = received_annotation['findex']
      stuid = received_annotation['stuid']
      del received_annotation['findex']
      del received_annotation['stuid']
      annotation.annotation = json.dumps(received_annotation)
      annotation.updated = timezone.now()
      annotation.save()
      response = HttpResponseSeeOtherRedirect('/annotate/annotations/'+str(annotation.id))
    else: # GET
      result = json.loads(annotation.annotation)
      user = User.objects.filter(id=annotation.user_id)[0]
      result['id'] = annotation.id
      result['supervisor']=user.first_name
      response = JsonResponse(result, safe=False)
  except Annotation.DoesNotExist:
    response = HttpResponseNotFound()
  return response

#
#
#
def search(request):
  findex = request.GET.get('findex')
  stuid = request.GET.get('stuid')
  annotations = [a for a in Annotation.objects.filter(findex=findex, stuid=stuid).order_by('id')]
  total = len(annotations)
  rows = []
  for annotation in annotations:
    anno = json.loads(annotation.annotation)
    anno['id'] = annotation.id
    user = User.objects.filter(id=annotation.user_id)[0]
    anno['supervisor'] = user.first_name
    rows.append(anno)
  data = {
    "total": total, 
    "rows": rows,
  }
  return JsonResponse(data, safe=False)