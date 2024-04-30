#include "widget.h"
#include <QtWidgets/QApplication>


int main(int argc, char *argv[]) {
    QApplication a(argc, argv);
    QApplication::setAttribute(Qt::AA_DisableWindowContextHelpButton);//удаляет помощь
    widget w;
    w.exec();
}
