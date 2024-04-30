#ifndef widget_H
#define widget_H

#include <QtWidgets/QDialog>
#include <QProgressBar>
#include <QGridLayout>
#include <QLabel>

#include "ThreadPool.h"

namespace Ui {
class widget;
}

class widget : public QDialog
{
    Q_OBJECT

public:
    explicit widget(QWidget *parent = nullptr);
    ~widget();

private:
    Ui::widget      *ui;
    QProgressBar    *bar_PROCESS = NULL;


private slots:
    void ss1(ThreadPool* myPool);
    void ss2(ThreadPool* myPool);
    void task(ThreadPool* myPool,QTableWidget* table1);
    void ref_thre(ThreadPool* myPool,QTableWidget* table1);

    void repic(int a);
    void restr(int a);
    void fo_dell_table_item();
};
#endif // WIDGET_H
