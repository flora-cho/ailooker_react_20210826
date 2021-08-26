from rest_framework.decorators import api_view
from django.shortcuts import HttpResponse
from rest_framework import status
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from aiLooker_app.models import Tbladvtbsc
import json
import datetime


def serialize_aiLooker(aiLooker):
    serialized = model_to_dict(aiLooker)
    serialized["advtno"]        = int(aiLooker.advtno)              # 광고번호
    serialized["advttpcd"]      = str(aiLooker.advttpcd)            # 광고종류코드
    serialized["advttitl"]      = str(aiLooker.advttitl)            # 광고제목
    serialized["advtstadate"]   = str(aiLooker.advtstadate)         # 광고시작일자
    serialized["advtenddate"]   = str(aiLooker.advtenddate)         # 광고종료일자
    serialized["advtdesc"]      = str(aiLooker.advtdesc)            # 광고내용
    serialized["advtgrdcd"]     = str(aiLooker.advtgrdcd)           # 광고등급코드
    serialized["delyn"]         = str(aiLooker.delyn)               # 삭제여부
    serialized["fstaddtmst"]    = str(aiLooker.fstaddtmst)          # 최초등록일시
    serialized["fstaddid "]     = str(aiLooker.fstaddid)            # 최초등록ID
    serialized["lastupttmst"]   = str(aiLooker.lastupttmst)         # 최종변경일시
    serialized["lastuptid"]     = str(aiLooker.lastuptid)           # 최종변경ID

    return serialized

def save_aiLooker(request, aiLooker, success_status):
    errors = []
    advtno = request.data.get("advtno", "")
    if advtno == "":
        errors.append({"advtno": "This field is required"})

    advttpcd = request.data.get("advttpcd", "")
    if advttpcd == "":
        errors.append({"advttpcd": "This field is required"})

    advttitl = request.data.get("advttitl", "")
    if advttitl == "":
        errors.append({"advttitl": "This field is required"})

    advtstadate = request.data.get("advtstadate", "")
    if advtstadate == "":
        advtstadate = datetime.datetime.now()

    advtenddate = request.data.get("advtenddate", "")
    if advtenddate == "":
        advtenddate = datetime.datetime.now()

    advtdesc = request.data.get("advtdesc", "")
    if advtdesc == "":
        errors.append({"advtdesc": "This field is required"})

    advtgrdcd = request.data.get("advtgrdcd", "")
    if advtgrdcd == "":
        errors.append({"advtgrdcd": "This field is required"})

    delyn = request.data.get("delyn", "")
    if delyn == "":
        delyn = "N"

    fstaddtmst = request.data.get("fstaddtmst", "")
    if fstaddtmst == "":
        fstaddtmst = datetime.datetime.now()

    fstaddid = request.data.get("fstaddid", "")
    if fstaddid == "":
        fstaddid = "admin"

    lastupttmst = request.data.get("lastupttmst", "")
    if lastupttmst == "":
        lastupttmst = datetime.datetime.now()

    lastuptid = request.data.get("lastuptid", "")
    if lastuptid == "":
        lastuptid = "admin"        

    if len(errors) > 0:
        return HttpResponse(json.dumps(
            {
                "errors": errors
            }), status=status.HTTP_400_BAD_REQUEST)

    try:
        aiLooker.advtno      = advtno                               # 광고번호
        aiLooker.advttpcd    = advttpcd                             # 광고종류코드
        aiLooker.advttitl    = advttitl                             # 광고제목
        aiLooker.advtstadate = advtstadate                          # 광고시작일자
        aiLooker.advtenddate = advtenddate                          # 광고종료일자
        aiLooker.advtdesc    = advtdesc                             # 광고내용
        aiLooker.advtgrdcd   = advtgrdcd                            # 광고등급코드
        aiLooker.delyn       = delyn                                # 삭제여부
        aiLooker.fstaddtmst  = fstaddtmst                           # 최초등록일시
        aiLooker.fstaddid    = fstaddid                             # 최초등록ID
        aiLooker.lastupttmst = lastupttmst                          # 최종변경일시
        aiLooker.lastuptid   = lastuptid                            # 최종변경ID                                               

        aiLooker.save()

    except Exception as e:
        return HttpResponse(json.dumps(
            {
                "errors": {"Tbladvtbsc": str(e)}
            }), status=status.HTTP_400_BAD_REQUEST)

    return HttpResponse(json.dumps({"data": serialize_aiLooker(aiLooker)}), status=success_status)


@api_view(['GET', 'POST'])
def aiLookers(request):
    if request.user.is_anonymous:
        return HttpResponse(json.dumps({"detail": "Not authorized"}), status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        aiLookers_data = Tbladvtbsc.objects.all()
        aiLookers_count= aiLookers_data.count()

        page_size      = int(request.GET.get("page_size", "5"))
        page_no        = int(request.GET.get("page_no"  , "0"))
        aiLookers_data = list(aiLookers_data[page_no * page_size:page_no * page_size + page_size])

        aiLookers_data = [serialize_aiLooker(aiLooker) for aiLooker in aiLookers_data]
        return HttpResponse(json.dumps({"count": aiLookers_count, "data": aiLookers_data}), status=status.HTTP_200_OK)

    if request.method == "POST":
        aiLooker = Tbladvtbsc()
        return save_aiLooker(request, aiLooker, status.HTTP_201_CREATED)

    return HttpResponse(json.dumps({"detail": "Wrong method"}), status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET', 'PUT', 'DELETE'])
def aiLooker(request, advtno):
    if request.user.is_anonymous:
        return HttpResponse(json.dumps({"detail": "Not authorized"}), status=status.HTTP_401_UNAUTHORIZED)

    try:
        aiLooker = Tbladvtbsc.objects.get(pk=advtno)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"detail": "Not found"}), status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return HttpResponse(json.dumps({"data": serialize_aiLooker(aiLooker)}), status=status.HTTP_200_OK)

    if request.method == "PUT":
        return save_aiLooker(request, aiLooker, status.HTTP_200_OK)

    if request.method == "DELETE":
        aiLooker.delete()
        return HttpResponse(json.dumps({"detail": "deleted"}), status=status.HTTP_410_GONE)

    return HttpResponse(json.dumps({"detail": "Wrong method"}), status=status.HTTP_501_NOT_IMPLEMENTED)
