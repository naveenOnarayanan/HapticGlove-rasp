from time import sleep
import peltier as peltier

print 'init'
peltier.Peltier.init()

print "hot"
peltier.Peltier.hot()
sleep(10)

print "cold"
peltier.Peltier.cold()
sleep(10)

peltier.Peltier.stop()
