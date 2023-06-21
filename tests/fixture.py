#!/usr/bin/env python
"""Test fixtures."""
from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture()
def img() -> bytes:
    return Path("tests/resources/pic.png").read_bytes()


beeimg = """{"files":{"name":"x8078479702","size":"","url":"\\/\\/beeimg.com\\/images\\/x80784797021.png","thumbnail_url":"\\/\\/i.beeimg.com\\/images\\/thumb\\/x80784797021-xs.png","view_url":"\\/\\/beeimg.com\\/view\\/x8078479702\\/","delete_url":"N\\/A","delete_type":"DELETE","status":"Duplicate","code":"200"}}"""
catbox = """https://files.catbox.moe/4yt1tj"""
fastpic = """<?xml version="1.0" encoding="UTF-8"?>
<UploadSettings xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
<imagepath>https://i122.fastpic.org/big/2023/0621/ba/4cde7fe843ecf35688167399d5b269ba.png</imagepath>
<imageid>4cde7fe843ecf35688167399d5b269ba</imageid>
<session>ykBMZJeE6p</session>
<status>ok</status>
<error></error>
<viewurl>https://fastpic.org/view/122/2023/0621/4cde7fe843ecf35688167399d5b269ba.png.html</viewurl>
<viewfullurl>https://fastpic.org/view/122/2023/0621/4cde7fe843ecf35688167399d5b269ba.png.html</viewfullurl>
<thumbpath>https://i122.fastpic.org/thumb/2023/0621/ba/4cde7fe843ecf35688167399d5b269ba.jpeg</thumbpath>
<sessionurl>https://fastpic.org/session/2023/0621/ykBMZJeE6p.html</sessionurl>
</UploadSettings>"""
filecoffee = """{"success":true,"message":"File successfully uploaded","file":"u3s_hXaFjVQ5bWm0NqSfp.png","size":91,"filename":"u/u3s_hXaFjVQ5bWm0NqSfp.png","url":"https://file.coffee/u/u3s_hXaFjVQ5bWm0NqSfp.png","mime":"image/png","md5":"45927ce6c3a6ba2e48a260328dc57d3d"}"""
freeimage = """{"status_code":200,"success":{"message":"image uploaded","code":200},"image":{"name":"upload","extension":"png","width":100,"height":100,"size":91,"time":1687346353,"expiration":0,"adult":8,"status":0,"cloud":0,"vision":1,"likes":0,"description":null,"original_exifdata":null,"original_filename":"upload","views_html":0,"views_hotlink":0,"access_html":0,"access_hotlink":0,"file":{"resource":{"chain":{"image":"https:\\/\\/iili.io\\/HPTxvWu.png","thumb":"https:\\/\\/iili.io\\/HPTxvWu.th.png"},"chain_code":{"image":"HPTxvWu","thumb":"HPTxvWu"}}},"is_animated":0,"nsfw":0,"id_encoded":"HPTxvWu","ratio":1,"size_formatted":"91 B","filename":"HPTxvWu.png","url":"https:\\/\\/iili.io\\/HPTxvWu.png","url_short":"https:\\/\\/freeimage.host\\/","url_seo":"https:\\/\\/freeimage.host\\/i\\/upload.HPTxvWu","url_viewer":"https:\\/\\/freeimage.host\\/i\\/HPTxvWu","url_viewer_preview":"https:\\/\\/freeimage.host\\/","url_viewer_thumb":"https:\\/\\/freeimage.host\\/","image":{"filename":"HPTxvWu.png","name":"HPTxvWu","mime":"image\\/png","extension":"png","url":"https:\\/\\/iili.io\\/HPTxvWu.png","size":91},"thumb":{"filename":"HPTxvWu.th.png","name":"HPTxvWu.th","mime":"image\\/png","extension":"png","url":"https:\\/\\/iili.io\\/HPTxvWu.th.png"},"display_url":"https:\\/\\/iili.io\\/HPTxvWu.png","display_width":100,"display_height":100,"views_label":"views","likes_label":"likes","how_long_ago":"5 hours ago","date_fixed_peer":"2023-06-21 11:19:13","title":"upload","title_truncated":"upload","title_truncated_html":"upload","is_use_loader":false},"status_txt":"OK"}"""
gyazo = """{"type":"png","thumb_url":"https://thumb.gyazo.com/thumb/200/eyJhbGciOiJIUzI1NiJ9.eyJpbWciOiJfOWU5YzJiOTA1ZTM4NTYwMWE1NjQ4NmViOGFiYzVmMjEifQ.UEnPXn6-dbc4G74aogPzfbStPQ0V5hlHf5ghhZOdA1c-png.jpg","created_at":"2023-02-24T08:50:18+0000","image_id":"45927ce6c3a6ba2e48a260328dc57d3d","permalink_url":"https://gyazo.com/45927ce6c3a6ba2e48a260328dc57d3d","url":"https://i.gyazo.com/45927ce6c3a6ba2e48a260328dc57d3d.png"}"""
imageban = """{"data":{"date":"2023.06.21","name":"55dd05177f9f8a35875447f0f0755e67.png","server":"i5.imageban.ru","img_name":"image.png","size":"91","res":"100x100","link":"https:\\/\\/i5.imageban.ru\\/out\\/2023\\/06\\/21\\/55dd05177f9f8a35875447f0f0755e67.png","short_link":"http:\\/\\/ibn.im\\/4i374hK","deletehash":"kdhi4WKT9gEH9rl1ob92H1o19M5hWF0p"},"success":true,"status":200}"""
imagebin = """status:7QknLCJgP5iN
url:https://ibin.co/7QknLCJgP5iN.png"""
imgbb = """{"data":{"id":"bs96JVz","title":"upload","url_viewer":"https:\\/\\/ibb.co\\/bs96JVz","url":"https:\\/\\/i.ibb.co\\/rxrQsh4\\/upload.png","display_url":"https:\\/\\/i.ibb.co\\/rxrQsh4\\/upload.png","width":100,"height":100,"size":91,"time":1687346358,"expiration":0,"image":{"filename":"upload.png","name":"upload","mime":"image\\/png","extension":"png","url":"https:\\/\\/i.ibb.co\\/rxrQsh4\\/upload.png"},"thumb":{"filename":"upload.png","name":"upload","mime":"image\\/png","extension":"png","url":"https:\\/\\/i.ibb.co\\/bs96JVz\\/upload.png"},"delete_url":"https:\\/\\/ibb.co\\/bs96JVz\\/8940c1ed55dd806e8b9de248b3707288"},"success":true,"status":200}"""
imgchest = """{"data":{"id":"qe4g522b7j2","title":null,"username":"lF2LP3","privacy":"hidden","report_status":1,"views":0,"nsfw":0,"image_count":1,"created":"2023-06-21T17:22:57.000000Z","delete_url":"https:\\/\\/api.imgchest.com\\/p\\/7b49jh6ggj7w8\\/delete","images":[{"id":"3yrgcr3jpp4","description":null,"link":"https:\\/\\/cdn.imgchest.com\\/files\\/3yrgcr3jpp4.png","position":1,"created":"2023-06-21T17:22:57.000000Z","original_name":"img.png"}]}}"""
imgur = """{"data":{"id":"SKAxiks","title":null,"description":null,"datetime":1687366735,"type":"image\\/png","animated":false,"width":100,"height":100,"size":91,"views":0,"bandwidth":0,"vote":null,"favorite":false,"nsfw":null,"section":null,"account_url":null,"account_id":0,"is_ad":false,"in_most_viral":false,"has_sound":false,"tags":[],"ad_type":0,"ad_url":"","edited":"0","in_gallery":false,"deletehash":"1NV90wWpO691n05","name":"","link":"https:\\/\\/i.imgur.com\\/SKAxiks.png"},"success":true,"status":200}"""
lensdump = """{"status_code":200,"success":{"message":"image uploaded","code":200},"image":{"name":"CJkLoa","extension":"png","size":91,"width":100,"height":100,"date":"2023-06-21 13:23:30","date_gmt":"2023-06-21 17:23:30","title":null,"description":null,"nsfw":0,"storage_mode":"direct","md5":"45927ce6c3a6ba2e48a260328dc57d3d","original_filename":"upload","original_exifdata":null,"views":0,"category_id":null,"chain":5,"thumb_size":292,"medium_size":0,"expiration_date_gmt":null,"likes":0,"is_animated":0,"source_md5":null,"is_approved":1,"is_360":0,"file":{"resource":{"type":"url"}},"id_encoded":"CJkLoa","filename":"CJkLoa.png","mime":"image\\/png","url":"https:\\/\\/i.lensdump.com\\/i\\/CJkLoa.png","ratio":1,"size_formatted":"91 B","url_viewer":"https:\\/\\/lensdump.com\\/i\\/CJkLoa","path_viewer":"\\/i\\/CJkLoa","url_short":"https:\\/\\/lensdump.com\\/i\\/CJkLoa","image":{"filename":"CJkLoa.png","name":"CJkLoa","mime":"image\\/png","extension":"png","url":"https:\\/\\/i.lensdump.com\\/i\\/CJkLoa.png","size":91},"thumb":{"filename":"CJkLoa.th.png","name":"CJkLoa.th","mime":"image\\/png","extension":"png","url":"https:\\/\\/i.lensdump.com\\/i\\/CJkLoa.th.png","size":292},"display_url":"https:\\/\\/i.lensdump.com\\/i\\/CJkLoa.png","display_width":100,"display_height":100,"views_label":"views","likes_label":"likes","how_long_ago":"moments ago","date_fixed_peer":"2023-06-21 17:23:30","title_truncated":"","title_truncated_html":"","is_use_loader":false,"delete_url":"https:\\/\\/lensdump.com\\/i\\/CJkLoa\\/delete\\/916e9c2b82ee44cc2f8cdff393bf6167f017ad8b3c2aca1b"},"status_txt":"OK"}"""
pixeldrain = """{"success":true,"id":"y61mKtGN"}"""
pixhost = """{"name":"upload.png","show_url":"https:\\/\\/pixhost.to\\/show\\/865\\/361824612_upload.png","th_url":"https:\\/\\/t87.pixhost.to\\/thumbs\\/865\\/361824612_upload.png"}"""
ptpimg = """[
    {
        "code": "8i531v",
        "ext": "png"
    }
]"""
smms = """{"success":true,"code":"success","message":"Upload success.","data":{"file_id":0,"width":100,"height":100,"filename":"upload","storename":"Bqv9EmdelxcM2XN.png","size":91,"path":"\\/2023\\/06\\/22\\/Bqv9EmdelxcM2XN.png","hash":"LgImaVk5s4UBujtdfeRzCQ9DX6","url":"https:\\/\\/s2.loli.net\\/2023\\/06\\/22\\/Bqv9EmdelxcM2XN.png","delete":"https:\\/\\/sm.ms\\/delete\\/LgImaVk5s4UBujtdfeRzCQ9DX6","page":"https:\\/\\/sm.ms\\/image\\/Bqv9EmdelxcM2XN"},"RequestId":"21A70D33-EFFC-4540-8C2A-8BF36131C122"}"""
sxcu = """{
    "id": "66iFnGoQ6",
    "url": "https://sxcu.net/66iFnGoQ6",
    "del_url": "https://sxcu.net/api/files/delete/66iFnGoQ6/dd6d902a-ebaa-453a-a794-458596a7badf",
    "thumb": "https://sxcu.net/t/66iFnGoQ6.png"
}"""
telegraph = """[{"src":"\\/file\\/994610b961b722e9fbd9c.png"}]"""
thumbsnap = """{"data":{"id":"GfQWVNwT","url":"https://thumbsnap.com/GfQWVNwT","media":"https://thumbsnap.com/i/GfQWVNwT.png","thumb":"https://thumbsnap.com/t/GfQWVNwT.jpg","width":100,"height":100},"success":true,"status":200}"""
tixte = """{"success":true,"size":91,"data":{"id":"lj5zsvnkwa0","name":"lj5zsvnkwa0","region":"us-east-1","filename":"lj5zsvnkwa0.png","extension":"png","domain":"cdx.tixte.co","type":1,"expiration":null,"permissions":[{"user":{"id":"0e0f89b4229244ff8b229d20e1e84852","username":"CdX"},"access_level":3}],"url":"https://cdx.tixte.co/lj5zsvnkwa0.png","direct_url":"https://cdx.tixte.co/r/lj5zsvnkwa0.png","deletion_url":"https://api.tixte.com/v1/users/@me/uploads/del/lj5zsvnkwa0?auth=e2ceedcd-2b46-4ded-b241-e6d310db6aac","message":"File uploaded successfully"}}"""
up2sha = """{"id":116031,"public_url":"https:\\/\\/up2sha.re\\/file?f=CozTXz35lv1Lk0o7NC","download_url":"https:\\/\\/up2sha.re\\/files\\/CozTXz35lv1Lk0o7NC\\/download"}"""
uplio = """https://upl.io/0w25y7"""
uploadcare = """{"filename":"7eb40c10-fc9b-42a2-a086-e9eef5bafb9c"}"""
vgy = """{"error":false,"size":91,"filename":"3Kyfvf","ext":"png","url":"https://vgy.me/u/3Kyfvf","image":"https://i.vgy.me/3Kyfvf.png","delete":"https://vgy.me/delete/357619c3-aab3-4a22-84ba-03ebb601efbf"}"""


RESPONSE: dict[str, tuple[str, str]] = {
    "beeimg": (beeimg, "https://beeimg.com/images/x80784797021.png"),
    "catbox": (catbox, "https://files.catbox.moe/4yt1tj"),
    "fastpic": (
        fastpic,
        "https://i122.fastpic.org/big/2023/0621/ba/4cde7fe843ecf35688167399d5b269ba.png",
    ),
    "filecoffee": (filecoffee, "https://file.coffee/u/u3s_hXaFjVQ5bWm0NqSfp.png"),
    "freeimage": (freeimage, "https://iili.io/HPTxvWu.png"),
    "gyazo": (gyazo, "https://i.gyazo.com/45927ce6c3a6ba2e48a260328dc57d3d.png"),
    "imageban": (
        imageban,
        "https://i5.imageban.ru/out/2023/06/21/55dd05177f9f8a35875447f0f0755e67.png",
    ),
    "imagebin": (imagebin, "https://ibin.co/7QknLCJgP5iN.png"),
    "imgbb": (imgbb, "https://i.ibb.co/rxrQsh4/upload.png"),
    "imgchest": (imgchest, "https://cdn.imgchest.com/files/3yrgcr3jpp4.png"),
    "imgur": (imgur, "https://i.imgur.com/SKAxiks.png"),
    "lensdump": (lensdump, "https://i.lensdump.com/i/CJkLoa.png"),
    "pixeldrain": (pixeldrain, "https://pixeldrain.com/api/file/y61mKtGN"),
    "pixhost": (pixhost, "https://pixhost.to/show/865/361824612_upload.png"),  # show_url
    "ptpimg": (ptpimg, "https://ptpimg.me/8i531v.png"),
    "smms": (smms, "https://s2.loli.net/2023/06/22/Bqv9EmdelxcM2XN.png"),
    "sxcu": (sxcu, "https://sxcu.net/66iFnGoQ6.png"),
    "telegraph": (telegraph, "https://telegra.ph/file/994610b961b722e9fbd9c.png"),
    "thumbsnap": (thumbsnap, "https://thumbsnap.com/i/GfQWVNwT.png"),
    "tixte": (tixte, "https://cdx.tixte.co/r/lj5zsvnkwa0.png"),
    "up2sha": (up2sha, "https://up2sha.re/media/raw/CozTXz35lv1Lk0o7NC.png"),
    "uplio": (uplio, "https://upl.io/i/0w25y7.png"),
    "uploadcare": (
        uploadcare,
        "https://ucarecdn.com/7eb40c10-fc9b-42a2-a086-e9eef5bafb9c/img.png",
    ),
    "vgy": (vgy, "https://i.vgy.me/3Kyfvf.png"),
}
