#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: zhangkai
Last modified: 2020-03-27 21:40:13
'''
import os  # NOQA: E402
import sys  # NOQA: E402
import urllib.parse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # NOQA: E402

import collections
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

import psutil
from apscheduler.schedulers.tornado import TornadoScheduler
from handler import bp as bp_disk
from monitor import FileMonitor
from pymongo import UpdateOne
from tornado.options import define, options
from tornado_utils import Application, bp_user
from utils import AioEmail, AioRedis, Motor, Request, connect

define('root', default='.', type=str)
define('auth', default=False, type=bool)
define('upload', default=True, type=bool)
define('delete', default=True, type=bool)
define('monitor', default=False, type=bool)
define('db', default='kk', type=str)
define('name', default='KK', type=str)
define('alist', default=False, type=bool)
define('quota', default=10240, type=int)
define('maxsize', default=5120, type=int)


class Application(Application):

    def init(self):
        self.opt.update({k.lower(): v for k, v in os.environ.items() if k.lower() in ['site_id', 'beian']})
        self.root = Path(options.root).expanduser().resolve()
        self.http = Request('tornado')
        self.monitor = FileMonitor(self.root)
        if options.monitor:
            self.monitor.start()

        self.sched = TornadoScheduler()
        self.sched.add_job(self.scan, 'cron', hour=4, minute=0,
                           executor='default',
                           next_run_time=datetime.now() + timedelta(seconds=60))

        if options.auth:
            self.db = Motor(options.db)
            self.email = AioEmail(use_tls=True)
            self.rd = AioRedis()
            self.sched.add_job(self.stat, 'interval', hours=1,
                               next_run_time=datetime.now() + timedelta(seconds=600))

        if options.auth and options.alist:
            token = 'alist-bc85b99e-f910-4126-9ee7-8d0b27ca24e6Ni9sfiJ0zLCskU44UET5bUyaKzHHo2M2YcuWbFGOOnrMoYtWwesWxmOjKtzMiAqg'
            self.opt.alist_address = os.environ.get('ALIST_ADDRESS', 'http://127.0.0.1:5244')
            self.opt.alist_token = os.environ.get('ALIST_TOKEN', token)
            self.sched.add_job(self.upload, 'interval', hours=1,
                               next_run_time=datetime.now() + timedelta(seconds=600))

        self.sched.start()

    async def shutdown(self):
        if options.monitor:
            self.monitor.stop()
        await super().shutdown()

    def scan(self):
        self.monitor.scan_dir(self.root, True)

    @staticmethod
    def decode(code):
        source = 'y8qto3nkalm67s0d5cxezgv4r9fh'
        checksum = sum(ord(c) for c in code[:-1]) % len(source)
        if code[-1] != source[checksum]:
            return None

        code = [x for x in code[:-1] if x in source]
        code = code[::-1]
        uid = 0
        for i, c in enumerate(code):
            uid += source.index(c) * pow(len(source), i)
        return uid

    async def stat(self):
        results = collections.defaultdict(lambda: collections.defaultdict(float))
        for k, files in self.monitor.files.items():
            uid = self.decode(k.relative_to(self.root).as_posix().split('/')[0])
            if not uid:
                continue
            for x in files:
                if not x.is_dir:
                    results['usage'][uid] += round(x.size / 1024 / 1024, 5)
                    results['files'][uid] += 1

        commands = [UpdateOne({'id': uid}, {'$set': {'usage': results['usage'][uid], 'files': int(results['files'][uid])}})
                    for uid in results['usage']]
        if self.opt.auth and commands:
            await self.db.users.bulk_write(commands)

    async def upload(self):
        exts = '''doc,docx,zip,rar,apk,txt,exe,7z,e,z,ct,ke,cetrainer,db,tar,pdf,w3x
epub,mobi,azw,azw3,osk,osz,xpa,cpk,lua,jar,dmg,ppt,pptx,xls,xlsx,mp3
ipa,iso,img,gho,ttf,ttc,txf,dwg,bat,imazingapp,dll,crx,xapk,conf
deb,rp,rpm,rplib,mobileconfig,appimage,lolgezi,flac
cad,hwt,accdb,ce,xmind,enc,bds,bdi,ssf,it
pkg,cfg,mp4,avi,png,jpeg,jpg,gif,webp'''.split(',')
        for k, files in self.monitor.files.items():
            for file in files:
                suffix = Path(file.path).suffix.lower()
                if not (suffix and suffix[1:] in exts):
                    continue
                if not (5 * 1024 * 1024 <= file.size <= 100 * 1024 * 1024):
                    continue
                if await self.db.disk.find_one({'path': file.path.as_posix()}):
                    continue
                url = f'{self.opt.alist_address}/api/fs/form'
                headers = {
                    'authorization': self.opt.alist_token,
                    'file-path': urllib.parse.quote(f'/lanzou/{file.path}'),
                }
                files = {'file': self.root / file.path}
                self.logger.info(f'uploading {file.path}')
                resp = await self.http.put(url, headers=headers, files=files, timeout=600)
                if resp.code == 200:
                    ret = resp.json()
                    if ret.code == 200:
                        doc = {
                            'path': file.path.as_posix(),
                            'created_at': datetime.now().replace(microsecond=0),
                        }
                        await self.db.disk.update_one({'path': doc['path']}, {'$set': doc}, upsert=True)
                        self.logger.info(f'upload {file.path} succeed')
                    else:
                        self.logger.info(f'upload {file.path} failed: {ret.message}')
                else:
                    self.logger.info(f'upload {file.path} failed: {resp}')

    def get_md5(self, path):
        if path.is_file():
            md5 = hashlib.md5()
            with path.open('rb') as fp:
                while True:
                    data = fp.read(4194304)
                    if not data:
                        break
                    md5.update(data)
            return md5.hexdigest()

    def get_port(self):
        port = 8000
        try:
            connections = psutil.net_connections()
            ports = set([x.laddr.port for x in connections])
            while port in ports:
                port += 1
        except:
            while connect('127.0.0.1', port):
                port += 1
        return port


def main():
    kwargs = dict(
        static_path=Path(__file__).parent.absolute() / 'static',
        template_path=Path(__file__).parent.absolute() / 'templates',
    )
    app = Application(**kwargs)
    app.register(bp_disk, bp_user)
    port = options.port if options.auth or options.port != 8000 else app.get_port()
    max_body_size = 10240 * 1024 * 1024
    app.run(port=port, max_body_size=max_body_size)


if __name__ == '__main__':
    main()
