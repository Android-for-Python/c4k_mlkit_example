Camera4Kivy MLKit Example
==========================

*MLKit Image Analysis using Camera4Kivy*

# Overview

Uses MLKit to detect to detect face, eyes, mouth.

MLKit is available on Android ONLY.

Illustrates using Camera4Kivy's `analyse_imageproxy_callback()`.

# Install

Camera4Kivy depends on Buildozer 1.3.0 or later

`pip3 install buildozer`

The example includes a [camera provider](https://github.com/Android-for-Python/camera4kivy#android-camera-provider) and a [buildozer.spec](https://github.com/Android-for-Python/camera4kivy#buildozerspec).

The buildozer.spec includes `android.gradle_dependencies = "com.google.mlkit:face-detection:16.0.6"`
