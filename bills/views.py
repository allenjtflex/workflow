from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.detail import  DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q

# Create your views here.
from .forms import BillCreateForm
from .models import Bill, BillItem
from customers.models import Customer
from dailywork.models import Dailylog
# from .forms import CustomerForm,CustomerEditForm


class BillDetail(DetailView):
    model = Bill



class BillList(ListView):
    model = Bill




def bill_create(request, id):


    #raw_id_fields = ['customer']
    if request.method == 'POST':
        customer = Customer.objects.get(pk=id)
        rq = request.POST.getlist('dailylogs')
        bill_number = Bill.objects.month_sequence()
        # print(id)   #客戶編號
        # print(rq)   #dailywork Item
        #
        print(bill_number)  # New Bill Number

        form = BillCreateForm(request.POST or None)
        form.instance.bill_number = bill_number

        print( form.instance.bill_number )
        bill = form.save()


        dailyworks = Dailylog.objects.filter( pk__in= rq )
        for dailylog in dailyworks:
            BillItem.objects.create(
                bill_id = bill.id,
                item = dailylog
            )

        dailyworks.update( payrequest=True  )

        return HttpResponseRedirect( '/bills/%s/' %( bill.id )  )


    return render(request,'/bills/%s/' %( bill.id ),locals())




def billitem_delete(request, id):
    # print( id )
    if request.POST or None:
        rq = request.POST.getlist('dailylogs')

        logitem = Dailylog.objects.filter(id__in = rq)
        logitem.update( payrequest=False  ) #先把已請款的標記更改爲False

        instance = BillItem.objects.filter(item__in= rq )
        instance.delete() #再刪除項目

        return HttpResponseRedirect("../")

    return render(request, "../", locals())


#
# class BillCreate(CreateView):
#     title = "Create New Customer"
#     model = Bill
#     form_class = CustomerForm
#     #fields = ['part_number', 'description', 'specification', 'image',  'category', 'cycle_status']
#     success_url = reverse_lazy('customers:customer_list')
#
#
#
# class CustomerUpdate(UpdateView):
#     model = Customer
#     form_class = CustomerEditForm
#     #fields = ['title', 'unikey', 'address', 'phone', 'faxno', 'invalid']
#
#     success_url = reverse_lazy('customers:customer_list') #因為不會回到該項資料的Detail, 所以先回到List吧
#
#
# class CustomerDelete(DeleteView):
#     model = Customer
#     #success_url = '/products'
#     success_url = reverse_lazy('customers:customer_list')





#use ReportLab
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm , letter

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.utils import ImageReader
# from django.contrib.staticfiles.templatetags.staticfiles import static


# 正式Quote-A

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
Title = "建龍環保股份有限公司"
Subject = "請款單"

# logo = settings.STATIC_ROOT +"/img/alder_logo.png"
# upline = settings.STATIC_ROOT +"/img/alder_upline.jpg"
# footer_line = settings.STATIC_ROOT +"/img/footer_line.jpg"
#factory_img = settings.STATIC_ROOT +"/img/factory.png"
# certification_img = settings.STATIC_ROOT +"/img/certification.png"
pdfmetrics.registerFont(TTFont('simhei', 'simhei.ttf'))
pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))

# 封面的Layout

def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('simhei', 18)
    canvas.drawCentredString(PAGE_WIDTH/2.0,PAGE_HEIGHT-45, Title )
    canvas.drawCentredString(PAGE_WIDTH/2.0,PAGE_HEIGHT-70, Subject )
    canvas.restoreState()



def myLaterPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('simhei', 9)
    contact_info = "Alder Optomechanical Corp."

    canvas.setFont('Times-Roman', 9)
    # canvas.drawImage(logo, 520,780, mask='auto', width=55,height=45)
    canvas.drawString(530, 0.45 * inch, "Page %d " % ( doc.page) )
    # canvas.drawString(inch, 0.45 * inch, "Page %d %s" % ( doc.page, pageinfo) )
    # canvas.drawImage(footer_line, 25, 805, mask='auto', width=485,height=20)
    contact_address = "No.171 Tianjin Street, Pignzhen Dist., Taoyuan City 32458, Taiwan.    www.alder.com.tw    sales@alder.com.tw    +886-3-4393588"

    # 地址放在上面的圖騰下
    canvas.setFont('VeraBd', 9)
    # canvas.drawString(30, 795 ,  contact_info  )
    canvas.setFont('Times-Roman', 9)
    # canvas.drawString(30, 785 ,  contact_address )
    # canvas.drawImage(upline, 25, 25, mask='auto', width=490,height=20)

    # 地址放在下面的圖騰下
    # canvas.setFont('VeraBd', 9)
    # canvas.drawString(30, 40 ,  contact_info  )
    # canvas.setFont('Times-Roman', 9)
    # canvas.drawString(30, 25 ,  contact_address )
    # canvas.drawImage(upline, 25, 50, mask='auto', width=540,height=20)


    canvas.restoreState()


from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle,PropertySet
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_LEFT, TA_CENTER
from reportlab.lib import colors

# 'fontName':'Times-Roman'
class ParagraphStyle(PropertySet):
    defaults = {
        'fontName':'simhei',
        'fontSize':10,
        'leading':12,
        'leftIndent':0,
        'rightIndent':0,
        'firstLineIndent':12,
        'alignment':0,
        'spaceBefore':0,
        'spaceAfter':0,
        'bulletFontName':'simhei',
        'bulletFontSize':10,
        'bulletIndent':0,
        'textColor': colors.black,
        'backColor':None,
        'wordWrap':None,
        'borderWidth': 0,
        'borderPadding': 0,
        'borderColor': None,
        'borderRadius': None,
        'allowWidows': 1,
        'allowOrphans': 0,
        'textTransform':None,
        'endDots':None,
        'splitLongWords':1,
        'underlineProportion': 0.0,
        'bulletAnchor': 'start',
        }


# 明確數量的報價單,有金額小計及總金額的報表模板
# 正式Quote-B
def _generate_pdfv2(course, output):
    from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_LEFT, TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table , TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle,PropertySet
    from reportlab.lib.units import mm, inch
    from reportlab.lib import colors
    from reportlab.platypus import XPreformatted, Preformatted
    from django.conf import settings
    from reportlab.pdfgen import canvas
    pdfmetrics.registerFont(TTFont('simhei', 'simhei.ttf'))
    pdfmetrics.registerFont(TTFont('Arialuni', 'arialuni.ttf'))


    doc = SimpleDocTemplate(
        output,pagesize=A4,
        rightMargin=.5*inch,leftMargin=.5*inch,
        topMargin=inch,bottomMargin=.6*inch
    )


    Story = [Spacer(1, 0.5*inch)]
    style = styles["Normal"]
    styleN = styles['Normal']
    styleH = styles['Heading1']

    ###
    stylesheet=getSampleStyleSheet()
    normalStyle = stylesheet['Normal']

    header = [
              ['請款單號',':', course.bill_number,'','請款日期',':', course.ord_date],
              ['客戶名稱',':', course.customer.title,'', '統一編號',':', course.customer.unikey],
              ['聯絡電話',':', course.customer.phone,'','傳真號碼',':', course.customer.faxno],
              ['地址',':', course.customer.address,'', '','', ""],
              ]

    h = Table(header, colWidths=[1.0*inch, 0.1*inch, 2.8*inch, 0.3*inch, 0.9*inch, 0.1*inch, 2.0*inch] ,style=[

                        ('FONTNAME', (0,0),(6,-1), 'simhei'),
                        ('SPAN',(2,0),(3,0)),
                        ('VALIGN',(0,0),(0,-1),'TOP'),
                        ('ALIGN',(3,0),(3,-1), 'LEFT'),

                    ])

    Story.append(h)


    element = []
    tableheader = ['項次','工作日期', '起迄地點', '內容描述' ,'數量','單價','小計']

    element.append(tableheader)
    loopcounter = 1
    grund_total = 0
    for obj in course.billitem_set.all():

        myitem = []
        myitem.append( loopcounter )

        workdate = obj.item.work_date
        place = obj.item.start_at + "-" +obj.item.end_with
        workdesc = obj.item.opreateDesc
        qty = obj.item.quantity
        uom = obj.item.uom
        str_qty = str('{:,.0f}'.format(int(qty))) + ' ' + str(uom)
        uniprice = obj.item.uniprice
        # amount = qty * uniprice
        # grund_total += amount

        myitem.append( workdate)
        myitem.append( place)
        myitem.append( workdesc )
        myitem.append( str_qty )
        myitem.append(  str('{:,.0f}'.format(int( uniprice )))  )
        myitem.append(  str('{:,.0f}'.format(int( obj.item.get_amount() ))) )

        element.append(myitem)
        loopcounter += 1

    #repeatRows=1 是指第一行(表頭) 換頁時會重複
    t = Table(element, colWidths=[0.3*inch, 0.8*inch, 0.8*inch, 2.6*inch, 0.8*inch,  0.8*inch, 1.0*inch] , repeatRows=1)

    t.setStyle(
        TableStyle(
            [('BACKGROUND',(0,0),(6,0),colors.skyblue),
             ('FONTNAME', (0,0),(6,-1), 'simhei'),
             ('ALIGN',(0,0),(3,0),'CENTER'),
             ('ALIGN',(4,0),(5,0),'LEFT'),
            #  ('SIZE',(0,1),(0,-1), 8),
            #  ('SIZE',(2,1),(2,-1), 8),
             ('VALIGN',(0,0),(4,-1),'TOP'),
             ('ALIGN',(4,0),(6,-1), 'RIGHT'),
            #  ('TEXTCOLOR',(3,1),(4,-1), colors.blue),
             ('SIZE',(0,1),(4,-1), 10),
             ('LINEBELOW', (0,-1), (-1,-1), 1, colors.black),
             ]
        )
    )

    Story.append(t)

    myinfo = "匯款帳號：" + "\n" +"        新光銀行：八德分行" + "\n" + "        帳號：0596-50-000-6453" + "\n" + "        戶名：林泰成"

    #頁首的資訊
    #因為要套用字型Arialuni, 所以將comment改為Paragraph
    comment = Paragraph('''
       <para align=left spaceb=3><font face="simhei" >'''+ str(myinfo).replace('\n','<br/>\n') +'''</font></para>''',
       styles["BodyText"])

    tax = int(course.get_tax_amount())
    total = int(course.get_grand_amount())


    footer = [
                [ '匯款帳號：', '', '金額小計：','', str('{:,.0f}'.format(int( course.get_total_amount() )))   ],
                ['','新光銀行：八德分行', '稅額：','', str('{:,.0f}'.format(int( tax )))  ],
                ['','帳號：0596-50-000-6453', '請款金額：','', str('{:,.0f}'.format(int( total )))  ],
                ['','戶名：林泰成', '', '',''  ],
                  ]

    f = Table(footer,colWidths=[ 0.6*inch, 2.5*inch, 2.5*inch, 0.8*inch, 0.6*inch] ,style=[

                        ('FONTNAME', (0,0),(4,-1), 'simhei'),
                        ('ALIGN',(2,0),(4,-1), 'RIGHT'),

                    ])

    Story.append(f)


    style = getSampleStyleSheet()['Normal']
    style.leading = 8


    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPage )

# 明確數量的報價單,有金額小計及總金額的  Quota-B
def gen_pdfv2(request,id):
    course = get_object_or_404(Bill,id=id)
    response = HttpResponse(content_type='application/pdf')
    filename = 'PaymentRequest%s.pdf' %( str(course.bill_number))
    response['Content-Disposition'] = 'filename=' + filename

    _generate_pdfv2(course, response)

    return response
