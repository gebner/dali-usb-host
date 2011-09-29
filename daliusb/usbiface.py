import usb, time, sys

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
	    yield devh
	except Exception, e:
	  print e

def send_cmd_msg(devh, addr, cmd):
  for i in range(3):
    res = devh.controlMsg(usb.TYPE_VENDOR | usb.RECIP_DEVICE | usb.ENDPOINT_IN, 2, 1, addr | (cmd << 8))[0]
    if res == 0:
      return True
    time.sleep(50e-3)
  raise 'could not send dali msg'

def send_res_msg(devh):
  for i in range(3):
    res = devh.controlMsg(usb.TYPE_VENDOR | usb.RECIP_DEVICE | usb.ENDPOINT_IN, 3, 2, 0)
    if res[0] & 1:
      return res
    time.sleep(30e-3)
  raise 'did not receive msg result'

def send_cmd(devh, addr, cmd):
  try:
    send_cmd_msg(devh, addr, cmd)
    time.sleep(70e-3)
    return send_res_msg(devh)
  except:
    print sys.exc_info()[1]
    return None

def find_and_send_cmd(addr, cmd):
  for devh in find_dev():
    return send_cmd(devh, addr, cmd)
  return None
