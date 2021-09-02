#!/usr/bin/env python3
import markdown
import shutil
import os
import glob
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

SRCDIR = './src'
TMPLDIR = './template'
DISTDIR = './dist'


def build(text):
    define = True
    data = {}
    content = ''
    for line in text.split('\n'):
        if define:
            pl = [s.strip() for s in line.split('=', 1)]
            if len(pl) == 2:
                data[pl[0]] = pl[1]
        else:
            content += line + '\n'
        if line == '%%':
            define = False
    if define:
        content += text + '\n'
    data['content'] = markdown.markdown(content[:-1])
    if 'template' not in data.keys():
        return data['content']
    env = Environment(loader=FileSystemLoader(TMPLDIR))
    try:
        tmpl = env.get_template('{}.html'.format(data['template']))
    except TemplateNotFound:
        return data['content']
    rendered = tmpl.render(data)
    return rendered


def main():
    if os.path.isdir(DISTDIR):
        shutil.rmtree(DISTDIR)
    elif os.path.exists(DISTDIR):
        os.remove(DISTDIR)
    shutil.copytree(SRCDIR, DISTDIR)
    mdl = glob.glob('{}/**/*.md'.format(DISTDIR), recursive=True)
    htl = []
    for mdpath in mdl:
        if os.path.isfile(mdpath):
            with open(mdpath, 'r') as f:
                md = f.read()
            html = build(md)
            htpath = mdpath[::-1].replace('dm', 'lmth', 1)[::-1]
            htl.append(htpath)
            with open(htpath, 'w') as f:
                f.write(html)
            os.remove(mdpath)
    return htl


if __name__ == '__main__':
    main()
