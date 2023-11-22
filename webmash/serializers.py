from webmash.models import Category,AboutUs,Post,PostTags,Writer
from django.utils.safestring import SafeString
def CategorySerializer(query):
	result=[]
	for q in query:
		result.append({'id':q.id,'text':q.text,'count':q.post_set.count()})
	return result

def PostTagsSerializer(query):
	result=[]
	for q in query:
		result.append({'id':q.id,'text':q.text,'count':q.post_set.count()})
	return result

def Category_Post(query):
	result=[]
	for q in query:
		result.append({'id':q.id,'headline':q.heading})
	return result

def MainPostSerializer(query):
	result=[]
	for q in query:
		result.append({'id':q.id,'headline':q.heading,'image':q.first_image.url,'date':q.getyear()})
	return result

def PostSerializers(query):
	result=[]
	for q in query:
		result.append({
			'id':q.id,
			'headline':q.heading,
			'summary':q.meta,
			'image':q.first_image.url,
			'date':q.getyear(),
			'writer':{
			'id':q.writer.id,
			'name':q.writer.name,
			'pic':q.writer.ProfilePic.url
			}})
	return result

def NewPostSerializers(query):
	result=[]
	for q in query:
		result.append({
			'id':q.id,
			'headline':q.heading,
			'summary':q.meta,
			'image':q.first_image.url,
			'date':q.getyear(),
			'writer':{
			'id':q.writer.id,
			'name':q.writer.name,
			'pic':q.writer.ProfilePic.url
			}})
	return result

def WriterSerializer(q):
	return {
	    'id':q.id,
	    'name':q.name,
	    'pic':q.ProfilePic.url
	}

def PagePostSerializers(query):
	result=[]
	for q in query:
		result.append({
			'id':q.id,
			'headline':q.heading,
			'summary':q.meta,
			'content':q.content,
			'writer':{
			'id':q.writer.id,
			'name':q.writer.name,
			'pic':q.writer.ProfilePic.url
			}})
	return result

def APIPostSerializer(res):
	result={}
	for r in res:
		result['id']=r.id
		result['posttags']=CategorySerializer(r.posttags.all())
		result['content']=SafeString(r.content)
		result['headline']=r.heading
		result['image']=r.first_image.url
		result['date']=r.getyear()
		result['writer']=WriterSerializer(r.writer)
	return result