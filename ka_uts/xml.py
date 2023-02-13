# coding=utf-8
"""
Koskya XML general Utilities Module
contains the Kosakya XML general Utilities Classes
"""

from lxml import etree
import xmltodict
# import collections


class AoB:
    """
    Array of Bytes
    """
    @staticmethod
    def write(aob, path_):
        with open(path_, 'wb') as fd:
            for bytes in aob:
                fd.write(bytes)

    @staticmethod
    def to_Bytes(aob):
        return b'\n'.join(aob)

    @staticmethod
    def to_String(aob):
        return '\n'.join(map(str, aob))

    @classmethod
    def to_Dic(cls, aob):
        bytes = cls.to_Bytes(aob)
        return Xml2Dic.mig(bytes)


class AoX:
    """
    Array of Xml Objects
    """
    @classmethod
    def write(
          cls, aox, path_, b_header=None, b_footer=None, docinfo=None):
        aob = cls.to_AoB(aox, b_header, b_footer, docinfo)
        with open(path_, 'wb') as fd:
            for bytes in aob:
                fd.write(bytes)

    @staticmethod
    def write_bytes(
          aox, path_, b_header=None, b_footer=None, docinfo=None):
        with open(path_, 'wb') as fd:
            if b_header is not None:
                fd.write(b_header)
            for item in aox:
                out_xml = etree.tostring(
                            item,
                            xml_declaration=False,
                            with_comments=True,
                            encoding=docinfo.encoding,
                            pretty_print=True)
                fd.write(out_xml)
            if b_footer is not None:
                fd.write(b_footer)

    @staticmethod
    def to_AoB(aox, docinfo=None):
        aob = []
        for item in aox:
            b_xmlstr = etree.tostring(
                         item,
                         xml_declaration=False,
                         with_comments=True,
                         encoding=docinfo.encoding,
                         pretty_print=True)
            aob.append(b_xmlstr)
        return aob

    @classmethod
    def to_ByteStr(cls, aox, b_header=None, b_footer=None, docinfo=None):
        aob = cls.to_AoB(aox, b_header, b_footer, docinfo)
        return b'\n'.join(aob)


class XML:
    """
    XML Class
    """
    @staticmethod
    def read_2dic(path, **kwargs):
        mode = kwargs.get('mode', 'rb')
        with open(path, mode) as fd:
            data = fd.read()
            dic = Xml2Dic.mig(data)
            return dic

    @staticmethod
    def read_2dic_with_xml2dicapc_mig(path, **kwargs):
        mode = kwargs.get('mode', 'rb')
        with open(path, mode) as fd:
            data = fd.read()
            dic = Xml2DicApc.mig(data, **kwargs)
            return dic

    @staticmethod
    def read_2dic_with_xmltodict(path, **kwargs):
        mode = kwargs.get('mode', 'rb')
        with open(path, mode) as fd:
            data = fd.read()
            dic = xmltodict.parse(data, **kwargs)
            return dic

    @staticmethod
    def sh_root_docinfo(path_):
        tree = etree.parse(path_)
        docinfo = tree.docinfo
        root = tree.getroot()
        return root, docinfo


class Xml2Dic2:

    """
    There is no one-true-mapping from an XML to a Python dict;
    one is a node tree, the other is a hash map,
    it's just an "apples and something-else comparison",
    so you'll have to make design decisions for yourself,
    considering what you want.

    The link by Sreehari has a solution that does a decent job of
    converting an lxml node to a Python dict, but:

    it requires lxml, which is fine, but I like standard modules
    when they do the job it doesn't capture attributes.
    I've taken that code and converted it work with Python's standard
    xml.ElementTree module/class, and it handles attributes in its own way.

    When I run this code against your sample, I get the following dict:

    {'fees': [{'@attribs': {'mail_retail': 'MAIL', 'member_group': '00400F'},
               'admin_fee': '0.76',
               'processing_fee': '1.83'},
              {'@attribs': {'mail_retail': 'RETAIL', 'member_group': '00400F'},
               'admin_fee': '1.335',
               'processing_fee': '1.645'},
              {'@attribs': {'mail_retail': 'MAIL', 'member_group': '00460G'},
               'admin_fee': '0.88',
           'processing_fee': '1.18'}]}
    Notice the @attribs key, that's how I decided attributes should be stored.
    If you need something else, you can modify it to your liking:
    """

    @classmethod
    def elem2dict(cls, node):
        """
        Convert an xml.ElementTree node tree into a dict.
        """
        result = {}

        for element in node:
            key = element.tag
            if '}' in key:
                # Remove namespace prefix
                key = key.split('}')[1]

            if node.attrib:
                result['@attribs'] = dict(node.items())

            # Process element as tree element if the inner XML contains
            # non-whitespace content
            if element.text and element.text.strip():
                value = element.text
            else:
                value = cls.elem2dict(element)

            # Check if a node with this name at this depth was already found
            if key in result:
                if type(result[key]) is not list:
                    # We've seen it before, but only once, we need to
                    # convert it to a list
                    tempvalue = result[key].copy()
                    result[key] = [tempvalue, value]
                else:
                    # We've seen it at least once, it's already a list,
                    # just append the node's inner XML
                    result[key].append(value)
            else:
                # First time we've seen it
                result[key] = value

        return result

    @classmethod
    def mig(cls, path):
        from xml.etree import ElementTree as ET
        root = ET.parse('input.xml').getroot()
        result = cls.elem2dict(root)
        return result


class Xml2Dic:
    """
    XML to Dictionary String Class
    Convert xml to dic, using lxml xml processing library.
    see http://lxml.de/
    """
    @staticmethod
    def init_dic(tree):
        """
        initialise tree dictionary
        """
        if tree.tag is etree.Comment:
            return dict()
        if tree.attrib:
            dic = dict()
            dic[tree.tag] = dict()
        else:
            if tree.tag:
                dic = dict()
                dic[tree.tag] = None
            else:
                dic = dict()
        return dic

    @staticmethod
    def normalize_value(dic):
        """
        show normalized dictionary
        """
        # if value is list with 1 element use element as value
        dic_new = dict()
        for k, v in dic.items():
            if len(v) == 1:
                dic_new[k] = v[0]
            else:
                dic_new[k] = v
        return dic_new

    @classmethod
    def sh_dic(cls, arr):
        """
        show children dictionary for children map
        """
        dic_new = dict()
        for c_tree in arr:
            for k, v in c_tree.items():
                if k not in dic_new:
                    dic_new[k] = list()
                dic_new[k].append(v)

        # if value is list with 1 element use element as value
        return cls.normalize_value(dic_new)

    @staticmethod
    def update_with_attribs(dic, tree):
        """
        update dictionary with attributes dictionary
        """
        attribs = {f'@{k}': v for k, v in tree.attrib.items()}
        dic[tree.tag].update(attribs)

    @staticmethod
    def update_with_text(dic, tree, children):
        """
        update dictionary with text
        """
        text = tree.text.strip()
        if children or tree.attrib:
            if text:
                dic[tree.tag]['#text'] = text
        else:
            dic[tree.tag] = text
        return dic

    @classmethod
    def update(cls, dic, tree, children):
        """
        update dictionary
        """
        if tree.tag is etree.Comment:
            return dic
        if tree.attrib:
            cls.update_with_attribs(dic, tree)
        if tree.text:
            cls.update_with_text(dic, tree, children)
        return dic

    @staticmethod
    def map_seq(fnc, lst):
        """
        apply function on list using list comprehension

        :param fnc: function
        :param List lst: List
        :return List: List of all elements of lst modified by fnc
        """
        return [fnc(entry) for entry in lst]

    @classmethod
    def tree2dic(cls, tree):
        """
        migrate tree to dictionary
        """
        children = list(tree)
        if len(children) > 0:
            aod = map(cls.tree2dic, children)
            dic = dict()
            if tree.tag is not etree.Comment:
                dic[tree.tag] = cls.sh_dic(aod)
        else:
            dic = cls.init_dic(tree)
        cls.update(dic, tree, children)
        return dic

    @classmethod
    def mig(cls, str):
        """
        migrate xml string to etree and etree to dictionary
        """
        tree = etree.fromstring(str)
        # Iterate through all XML elements
        for elem in tree.getiterator():
            # Skip comments and processing instructions,
            # because they do not have names
            if not (
                isinstance(elem, etree._Comment)
                or isinstance(elem, etree._ProcessingInstruction)
            ):
                # Remove a namespace URI in the element's name
                elem.tag = etree.QName(elem).localname
        etree.cleanup_namespaces(tree)
        dic = cls.tree2dic(tree)
        return {tree.tag: dic}


class Xml2DicApc:

    @staticmethod
    def dic_normalize(dic):
        return {k: v[0] if len(v) == 1 else v for k, v in dic.items()}

    @staticmethod
    def sh_v(v, child, arr_child):
        a_key_to_agg = ['Attribute', 'Step']
        if child.tag == etree.Comment:
            text = child.text.strip()
            dic = dict()
            return text
        if child.tag not in a_key_to_agg:
            return v
        if not child.attrib and not child.text:
            return v
        if child.attrib:
            dic = {f'@{k}': v for k, v in child.attrib.items()}
        if child.text:
            text = child.text.strip()
            if len(arr_child) > 0 or child.attrib:
                if text:
                    dic['#text'] = text
            else:
                return text
        return dic

    @classmethod
    def tree2dic(cls, tree):
        obj = {tree.tag: [] if tree.attrib else None}
        a_child = list(tree)
        if len(a_child) > 0:
            aod = map(cls.tree2dic, a_child)
            dd = dict()
            a_tree = []
            for ix, dic in enumerate(aod):
                child = a_child[ix]
                if child.tag == etree.Comment:
                    continue
                for k, v in dic.items():
                    v = cls.sh_v(v, child, a_child)
                    a_key_to_agg = ['Attribute', 'Step']
                    if k in a_key_to_agg:
                        if k not in dd:
                            dd[k] = []
                        dd[k].append(v)
                    else:
                        if len(dd) > 0:
                            a_tree.append(dd)
                            dd = dict()
                        _dic = dict()
                        _dic[k] = v
                        a_tree.append(_dic)
            if len(dd) > 0:
                a_tree.append(dd)
                dd = dict()
            obj = {tree.tag: a_tree}
            # obj = {tree.tag: cls.dic_normalize(dd)}
        # obj = set_obj(obj, tree, a_child)
        return obj

    @classmethod
    def mig(cls, str, **kwargs):
        """
        migrate xml string to etree and etree to dictionary
        """
        tree = etree.fromstring(str)
        # Iterate through all XML elements
        for elem in tree.getiterator():
            # Skip comments and processing instructions,
            # because they do not have names
            if not (
                isinstance(elem, etree._Comment)
                or isinstance(elem, etree._ProcessingInstruction)
            ):
                # Remove a namespace URI in the element's name
                elem.tag = etree.QName(elem).localname
        etree.cleanup_namespaces(tree)
        dic = cls.tree2dic(tree)
        return {tree.tag: dic}
