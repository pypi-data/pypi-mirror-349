import base64
import os
import random
import time
import traceback
from typing import List

import subprocess

import os
import subprocess
import zipfile
import tempfile
import io

allow_pandoc = True

_is_pandoc_installed = None

def test_is_pandoc_installed():
    try:
        subprocess.check_output(['pandoc', '--version'])
        return True
    except subprocess.CalledProcessError:
        return False

def can_run_pandoc(force_retest=False):
    if not allow_pandoc:
        return False
    
    global _is_pandoc_installed
    if _is_pandoc_installed is None or force_retest:
         _is_pandoc_installed = test_is_pandoc_installed()
    return _is_pandoc_installed


def pandoc_convert(input_string, input_format, output_format, is_binary=False, *args):
    if input_format == output_format:
        return input_string # pandoc would just return the same anyways
    
    inp = ['pandoc'] + list(args) + ['--wrap=none', '--from', input_format, '--to', output_format]

    process = subprocess.Popen(inp, 
                               stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    
    output, error = process.communicate(input_string.encode('utf-8'))
    if error:
        raise RuntimeError(error.decode('utf-8'))
    
    if not is_binary:
        o = output.decode('utf-8')
        if o.endswith('\r\n') and not input_string.endswith('\r\n'):
            o = o.rstrip()
        elif o.endswith('\n') and not input_string.endswith('\n'):
            o = o.rstrip()

        if o.startswith('\r\n') and not input_string.startswith('\r\n'):
            o = o.lstrip()
        elif o.startswith('\n') and not input_string.startswith('\n'):
            o = o.lstrip()
        return o
    else:
        return output

def pandoc_set_allowed(is_allowed):
    """Set whether or not pandoc is allowed to be used as a valid conversion option"""

    global allow_pandoc
    allow_pandoc = True if is_allowed else False
    return allow_pandoc

    
def pandoc_convert_file(inp_file, out_file_or_format):
    """
    Convert a file using pandoc.

    Parameters:
    inp_file (str): The path to the input file.
    out_file_or_format (str or Path): The path to the output file or the desired output format.
        If it's a string starting with a dot, it's considered as a file extension and the output file
        will be the input file with the new extension.

    Returns:
    subprocess.CompletedProcess: The result of the pandoc conversion command.

    Raises:
    AssertionError: If the input file does not exist or if no output file or format is provided.
    """
    
    assert inp_file, "Need to give an inout file name!"
    assert os.path.exists(inp_file), f"input file {inp_file=} does not exist!"

    out_file = out_file_or_format

    if isinstance(out_file, str) and out_file.startswith("."):
        out_file = os.path.splitext(inp_file)[0] + out_file
        
    assert out_file, "Need to give an output file name!"
    return subprocess.run(['pandoc', inp_file, '-o', out_file])



def convert(output_format, doc:List[dict], with_attachments=True, files_to_upload=None):

    files_to_upload = {} if not files_to_upload else files_to_upload

    assert not files_to_upload, 'pandoc formatter does not allow to upload additional files!'
    formatter = PandocFormatter(output_format)
    s = formatter.format(doc)
    
    text = '\n'.join(s) if isinstance(s, list) else s
    if with_attachments:
        return text, {}
    else:
        return text
    


# def to_docx(doc:List[dict], with_attachments=True, files_to_upload=None):
#     raise NotImplementedError('Generating docx is not implemented yet!')
#     txt, _ = convert('html', doc, with_attachments=True, files_to_upload=files_to_upload)
#     return pandoc_convert(txt, 'html', 'docx', True, '-o', '-')

# def to_html(doc:List[dict], with_attachments=True, files_to_upload=None):
#     txt, _ = convert('html', doc, with_attachments=True, files_to_upload=files_to_upload)
#     return txt

# def to_ipynb(doc:List[dict], with_attachments=True, files_to_upload=None):
#     raise NotImplementedError('Generating PDF reports is not possible in pandoc backend... please choose a different backend!')

# def to_md(doc:List[dict], with_attachments=True, files_to_upload=None):
#     txt, _ = convert('markdown', doc, with_attachments=True, files_to_upload=files_to_upload)
#     return txt

# def to_html(doc:List[dict], with_attachments=True, files_to_upload=None):
#     txt, _ = convert('html', doc, with_attachments=True, files_to_upload=files_to_upload)
#     return txt

# def to_tex(doc:List[dict], with_attachments=True, files_to_upload=None):
#     txt, _ = convert('latex', doc, with_attachments=True, files_to_upload=files_to_upload)
#     return txt

# def to_pdf(doc:List[dict], with_attachments=True, files_to_upload=None):
#     txt, _ = convert('latex', doc, with_attachments=True, files_to_upload=files_to_upload)
#     return pandoc_convert(txt, 'latex', 'pdf', True, '-o', '-')




###########################################################################################
"""

███████  ██████  ██████  ███    ███  █████  ████████ 
██      ██    ██ ██   ██ ████  ████ ██   ██    ██    
█████   ██    ██ ██████  ██ ████ ██ ███████    ██    
██      ██    ██ ██   ██ ██  ██  ██ ██   ██    ██    
██       ██████  ██   ██ ██      ██ ██   ██    ██    
                                                     
"""
###########################################################################################

# NOTE: This is not really used anywhere, but I keep it in since it "does not hurt"
class PandocFormatter:

    def __init__(self, output_format, *pandoc_args) -> None:
        self.output_format = output_format
        self.pandoc_args = pandoc_args

    def conv(self, string, input_format, *args):
        pandoc_args = self.pandoc_args + args
        return pandoc_convert(string, input_format, self.output_format, False, *pandoc_args)
    

    def handle_error(self, err, el):
        txt = 'ERROR WHILE HANDLING ELEMENT:\n{}\n\n'.format(el)
        if not isinstance(err, str):
            txt += '\n'.join(traceback.format_exception(err, limit=5)) + '\n'
        else:
            txt += err + '\n'
        txt = r"""
\begin{verbatim}

<REPLACEME:VERBTEXT>

\end{verbatim}""".replace('<REPLACEME:VERBTEXT>', txt)
        txt = f'{{\\color{{red}}{txt}}}'

        return self.conv(txt, 'latex')
    

    def digest_markdown(self, children='', **kwargs) -> str:
        return self.conv(children, 'markdown')

    def digest_image(self, children='', width=0.8, caption="", imageblob=None, **kwargs):               
        
        if imageblob is None:
            imageblob = ''

        caption = kwargs.get('caption')
        
        if not children:
            uid = (id(imageblob) + int(time.time()) + random.randint(1, 100))
            children = f'image_{uid}.png'

        s = imageblob.decode("utf-8") if isinstance(imageblob, bytes) else imageblob
        if not s.startswith('data:image'):
            s = 'data:image/png;base64,' + s
        
        if children:
            children = [
                # f'<div style="margin-top: 1.5em; width: 100%; text-align: center;"><span style="min-width:100;display: inline-block;"><b>image-name: </b>{children}</span></div>',
            ]
        else:
            children = []
        
        children += [    
            f"<div style=\"width: 100%; text-align: center;\"><img src=\"{s}\" style=\"max-width:{int(width*100)}%;display: inline-block;\"></img></div>",
        ]

        if caption:
            children.append(f'<div style="width: 100%; text-align: center;"><span style="min-width:100;display: inline-block;"><b>caption: </b>{caption}</span></div>')
        txt =  '\n\n'.join(children)
        
        return self.conv(txt, 'html', '--embed-resources')


    def digest_verbatim(self, children='', **kwargs) -> str:
        label = kwargs.get('caption', kwargs.get('label', ''))
        content = kwargs.get('content', kwargs.get('children'))
        color = kwargs.get('color', '')
        if color:
            color = f'color:{color};'

        j = content

        children = [
            f'<div style="min-width:100;{color}">{label}</div>',
            # f'<textarea cols="{w}" rows="{n}" disabled=True>\n\n{j}\n\n</textarea>'
            f'<pre style="white-space: pre-wrap; margin: 15px; margin-left: 25px; padding: 10px; border: 1px solid gray; border-radius: 3px;">{j}</pre>'
        ]
        txt = '\n\n'.join(children)
        return self.conv(txt, 'latex')

    def digest_iterator(self, el) -> str:
        if isinstance(el, dict) and el.get('typ', '') == 'iter' and isinstance(el.get('children', None), list):
            el = el['children']
        return '\n\n'.join([self.digest(e) for i, e in enumerate(el)])
    
    def digest_str(self, el):
        return el
        
    def digest_text(self, children:str, **kwargs):
        color = kwargs.get('color', '')
        if color:
            c = f'color:{color};'
            txt = f'<div style="{c}">{children}</div>'
            print(txt)
            return self.conv(txt, 'html')
        else:
            return children
        
    def digest_line(self, children:str, **kwargs):
        color = kwargs.get('color', '')
        if color:
            color = f'color:{color};'
            txt = f'<div style="{color}">{children}</div>'
            return self.conv(txt, 'html') + '\n'
        else:
            return children + '\n'
    
    def digest_latex(self, children:str, **kwargs):
        return self.conv(children, 'latex')
    
    def digest(self, el):

        try:
            
            if not el:
                return ''
            elif isinstance(el, str):
                ret = self.digest_str(el)
            elif isinstance(el, dict) and el.get('typ') == 'iter':
                ret = self.digest_iterator(el)
            elif isinstance(el, list) and el:
                ret = self.digest_iterator(el)
            elif isinstance(el, dict) and el.get('typ', None) == 'image':
                ret = self.digest_image(**el)
            elif isinstance(el, dict) and el.get('typ', None) == 'text':
                ret = self.digest_text(**el)
            elif isinstance(el, dict) and el.get('typ', None) == 'latex':
                ret = self.digest_latex(**el)
            elif isinstance(el, dict) and el.get('typ', None) == 'line':
                ret = self.digest_line(**el)
            elif isinstance(el, dict) and el.get('typ', None) == 'verbatim':
                ret = self.digest_verbatim(**el)
            elif isinstance(el, dict) and el.get('typ', None) == 'markdown':
                ret = self.digest_markdown(**el)
            else:
                return self.handle_error(f'the element of typ {type(el)}, could not be parsed.', el)
            
            return ret
        
        except Exception as err:
            return self.handle_error(err, el)


    def format(self, doc:list) -> str:
        return '\n\n'.join([self.digest(e) for e in doc])





