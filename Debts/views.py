# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    import psycopg2
    myConnection = psycopg2.connect(port="6773",host="51.140.33.76", user="dev001", password="EV5gy2pQPDhC4H&fg3$5qzWL*9P4=D2K8ta9x&Qr2", dbname="testdb")
    cur = myConnection.cursor()
    cur.execute("select row_to_json(tbl_due_listing) from tbl_due_listing;")

    global g
    g=cur.fetchall()
    return g

def extract_profiles():
    import psycopg2
    myConnection = psycopg2.connect(port="6773",host="51.140.33.76", user="dev001", password="EV5gy2pQPDhC4H&fg3$5qzWL*9P4=D2K8ta9x&Qr2", dbname="testdb")
    cur = myConnection.cursor()
    cur.execute("select row_to_json(tbl_profiles) from tbl_profiles;")
    global f
    f=cur.fetchall()
    return f


import json
def all(request):
    extract()
    return HttpResponse(dict_data.values())
    
def profiles(request):
    #return HttpResponse(json.dumps(extract_profiles()))
    extract_profiles()
    global f
    paginator = Paginator(f, 25) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        f = paginator.page(page)
    except  PageNotAnInteger:
        # If page is not an integer, deliver first page.
        f = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        f = paginator.page(paginator.num_pages)
    except:
        f = paginator.page(1)
    return render(request, 'jsonprofiles.html', {'profiles':f})

def duelisting(request):
    #return HttpResponse(json.dumps(extract_duelisting()))
    extract_duelisting()
    global g
    paginator = Paginator(g, 25) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        g = paginator.page(page)
    except  PageNotAnInteger:
        # If page is not an integer, deliver first page.
        g = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        g = paginator.page(paginator.num_pages)
    except:
        g = paginator.page(1)
    return render(request, 'jsonduelisting.html', {'dues':g})
