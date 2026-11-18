
[app]

title = Inside The Scan
package.name = insidethescan
package.domain = org.insidethescan

source.dir = .
source.include_exts = py,json,png,jpg,kv

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

[buildozer]

log_level = 2

[android]

android.api = 35
android.minapi = 23
android.archs = arm64-v8a

android.accept_sdk_license = True
