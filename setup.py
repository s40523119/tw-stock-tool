#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyInstaller.__main__ import run

if __name__ == '__main__':
    opts = ['-w','--paths=C:\\Users\\Kane\\AppData\\Local\\Programs\\Python\\Python37-32\\Lib\\site-packages\\PyQt5\\Qt\\bin',
            '--paths=C:\\Users\\Kane\\AppData\\Local\\Programs\\Python\\Python37-32\\Lib\\site-packages\\PyQt5\\Qt\\plugins',
            '--paths=C:\\Windows\\WinSxS\\x86_microsoft-windows-m..namespace-downlevel_31bf3856ad364e35_10.0.17134.1_none_50c6cb8431e7428f',
            '--paths=C:\\Windows\\System32',
            '--icon', 'C:\\Users\\Kane\\Documents\\Untitled Folder\\money.ico',
            'stock.py']

    run(opts)
