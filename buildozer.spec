[app]
title = OpenAir Generator
package.name = openairgen
package.domain = org.flyingnomads
source.dir = .
source.include_exts = py,txt,kv
version = 1.0
requirements = python3,kivy,kivymd,requests,beautifulsoup4
orientation = portrait
fullscreen = 0

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET
android.minapi = 21
android.api = 31
android.arch = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1