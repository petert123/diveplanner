import math


# Dive Profile
avg_depth = 30 # Feet
psi_start = 3300 # PSI
psi_end   = 1350 # PSI
time      = 53 # Minutes
tank_type = 'hp100'
o2Percent = .32


class DiveCalculator:

  min_gas_scr  = .75
  my_scr       = .55
  tank_factors = {'al80':  2.5,
                  'al40':  1,
                  'hp100': 3,
                  'hp120': 3.5,
                  'hp130': 3.5,
                  'lp85':  3,
                  'lp95':  3.5,
                  'lp104': 4,
                  'dal80':  5,
                  'dal40':  2,
                  'dhp100': 6,
                  'dhp120': 7,
                  'dhp130': 7,
                  'dlp85':  6,
                  'dlp95':  7,
                  'dlp104': 8,
              }

  # Calculate SCR
  def calculateSCR(self, gas_used, avg_depth, time, type):
    return round(self.pressureToVolume(gas_used, type) / (avg_depth / 33.3 + 1) / time, 2)

  # Plan Min Gas
  def planMinGas(self, max_depth, scr):
    consumption = scr * 2
    averageATA  = self.depthFswToATA(max_depth) / 2
    time        = max_depth / 10 + 1
    
    return math.ceil(consumption * averageATA * time)

  # Convert pressure to volume
  def pressureToVolume(self, pressure, type):
    return pressure / 100 * self.tank_factors[type]

  # Convert volume to pressure
  def volumeToPressure(self, volume, type):
    return volume / self.tank_factors[type] * 100

  # Round to nearest hundred PSI
  def roundUpPSI(self, psi, roundLessThan500=True):
    if not roundLessThan500:
      return int(math.ceil(psi / 100.0)) * 100
    val = int(math.ceil(psi / 100.0)) * 100
    if val < 500:
      return 500
    return val

  # Calculate PPO2 of Nitrox
  def calculatePPO2(self, percent, depth):
    return round(percent * self.depthFswToATA(depth), 2)

  # Convert depth / feet sea water to ATA
  def depthFswToATA(self, depth):
    return depth / 33.3 + 1

  # Plan gas consumption rate
  def planGas(self, depth, scr=0):

    if (0==scr):
      scr = self.my_scr

    # Gas volume used per minute
    #return math.ceil(scr * self.depthFswToATA(depth))
    return round(scr * self.depthFswToATA(depth), 2)


dive_calculator = DiveCalculator()


# Post dive
print 'Calculations based on:'
print 'Avg Depth: ' + str(avg_depth) + ' feet'
print 'Gas Used:  ' + str(psi_start - psi_end) + ' PSI'
print 'Tank Type: ' + str.upper(tank_type)
print 'Dive Time: ' + str(time) + ' minutes'
print '**********************'
print 'SCR:       ' + str(dive_calculator.calculateSCR(psi_start - psi_end, avg_depth, time, 'hp100'))
print '----'
print ''

# Pre dive
print 'Gas Planning / Min Gas:'
for x in range(10,110,10):
  min_gas = dive_calculator.roundUpPSI(dive_calculator.volumeToPressure(dive_calculator.planMinGas(x, dive_calculator.min_gas_scr), tank_type))
  ppo2 = dive_calculator.calculatePPO2(o2Percent, x)
  print str.upper(tank_type) + ' @ ' + str(x) +'ft: ' + str(min_gas)


print '--------'
print 'Gas Tracking:'
for x in range(10,110,10):
  print str(x) + 'ft: ' + str(int(dive_calculator.volumeToPressure(dive_calculator.planGas(x),tank_type))) + 'PSI/min'
