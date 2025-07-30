import os

from kivy.lang import Builder

from carbonkivy.config import UIX

from .link import CLink, CLinkIcon, CLinkLabel

filename = os.path.join(UIX, "link", "link.kv")
if not filename in Builder.files:
    Builder.load_file(filename)
