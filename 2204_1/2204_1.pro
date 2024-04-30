greaterThan(QT_MAJOR_VERSION, 4): QT += widgets
CONFIG += c++11 console
CONFIG -= app_bundle

DEFINES += QT_DEPRECATED_WARNINGS
SOURCES += \
        main.cpp \
        widget.cpp

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

HEADERS += \
    ThreadPool.h \
    widget.h

FORMS += \
    widget.ui

DISTFILES += \
    CMakeLists.txt \
    cmakelist2.txt

