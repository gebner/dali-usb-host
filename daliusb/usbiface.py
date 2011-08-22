import usb

VENDOR_ID = 0x16c0
PRODUCT_ID = 0x05dc
MANUFACTURER = '2b7e.org'
PRODUCT = 'dali'

def bytes_to_ascii(bs):
  return ''.join(map(chr, bs[2::2]))

def usb_get_string(devh, i, langid = 0x0409, maxsize = 256):
  return bytes_to_ascii(devh.controlMsg(usb.ENDPOINT_IN,
    usb.REQ_GET_DESCRIPTOR, maxsize, (usb.DT_STRING << 8) + i, langid))

def find_dev():
  for bus in usb.busses():
    for dev in bus.devices:
      if dev.idProduct == PRODUCT_ID and dev.idVendor == VENDOR_ID:
	try:
	  devh = dev.open()
	  manuf = usb_get_string(devh, dev.iManufacturer)
	  prod = usb_get_string(devh, dev.iProduct)
	  if manuf == MANUFACTURER and prod == PRODUCT:
	    return devh
	except Exception, e:
	  print e

def send_cmd(devh, addr, cmd):
  devh.controlMsg(usb.TYPE_VENDOR | usb.RECIP_DEVICE | usb.ENDPOINT_IN, 2, 0, addr | (cmd << 8))

def find_and_send_cmd(addr, cmd):
  devh = find_dev()
  if devh is not None:
    send_cmd(devh, addr, cmd)
    return True
  return False
