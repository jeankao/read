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
    ftype = received_annotation.get('ftype', 0)
    atype = received_annotation.get('atype', 0)
    del received_annotation['findex']
    del received_annotation['stuid']
    received_annotation.pop('ftype', None)
    received_annotation.pop('atype', None)
    # del received_annotation['ftype']
    # del received_annotation['atype']
    annotation = Annotation(user_id=request.user.id, ftype=ftype, findex=findex, stuid=stuid, atype=atype, annotation=json.dumps(received_annotation))
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
    # 只有自己可以刪除或修改自己的建立的標註資料
    annotation = Annotation.objects.get(id=annotation_id, user_id=request.user.id)
    if request.method == "DELETE":
      result = annotation
      annotation.delete()
      response = HttpResponse(status=204)
    elif request.method == "PUT": # 修改標註
      received_annotation = json.loads(request.body)
      # 這幾個欄位應該不會變
      # findex = received_annotation['findex']
      # stuid = received_annotation['stuid']
      # ftype = received_annotation.get('ftype', 0)
      atype = received_annotation.get('atype', 0)
      del received_annotation['findex']
      del received_annotation['stuid']
      received_annotation.pop('ftype', None)
      received_annotation.pop('atype', None)
      # del received_annotation['ftype']
      # del received_annotation['atype']
      annotation.atype = atype
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
  ftype = request.GET.get('ftype', default=0)  
  findex = request.GET.get('findex')
  stuid = request.GET.get('stuid')
  annotations = [a for a in Annotation.objects.filter(ftype=ftype, findex=findex, stuid=stuid).order_by('id')]
  total = len(annotations)
  rows = []
  for annotation in annotations:
    anno = json.loads(annotation.annotation)
    anno['id'] = annotation.id
    anno['atype'] = annotation.atype
    user = User.objects.filter(id=annotation.user_id)[0]
    anno['supervisor'] = user.first_name
    rows.append(anno)
  data = {
    "total": total, 
    "rows": rows,
  }
  return JsonResponse(data, safe=False)