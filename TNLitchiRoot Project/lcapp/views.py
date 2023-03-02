import os, random
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.template import loader
from django.core.paginator import Paginator
from lcapp.models import Seeker, Company, Apply, Recruitment
from django.conf import settings
from datetime import datetime
from django.core.mail import EmailMessage
from django.core import serializers

# Create your views here.

def index(request):
    request.session['url'] = request.path
    return render(request, 'index.html')

def terms(request):
    request.session['url'] = request.path
    return render(request, 'terms.html')
def introduce(request):
    request.session['url'] = request.path
    return render(request, 'introduce.html')
def map(request):
    request.session['url'] = request.path
    return render(request, 'map.html')
def subsidiary(request):
    request.session['url'] = request.path
    return render(request, 'subsidiary.html')

def join(request):
    return render(request, 'join.html')

def join_ok(request):
    if request.method == 'POST':
        try:
            url = request.session['url']
        except:
            url = "/"
        email = request.POST['email']
        pwd = request.POST['pwd']
        name = request.POST['name']
        phone = request.POST['phone']
        gender = request.POST['gender']
        cdate = timezone.now().strftime('%Y-%m-%d')
        print(url, email, pwd, name, phone, gender, cdate)
        used_email = Seeker.objects.filter(Q(email=email))
        used_phone = Seeker.objects.filter(Q(phone=phone))
        if used_email:
            message = '사용중인 email 입니다'
            return HttpResponse("<script>alert('"+ message +"');history.back();</script>")
        elif used_phone:
            message = '사용중인 휴대전화 입니다'
            return HttpResponse("<script>alert('"+ message +"');history.back();</script>")
        
        seeker = Seeker(email=email, pwd=pwd, name=name, phone=phone, gender=gender, cdate=cdate)
        seeker.save()
        messages.success(request, "회원가입에 성공하셨습니다")
        return redirect(url)
    return HttpResponseRedirect(reverse('join'))

def login(request):
    return render(request,'login.html')

def login_ok(request):
    if request.method == 'POST':
        try:
            url = request.session['url']
        except:
            url = "/"
        login_email = request.POST.get('login-email')
        login_pwd = request.POST.get('login-pwd')

        try:
            check_email=Seeker.objects.get(email=login_email)
            if check_email.pwd == login_pwd:
                request.session['email'] = login_email
                messages.success(request, "로그인에 성공하셨습니다")
                return redirect(url)
            else:
                message = '비밀번호를 확인해 주세요'
                return HttpResponse("<script>alert('"+ message +"');history.back();</script>")
        except:
            message = '이메일을 확인해 주세요'
            return HttpResponse("<script>alert('"+ message +"');history.back();</script>")
    else:
        message = '알 수 없는 오류가 발행하였습니다.'
        return HttpResponse("<script>alert('"+ message +"');history.back()</script>")

def logout(request):
   if request.session['email']:
      del(request.session['email'])
   message = '로그아웃하였습니다.'
   try:
      url = request.session['url']
   except:
      url = "/"
   return HttpResponse("<script>alert('"+ message +"');location.href='"+url+"';</script>")

def list(request):
    templates = loader.get_template('list.html')
    request.session['url'] = request.path
    sector_set = set()
    recruitments = Recruitment.objects.select_related('re_affiliate').order_by('re_edate')
    companies = Company.objects.all().values()
    if recruitments:
        for recruitment in recruitments:
            sector_set.add(recruitment.re_sector)
            recruitment.dDay = (recruitment.re_edate-datetime.now().date()).days
    
    context = {
        'recruitments' : recruitments,
        'companies' : companies,
        'sector_set' : sector_set,
    }
            
    if request.method == 'POST':
        company_option = request.POST.get('company')
        sector_option = request.POST.get('sector')
        career_option = request.POST.get('career')
        
        q = Q()
        if company_option != "primary":
            q &= Q(re_affiliate = company_option)
        if sector_option != "primary":
            q &= Q(re_sector=sector_option)
        if career_option != "primary":
            q &= Q(re_career__contains=career_option)
        recruitments = Recruitment.objects.select_related('re_affiliate').filter(q).order_by('re_edate')
        for recruitment in recruitments:
            recruitment.dDay = (recruitment.re_edate-datetime.now().date()).days
        
        context = {
            'recruitments' : recruitments,
            'companies' : companies,
            'sector_set' : sector_set,
            'company_option' : company_option,
            'sector_option' : sector_option,
            'career_option' : career_option,
        }
    
    return HttpResponse(templates.render(context, request))


def search(request):
    if request.method == 'POST':
        ajax_data = request.POST['get_data']
        if ajax_data.isdigit():
            data_for_jasons = Recruitment.objects.select_related('re_affiliate').filter(Q(re_affiliate=ajax_data))
        else:
            data_for_jasons = Recruitment.objects.select_related('re_affiliate').filter(Q(re_sector=ajax_data))

        report_list = serializers.serialize('json', data_for_jasons)
        return JsonResponse(report_list, safe=False)
    else:
        message = '알 수 없는 오류가 발행하였습니다.'
        return HttpResponse("<script>alert('"+ message +"');history.back()</script>")
    
#입사지원 상세화면
def apply(request, company, recruitment):
   #----------------------
   try:
      sessionEmail = request.session['email']
   except:
      message = '로그인이 필요한 서비스입니다.'
      return HttpResponse("<script>alert('"+ message +"');location.href='/list';</script>")
   #--------------------
   request.session['url'] = request.path
   selectedCompany = company
   selectedRecruitment = recruitment
   companies = Company.objects.all()
   #네비에 있는 입사지원으로 들어올경우 모든 직종을 들고간다
   if selectedCompany == 0 and selectedRecruitment  ==0:
      recruitmentes = Recruitment.objects.all()
      context = {
         'companies' : companies,
         'selectedCompany' : selectedCompany,
         'recruitmentes':recruitmentes,
         'selectedRecruitment' : selectedRecruitment,
      }
   #회사를 선택하고나 또는 직종을 선택하고 들어온 경우
   else:
      #직종에 따라 회사를 찾아옴
      if selectedCompany == 0 and selectedRecruitment != 0:
         selectedCompany = Recruitment.objects.filter(id=recruitment).values('re_affiliate')[0].get('re_affiliate')
      #회사에 맞는 직종을 찾아옴 그중 첫번째 직종으로 선택하여 가져옴
      if selectedRecruitment == 0 and selectedCompany != 0:
         selectedRecruitment = Recruitment.objects.filter(re_affiliate=selectedCompany).values('id')[0].get('id')
      recruitmentes = Recruitment.objects.select_related("re_affiliate").filter(re_affiliate=selectedCompany)
      #직종 상세
      recruitmentDetail = Recruitment.objects.get(id=selectedRecruitment)
      #세션에 있는 이메일로 선택된 직종에 지원된것이 있는지 확인
      applyDetail = Apply.objects.filter(ap_seeker_id=sessionEmail, ap_recruitment=selectedRecruitment)
      if  applyDetail :
         applyDetail = applyDetail[0]
      #직종 상세에 마감일까지 몇 일 남았는지 확인
      recruitmentDetail.dDay = (recruitmentDetail.re_edate - datetime.now().date()).days
      context = {
         'companies' : companies,
         'selectedCompany' : selectedCompany,
         'recruitmentes':recruitmentes,
         'selectedRecruitment' : selectedRecruitment,
         'recruitmentDetail' : recruitmentDetail,
         'applyDetail':applyDetail
      }
   return render(request, 'apply.html', context)

#지원서 작성 및 수정
def apply_ok(request):
   if request.method == 'POST':
      try:
         url = request.session['url']
      except:
         url = "/"
      #----------------------
      try:
         sessionEmail = request.session['email']
      except:
         message = '로그인이 필요한 서비스입니다.'
         return HttpResponse("<script>alert('"+ message +"');location.href='/';</script>")
      #--------------------
      selectedRecruitment = request.POST['ap_recruitment_id']
      resume = request.FILES["resume"]
      #세션에 있는 이메일로 선택된 직종에 지원된것이 있는지 확인
      applyDetail = Apply.objects.filter(ap_seeker_id=sessionEmail, ap_recruitment=selectedRecruitment)
      #지원서가 존재한다면
      if applyDetail:
         #파일만 바꿔서 세이브
         applyDetail[0].ap_resume=resume
         applyDetail[0].save()
      #지원서가 존재하지 않는다면 
      else:
         #지원서를 생성하여 세이브
         apply = Apply(
            ap_seeker_id=sessionEmail,
            ap_recruitment_id=selectedRecruitment,
            ap_resume=resume,
         )
         apply.save()
      #마이페이지에서 저장하였다면 마이페이지로
      if url == 'myPage':
         return redirect('/myPage/')
      return redirect('../apply/0/'+selectedRecruitment)
   else:
      message = '알 수 없는 오류가 발행하였습니다.'
      return HttpResponse("<script>alert('"+ message +"');history.back()</script>")

def apply_delete(request, recruitment):
   try:
      url = request.session['url']
   except:
      url = "/"
   #----------------------
   try:
      sessionEmail = request.session['email']
   except:
      message = '로그인이 필요한 서비스입니다.'
      return HttpResponse("<script>alert('"+ message +"');location.href='/';</script>")
   #--------------------
   #세션에 있는 이메일로 선택된 직종에 지원된것이 있는지 확인
   applyDetail = Apply.objects.filter(ap_seeker_id=sessionEmail, ap_recruitment=recruitment)
   #지원서가 존재한다면
   applyDetail.delete()
   #마이페이지에서 저장하였다면 마이페이지로
   if url == 'myPage':
      return redirect('/myPage/')
   return redirect('../apply/0/'+str(recruitment))
    
#지원한 파일 다운로드
def fileDownload(request):
    #다운로드할 데이터를 불러옴
    path = request.GET['path']
    print(path)
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    #파일이 존재한다면 파일을 리턴
    if os.path.exists(file_path):
        binary_file = open(file_path, 'rb')
        response = HttpResponse(binary_file.read(), content_type="application/octet-stream; charset=utf-8")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    else:
        message = '알 수 없는 오류가 발행하였습니다.'
        return HttpResponse("<script>alert('"+ message +"');history.back()</script>")

#지원한 목록
def myPage(request):
   request.session['url'] = request.path
   #----------------------------
   try:
      sessionEmail = request.session['email']
   except:
      message = '로그인이 필요한 서비스입니다.'
      return HttpResponse("<script>alert('"+ message +"');location.href='/';</script>")
   #----------------------------
   #세션에 등록된 아이디로 지원한 목록을 불러옴 apply로 recruitment을 엮고 이걸로 company를 엮음
   myApplicationes = Apply.objects.filter(ap_seeker_id=sessionEmail).select_related('ap_recruitment__re_affiliate')
   print(myApplicationes.count)
   if not myApplicationes:
      message = '지원한 공고가 존재하지 않습니다.'
      return HttpResponse("<script>alert('"+ message +"');history.back()</script>")
   #각 직종들의 마감일까지 dDay를 계산
   for myApplication in myApplicationes:
      myApplication.dDay = (myApplication.ap_recruitment.re_edate-datetime.now().date()).days
   context = {
      'myApplicationes' : myApplicationes,
   }
   return render(request, 'myPage.html', context)

#회원정보 화면
def info(request):
   templates = loader.get_template('info.html')
   request.session['url'] = request.path
   #----------------------------
   try:
      sessionEmail = request.session['email']
   except:
      message = '로그인이 필요한 서비스입니다.'
      return HttpResponse("<script>alert('"+ message +"');location.href='/';</script>")
   #----------------------------
   seeker = Seeker.objects.get(email=sessionEmail)
   context = {
      'seeker' : seeker,
   }
   return HttpResponse(templates.render(context, request))

#회원정보 수정
def info_ok(request):
   if request.method == 'POST':
      #----------------------------
      try:
         sessionEmail = request.session['email']
      except:
         message = '로그인이 필요한 서비스입니다.'
         return HttpResponse("<script>alert('"+ message +"');location.href='/';</script>")
      #----------------------------
      pwd = request.POST['pwd']
      name = request.POST['name']
      gender = request.POST['gender']
      phone = request.POST['phone']
      #입력받은 휴대폰 번호 조회
      used_phone = Seeker.objects.filter(Q(phone=phone))
      seeker = Seeker.objects.get(email=sessionEmail)
      #입력받은 번호가 기존에 번호와 같지 않고 번호가 존재한다면
      if seeker.phone!=phone and used_phone:
         message = '사용중인 휴대전화 입니다'
         return HttpResponse("<script>alert('"+ message +"');history.back();</script>")
      #비밀번호가 입력되었다면 수정
      if pwd != "":
         seeker.pwd = pwd
      seeker.name = name
      seeker.gender = gender
      seeker.phone = phone
      seeker.save()
      message = '회원정보가 수정되었습니다.'
      return HttpResponse("<script>alert('"+ message +"');location.href='/info';</script>")
   else:
      message = '알 수 없는 오류가 발행하였습니다.'
      return HttpResponse("<script>alert('"+ message +"');history.back()'</script>")
    
#1:1문의
def ask(request):
   #----------------------------
   try:
      sessionEmail = request.session['email']
   except:
      message = '로그인이 필요한 서비스입니다.'
      return HttpResponse("<script>alert('"+ message +"');location.href='/';</script>")
   #----------------------------
   request.session['url'] = request.path
   companies = Company.objects.all()
   print(companies)
   context = {
      'companies' : companies,
   }
   return render(request, 'ask.html', context)

#회사로 검색해서 직종목록 반환해주기
def selectCompany(request, company):
    recruitmentes = Recruitment.objects.filter(re_affiliate_id=company)
    recruitmentes = serializers.serialize('json', recruitmentes)
    return JsonResponse(recruitmentes, safe=False)

#1:1문의 관리자에게 이메일 보내기
def ask_ok(request):
   if request.method == 'POST':
      title=request.POST['title']
      context=request.POST['context']
      company=request.POST['company']
      recruitment=request.POST['recruitment']
      sessionEmail = request.session['email']
      #----------------------------
      try:
         sessionEmail = request.session['email']
      except:
         message = '로그인이 필요한 서비스입니다.'
         return HttpResponse("<script>alert('"+ message +"');location.href='/';</script>")
      #----------------------------
      context = company + " : " + recruitment+ "\n" +context
      email = EmailMessage(
         "리치루트 : 문의가 접수되었습니다. : "+title, #이메일 제목
         context, #내용
         to=[sessionEmail], #받는 이메일 관리자 이메일
      )
      email.send()
      context = context+"\n\n이쪽으로 답신 부탁드립니다. : "+sessionEmail
      email = EmailMessage(
         "리치루트 : 문의가 접수되었습니다. : "+title, #이메일 제목
         context, #내용
         to=['dqas1004s@naver.com'], #받는 이메일 관리자 이메일
      )
      email.send()
      message = "정상적으로 접수되었습니다."
      return HttpResponse("<script>alert('"+ message +"');location.href='/ask/'</script>")
   else:
      message = '알 수 없는 오류가 발행하였습니다.'
      return HttpResponse("<script>alert('"+ message +"');history.back();</script>")

def sendEmail(request):
    #----------------------------
    sessionEmail = 'dqas1004t@naver.com'
    #----------------------------
    code=random.randint(1000,9999)
    email = EmailMessage(
        "", #이메일 제목
        str(code), #내용
        to=[sessionEmail], #받는 이메일
    )
    email.send()
    return JsonResponse(str(code), safe=False)