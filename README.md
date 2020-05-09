# ASSD-TP4

## Requirements
To automatically install all python requirements you can run the commands:

* pip install -r requirements_pip
* conda install -y --file requirements_conda

Note: For this the files `requirements_pip` and `requirements_conda` are needed, which can be found in the repository root!

If you do not have an Anaconda distribution and therefore cannot run the `conda` command, run:

* pip install -r requirements_no_conda

Note: If your Python distribution is 3.7 or higher, you may need to install PyAudio's wheels (PyAudio depends on C) BEFORE running `pip install`. Follow [this link](https://stackoverflow.com/questions/52283840/i-cant-install-pyaudio-on-windows-how-to-solve-error-microsoft-visual-c-14/52284344#52284344) and go to the answer by "Agalin", who explains how to do it.