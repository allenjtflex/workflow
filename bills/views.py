from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.detail import  DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.contrib import messages

# Create your views here.
from .forms import BillCreateForm,BillGenerateForm,BatchPrintBills,BillEditForm
from .models import Bill, BillItem
from customers.models import Customer
from dailywork.models import Dailylog



class BillDetail(DetailView):
    model = Bill



class BillList(ListView):
    title = "未付款清單"
    model = Bill
    queryset = Bill.objects.filter( is_valid__exact=False ,paied=False)
    paginate_by = 15


class BillUpdate(UpdateView):
    title = '修訂請款單'
    model = Bill
    form_class = BillEditForm
    success_url = reverse_lazy('bills:bill_list')


# 批次產生請款單
def generate_bill(request):
# 先抓出符合條件的工作日誌
    title = '結轉請款單'
    form = BillGenerateForm(request.POST or None)
    dutydate =  request.POST.get('ord_date')
    if form.is_valid():

        logs = Dailylog.objects.filter(payrequest=False ,
                                        is_freecharge=False,
                                        invalid=False,
                                        work_date__lte  =dutydate
                                )#.values('customer').order_by('customer').distinct()

        custs = logs.values('customer').order_by('customer').distinct()# 去除重複的客戶編號

        if custs.count()== 0:
            messages.success(request, '無可新增的請款單')
            return render(request,'bills/bill_generate.html',locals())

    # 迴圈產生請款單
        for cust in custs:
            customer = Customer.objects.get(pk= cust.get('customer'))
            next_number = Bill.objects.month_sequence( dutydate )            
            bill = Bill.objects.create(customer=customer,ord_date=dutydate,bill_number=next_number)

            cust_logs = logs.filter(customer=customer)
            for cust_log in cust_logs:
                BillItem.objects.create(
                    bill_id = bill.id,
                    item = cust_log
                )

            #把已經轉成請款單的工作日誌補上請款單號和已請款欄位爲True
            cust_logs.update( payrequest=True, bill_number=next_number  )

        messages.success(request, '新增請款單成功')
        return redirect('bills:bill_list')

    return render(request,'bills/bill_generate.html',locals())




#   產生單張請款單
def bill_create(request, id):
    #raw_id_fields = ['customer']
    if request.method == 'POST':
        customer = Customer.objects.get(pk=id)
        rq = request.POST.getlist('dailylogs')
        next_number = Bill.objects.month_sequence()

        bill = Bill.objects.create( customer = customer, bill_number=next_number )
        bill.save()

        dailyworks = Dailylog.objects.filter( pk__in= rq )
        for dailylog in dailyworks:
            BillItem.objects.create(
                bill_id = bill.id,
                item = dailylog
            )

            #把已經轉成請款單的工作日誌補上請款單號和已請款欄位爲True
        dailyworks.update( payrequest=True, bill_number=next_number  )
        return HttpResponseRedirect( '/bills/%s/' %( bill.id )  )

    return render(request,'/bills/%s/' %( bill.id ),locals())




def billitem_delete(request, id):
    # print( id )
    if request.POST or None:
        rq = request.POST.getlist('dailylogs')

        logitem = Dailylog.objects.filter(id__in = rq)
        logitem.update( payrequest=False, bill_number=None ) #先把已請款的標記更改爲False
        instance = BillItem.objects.filter(item__in= rq )
        instance.delete() #再刪除項目

        return HttpResponseRedirect("../")

    return render(request, "../", locals())



#  批次列印請款單的入口, 用單據號碼區間查詢
def print_bills(request):
    title = '批次列印請款單'

    form = BatchPrintBills(request.POST or None)
    if form.is_valid():
        start= request.POST.get('start_number')
        end= request.POST.get('end_number')

        course = Bill.objects.filter(bill_number__range=(start, end),is_valid=False, paied=False)

        if course.count()==0:
            messages.error(request, '找不到可以列印的請款單,可能是單據已作廢或已付款')
            return render(request,'bills/bill_generate.html',locals())

        response = HttpResponse(content_type='application/pdf')
        filename = 'bill.pdf'
        response['Content-Disposition'] = 'filename=' + filename
        _generate_batch(course, response)

        return  response

    return render(request,'bills/bill_generate.html',locals())



#  列印請款單的入口, 用賬單id查詢
def gen_pdfv2(request,id):
    # course = get_object_or_404(Bill,id=id)
    course = Bill.objects.filter(id=id,is_valid=False, paied=False)

    if course.count()==0:
        messages.error(request, '找不到可以列印的請款單,可能是單據已作廢或已付款')
        return render(request,'bills/bill_generate.html',locals())

    response = HttpResponse(content_type='application/pdf')
    filename = '%s-%s.pdf' %( str(course[0].bill_number), course[0].customer)
    response['Content-Disposition'] = 'filename=' + filename

    _generate_batch(course, response)

    return response



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


from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
Title = "建龍環保有限公司"
Subject = "請款單"


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
    contact_info = "建龍環保有限公司"

    canvas.setFont('Times-Roman', 9)
    # canvas.drawImage(logo, 520,780, mask='auto', width=55,height=45)
    canvas.drawString(530, 0.45 * inch, "Page %d " % ( doc.page) )

    contact_address = ""

    # 地址放在上面的圖騰下
    canvas.setFont('VeraBd', 9)
    # canvas.drawString(30, 795 ,  contact_info  )
    canvas.setFont('Times-Roman', 9)



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



# 批次的請款單
def _generate_batch(course, output):
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
        topMargin=.4*inch,bottomMargin=.6*inch
    )


    Story = [Spacer(0, 0.0*inch)]
    style = styles["Normal"]
    styleN = styles['Normal']
    styleH = styles['Heading1']

    for bill in course:

        stylesheet=getSampleStyleSheet()
        normalStyle = stylesheet['Normal']

        hat = [
                ['建龍環保有限公司'],
                ['請款單'],
                ['']
        ]


        h = Table( hat, colWidths=[3.2*inch] ,style=[
                            ('FONTNAME', (0,0),(0,-1), 'simhei'),
                            ('SPAN',(0,0),(0,0)),
                            ('VALIGN',(0,0),(0,-1),'TOP'),
                            ('SIZE',(0,0),(0,-1), 18),
                            ('ALIGN',(0,0),(0,-1), 'CENTER'),
                        ])

        Story.append(h)




        header = [
                  ['請款單號',':', bill.bill_number,'','請款月份',':', str(bill.ord_date)[:7]  ],
                  ['客戶名稱',':', bill.customer.title,'', '統一編號',':', bill.customer.unikey],
                  ['聯絡電話',':', bill.customer.phone,'','傳真號碼',':', bill.customer.faxno],
                  ['地址',':', bill.customer.address,'', '','', ""],
                  ]

        h = Table(header, colWidths=[0.6*inch, 0.1*inch, 3.2*inch, 1.4*inch, 0.6*inch, 0.1*inch, 1.6*inch] ,style=[

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
        for obj in bill.billitem_set.all():

            myitem = []
            myitem.append( loopcounter )

            workdate = obj.item.work_date
            place = obj.item.start_at + "-" +obj.item.end_with
            workdesc = obj.item.opreateDesc
            qty = obj.item.quantity
            uom = obj.item.uom
            str_qty = str('{:,.0f}'.format(int(qty))) + ' ' + str(uom)
            uniprice = obj.item.uniprice

            myitem.append( workdate)
            myitem.append( place)
            myitem.append( workdesc )
            myitem.append( str_qty )
            myitem.append(  str('{:,.0f}'.format(int( uniprice )))  )
            myitem.append(  str('{:,.0f}'.format(int( obj.item.get_amount() ))) )

            element.append(myitem)
            loopcounter += 1

        #repeatRows=1 是指第一行(表頭) 換頁時會重複
        t = Table(element, colWidths=[0.3*inch, 0.8*inch, 1.4*inch, 2.8*inch, 0.6*inch,  0.8*inch, 0.8*inch] , repeatRows=1)

        t.setStyle(
            TableStyle(
                [
                #   ('BACKGROUND',(0,0),(6,0),colors.skyblue),
                ('LINEBELOW', (0,0), (6,0), 1, colors.black),
                 ('FONTNAME', (0,0),(6,-1), 'simhei'),
                 ('ALIGN',(0,0),(0,0),'CENTER'),
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



        #頁尾的資訊
        # myinfo = "匯款帳號：" + "\n" +"        新光銀行：八德分行" + "\n" + "        帳號：0596-50-000-6453" + "\n" + "        戶名：林泰成"
        #
        # #因為要套用字型Arialuni, 所以將comment改為Paragraph
        # comment = Paragraph('''
        #    <para align=left spaceb=3><font face="simhei" >'''+ str(myinfo).replace('\n','<br/>\n') +'''</font></para>''',
        #    styles["BodyText"])

        tax = int(bill.get_tax_amount())
        total = int(bill.get_grand_amount())

        footer = [
                    [ '', '', '','', ''   ],
                    [ '匯款帳號：', '', '金額小計：','', str('{:,.0f}'.format(int( bill.get_total_amount() )))   ],
                    ['','新光銀行：八德分行', '稅額：','', str('{:,.0f}'.format(int( tax )))  ],
                    ['','帳號：0596-50-000-6453', '請款金額：','', str('{:,.0f}'.format(int( total )))  ],
                    ['','戶名：林泰成', '', '',''  ],
                      ]

        f = Table(footer,colWidths=[ 0.6*inch, 2.5*inch, 2.5*inch, 0.6*inch, 0.6*inch] ,style=[

                            ('FONTNAME', (0,0),(4,-1), 'simhei'),
                            ('ALIGN',(2,0),(4,-1), 'RIGHT'),

                        ])

        Story.append(f)
        Story.append( PageBreak() )
        style = getSampleStyleSheet()['Normal']
        style.leading = 8
    doc.build(Story )
























# 單張的請款單, 作廢, 以批次列印的function取代
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

    h = Table(header, colWidths=[0.6*inch, 0.1*inch, 3.2*inch, 1.4*inch, 0.6*inch, 0.1*inch, 1.6*inch] ,style=[

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

        myitem.append( workdate)
        myitem.append( place)
        myitem.append( workdesc )
        myitem.append( str_qty )
        myitem.append(  str('{:,.0f}'.format(int( uniprice )))  )
        myitem.append(  str('{:,.0f}'.format(int( obj.item.get_amount() ))) )

        element.append(myitem)
        loopcounter += 1

    #repeatRows=1 是指第一行(表頭) 換頁時會重複
    t = Table(element, colWidths=[0.3*inch, 0.8*inch, 1.4*inch, 2.8*inch, 0.6*inch,  0.8*inch, 0.8*inch] , repeatRows=1)

    t.setStyle(
        TableStyle(
            [
            #   ('BACKGROUND',(0,0),(6,0),colors.skyblue),
            ('LINEBELOW', (0,0), (6,0), 1, colors.black),
             ('FONTNAME', (0,0),(6,-1), 'simhei'),
             ('ALIGN',(0,0),(0,0),'CENTER'),
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
                [ '', '', '','', ''   ],
                [ '匯款帳號：', '', '金額小計：','', str('{:,.0f}'.format(int( course.get_total_amount() )))   ],
                ['','新光銀行：八德分行', '稅額：','', str('{:,.0f}'.format(int( tax )))  ],
                ['','帳號：0596-50-000-6453', '請款金額：','', str('{:,.0f}'.format(int( total )))  ],
                ['','戶名：林泰成', '', '',''  ],
                  ]

    f = Table(footer,colWidths=[ 0.6*inch, 2.5*inch, 2.5*inch, 0.6*inch, 0.6*inch] ,style=[

                        ('FONTNAME', (0,0),(4,-1), 'simhei'),
                        ('ALIGN',(2,0),(4,-1), 'RIGHT'),

                    ])

    Story.append(f)


    style = getSampleStyleSheet()['Normal']
    style.leading = 8


    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPage )
