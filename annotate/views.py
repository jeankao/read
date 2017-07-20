# -*- coding: UTF-8 -*-

from django.http import JsonResponse
from django.http.response import HttpResponse, HttpResponseRedirectBase, HttpResponseNotFound
from django.utils import timezone
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
    page_path = received_annotation['page_path']
    del received_annotation['page_path']
    annotation = Annotation(user_id=request.user.id, page_path=page_path, annotation=json.dumps(received_annotation))
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
      page_path = received_annotation['page_path']
      del received_annotation['page_path']
      annotation.annotation = json.dumps(received_annotation)
      annotation.updated = timezone.now()
      annotation.save()
      response = HttpResponseSeeOtherRedirect('/annotate/annotations/'+str(annotation.id))
    else: # GET
      result = json.loads(annotation.annotation)
      result['id'] = annotation.id
      response = JsonResponse(result, safe=False)
  except Annotation.DoesNotExist:
    response = HttpResponseNotFound()
  return response

#
#
#
def search(request):
  page_path = request.GET.get('page_path')
  annotations = [a for a in Annotation.objects.filter(user_id=request.user.id, page_path=page_path).order_by('id')]
  total = len(annotations)
  rows = []
  for annotation in annotations:
    anno = json.loads(annotation.annotation)
    anno['id'] = annotation.id
    rows.append(anno)
  data = {
    "total": total, 
    "rows": rows,
  }
  return JsonResponse(data, safe=False)