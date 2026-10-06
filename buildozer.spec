[app]

title = Daily Science
package.name = dailyscience
package.domain = com.dailyscience.nda
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.2.1,kivymd,sqlite3
android.permissions = POST_NOTIFICATIONS
android.api = 34
android.minapi = 24
android.sdk = 34
android.build_tools_version = 34.0.0
android.archs = arm64-v8a
android.accept_sdk_licenses = True

[buildozer]
log_level = 2
warn_on_root = 1
