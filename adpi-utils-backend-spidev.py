#!/usr/bin/python3

import spidev
import smbus
import adpi
import sys
import re
from time import sleep

DEVICE_CLASS = {
	"adpipro": adpi.ADPiPro,
}
RAW_OFFSET = (1 << 23)
RAW_SCALE = (
	0.000596040,
	0.000298020,
	0.000149010,
	0.000074500,
	0.000037250,
	0.000018620,
	0.000009310,
	0.000004650,
)
TEMP_VREF = 1.17

def v2k(dict, val):
	for k, v in dict.items():
		if v == val:
			return k

def single_conversion(dev, ch):
	c = dev.adc.channel[ch]
	g, _ = dev.read_configuration()
	dev.write_configuration(g, c)
	_, r = dev.read_mode()
	dev.write_mode(dev.adc.mode['single'], r)
	rate = v2k(dev.adc.rate, r)
	
	while True:
		sleep(2 * 1.0 / float(rate))
		if not dev.read_status() & 0x80:
			break
	
	raw = dev.read_data()
	return raw, g

def set_calib(dev, g):
	bias = dev.load_bias(g)
	scale = dev.load_scale(g)
	_, r = dev.read_mode()
	for i in range(dev.channels):
		dev.write_configuration(g, i)
		dev.write_mode(dev.adc.mode['idle'], r)
		dev.write_offset(bias[i])
		dev.write_mode(dev.adc.mode['idle'], r)
		dev.write_fullscale(scale[i])

def get_frequency(dev):
	_, r = dev.read_mode()
	rate = v2k(dev.adc.rate, r)
	return rate

def set_frequency(dev, vals):
	rate = vals[0]
	r = dev.adc.rate[rate]
	dev.write_mode(dev.adc.mode['idle'], r)

def get_gain(dev):
	g, _ = dev.read_configuration()
	gain = v2k(dev.adc.gain, g)
	return gain

def set_gain(dev, vals):
	gain = vals[0]
	g = dev.adc.gain[gain]
	dev.write_configuration(g, 0)
	set_calib(dev, g)

def get_output(dev, vals):
	c = dev.adc.channel[vals[0]]
	out = dev.get_output(c)
	if out:
		return 'on'
	else:
		return 'off'

def set_output(dev, vals):
	c = dev.adc.channel[vals[0]]
	val = vals[1]
	if val == 'on':
		dat = 1
	elif val == 'off':
		dat = 0
	else:
		dat = int(val)
	dev.set_output(c, dat)

def get_scale(dev):
	g, _ = dev.read_configuration()
	scale = RAW_SCALE[g]
	return "{0:.9f}".format(scale)
	
def set_scale(dev, vals):
	scale = float(vals[0])
	for g in range(len(RAW_SCALE)):
		if RAW_SCALE[g] == scale:
			dev.write_configuration(g, 0)
			set_calib(dev, g)
			return
	raise KeyError(scale)

def get_temperature(dev):
	raw, _ = single_conversion(dev, 'temp')
	temp = 1170.0 * (raw - RAW_OFFSET) / (2 ** 23) / 0.81 - 273.15
	return "{0:.9f}".format(temp)

def get_voltage(dev, vals):
	ch = vals[0]
	raw, g = single_conversion(dev, ch)
	vol = RAW_SCALE[g] * (raw - RAW_OFFSET)
	return "{0:.9f}".format(vol)

def adpi_get(dev, opts):
	param = opts[0]
	vals = opts[1:]
	if param in ("frequency", "gain", "scale", "temperature"):
		return eval('get_' + param)(dev)
	elif param in ("output", "voltage"):
		return eval('get_' + param)(dev, vals)
	else:
		raise ValueError(param)

def adpi_set(dev, opts):
	param = opts[0]
	vals = opts[1:]
	if param in ("frequency", "gain", "output", "scale"):
		eval('set_' + param)(dev, vals)
	else:
		raise ValueError(param)

def adpi_reset(dev):
	dev.reset()

#
# Usage: adpi-utils-backend-spidev.py 
#          devie=<DEV_NAME> adc=<ADC_SPI> eeprom=<EEPROM_I2C> gpio=<GPIO_I2C> \
#          { get | set } <PARAM> [VALUE [,...]]
#
if __name__ == "__main__":
	args = sys.argv
	adpidev = DEVICE_CLASS[re.findall(r'device=(.*)', args[1])[0]]
	spinum = re.findall(r'spi(\d+)\.(\d+)', args[2])[0]
	spibus = int(spinum[0])
	spics = int(spinum[1])
	eepromnum = re.findall(r'(\d+)-(\d+)', args[3])[0]
	eeprombus = int(eepromnum[0])
	eepromaddr = int(eepromnum[1], 16)
	gpionum = re.findall(r'(\d+)-(\d+)', args[4])[0]
	gpiobus = int(gpionum[0])
	gpioaddr = int(gpionum[1], 16)
	cmd = args[5]
	opts = args[6:]
	
	spi = spidev.SpiDev()
	i2c = smbus.SMBus(eeprombus)
	try:
		spi.open(spibus, spics)
		spi.mode = 0b11
		spi.max_speed_hz = 1000000
		
		ad = adpidev(spi, i2c, eepromaddr, gpioaddr)
		
		if cmd == 'get':
			print(adpi_get(ad, opts))
		elif cmd == 'set':
			adpi_set(ad, opts)
		elif cmd == 'reset':
			adpi_reset(ad)
		else:
			raise ValueError(cmd)
		
	except (IndexError, ValueError):
		sys.exit(2)
	finally:
        	spi.close()

