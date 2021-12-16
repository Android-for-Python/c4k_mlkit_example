Camera4Kivy MLKit Example
==========================

*MLKit Image Analysis using Camera4Kivy*

# Overview

Uses MLKit to detect to detect face, eyes, mouth.

MLKit is available on Android ONLY.

Illustrates using Camera4Kivy's `analyse_imageproxy_callback()`.

# Install

Camera4Kivy depends on the 'master' version of Buildozer. Currently `1.2.0.dev0`

`pip3 install git+https://github.com/kivy/buildozer.git`

The example includes a camera provider and a buildozer.spec

For any other project, follow the [camerax_provider install instructions](https://github.com/Android-for-Python/Camera4Kivy#candroid-camerax_provider)

And the following **must** be in the buildozer.spec:

`requirements= python3, kivy, camera4kivy`

`android.permissions = CAMERA`

`android.api = 30`  or greater (min 29)

`android.add_src = mlkit_src`

`android.gradle_dependencies = "com.google.mlkit:face-detection:16.0.6"`

`p4a.local_recipes = ./camerax_provider/recipes`

`p4a.hook = ./camerax_provider/gradle_options.py`

