# This is a debug mode for your code. Import this at the start of your code
# It is deactivated by default
# if you want the information printed, use the debug_info function
# In your code you can use if statements to use debug mode
# Ex:
#   if debug:
#       __Code during debug mode__
#   else:
#       __Code without debug mode__


from KloockyDE.helpers import str_len

debug = False   # Change this to True to activate Debug mode

def debug_info(lines=None):
    '''
    Print debug information
    :param lines:   list : list of lines you want in the debug information
    '''
    if not debug:
        return
    # checks and default values for parameters
    if lines is None:
        lines = []
    lines = list(lines)
    for line in lines:
        if type(line) != str:
            raise TypeError('All lines have to be of type str')
    # actual code starts here
    deb_lines = ['Debug mode is on. These Changes will apply:'] + lines     # Add the lines
    # make it pretty
    deb_m = max(*[len(x) for x in deb_lines])
    deb_lines = ['║ ' + str_len(x, deb_m) + ' ║\n' for x in deb_lines]
    deb_lines.append('╔' + str_len('', deb_m+2, '═') + '╗\n')
    for i in range(len(deb_lines) - 1):
        deb_lines[-1] += deb_lines[i]
    deb_lines[-1] += '╚' + str_len('', deb_m+2, '═') + '╝'
    print(deb_lines[-1])    # print the info
    del deb_m
    del deb_lines