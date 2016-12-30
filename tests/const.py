import sys
sys.path.append("..")

from ztool import const

const.name = "zuston"
print const.name

try:
    const.name = "shacha"
except Exception as e:
    print e