alphabet = "abcdefghijklmnopqrstuvwxyz"
ziffern = "0123456789"
sonderzeichen = " ,;.:-_#'+*~@€<>|^°" + '"§$%&/=?`´(){}[]'
escape_chars = "\\\n\t"
ascii_128 = ' !"#$%&' + "'()*+,-./" + ziffern + ":;<=>?@" + alphabet.upper() + "[\\]^_`" + alphabet + "{|}~"
ascii_128_alle = ['NUL', 'SOH', 'STX', 'ETX', 'EOT', 'ENQ', 'ACK', 'BEL', 'BS', 'TAB', 'LF', 'VT', 'FF', 'CR', 'SO', 'SI', 'DLE', 'DC1', 'DC2', 'DC3', 'DC4', 'NAK', 'SYN', 'ETB', 'CAN', 'EM', 'SUB', 'ESC', 'FS', 'GS', 'RS', 'US']
ascii_128_alle = ascii_128_alle + list(ascii_128) + ["DEL"]
