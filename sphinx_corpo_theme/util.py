import os

def deduce_docname(relpath : str, current_docname : str) -> str:
    dirname = os.path.dirname(current_docname)
    if (pos := relpath.find('#')) >= 0:
        relpath = relpath[:pos]
    if relpath == '':
        docname = current_docname
    else:
        docname = os.path.normpath(os.path.join(dirname, relpath))
    docname = docname[:-5] if docname.endswith('.html') else docname
    return docname

def format_date(value, format):
    value = datetime.fromisoformat(value)
    return value.strftime(format)