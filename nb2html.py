from glob import glob
# import itertools as it
from os.path import basename, splitext, join, abspath
import re
import subprocess
import toolz.curried as z
import argparse
import yaml

fst = z.operator.itemgetter(0)
snd = z.operator.itemgetter(1)

NOTEBOOK_DIR = '_notebooks'
# NOTEBOOK_HTML_DIR = 'ipy_html'
NOTEBOOK_HTML_DIR = '_includes'

base = z.comp(fst, splitext, basename)
htmlname = z.comp(z.curry(join, NOTEBOOK_HTML_DIR), '{}.html'.format, base)

pat = re.compile(r'''^---\n
(.+?)\n
---
''', re.VERBOSE + re.DOTALL)  # # ^---
# print(pat.findall(txt)[0])


def post_todict(posttxt, ret_yaml=False):
    m = pat.findall(posttxt)
    if not m:
        if ret_yaml:
            return (None, None)
        return
    [txt] = m
    dct = yaml.load(txt)
    if ret_yaml:
        return dct, txt
    return dct


def nbconvert(frm, to, template=None):
    template = template or join(NOTEBOOK_DIR, 'output_toggle_html.tpl')
    cmd = ['ipython', 'nbconvert', '--to', 'html', '--template', template,
           '--output', to, frm, ]
    try:
        res = subprocess.check_output(cmd, cwd=abspath('.'), stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        # import ipdb; ipdb.set_trace()
        # import traceback
        # traceback.print_exc()
        print(e.output.decode('utf-8'))
        raise e

    print(res)
    return res


def rewrite_post_spec(post_txt, key='ipynb'):
    dct, yamtxt = post_todict(post_txt, ret_yaml=True)
    if (dct is None) or key not in dct:
        return (None, None, None)

    src = dct[key]
    html_fn = htmlname(src)
    new_yaml = """---
{yaml}
---

{{% include {html} %}}
""".format(yaml=yamtxt, html=basename(html_fn))
    return new_yaml, html_fn, src


def convert_and_update(yamlfn, write=True):
    with open(yamlfn, 'rb') as f:
        yamltxt = f.read().decode()
#         print(yamltxt)
    new_yaml, html_out, isrc = rewrite_post_spec(yamltxt)
    if new_yaml is None:
        print('Pattern not found')
        return

    nbconvert(isrc, html_out)
#     print(new_yaml)
    if write:
        with open(yamlfn, 'w') as f:
            f.write(new_yaml)

    return 0


def main(files):
    list(map(z.comp(convert_and_update, z.do(print)), files))


if __name__ == '__main__':
    desc = 'Convert ipython notebooks to blog-friendly htmls.'
    parser = argparse.ArgumentParser(description=desc)
    add = parser.add_argument
    add('--files', '-f', type=str, nargs='+', help='Markdown file specs to convert.')
    add('--all', '-a', action='store_true', help='Convert all .md files in `_posts` directory')

    args = parser.parse_args()
    if args.all:
        files = glob('_posts/*.md')
    else:
        files = args.files
    print(files)
    main(files)
