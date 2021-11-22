from idc import GetManyBytes
class AA:
    def cc(self):
        for b in GetManyBytes(0x402150, 168):
            print(b)
if __name__ == '__main__':
    alipay = AA()
    alipay.cc()