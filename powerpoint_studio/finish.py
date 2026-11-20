"""Финишная обработка PPTX: шрифты, тема, свойства документа.

python-pptx не умеет встраивать шрифты и править тему, поэтому здесь работаем
напрямую с OPC-пакетом. Всё опционально: если шаг не удался, файл остаётся
валидным — просто без соответствующей доработки.
"""
from __future__ import annotations

import io
import os
import re
import shutil
import zipfile

from pptx.opc.package import Part
from pptx.opc.packuri import PackURI
from lxml import etree

from . import brand as B

NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
REL_FONT = NS_R + "/font"


# ------------------------------------------------------------------ fonts
def embed_fonts(prs, fonts_dir, family=None):
    """Вложить regular+bold в пакет (embeddedFontLst + /ppt/fonts/fntdata-*.odttf).

    PowerPoint возьмёт шрифт из файла, даже если он не установлен в системе.
    Шрифты с fsType, запрещающим вложение, пропускаются.
    """
    from fontTools.ttLib import TTFont as FTFont

    family = family or B.FONT
    pkg = prs.part.package
    root = prs.part._element

    faces = []
    for weight, style in ((400, "regular"), (700, "bold")):
        path = os.path.join(fonts_dir, "LMMain-%d.ttf" % weight)
        if not os.path.exists(path):
            continue
        with open(path, "rb") as fh:
            data = fh.read()
        tt = FTFont(io.BytesIO(data), fontNumber=0, lazy=True)
        if tt["OS/2"].fsType & 0x0002:          # restricted — вложение запрещено
            continue
        part = Part(PackURI("/ppt/fonts/fntdata-%s.odttf" % style),
                    "application/x-fontdata", pkg, data)
        rid = prs.part.relate_to(part, REL_FONT)
        faces.append((style, rid))

    if not faces:
        return []

    old = root.find("{%s}embeddedFontLst" % NS_P)
    if old is not None:
        root.remove(old)
    lst = etree.SubElement(root, "{%s}embeddedFontLst" % NS_P)
    ef = etree.SubElement(lst, "{%s}embeddedFont" % NS_P)
    face = etree.SubElement(ef, "{%s}font" % NS_P)
    face.set("typeface", family)
    face.set("pitchFamily", "34")
    face.set("charset", "204")
    for style, rid in faces:
        etree.SubElement(ef, "{%s}%s" % (NS_P, style)).set("{%s}id" % NS_R, rid)

    # порядок дочерних элементов presentation.xml жёстко задан схемой
    _reorder(root, ["sldMasterIdLst", "notesMasterIdLst", "handoutMasterIdLst",
                    "sldIdLst", "sldSz", "notesSz", "embeddedFontLst", "custShowLst",
                    "photoAlbum", "custDataLst", "kinsoku", "defaultTextStyle",
                    "modifyVerifier", "extLst"])
    return [s for s, _ in faces]


def _reorder(root, order):
    kids = list(root)
    def rank(el):
        tag = etree.QName(el).localname
        return order.index(tag) if tag in order else len(order)
    for el in kids:
        root.remove(el)
    for el in sorted(kids, key=rank):
        root.append(el)


# ------------------------------------------------------------------ theme
def set_theme_fonts(prs, family=None):
    """Тема pptx должна ссылаться на тот же шрифт, что и тексты слайдов."""
    family = family or B.FONT
    import pptx
    root = prs.part.package
    changed = 0
    for part in root.iter_parts():
        if not str(part.partname).startswith("/ppt/theme/theme"):
            continue
        xml = part.blob if isinstance(part.blob, str) else part.blob.decode("utf-8")
        xml = re.sub(r'(<a:(?:major|minor)Font>\s*<a:latin typeface=")[^"]*(")',
                     lambda m: m.group(1) + family + m.group(2), xml)
        xml = re.sub(r'(<a:(?:major|minor)Font>\s*<a:latin typeface="[^"]*"[^>]*/>\s*<a:ea typeface=")[^"]*(")',
                     lambda m: m.group(1) + family + m.group(2), xml)
        xml = re.sub(r'(<a:font script="Cyrl" typeface=")[^"]*(")',
                     lambda m: m.group(1) + family + m.group(2), xml)
        part._blob = xml.encode("utf-8")
        changed += 1
    return changed


# ------------------------------------------------------------------ props
def set_props(prs, title, subject, author="Лемана ПРО", keywords="", category="Стратегия"):
    cp = prs.core_properties
    cp.title = title
    cp.subject = subject
    cp.author = author
    cp.last_modified_by = author
    cp.keywords = keywords
    cp.comments = ("Фирменный шаблон Лемана ПРО: жёлтый #FFC100, графит #303738, "
                   "белый #FFFFFF и тинты графита.")
    cp.category = category
    cp.language = "ru-RU"
    cp.revision = 1


# ------------------------------------------------------------------ checks
def package_report(path):
    """Проверка целостности готового файла."""
    z = zipfile.ZipFile(path)
    names = z.namelist()
    slides = sorted(n for n in names
                    if re.fullmatch(r"ppt/slides/slide\d+\.xml", n))
    media = [n for n in names if n.startswith("ppt/media/")]
    fonts = [n for n in names if n.startswith("ppt/fonts/")]
    present = z.read("ppt/presentation.xml").decode("utf-8")
    return dict(
        ok=z.testzip() is None,
        slides=len(slides),
        media=len(media),
        fonts=fonts,
        has_font_lock="embeddedFontLst" in present,
        size_mb=round(os.path.getsize(path) / 1e6, 2),
    )
