from __future__ import absolute_import
from __future__ import print_function
TABLE_NOW='texts'
TABLE_NEXT='texts2'

def make_metadata_db(dbname='llp',tablename=TABLE_NEXT, buffer_size=1000):
	import pymongo
	from pymongo import MongoClient

	client = MongoClient()
	db = client[dbname]
	table = db[tablename]
	print('>> removing')
	table.drop()

	from .. import corpus
	from corpus import corpora

	print('>> creating index')
	table.create_index([('corpus', pymongo.ASCENDING)])
	table.create_index([('corpus', pymongo.ASCENDING), ('id', pymongo.ASCENDING)],unique=True)

	for corpus_name,corpus in corpora():
		print('>>',corpus,'...')
		#if corpus_name!='ChadwyckDrama': continue
		ild=[]
		for ti,text in enumerate(corpus.texts()):
			if not text.id: continue
			#odx={'corpus_textid':(corpus_name, text.id), 'corpus':corpus_name, 'id':text.id}
			odx={'corpus':corpus_name, 'id':text.id}
			for k,v in list(text.meta.items()):
				if not k: continue
				k=k.replace('.','_')
				if k=='_id': continue
				odx[k]=v
			#odx=dict(odx.items())
			if '_id' in odx: del odx['_id']

			#print corpus_name,text.id,ti,table.insert_one(dict(odx.items())).inserted_id
			# try:
			# 	table.insert_one(odx)
			# except pymongo.errors.DuplicateKeyError as e:
			# 	print "!!",e
			# 	print "!!",odx


			ild+=[odx]

			if len(ild)>=buffer_size:
				try:
					print(odx['corpus'],odx['id'],len(ild),ti,table.insert_many(ild).inserted_ids[:2],'...')
				except pymongo.errors.BulkWriteError as e:
					print("!!",e)
				ild=[]

		if ild:
			try:
				print(odx['corpus'],odx['id'],len(ild),ti,table.insert_many(ild).inserted_ids[:2],'...')
			except pymongo.errors.BulkWriteError as e:
				print("!!",e)


def get_text_meta(corpus,text_id,dbname='llp',tablename=TABLE_NOW):
	from pymongo import MongoClient
	client = MongoClient()
	db = client[dbname]
	table = db[tablename]

	dx=table.find_one({'corpus':corpus, 'id':text_id})
	if dx and '_id' in dx: del dx['_id']
	return dx

def get_corpus_meta(corpus,dbname='llp',tablename=TABLE_NOW):
	from pymongo import MongoClient
	client = MongoClient()
	db = client[dbname]
	table = db[tablename]

	for dx in table.find({'corpus':corpus}):
		if dx and '_id' in dx: del dx['_id']
		yield dx
	#for dx in ld: del dx['_id']
	#return ld
