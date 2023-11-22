from django.shortcuts import render,get_object_or_404
from webmash.models import Category,AboutUs,Post,PostTags,Writer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from random import shuffle
from django.http import HttpResponse,JsonResponse
from webmash import serializers

def main(request):
	query=Post.objects.all().order_by('heading')
	main_post=query[:4]
	remaining_post=query
	writer=Writer.objects.all()
	latest=Post.objects.all().order_by('post_date')[:4]
	query2=list(Post.objects.all()[:4])

	shuffle(query2)
	print(query2)
	popular=query2
	aboutus=AboutUs.objects.all()
	tag=PostTags.objects.all().order_by('text')
	catt=Category.objects.all().order_by('text')
	page = request.GET.get('page', 1)
	paginator = Paginator(remaining_post, 1)
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)
	return render(request,'main.html',{'mainp':main_post,'writer':writer,
		'latest':latest,'popular':popular,'tag':tag,'catt':catt,'cat':users,'a':aboutus})

def category(request):
	query=Category.objects.all().order_by('text').distinct()
	aboutus=AboutUs.objects.all()
	return render(request,'category.html',{'cat':query,'a':aboutus})

def posttags(request):
	query=PostTags.objects.all().order_by('text').distinct()
	aboutus=AboutUs.objects.all()
	return render(request,'posttags.html',{'cat':query,'a':aboutus})

def catdetail(request,arg):
	test=get_object_or_404(Category,text=arg)
	querys=Post.objects.filter(Category__text=arg)
	aboutus=AboutUs.objects.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(querys, 2)
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)
	return render(request,'category_detail.html',{'cat':users,'a':aboutus,'arg':arg
		})

def api_category_detail(request,cat):
	test=get_object_or_404(Category,id=cat)
	querys=Post.objects.filter(Category__id=cat).prefetch_related('writer')
	return JsonResponse({'category':test.text ,'posts':serializers.NewPostSerializers(querys)})

def api_tagdetail(request,tag):
	test=get_object_or_404(PostTags,id=tag)
	querys=Post.objects.filter(posttags__id=tag).prefetch_related('writer')
	return JsonResponse({'tag':test.text,'posts':serializers.NewPostSerializers(querys)})

def postdetail(request,pkid):
	query=get_object_or_404(Post,id=pkid)
	past=Post.objects.none()
	nextt=Post.objects.none()
	if Post.objects.filter(id=pkid-1).exists():
		past=Post.objects.get(id=pkid-1)
	if Post.objects.filter(id=pkid+1).exists():
		nextt=Post.objects.get(id=pkid+1)
	aboutus=AboutUs.objects.all()
	return render(request,'postdetail.html',{'cat':query,'a':aboutus,'p':past,'n':nextt})

def api_writer(request):
	query=Writer.objects.all()
	res={
	'id':query[0].id,
	'name':query[0].name,
	'bio':query[0].bio,
	'pic':query[0].ProfilePic.url
	}
	return JsonResponse({'writer':res})

def api_mainpost(request,pkid):
	query=get_object_or_404(Post,id=pkid)
	past=Post.objects.none()
	nextt=Post.objects.none()
	pastpost={}
	if Post.objects.filter(id=pkid-1).exists():
		past=Post.objects.get(id=pkid-1)
		pastpost['id']=past.id
		pastpost['headline']=past.heading
	nextpost={}
	if Post.objects.filter(id=pkid+1).exists():
		nextt=Post.objects.get(id=pkid+1)
		nextpost['id']=nextt.id
		nextpost['headline']=nextt.heading
	lol=Post.objects.filter(id=pkid).prefetch_related('posttags','writer')
	return JsonResponse({
		"post":serializers.APIPostSerializer(lol),
		"prev":pastpost,
		"next":nextpost
		})

def tagdetail(request,arg):
	test=get_object_or_404(PostTags,text=arg)
	querys=Post.objects.filter(posttags__text=arg)
	aboutus=AboutUs.objects.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(querys, 4)
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)
	return render(request,'post_detail.html',{'cat':users,'a':aboutus,'arg':arg
		})

def search(request):
	if request.method=="POST":
		p,c,t=GetSearchResults(request.POST['search_input'])
		return render(request,'search.html',{'p':p,'c':c,'t':t})
	else:
		return HttpResponse("Invalid Action!!!")

def GetSearchResults(query):
	post_result=Post.objects.filter(heading__icontains=query)
	category_result=Category.objects.filter(text__icontains=query)
	tag_result=PostTags.objects.filter(text__icontains=query)
	return post_result,category_result,tag_result

def api_main(request):
	remaining_post=Post.objects.all().order_by('heading')
	page = request.GET.get('page', 1)
	paginator = Paginator(remaining_post, 1)
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)
	return JsonResponse({
		'main_post':serializers.PostSerializers(users.object_list),
		'pages':paginator.num_pages
		})
def api_categories(request):
	query=Category.objects.all().order_by('text').distinct()
	return JsonResponse({'categories':serializers.CategorySerializer(query)})

def api_posttags(request):
	query=PostTags.objects.all().order_by('text').distinct()
	return JsonResponse({'posttags':serializers.PostTagsSerializer(query)})
