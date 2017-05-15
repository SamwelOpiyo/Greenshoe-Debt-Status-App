# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.

def extract():
    import psycopg2
    myConnection = psycopg2.connect(port="6773",host="51.140.33.76", user="dev001", password="EV5gy2pQPDhC4H&fg3$5qzWL*9P4=D2K8ta9x&Qr2", dbname="testdb")
    cur = myConnection.cursor()

    global dict_data
    dict_data = {}
    cur.execute("SELECT attname FROM pg_attribute,pg_class WHERE attrelid=pg_class.oid AND relname='tbl_profiles' AND attstattarget <>0;")
    dict_data["tbl_profiles_names"] = cur.fetchall()

    cur.execute("SELECT attname FROM pg_attribute,pg_class WHERE attrelid=pg_class.oid AND relname='tbl_due_listing' AND attstattarget <>0;")
    dict_data["tbl_due_listing_names"] = cur.fetchall()

    cur.execute("select column_name, data_type, character_maximum_length from INFORMATION_SCHEMA.COLUMNS where table_name = 'tbl_profiles';")
    dict_data["tbl_profiles_properties"] = cur.fetchall()

    cur.execute("select column_name, data_type, character_maximum_length from INFORMATION_SCHEMA.COLUMNS where table_name = 'tbl_due_listing';")
    dict_data["tbl_due_listing_properties"] = cur.fetchall()

    cur.execute( "SELECT * FROM tbl_profiles;")
    dict_data["list_tbl_profiles"] = cur.fetchall()

    cur.execute( "SELECT * FROM tbl_due_listing;")
    dict_data["list_tbl_due_listing"] = cur.fetchall()

    cur.execute("SELECT * FROM pg_catalog.pg_tables;")
    dict_data["list_database_table_properties"] = cur.fetchall()

    cur.execute("SELECT table_schema || '.' || table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema');")
    dict_data["names_created_tables"] = cur.fetchall()

    myConnection.close()


def extract_duelisting():
    global list_tbl_due_listing
    import psycopg2
    myConnection = psycopg2.connect(port="6773",host="51.140.33.76", user="dev001", password="EV5gy2pQPDhC4H&fg3$5qzWL*9P4=D2K8ta9x&Qr2", dbname="testdb")
    cur = myConnection.cursor()
    cur.execute( "SELECT * FROM tbl_due_listing;")
    list_tbl_due_listing = cur.fetchall()
    myConnection.close()
    return list_tbl_due_listing
    

def extract_profiles():
    global list_tbl_profiles
    import psycopg2
    myConnection = psycopg2.connect(port="6773",host="51.140.33.76", user="dev001", password="EV5gy2pQPDhC4H&fg3$5qzWL*9P4=D2K8ta9x&Qr2", dbname="testdb")
    cur = myConnection.cursor()
    cur.execute( "SELECT * FROM tbl_profiles;")
    list_tbl_profiles = cur.fetchall()
    myConnection.close()
    return list_tbl_profiles
    


@user_passes_test(lambda u: u.is_staff, login_url='/debts/search/') 
#@user_passes_test(lambda u: u.groups.filter(name='role1').count() == 0,login_url='/debts/search/')
def profiles(request):
    extract_profiles()
    global list_tbl_profiles
    paginator = Paginator(list_tbl_profiles, 100) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        list_tbl_profiles_new = paginator.page(page)
    except  PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list_tbl_profiles_new = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list_tbl_profiles_new = paginator.page(paginator.num_pages)
    except:
        list_tbl_profiles_new = paginator.page(1)
    return render(request, 'jsonprofiles.html', {'profiles': list_tbl_profiles_new})

@user_passes_test(lambda u: u.is_staff, login_url='/debts/search/')
#@user_passes_test(lambda u: u.groups.filter(name='role1').count() == 0,login_url='/debts/search/')
def duelisting(request):
    extract_duelisting()
    global list_tbl_due_listing
    paginator = Paginator(list_tbl_due_listing, 100) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        list_tbl_due_listing = paginator.page(page)
    except  PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list_tbl_due_listing = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list_tbl_due_listing = paginator.page(paginator.num_pages)
    except:
        list_tbl_due_listing = paginator.page(1)
    return render(request, 'jsonduelisting.html', {'dues':list_tbl_due_listing})

def all(request):
    extract()
    global dict_data
    return HttpResponse((dict_data,dict_data["tbl_profiles_properties"],dict_data["tbl_due_listing_properties"],dict_data["list_tbl_profiles"],dict_data["list_tbl_due_listing"],dict_data["list_database_table_properties"]))


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@login_required  
def search(request):
    extract_profiles()
    if request.POST:
        print request.POST["search"]
        result = []
        for each in list_tbl_profiles:
            if request.POST["search"] in each[1] or int(request.POST["search"]) == each[2]:
                result.append(each)
        return render(request,'search.html', {'result':result })
	#return HttpResponseRedirect("/")
    else:
        return render(request,'search.html')


import csv
def csv_view(request):
    import StringIO
    extract_profiles()

    f = StringIO.StringIO()
    writer = csv.writer(f)
    #writers = csv.writer(response)
    writer.writerow(['Id', 'National Id', 'Mobile Number', 'Fully Cleared', 'Date Cleared', 'Clearing Mpesa Transaction Id', 'Batch Numbers'])
    for each in list_tbl_profiles:
        writer.writerow([each[0], each[1], each[2], each[3], each[4], each[5], each[6]])
    
    f.seek(0)
    response = HttpResponse(f, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Customer_debt_information.csv"'
    return response
    

def listing_csv(request):
    import StringIO
    extract_duelisting()

    f = StringIO.StringIO()
    writer = csv.writer(f)
 
    writer.writerow(['Id', 'Customer Mobile Number', 'Customer Id', 'Customer Name', 'Customer Account No', 'Loan Amount', 'Loan Issue Date', 'Loan Balance','Loan Due Date'])
    for each in list_tbl_due_listing:
        writer.writerow([each[0], each[8], each[2], each[1], each[3], each[4], each[6], each[5], each[7]])

    f.seek(0)
    response = HttpResponse(f, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Listings.csv"'
    return response




          
