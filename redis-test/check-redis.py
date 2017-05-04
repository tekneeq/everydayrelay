import redis

pool = redis.ConnectionPool(host='10.2.48.99', port=6379, db=0)
r = redis.StrictRedis(connection_pool=pool)
print r.ping()
cnt = 0
for k,v in r.hgetall('fromkeys').iteritems():
    cnt += 1
    print "%s: %s-%s" % (cnt, k,v)

cmd = "hscan fromkeys 0 match eugene*"
#cmd = "hscan fromkeys 0 match *:zaaaa0033*"
num, res = r.execute_command(cmd)
res = [i for i in res if ':' in i]
print res
