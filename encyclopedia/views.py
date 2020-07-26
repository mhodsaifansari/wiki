from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect,Http404
from django.contrib import messages
from django.urls import reverse
from . import util
import markdown2
from django import forms
import random
class Pageform(forms.Form):
    title = forms.CharField(label="Title of Page")
    content = forms.CharField(label="Page Content",widget=forms.Textarea)
def search(temp,request):
    if util.get_entry(temp['q']) is not None:
                a = reverse("goto",None,[temp['q']])
                return HttpResponseRedirect(a)
    else:
            l=[]
            t=util.list_entries()
            for a in t:
                if str(temp['q']) in str(a):
                    l+=[a]
            return render(request, "encyclopedia/index.html", {
            "entries": l
            })
def randompage(request):
    l=random.choice(util.list_entries())
    return search({'q':l},request)

def index(request):
        temp = request.GET
        if bool(temp) is False:

            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
            })
        else:
           return search(temp,request)

def goto(request,name):
    temp = request.GET
    if bool(temp) is False:
        en=util.get_entry(name)
        if en is None:
            raise Http404
        else:
            return render(request,"encyclopedia/wiki.html",{
                "name":name,
                "entries":markdown2.markdown(en)
            })
    else:
        return search(temp,request)

def newpage(request):
    if request.method == "POST":
        form = Pageform(request.POST)
        if form.is_valid():
            if util.get_entry(form.cleaned_data["title"]) is None:
                util.save_entry(form.cleaned_data["title"],form.cleaned_data["content"])
                
                return HttpResponseRedirect(reverse("goto",None,[form.cleaned_data["title"]]))
            else:
                alert=["this title already exist"]
                return render(request,"encyclopedia/newpage.html",{
                    "form":form,
                    "alert":alert
                })
    elif request.method == "GET":
        temp=request.GET
        if bool(temp) is False:
                return render(request,"encyclopedia/newpage.html",{
                "form":Pageform()
                 })
        else:
           return search(temp,request)

def edit(request,name):
    if request.method=="POST":
        page=Pageform(request.POST)
        if page.is_valid():
            util.save_entry(name,page.data["content"])
            return HttpResponseRedirect(reverse("goto",None,[name]))
    form = Pageform({"title":name,"content":util.get_entry(name)})
    return render(request,"encyclopedia/edit.html",{
        "name":name,
        "form":form
    })