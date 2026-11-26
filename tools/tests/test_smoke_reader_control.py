"""Reduced shape of the production Compose reader, including its misleading page header."""
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from smoke_android_upgrade import PKG, counter, exact_control

class ReaderControlTest(unittest.TestCase):
    def hierarchy(self, button):
        xml=ET.Element("hierarchy")
        def node(parent,text="",click="false",enabled="true",rect="[0,0][720,100]"):
            return ET.SubElement(parent,"node",text=text,package=PKG,clickable=click,enabled=enabled,bounds=rect)
        node(xml,"第 1 / 50 句 · 可以按上一句或下一句浏览")
        if button:
            parent=node(xml,click="true",enabled=button,rect="[360,1200][680,1300]")
            node(parent,"下一句",rect="[450,1220][580,1280]")
        return xml

    def test_header_and_disabled_control_are_not_actions(self):
        self.assertIsNone(exact_control(self.hierarchy(None),"下一句"))
        self.assertIsNone(exact_control(self.hierarchy("false"),"下一句"))

    def test_exact_text_uses_enabled_clickable_parent(self):
        self.assertEqual(exact_control(self.hierarchy("true"),"下一句"),(360,1200,680,1300))

    def test_page_counter_must_advance(self):
        self.assertFalse(counter(2).search("第 1 / 50 句 · 可以按上一句或下一句浏览"))
        self.assertTrue(counter(2).search("第 2 / 50 句 · 可以按上一句或下一句浏览"))
        self.assertFalse(counter(2).search("第 20 / 50 句"))
