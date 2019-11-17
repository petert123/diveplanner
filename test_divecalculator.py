import divecalculator


def test_mod_32():
  d = divecalculator.DiveCalculator()
  assert 4.375 == d.calculateFswMod(32, 1.4)

def test_mod_100():
  d = divecalculator.DiveCalculator()
  assert 1.6 == d.calculateFswMod(100, 1.6)

def test_ata_to_fsw():
  d = divecalculator.DiveCalculator()
  assert 0 == d.convertAtaToFsw(1)
  assert 66.6 == d.convertAtaToFsw(3)

def test_min_gas():
  d = divecalculator.DiveCalculator()
  assert .53 == d.calculateSCR(50, 45, 40)
  assert .58 == d.calculateSCR(70, 100, 30)

def test_plan_min_gas():
  d = divecalculator.DiveCalculator()
  assert 28 == d.planMinGas(100, .5)
  assert 16 == d.planMinGas(60, .6)

def test_pressure_to_volume():
  d = divecalculator.DiveCalculator()
  assert 30 == d.pressureToVolume(1000, 'hp100')
  assert 120 == d.pressureToVolume(2000, 'dhp100')
  assert 28 == d.pressureToVolume(800, 'hp120')

def test_volume_to_pressure():
  d = divecalculator.DiveCalculator()
  assert 1200 == d.volumeToPressure(30, 'al80')

def test_round_up_psi():
  d = divecalculator.DiveCalculator()
  assert 800 == d.roundUpPSI(792)
  assert 500 == d.roundUpPSI(432)
  assert 1000 == d.roundUpPSI(921)

