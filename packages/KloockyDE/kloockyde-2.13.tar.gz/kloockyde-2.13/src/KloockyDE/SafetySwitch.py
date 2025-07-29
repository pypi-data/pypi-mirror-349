#   Import this at beginning of code (or where you need a safety switch)
#   Raises an Exception and with that stops the execution of code
#   Put in Comment to disengage and let the code run through

class SafetySwitch(Exception):
    pass


raise SafetySwitch('Safety Switch is engaged')
