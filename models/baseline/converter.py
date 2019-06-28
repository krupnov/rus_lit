def char2num(sym):
    if sym == ' ':
        return 2000
    return int.from_bytes(sym.encode('utf8'), byteorder='big') - int.from_bytes('а'.encode('utf8'), byteorder='big')

def num2char(num):
    if num == 2000:
        return ' '
    return (int.from_bytes('а'.encode('utf8'), byteorder='big') + num).to_bytes(2, byteorder='big').decode('utf8')

sant_num = [[char2num(ch) for ch in s] for s in by_sant]
sant_from_num = [''.join([num2char(num) for num in ar]) for ar in sant_num]
