import math
import divecalculator
import sys
import getopt

# Initializee
tank_type      = ''
scr            = 0.0
oxygen_percent = 20.9 # Default to air
print_spacing  = 15

dive_calculator = divecalculator.DiveCalculator()

# Get input parameters
options, remainder = getopt.getopt(sys.argv[1:], 'o:s:t:', ['oxygen-percent=', 'scr=', "tank-type="])
for opt, arg in options:
  if opt in ('-o', '--oxygen-percent'):
    oxygen_percent = float(arg)
  elif opt in ('-s', '--scr'):
    scr = float(arg)
  elif opt in ('-t', '--tank-type'):
    if not arg in dive_calculator.getTankFactors():
      print('Invalid tank type')
      exit(1)
    tank_type = arg

# Validate
if '' == tank_type:
  print('Invalid tank type')
  exit(2)
if 0 == scr:
  print('Invalid SCR')
  exit(3)

# Output
print '***************************'
print('SCR        : '+str(scr)+' ft3/min')
print('Oxygen     : '+str(oxygen_percent)+' %')
print 'Tank Type  : '+str.upper(tank_type)
print '***************************'
print('MOD (ATA)  : '+str(dive_calculator.calculateFswMod(oxygen_percent, 1.4))+' ATA')
print('MOD (feet) : '+str(int(dive_calculator.convertAtaToFsw(dive_calculator.calculateFswMod(oxygen_percent, 1.4))))+' feet')
print '***************************'

# Plan dive
print 'FSW'.ljust(print_spacing), 'Min Gas'.ljust(print_spacing), 'PSI/min'.ljust(print_spacing), 'PSI/5-min'.ljust(print_spacing), 'PPO2'.ljust(print_spacing), 'ATA'.ljust(print_spacing)
for x in range(10,110,10):
  fsw       = str(x)+' ft'
  min_gas   = str(dive_calculator.roundUpPSI(dive_calculator.volumeToPressure(dive_calculator.planMinGas(x, dive_calculator.getMinGasScr()), tank_type)))+' PSI'
  psi_min   = str(int(dive_calculator.volumeToPressure(dive_calculator.planGas(x, scr),tank_type))) + ' PSI/min'
  psi_5_min = str(int(dive_calculator.volumeToPressure(dive_calculator.planGas(x, scr),tank_type))*5) + ' PSI/5min'
  ppo2      = str("{:.2f}".format(dive_calculator.calculatePPO2(oxygen_percent/100, x)))
  ata       = str(round(dive_calculator.depthFswToATA(x),2))

  if float(ppo2) > 1.4:
    continue

  print fsw.ljust(print_spacing), min_gas.ljust(print_spacing), psi_min.ljust(print_spacing), psi_5_min.ljust(print_spacing), ppo2.ljust(print_spacing), ata.ljust(print_spacing)
