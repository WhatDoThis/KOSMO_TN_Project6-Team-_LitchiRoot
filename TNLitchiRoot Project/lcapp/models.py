from django.db import models

# Create your models here.

class Seeker(models.Model):
    email = models.TextField(primary_key=True) # '@', '.' 외 특수문자 안됨
    pwd = models.CharField(max_length=30)
    name = models.CharField(max_length=30) # 이름 -> 특수문자, 숫자 안됨
    phone = models.CharField(max_length=50) # 폰넘버 -> 하이픈 포함해서 받기
    gender = models.CharField(max_length=6) # 성별 -> 콤보박스로 받아서 넣어주기
    cdate = models.DateField(auto_now_add=True)
    
class Company(models.Model): # PK자동 id 부여
    co_affiliate = models.CharField(max_length=45) # 계열사 이름
    
class Recruitment(models.Model): # PK자동 id 부여
    re_affiliate = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company') # 계열사 참조 -> 회사가 망하면 삭제
    re_sector = models.CharField(max_length=45) # 업종 이름
    re_career = models.CharField(max_length=20) # 신입, 경력, 신입/경력 3가지 가능
    re_prefer = models.TextField() # 각종 우대사항 ','로 구분하여 적기
    re_sdate = models.DateField() # 모집시작일 설정
    re_edate = models.DateField() # 모집마감일 설정
    
class Apply(models.Model): # PK자동 id 부여
    ap_seeker = models.ForeignKey(Seeker, on_delete=models.CASCADE) # 구직자 참조 -> 탈퇴 시 지원기록 삭제
    ap_recruitment = models.ForeignKey(Recruitment, on_delete=models.CASCADE) # 계열사 참조 -> 모집마감 시 지원기록 삭제
    ap_resume = models.FileField(upload_to= "%Y_%m_%d/", blank=True) # 파일 업로드 "/resume/(년도)/" 경로에 저장됨git 