#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: zhangkai
Last modified: 2020-03-27 21:17:57
'''

import asyncio
import datetime
import functools
import hashlib
import io
import json
import math
import re
import shutil
import string
import tarfile
import tempfile
import time
import urllib.parse
import zipfile
from functools import cached_property
from pathlib import Path

import markdown
import tornado.web
from bson import ObjectId
from tornado.concurrent import run_on_executor
from tornado_utils import BaseHandler, Blueprint
from utils import Dict

bp = Blueprint(__name__)


def check_auth(method):
    @functools.wraps(method)
    async def wrapper(self, name, *args, **kwargs):
        if await self.check(name):
            await method(self, name, *args, **kwargs)
        elif self.request.method in ['GET', 'HEAD']:
            url = self.get_login_url()
            if "?" not in url:
                if urllib.parse.urlsplit(url).scheme:
                    # if login url is absolute, make next absolute too
                    next_url = self.request.full_url()
                else:
                    assert self.request.uri is not None
                    next_url = self.request.uri
                url += "?" + urllib.parse.urlencode(dict(next=next_url))
            return self.redirect(url)
        else:
            raise tornado.web.HTTPError(403)

    return wrapper


class BaseHandler(BaseHandler):

    default = {
        'pptx.png': ['.ppt', '.pptx'],
        'docx.png': ['.doc', '.docx'],
        'xlsx.png': ['.xls', '.xlsx'],
        'pdf.png': ['.pdf'],
        'txt.png': ['.txt'],
        'vue.png': ['.vue'],
        'exe.png': ['.exe'],
        'dmg.png': ['.dmg', '.pkg'],
        'apk.png': ['.apk'],
        'iso.png': ['.iso'],
        'json.png': ['.json'],
        'yaml.png': ['.yml', '.yaml'],
        'xml.png': ['.xml'],
        'ini.png': ['.ini'],
        'markdown.png': ['.md'],
        'kindle.png': ['.mobi', '.epub'],
        'database.png': ['.db', '.sql'],
        'image.png': ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp', '.svg', '.avif', '.ico'],
        'audio.png': ['.amr', '.ogg', '.wav', '.mp3', '.flac', '.wma', '.aac'],
        'video.png': ['.rmvb', '.rm', '.mkv', '.mov', '.mp4', '.m4v', '.avi', '.wmv', '.mpeg', '.flv', '.f4v', '.m3u8', '.ts'],
        'zip.png': ['.rar', '.tar', '.tgz', '.gz', '.bz2', '.xz', '.zip', '.7z', '.z'],
        'c.png': ['.c', '.h'],
        'cpp.png': ['.cpp'],
        'python.png': ['.py', '.pyc'],
        'shell.png': ['.sh'],
        'golang.png': ['.go'],
        'java.png': ['.java', '.javac', '.class', '.jar'],
        'javascript.png': ['.js'],
        'html.png': ['.html'],
        'css.png': ['.css', '.less', '.sass', '.scss'],
    }
    icon = {}
    for key, value in default.items():
        for v in value:
            icon[v] = key

    @staticmethod
    def convert_size(size):
        ret = size / (1024 * 1024 * 1024 * 1024)
        if ret >= 1:
            return f'{ret:.1f} TB'
        ret *= 1024
        if ret >= 1:
            return f'{ret:.1f} GB'
        ret *= 1024
        if ret >= 1:
            return f'{ret:.1f} MB'
        ret *= 1024
        return f'{ret:.1f} KB'

    @staticmethod
    def convert_time(mtime):
        if isinstance(mtime, (int, float)):
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime))
        elif isinstance(mtime, datetime.datetime):
            return mtime.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return mtime

    @property
    def is_preview(self):
        if not self.opt.auth and not self.get_cookie('preview'):
            return True
        else:
            return self.get_cookie('preview') == 'on' and self.args.f is None

    @property
    def show_upload(self):
        if not self.opt.upload:
            return False
        if re.match('^/disk/public', self.request.path) and self.current_user.id != 1:
            return False
        return True

    @property
    def show_delete(self):
        if not self.opt.delete:
            return False
        if re.match('^/disk/public', self.request.path) and self.current_user.id != 1:
            return False
        return True

    @property
    def show_share(self):
        if not self.opt.auth:
            return False

        if res := re.match(r'^/(disk)/(\w+)', self.request.path):
            if uid := self.decode(res.groups()[1]):
                return uid == self.current_user.id

        return False

    @run_on_executor
    def get_md5(self, path):
        return self.app.get_md5(path)


@bp.route('/')
class IndexHandler(BaseHandler):

    def get(self):
        if self.args.code:
            ret = {'maxsize': self.opt.maxsize}
            if self.opt.auth and self.current_user and self.current_user.id != 1:
                ret['quota'] = (self.opt.quota - self.current_user.get('usage', 0))
            return self.finish(ret)

        if self.opt.auth:
            if self.current_user:
                self.redirect(f'/disk/{self.current_user.code}')
            else:
                self.render('landing.html')
        else:
            self.redirect('/disk')


@bp.route('/share')
class ShareHandler(BaseHandler):

    def get(self):
        if self.opt.auth:
            if self.current_user:
                self.redirect(f'/share/{self.current_user.code}')
            else:
                self.render('landing.html')
        else:
            self.redirect('/disk')


@bp.route('/admin')
class AdminHandler(BaseHandler):

    @tornado.web.authenticated
    async def get(self):
        self.current_user.setdefault('usage', 0)
        self.current_user.setdefault('visit', {})
        month = datetime.datetime.now().strftime('%Y%m')
        self.current_user.visit = self.current_user.visit.get(month, 0)
        self.render('admin.html')

    @tornado.web.authenticated
    async def post(self):
        if self.args.kindle and self.args.kindle != self.current_user.kindle:
            code = await self.rd.get(f'{self.prefix}_code_{self.args.kindle}')
            if self.args.kindle and not (code and code == self.args.code):
                return self.finish({'err': 1, 'msg': '邮箱验证码不正确'})

        update = {
            'direct_file': self.args.direct_file == 'on',
            'direct_dir': self.args.direct_dir == 'on',
        }
        if self.args.kindle:
            update['kindle'] = self.args.kindle
        await self.db.users.update_one({'_id': self.current_user._id}, {'$set': update})
        self.finish({'err': 0})


@bp.route('/manage')
class ManageHandler(BaseHandler):

    @tornado.web.authenticated
    async def get(self):
        if not self.current_user.id == 1:
            raise tornado.web.HTTPError(403)

        query = self.get_args()
        if query.username:
            query.username = {'username': {'$regex': re.compile(query.username)}}
        entries = await self.query('users', query, schema={'id': int})
        self.render('manage.html', entries=entries)

    @tornado.web.authenticated
    async def post(self):
        if not self.current_user.id == 1:
            return self.finish({'err': 1, 'msg': '当前用户无权限'})

        _id = self.get_argument('id', None)
        if not _id:
            return self.finish({'err': 1, 'msg': '用户未指定'})
        user = await self.db.users.find_one({'_id': ObjectId(_id)})
        if not user:
            return self.finish({'err': 1, 'msg': '用户不存在'})

        if self.args.action == 'delete':
            await self.db.users.delete_one({'_id': user._id})
            shutil.rmtree(self.app.root / user.code, ignore_errors=True)
        elif self.args.action == 'deny':
            await self.db.users.update_one({'_id': user._id}, {'$set': {'deny': True}})

        self.finish({'err': 0})


@bp.route('/share/?(.*)')
@bp.route('/disk/?(.*)')
@tornado.web.stream_request_body
class DiskHandler(tornado.web.StaticFileHandler, BaseHandler):

    def __init__(self, application, request, **kwargs):
        tornado.web.StaticFileHandler.__init__(self, application, request, path=self.app.root)
        BaseHandler.__init__(self, application, request, path=self.app.root)

    def compute_etag(self):
        if hasattr(self, 'absolute_path'):
            return super().compute_etag()

    def set_default_headers(self):
        if not self.opt.auth:
            self.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.set_header('Pragma', 'no-cache')
            self.set_header('Expires', '0')

    def set_extra_headers(self, path):
        if path.endswith('.webp'):
            self.set_header('content-type', 'image/webp')
        elif path.endswith('.ts'):
            self.set_header('content-type', 'application/octet-stream')

    async def prepare(self):
        if not self.opt.auth and not self.get_cookie('preview'):
            self.set_cookie('preview', 'on', expires=365)

        self.route = self.request.path.split('/')[1]
        if self.request.method == 'PUT':
            self.received = 0
            self.process = 0
            self.length = int(self.request.headers['Content-Length'])
            path = (self.root / self.path_args[0]).expanduser().resolve()
            if not path.is_relative_to(self.root):
                return self.finish('target is forbidden\n')
            if path.is_dir():
                return self.finish('target is directory\n')
            path.parent.mkdir(parents=True, exist_ok=True)
            self.fp = open(path, 'wb')
            self.md5 = hashlib.md5()
        else:
            DiskHandler._stream_request_body = False
        await super().prepare()

    def data_received(self, chunk):
        self.received += len(chunk)
        process = int(self.received / self.length * 100)
        if process > self.process + 5:
            self.process = process
            self.write(f'uploading process {process}%\n')
            self.flush()
        self.fp.write(chunk)
        self.md5.update(chunk)

    async def put(self, name):
        self.fp.close()
        self.finish(f'upload succeed, md5: {self.md5.hexdigest()}\n')

    @cached_property
    def current_uid(self):
        name = self.path_args[0].split('/')[0]
        return self.decode(name) if name else None

    async def check(self, name):
        if not self.opt.auth or self.current_user.id == 1:
            return True

        if name.startswith('public') and self.request.method in ['GET', 'HEAD']:
            return True

        if not name:
            return False

        uid = self.decode(name.split('/')[0])
        if not uid:
            return False
        if uid == self.current_user.id:
            return True

        if self.request.method in ['GET', 'HEAD']:
            if self.route == 'disk':
                user = await self.db.users.find_one({'id': uid}, {'direct_file': 1, 'direct_dir': 1})
                if user and (user.direct_file or user.direct_dir) and (self.root / name).is_file():
                    return True
                if user and user.direct_dir and (self.root / name).is_dir():
                    return True
            elif self.route == 'share':
                paths = [str(x) for x in list(Path(name).parents)[:-2]]
                paths.insert(0, str(name))
                if await self.db.share.count_documents({'path': {'$in': paths}}):
                    return True

        return False

    @run_on_executor
    def search(self, path):
        entries = []
        q = self.args.q.lower()
        cache = self.app.monitor.files.copy()
        for key, files in cache.items():
            if str(key).startswith(str(path)):
                for doc in files:
                    if doc.path.name.lower().find(q) >= 0:
                        entries.append(doc)
        doc = self.get_args(page=1, size=50)
        self.args.total = len(entries)
        self.args.pages = int(math.ceil(len(entries) / doc.size))
        entries = entries[(doc.page - 1) * doc.size:doc.page * doc.size]
        return entries

    @run_on_executor
    def listdir(self, path):
        entries = self.app.monitor.scan_dir(path)
        doc = self.get_args(page=1, size=50, order=1)
        if self.args.sort == 'mtime':
            entries.sort(key=lambda x: x.mtime, reverse=(self.args.order == - 1))
        elif self.args.sort == 'size':
            entries.sort(key=lambda x: x.size, reverse=(self.args.order == - 1))
        else:
            entries.sort(key=lambda x: x.path, reverse=(self.args.order == - 1))
        self.args.total = len(entries)
        self.args.pages = int(math.ceil(len(entries) / doc.size))
        entries = entries[(doc.page - 1) * doc.size:doc.page * doc.size]
        return entries

    @run_on_executor
    def download(self, path):
        # new_loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(new_loop)
        with io.BytesIO() as stream:
            with zipfile.ZipFile(stream, 'a', zipfile.ZIP_DEFLATED, True) as zf:
                for f in path.rglob('*'):
                    if f.is_file():
                        zf.writestr(f'{path.name}/{f.relative_to(path)}', f.read_bytes())
                #  Mark the files as having been created on Windows so that Unix permissions are not inferred as 0000
                for file in zf.filelist:
                    file.create_system = 0
            data = stream.getvalue()

        return data

    async def send_file(self, path, include_body=False):
        name = path.relative_to(self.root).as_posix()
        if include_body and self.opt.auth and not self.request.path.startswith('/disk/public'):
            uid = self.current_uid
            size = len(path) if isinstance(path, bytes) else path.stat().st_size
            size = round(size / 1024 / 1024, 5)
            month = datetime.datetime.now().strftime('%Y%m')
            await self.db.users.update_one({'id': uid}, {'$inc': {f'visit.{month}': size}})
            await self.db.visit.update_one(
                {'path': name},
                {'$set': {'path': name, 'uid': uid, 'size': size, 'uid': uid}, '$inc': {'count': 1}},
                upsert=True)

        if isinstance(path, bytes):
            return self.finish(path)

        if include_body and self.opt.auth and self.opt.alist:
            if await self.db.disk.find_one({'path': name}):
                url = f'{self.opt.alist_address}/api/fs/get'
                headers = {
                    'authorization': self.opt.alist_token,
                }
                data = {
                    'path': f'/lanzou/{name}',
                    'password': '',
                }
                resp = await self.http.post(url, headers=headers, json=data)
                if resp.code == 200:
                    ret = resp.json()
                    self.logger.info(f'get alist response: {ret}')
                    if ret.code == 200:
                        self.set_header("referrer-policy", "no-referrer")
                        return self.redirect(ret.data.raw_url)

        await super().get(name, include_body)

    def get_nodes(self, path):
        nodes = []
        key = self.app.root / path
        if key in self.app.monitor.files:
            entries = self.app.monitor.files[key]
            for doc in entries:
                if doc.is_dir:
                    nodes.append({'title': doc.path.name, 'href': f'/disk/{doc.path}',
                                 'children': self.get_nodes(doc.path)})
                else:
                    nodes.append({'title': doc.path.name, 'href': f'/disk/{doc.path}'})
        return nodes

    def preview_html(self, html, padding=0, background='#23241f'):
        lines = [
            '<html><head>',
            '<link rel="stylesheet" href="/static/src/css/monokai_sublime.css">',
            '<style>img{margin:10px auto;max-width:100%}</style>',
            f'</head><body style="padding:{padding}px;margin:0;background:{background};">',
            html,
            '<script src="/static/src/js/highlight.pack.min.js"></script>',
            '<script>hljs.initHighlightingOnLoad()</script>',
            '</body></html>'
        ]
        self.finish(''.join(lines))

    def preview_office(self):
        url = f'http://{self.request.host}{self.request.path}'
        if self.opt.auth:
            url += f'?token={self.current_user.token}'
        src = urllib.parse.quote(url, safe=string.printable)
        url = f'https://view.officeapps.live.com/op/view.aspx?src={src}'
        self.redirect(url)

    def preview_video(self, url):
        html = [
            '<html><head>',
            '<link rel="stylesheet" href="/static/src/css/DPlayer.min.css">',
            '</head><body style="width:100%;height:100%;margin:auto;background:#000;overflow:hidden;">',
            '<div id="video"></div>',
            '<script src="/static/src/js/flv.min.js"></script>',
            '<script src="/static/src/js/hls.min.js"></script>',
            '<script src="/static/src/js/DPlayer.min.js"></script>',
            '<script>new DPlayer({container: document.getElementById("video"), autoplay: true, loop: true, video: { type: "auto", url: "' + url + '" } })</script>',
            '</body></html>'
        ]
        self.finish(''.join(html))

    def preview_audio(self, path):
        files = [x for x in path.parent.iterdir() if x.is_file() and x.name != path.name
                 and re.match('(mp3|wav|flac|aac|ogg|amr|wma)$', x.suffix[1:])]
        files.sort(key=lambda x: x.name)
        urls = [self.request.path] + \
            [f'{Path(self.request.path).parent}/{urllib.parse.quote(x.name)}' for x in files]
        audios = [{
            'theme': '#fff',
            'cover': '/static/img/audio.png',
            'name': urllib.parse.unquote(Path(x).name),
            'url': x
        } for x in urls]
        text = json.dumps(audios, ensure_ascii=False)
        html = [
            '<html><head>',
            '<link rel="stylesheet" href="/static/src/css/APlayer.min.css">',
            '</head><body style="display:flex;justify-content:center;align-items:center;background:#23241f">',
            '<div id="audio" style="padding:10px;width:100%"></div>',
            '<script src="/static/src/js/APlayer.min.js"></script>',
            '<script>new APlayer({container: document.getElementById("audio"), autoplay: true, audio: ' + text + '})</script>',
            '</body></html>'
        ]
        self.finish(''.join(html))

    def preview_image(self, path):
        files = [x for x in path.parent.iterdir() if x.is_file()
                 and re.match('(jpeg|jpg|png|gif|bmp|webp|svg|tif|webp|ai|ico)$', x.suffix[1:])]
        files.sort(key=lambda x: x.name)
        urls = [f'{Path(self.request.path).parent}/{urllib.parse.quote(x.name)}' for x in files]
        index = files.index(path)
        self.render('image.html', url=urls[index], index=index, urls=json.dumps(urls))

    def preview_zip(self, path):
        zf = zipfile.ZipFile(path)
        entries = []
        for item in sorted(zf.infolist(), key=lambda x: x.filename):
            if item.is_dir():
                continue
            try:
                item.filename = item.filename.encode('cp437').decode('gbk')
            except:
                pass
            entries.append(Dict({
                'path': Path(item.filename),
                'mtime': datetime.datetime(*item.date_time).strftime("%Y-%m-%d %H:%M:%S"),
                'size': item.file_size,
                'is_dir': item.is_dir(),
            }))
        self.render('files.html', entries=entries)

    def preview_tar(self, path):
        tf = tarfile.open(path)
        entries = []
        for item in sorted(tf.getmembers(), key=lambda x: x.name):
            if item.isdir():
                continue
            entries.append(Dict({
                'path': Path(item.name),
                'mtime': item.mtime,
                'size': item.size,
                'is_dir': item.isdir(),
            }))
        self.render('files.html', entries=entries)

    @check_auth
    async def get(self, name, include_body=True):
        if not self.get_cookie('preview'):
            self.set_cookie('preview', 'off' if self.opt.auth else 'on')

        path = self.root / name
        if self.args.q:
            entries = await self.search(path)
            self.render('index.html', entries=entries)
        elif self.args.f == 'tree':
            nodes = self.get_nodes(path)
            self.finish({'nodes': nodes})
        elif self.args.f == 'download':
            self.set_header('Content-Type', 'application/octet-stream')
            filename = urllib.parse.quote(path.name)
            if path.is_file():
                self.set_header('Content-Disposition', f'attachment;filename={filename}')
                await self.send_file(path, include_body=True)
            elif path.is_dir():
                self.set_header('Content-Disposition', f'attachment;filename={filename}.zip')
                data = await self.download(path)
                await self.send_file(data, include_body=True)
            else:
                raise tornado.web.HTTPError(404)
        elif path.is_file() and self.args.f == 'preview':
            suffix = path.suffix.lower()[1:]
            if suffix == 'zip':
                self.preview_zip(path)
            elif re.match('(tar|gz|bz2|tgz|z)$', suffix) and tarfile.is_tarfile(path):
                self.preview_tar(path)
            elif re.match('(docx|doc|xlsx|xls|pptx|ppt)$', suffix):
                self.preview_office()
            elif re.match('(jpeg|jpg|png|gif|bmp|webp|svg|tif|webp|ai|ico)$', suffix):
                self.preview_image(path)
            elif re.match('(mp4|mkv|flv|m3u8)$', suffix):
                self.preview_video(self.request.path)
            elif re.match('(mp3|wav|flac|aac|ogg|amr|wma)$', suffix):
                self.preview_audio(path)
            elif re.match('(md|markdown)$', suffix):
                exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite',
                        'markdown.extensions.tables', 'markdown.extensions.toc']
                html = markdown.markdown(path.read_text(), extensions=exts)
                self.preview_html(html, padding=20, background='#fff')
            elif suffix == 'ipynb':
                with tempfile.NamedTemporaryFile('w+', suffix='.html', delete=True) as fp:
                    command = f'jupyter nbconvert --to html --template full --output {fp.name} {path}'
                    cmd = await asyncio.create_subprocess_shell(command)
                    await cmd.wait()
                    self.finish(fp.read().replace('<link rel="stylesheet" href="custom.css">', ''))
            elif re.match('(py|sh|cu|h|hpp|c|cpp|vue|php|js|css|html|less|scss|pig|java|go|ini|conf|txt|cfg|log|json|yml|yaml|xml|toml)$', suffix):
                try:
                    text = path.read_text()
                except:
                    text = path.read_text(encoding='unicode_escape')
                if suffix == 'json':
                    text = json.dumps(json.loads(text), indent=4, ensure_ascii=False)
                self.preview_html(f'<pre><code>{tornado.escape.xhtml_escape(text)}</code></pre>')
            elif re.match('(pdf)$', suffix):
                await super().get(name, include_body)
            else:
                icon = 'folder.png' if path.is_dir() else self.icon.get(path.suffix.lower(), 'file.png')
                size = self.convert_size(path.stat().st_size)
                mtime = datetime.datetime.fromtimestamp(path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                self.render('unknown.html', icon=icon, size=size, mtime=mtime, path=path, name=name)
        elif path.is_file():
            await self.send_file(path, include_body)
        elif self.request.path == f'/share/{self.current_user.code}':
            docs = await self.query('share', {'uid': self.current_uid})
            entries = []
            for doc in docs:
                entries.append(Dict({
                    'path': Path(doc.path),
                    'mtime': doc.mtime,
                    'size': doc.size,
                    'is_dir': doc.is_dir,
                    'expired_at': doc.expired_at,
                }))
            self.render('index.html', entries=entries)
        else:
            entries = await self.listdir(path)
            self.render('index.html', entries=entries)

    @check_auth
    async def post(self, name):
        path = self.root / name

        if self.args.action == 'folder':
            folder = (path / self.args.name).expanduser().resolve()
            if not folder.is_relative_to(self.root):
                self.finish({'err': 1, 'msg': '文件名包含非法字符'})
            else:
                folder.mkdir(parents=True, exist_ok=True)
                self.finish({'err': 0})
        elif self.args.action == 'kindle':
            if not path.exists():
                self.finish({'err': 1, 'msg': f'{name} 文件不存在'})
            elif path.is_dir():
                self.finish({'err': 1, 'msg': '不可推送文件夹'})
            elif not self.current_user.kindle:
                self.finish({'err': 1, 'msg': '未设置Kindle推送邮箱'})
            elif path.stat().st_size > 52428800:
                self.finish({'err': 1, 'msg': '文件大小不可大于50MB'})
            elif not re.match('.(pdf|txt|mobi|azw|doc|docx|html|htm|rtf|jpeg|jpg|png|gif|bmp|webp)$', path.suffix.lower()):
                self.finish({'err': 1, 'msg': '文件类型不支持推送至Kindle'})
            else:
                await self.app.email.send(self.current_user.kindle, 'convert', files=str(path))
                self.finish({'err': 0, 'msg': '推送成功'})
        elif self.args.action == 'rename':
            name = self.args.name.strip('./')
            new_path = (path.parent / name).expanduser().resolve()
            if not new_path.is_relative_to(self.root):
                return self.finish({'err': 1, 'msg': '文件名包含非法字符'})
            if new_path.exists():
                return self.finish({'err': 1, 'msg': '目标文件名已存在'})
            new_path.parent.mkdir(parents=True, exist_ok=True)
            path.rename(new_path)
            self.finish({'err': 0, 'msg': '重命名成功'})
        elif self.args.action == 'share':
            if not self.opt.auth:
                return self.finish({'err': 0})
            if not path.exists():
                return self.finish({'err': 1, 'msg': f'{name} 文件不存在'})

            doc = {
                'uid': self.current_user.id,
                'path': name,
                'mtime': int(path.stat().st_mtime),
                'size': path.stat().st_size,
                'is_dir': path.is_dir(),
                'created_at': datetime.datetime.now().replace(microsecond=0)
            }
            if self.args.days and self.args.days != '0':
                doc['expired_at'] = doc['created_at'] + datetime.timedelta(days=int(self.args.days))
            doc = await self.db.share.find_one_and_update(
                {'uid': self.current_user.id, 'path': name},
                {'$set': doc},
                upsert=True,
                return_document=True
            )
            self.finish({'err': 0, 'msg': f'{path.name}分享成功'})
        elif self.args.action == 'unshare':
            if not self.opt.auth:
                return self.finish({'err': 0})

            await self.db.share.delete_one({'uid': self.current_user.id, 'path': name})
            self.finish({'err': 0, 'msg': f'{path.name}已取消分享'})
        elif self.args.action == 'download':
            filename = urllib.parse.urlparse(self.args.src).path.split('/')[-1]
            filename = path / filename
            ret = await self.http.download(self.args.src, filename, threads=10)
            if ret:
                return self.finish({'err': 0, 'msg': '下载成功'})
            else:
                return self.finish({'err': 1, 'msg': '下载失败'})

            # command = f"axel -n5 '{self.args.src}' -o '{filename}'"
            # p = await asyncio.create_subprocess_shell(command)
            # await p.wait()
            # self.logger.info(f'download result: {p.returncode}, {self.args.url}')
            # ret = {'err': p.returncode, 'msg': '下载成功' if p.returncode == 0 else '下载失败'}
            # self.finish(ret)
        elif self.args.action == 'delete':
            await self.delete(name)
        else:
            await self.upload(path)

    async def merge(self, path):
        dirname = Path(f'/tmp/{self.args.guid}-{self.args.id}')
        dirname.mkdir(parents=True, exist_ok=True)
        filename = path / urllib.parse.unquote(self.args.name)
        filename.parent.mkdir(parents=True, exist_ok=True)
        chunks = int(list(dirname.glob("*"))[0].name.split('_')[0])
        md5 = hashlib.md5()
        with filename.open('wb') as fp:
            for i in range(int(chunks)):
                chunk = dirname / f'{chunks}_{i}'
                if not chunk.exists():
                    return self.finish({'err': 1, 'msg': f'缺少分片: {i}'})
                data = chunk.read_bytes()
                md5.update(data)
                fp.write(data)
        md5 = md5.hexdigest()
        shutil.rmtree(dirname)
        if self.args.md5 and self.args.md5 != 'undefined' and self.args.md5 != md5:
            filename.unlink(missing_ok=True)
            self.finish({'err': 1, 'msg': 'md5校验失败'})
        else:
            if self.opt.auth:
                size = round(filename.stat().st_size / 1024 / 1024, 5)
                await self.db.users.update_one({'id': self.current_user.id}, {'$inc': {'usage': size}})
            self.finish({'err': 0, 'path': filename.relative_to(self.app.root)})

    async def upload(self, path):
        if not self.opt.upload:
            raise tornado.web.HTTPError(403)

        if self.opt.auth and self.current_user.id != 1 and self.current_user.get('usage', 0) >= self.opt.quota:
            return self.finish({'err': 1, 'msg': '容量不足'})

        if self.args.action == 'merge':
            await self.merge(path)
        elif self.args.chunks and self.args.chunk:
            filename = Path(f'/tmp/{self.args.guid}-{self.args.id}/{self.args.chunks}_{self.args.chunk}')
            filename.parent.mkdir(parents=True, exist_ok=True)
            filename.write_bytes(self.request.files['file'][0].body)
            self.finish({'err': 0})
        elif self.request.files:
            path.mkdir(parents=True, exist_ok=True)
            urls = []
            size = 0
            for items in self.request.files.values():
                for item in items:
                    filename = path / urllib.parse.unquote(item.filename)
                    filename.parent.mkdir(parents=True, exist_ok=True)
                    filename.write_bytes(item.body)
                    size += round(len(item.body) / 1024 / 1024, 5)
                    urls.append(filename.relative_to(self.app.root))

            if self.opt.auth:
                await self.db.users.update_one({'id': self.current_user.id}, {'$inc': {'usage': size}})

            ret = {'err': 0, 'path': urls[0]}
            if len(urls) > 1:
                ret['paths'] = urls
            self.finish(ret)
        else:
            self.finish({'err': 1, 'msg': '未选择文件'})

    @check_auth
    async def delete(self, name):
        if not self.opt.delete:
            return self.finish({'err': 1, 'msg': '无权限删除文件'})

        path = self.root / name
        if self.opt.auth and self.route == 'share':
            await self.db.share.delete_one({'uid': self.current_user.id, 'path': name})
            return self.finish({'err': 0, 'msg': f'{path.name} 已取消分享'})

        if not path.exists():
            return self.finish({'err': 1, 'msg': f'{path.name} 文件不存在'})

        if self.opt.auth:
            if path.is_file():
                size = round(path.stat().st_size / 1024 / 1024, 5)
            else:
                size = sum([round(x.stat().st_size / 1024 / 1024, 5) for x in path.glob('*') if x.is_file()])
            await self.db.users.update_one({'id': self.current_user.id}, {'$inc': {'usage': -size}})
            await self.db.share.delete_one({'uid': self.current_user.id, 'path': name})

        if self.opt.auth and self.opt.alist:
            if await self.db.disk.find_one({'path': name}):
                url = f'{self.opt.alist_address}/api/fs/remove'
                headers = {
                    'authorization': self.opt.alist_token,
                }
                data = {
                    'dir': f'/lanzou/{path.relative_to(self.root).parent}',
                    'names': [path.name],
                }
                resp = await self.http.post(url, headers=headers, json=data)
                if resp.code == 200:
                    ret = resp.json()
                    self.logger.info(f'remove alist response: {ret}')
                    if ret.code == 200:
                        await self.db.disk.delete_one({'path': path.relative_to(self.root).as_posix()})

        if path.is_file():
            path.unlink(missing_ok=True)
        else:
            shutil.rmtree(path, ignore_errors=True)
        self.finish({'err': 0, 'msg': f'{path.name}删除成功'})


@bp.route(r"/chart/?(.*)")
class ChartHandler(BaseHandler):

    async def get(self, name):
        if not name:
            docs = await self.query('charts')
            self.render('chart.html', docs=docs)
        else:
            chart = await self.db.charts.find_one({'name': name})
            if not chart:
                raise tornado.web.HTTPError(404)

            if self.args.f == 'json':
                self.finish({'containers': json.loads(chart.containers)})
            else:
                self.render('chart.html')

    async def delete(self, name):
        await self.db.charts.delete_one({'name': name})
        self.finish({'err': 0})

    async def post(self, name):
        charts = json.loads(self.request.body)
        if isinstance(charts, dict):
            charts = [charts]
        containers = []
        for chart in charts:
            chart = Dict(chart)
            if chart.chart:
                chart.credits = {'enabled': False}
                containers.append(chart)
            else:
                chart.setdefault('xAxis', [])
                data = {
                    'chart': {
                        'type': chart.type,
                        'zoomType': 'x',
                    },
                    'credits': {
                        'enabled': False
                    },
                    'title': {
                        'text': chart.title,
                        'x': -20
                    },
                    'xAxis': {
                        'tickInterval': int(math.ceil(len(chart.xAxis) / 20.0)),
                        'labels': {
                            'rotation': 45 if len(chart.xAxis) > 20 else 0,
                            'style': {
                                'fontSize': 12,
                                'fontWeight': 'normal'
                            }
                        },
                        'categories': chart.xAxis
                    },
                    'yAxis': {
                        'title': {
                            'text': ''
                        },
                        'plotLines': [{
                            'value': 0,
                            'width': 1,
                            'color': '#808080'
                        }]
                    },
                    'tooltip': {
                        # 'headerFormat': '<span style="font-size:10px">{point.key}</span><table>',
                        # 'pointFormat': '<tr><td style="padding:0">{series.name}: </td><td style="padding:0"><b>{point.y:.2f}</b></td></tr>',
                        # 'footerFormat': '</table>',
                        'shared': True,
                        'useHTML': True
                    },
                    'legend': {
                        'layout': 'horizontal',
                        'align': 'center',
                        'verticalAlign': 'bottom',
                        'borderWidth': 0,
                        'y': 0,
                        'x': 0
                    },
                    'plotOptions': {
                        'series': {
                            'marker': {
                                'radius': 1,
                                'symbol': 'diamond'
                            }
                        },
                        'pie': {
                            'allowPointSelect': True,
                            'cursor': 'pointer',
                            'dataLabels': {
                                'enabled': True,
                                'color': '#000000',
                                'connectorColor': '#000000',
                                'format': '<b>{point.name}</b>: {point.percentage:.3f} %'
                            }
                        }
                    },
                    'series': chart.series
                }
                containers.append(data)

        if containers:
            doc = {
                'name': name,
                'containers': json.dumps(containers, ensure_ascii=False),
                'charts': json.dumps(charts, ensure_ascii=False),
                'date': datetime.datetime.now().replace(microsecond=0)
            }
            await self.db.charts.update_one({'name': name}, {'$set': doc}, upsert=True)
            self.finish({'err': 0})
        else:
            self.finish({'err': 1, 'msg': '未获取到必需参数'})


@bp.route(r"/table/?(.*)")
class TableHandler(BaseHandler):

    async def get(self, name):
        if not name:
            docs = await self.query('tables')
            self.render('table.html', docs=docs)
        else:
            meta = await self.db.tables.find_one({'name': name})
            if not meta:
                raise tornado.web.HTTPError(404)

            schema = dict(map(lambda x: x.split(':'), meta['fields']))
            entries = await self.query(f'table_{name}', self.args, schema=schema)

            self.args.fields = list(
                map(lambda item: item.split(':')[0], meta['fields']))
            self.args.searchs = meta.get('search', [])
            self.args.marks = meta.get('mark', [])
            self.args.options = {
                'sort': self.args.fields,
                'order': ['1:asc', '-1:desc'],
            }
            self.render('table.html', entries=entries)

    async def delete(self, name):
        table = f'table_{name}'
        await self.db[table].drop()
        await self.db.tables.delete_one({'name': name})
        self.finish({'err': 0})

    async def post(self, name):
        table = f'table_{name}'
        doc = json.loads(self.request.body)
        await self.db[table].drop()
        for key in doc.get('search', []):
            await self.db[table].create_index(key)

        fields = dict(map(lambda x: x.split(':'), doc['fields']))
        if doc.get('docs'):
            dts = dict(filter(lambda x: x[1] == 'datetime', fields.items()))
            for k in dts:
                for item in doc['docs']:
                    item[k] = datetime.datetime.strptime(
                        item[k], '%Y-%m-%d %H:%M:%S')
            await self.db[table].insert_many(doc['docs'])

        meta = {'name': name, 'date': datetime.datetime.now().replace(microsecond=0)}
        meta.update(
            dict(filter(lambda x: x[0] in ['fields', 'search', 'mark'], doc.items())))
        await self.db.tables.update_one({'name': name}, {'$set': meta}, upsert=True)
        self.finish({'err': 0})

    async def put(self, name):
        table = f'table_{name}'
        doc = json.loads(self.request.body)
        meta = await self.db.tables.find_one({'name': name})
        type_dict = dict(map(lambda x: x.split(':'), meta['fields']))
        if type_dict[doc['key']] == 'int':
            doc['value'] = int(doc['value'])
        elif type_dict[doc['key']] == 'float':
            doc['value'] = float(doc['value'])
        elif type_dict[doc['key']] == 'datetime':
            doc['value'] = datetime.datetime.strptime(
                doc['value'], '%Y-%m-%d %H:%M:%S')

        if doc['action'] == 'add':
            op = '$set' if doc.get('unique') else '$addToSet'
        else:
            op = '$unset' if doc.get('unique') else '$pull'
        await self.db[table].update_one({'_id': ObjectId(doc['_id'])}, {op: {doc['key']: doc['value']}})
        self.finish({'err': 0})
