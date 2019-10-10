import platform
print("\nSystem Architecture: %s" % platform.architecture()[0])
print("\nmacOS Version: %s" % platform.mac_ver()[0])
print("\nProcessor Architecture: %s" % platform.processor())
print("\nPython Build: %s" % platform.python_build()[0])
print("\nMachine Name: %s" % platform.uname()[1])
