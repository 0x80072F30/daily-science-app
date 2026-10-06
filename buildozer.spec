[app]
title = Daily Science
package.name = dailyscience
package.domain = com.dailyscience.nda
source.dir = .
source.include_exts = py,png,jpg,kv,json,db
version = 1.0
requirements = python3,kivy==2.2.1,kivymd==1.2.0,pillow,materialyoucolor,exceptiongroup,asyncgui,asynckivy
android.permissions = POST_NOTIFICATIONS, WAKE_LOCK
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_licenses = True

[buildozer]
log_level = 2
warn_on_root = 1
