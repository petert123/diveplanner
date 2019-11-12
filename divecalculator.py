import math

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

  def getTankFactors(self):
    return self.tank_factors

  def getMinGasScr(self):
    return self.min_gas_scr

  # Calculate SCR
  def calculateSCR(self, gas_volume, avg_depth, time):
    return round(gas_volume / (avg_depth / 33.3 + 1) / time, 2)

  # Calculate MOD
  def calculateFswMod(self, percent, ppo2):
    return ppo2 / (percent / 100)

  # Convert ATA to FSW
  def convertAtaToFsw(self, ata):
    return (ata-1)*33.3

  # Plan Min Gas
  def planMinGas(self, max_depth, scr):
    consumption = scr * 2
    averageATA  = (1+self.depthFswToATA(max_depth)) / 2
    time        = max_depth / 10 + 1
    
    return math.ceil(consumption * averageATA * time)

  # Convert pressure to volume
  def pressureToVolume(self, pressure, type):
    return float(pressure) / 100 * self.tank_factors[type]

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

