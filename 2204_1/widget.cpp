#include "widget.h"
#include "ui_widget.h"

//pool
ttasks tasks;
auto *fa = &tasks.deq;
ThreadPool myPool;

std::deque<QProgressBar> bars;

widget::widget(QWidget *parent):
    QDialog(parent),
    ui(new Ui::widget)
{
   ui->setupUi(this);
   QColor dark(Qt::darkGray);
   QPalette pl; pl.setColor (QPalette::Active, QPalette::Window, dark);
   setPalette(pl);
   setStyleSheet(
               "QWidget {border: 0.1px solid DarkCyan ;text-align: center;"
               "color:rgba(255,255,250,255);"
               "border-radius: 2px;"
               "border-width: 2px;"
               "border-image: 9,2,5,2; "
               "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(70, 70, 70, 255), stop:1 rgba(10, 0, 0, 200));"
               "}"
               "QHeaderView::section:horizontal {color: #fff;border-style: solid;background-color: qlineargradient( x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #20B2AA, stop: 1 #356ccc);}"

               "QTableView {font-family: \"Times New Roman\"; font-size: 12pt ;"
               "border: 2px solid #3873d9;border-top-color: #808000;border-radius: 4px;background-color: #696969;gridline-color: #777;selection-background-color: #808000;color:#000000;font-size:12px;}"
               );
    ThreadPool* myPool_uk = &myPool;

    QStringList headerList;
    headerList <<"№ task"<<"%";

    QTableWidget  *table1 = ui->tableWidget;

    table1->setColumnCount(headerList.size());
    table1->setHorizontalHeaderLabels(headerList);
    table1->horizontalHeader()->setVisible(true);
    table1->setStyleSheet("QTableView {font-size: 12pt ;}");

    connect(ui->btn_1,&QPushButton::clicked,this,[=](void){ref_thre(myPool_uk,table1);});
    connect(ui->btn_2,&QPushButton::clicked,this,[=](void){task(myPool_uk,table1);});
    connect(ui->btn_3,&QPushButton::clicked,this,[=](void){ss1(myPool_uk);});
    connect(ui->btn_4,&QPushButton::clicked,this,[=](void){ss2(myPool_uk);});

    QProgressBar *bar_PROCESS = new QProgressBar;
    bars.emplace_back(bar_PROCESS);

    QObject::connect(myPool_uk,&ThreadPool::for_table,this,
                           [=](void)
                            //VVV mem leak по valgrin, но все трется когдатаблица обнуляется
                           {QProgressBar *bar_PROCESS = new QProgressBar;
                            bars.emplace_back(bar_PROCESS);
                            bars.back().setValue(0);
                            table1->setCellWidget(0,table1->columnCount()-1,&bars[table1->rowCount()]);
                            table1->setItem(0, 0,new QTableWidgetItem(QString::number(table1->rowCount())
                                                                      )
                                            );
                           },Qt::QueuedConnection);



    /*connect(ui->btn_3,&QPushButton::clicked,this,
                     [=](void){bars[1].setValue(0);
                               });*/

    QObject::connect(myPool_uk, SIGNAL(bar_pr(int)),this,SLOT(repic(int)),Qt::QueuedConnection);

    QTextEdit *aaa = ui->textEdit;
    QObject::connect(myPool_uk, SIGNAL(bar_pr(int)),this,SLOT(restr(int)),Qt::QueuedConnection);
    QObject::connect(myPool_uk, SIGNAL(init_thread(const QString &)),aaa,SLOT(append(const QString &)),Qt::QueuedConnection);
    QObject::connect(myPool_uk, SIGNAL(del_thread(const QString &)),aaa,SLOT(append(const QString &)),Qt::QueuedConnection);
    QObject::connect(myPool_uk, SIGNAL(del_task()),this,SLOT(fo_dell_table_item()),Qt::QueuedConnection);

    QObject::connect(&tasks, SIGNAL(s_fakt(const QString &)),aaa,SLOT(append(const QString &)),Qt::QueuedConnection);
    QObject::connect(&tasks, SIGNAL(s_fib(const QString &)),aaa,SLOT(append(const QString &)),Qt::QueuedConnection);
    QObject::connect(&tasks, SIGNAL(s_fsec(const QString &)),aaa,SLOT(append(const QString &)),Qt::QueuedConnection);
    //QObject::connect(&tasks, SIGNAL(init_thread(const QString &)),aaa,SLOT(append(const QString &)),Qt::QueuedConnection);

}

void widget::restr(int a){
    QString namel =  "--№-- " + QString::number(a);
    QTextEdit *aaa = ui->textEdit;
    aaa->textCursor().movePosition(QTextCursor::End);
    aaa->insertPlainText(namel);
}

void widget::fo_dell_table_item(){
    ui->tableWidget->clearContents();
    //ui->tableWidget->setRowCount(0);
    //ui->tableWidget->model()->removeRows(0, ui->tableWidget->rowCount());
}

void widget::repic(int a){
    bars[a].setValue(100);
}

void widget::ss1(ThreadPool* myPool){
    myPool->joinwait_del_threads(fa);
}

void widget::ref_thre(ThreadPool* myPool,QTableWidget* table1){
    //int nthreads = std::thread::hardware_concurrency(); // max colvo threads
    std::string n = ui->count_tr->text().toStdString();
    int count_trd{ std::stoi(n) };
    myPool->new_count(count_trd,fa,table1);
}

void widget::task(ThreadPool* myPool,QTableWidget* table1){
    int x = ui->n_chisl->text().toInt();
    //std::cout << ui->comboBox->currentText().toStdString()<< "\n";
    if ("factorial" == ui->comboBox->currentText().toStdString()){
        myPool->ad_task([=](void) {tasks.fakt(x); },fa,table1);
    }
    if ("fibonachi" == ui->comboBox->currentText().toStdString()){
        myPool->ad_task([=](void) {tasks.fib(x); },fa,table1);
    }
    if ("time2s" == ui->comboBox->currentText().toStdString()){
        myPool->ad_task([=](void) {tasks.fsec(x); },fa,table1);
    }
}

void widget::ss2(ThreadPool* myPool){
    myPool->deltask(fa);
}

widget::~widget(){
    delete ui;
}
