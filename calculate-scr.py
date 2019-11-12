import math
import getopt
import sys
import divecalculator

dive_calculator = divecalculator.DiveCalculator()

# Initialize
psi_start = 0
psi_end   = 0
time      = 0
avg_depth = 0.0
tank_type = ''

# Get input parameters
options, remainder = getopt.getopt(sys.argv[1:], 's:e:m:t:a:', ['start-psi=', 'end-psi=','minutes=', "tank-type=", "average-depth="])
for opt, arg in options:
  if opt in ('-s', '--start-psi'):
    psi_start = int(arg)
  elif opt in ('-e', '--end-time'):
    psi_end = int(arg)
  elif opt in ('-m', '--minutes'):
    time = int(arg)
  elif opt in ('-t', '--tank-type'):
    if not arg in dive_calculator.getTankFactors():
      print('Invalid tank type')
      exit(1)
    tank_type = arg
  elif opt in ('-a', '--average-depth'):
    avg_depth = float(arg)

# Validate
if 0 == psi_start:
  print('Starting PSI missing')
  exit(1)
if 0 == psi_end:
  print('Ending PSI missing')
  exit(2)
if 0 == time:
  print('Invalid time in minutes')
  exit(3)
if 0 == avg_depth:
  print('Invalid average depth')
  exit(4)
if '' == tank_type:
  print('Invalid tank type')
  exit(5)

# Post dive
print '***************************'
print 'Avg Depth   : ' + str(avg_depth) + ' feet'
print 'Gas Used    : ' + str(psi_start - psi_end) + ' PSI'
print 'Volume Used : ' + str(dive_calculator.pressureToVolume(psi_start-psi_end , tank_type)) + ' ft3'
print 'Dive Time   : ' + str(time) + ' min'
print 'Tank Type   : ' + str.upper(tank_type)
print '***************************'
print 'SCR         : ' + "{:.2f}".format(dive_calculator.calculateSCR(dive_calculator.pressureToVolume(psi_start-psi_end , tank_type), avg_depth, time)) + ' ft3/min'

