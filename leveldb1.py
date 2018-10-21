#coding: utf-8
import leveldb

db = leveldb.LevelDB('./leveldb')
put_in = hash('hahaha')
db.Put('foo',str(put_in))
print 11111
try:db.Get('foo1')
except:print('not exist')
#db.Delete('foo')
print db.Get('foo')