from django.db import models
from datetime  import datetime

class Tbladvtbsc(models.Model):
    advtno      = models.IntegerField(default=0, primary_key=True)            # 광고번호
    advttpcd    = models.CharField(max_length=30)                             # 광고종류코드
    advttitl    = models.CharField(max_length=200)                            # 광고제목
    advtstadate = models.CharField(max_length=8)                              # 광고시작일자
    advtenddate = models.CharField(max_length=8)                              # 광고종료일자
    advtdesc    = models.CharField(max_length=3000)                           # 광고내용
    advtgrdcd   = models.CharField(max_length=30)                             # 광고등급코드
    filepath    = models.CharField(max_length=1000, blank=True)               # 파일첨부
    delyn       = models.CharField(max_length=1)                              # 삭제여부
    fstaddtmst  = models.DateTimeField(default=datetime.now(), blank=True)    # 최초등록일시
    fstaddid    = models.CharField(max_length=30)                             # 최초등록ID
    lastupttmst = models.DateTimeField(default=datetime.now(), blank=True)    # 최종변경일시
    lastuptid   = models.CharField(max_length=30)   

    def __str__(self):
        return f"{self.advtno}: {self.advttpcd}"

    class Meta:
        ordering = ["-advtno"]

        

