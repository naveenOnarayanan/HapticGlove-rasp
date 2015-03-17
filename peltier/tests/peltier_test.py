from time import sleep
import peltier.peltier as peltier

print 'init'
peltier.Peltier.init()

print "hot"
peltier.Peltier.hot()
sleep(5)

print "cold"
peltier.Peltier.cold()
sleep(5)

peltier.Peltier.stop()
