#pragma once
#include <deque> // для двухсторонней очереди
#include <iostream>
#include <mutex>
#include <string>
#include <sstream>

//VVV for linx
#include <thread>
#include <stdlib.h>
#include <condition_variable>
#include <chrono>
//^^^

#include <QTableWidget>
#include <QString>
//////////////////////
class ThreadPool: public QObject
{
    Q_OBJECT

signals:
    void bar_pr(int);
    void for_table();
    void init_thread(const QString&);
    void del_thread(const QString&);
    void del_task();

private:
    std::vector<std::thread> threads;
    // stop for deq
    std::mutex queue_mutex;
    std::condition_variable condition;
    bool joinStop;
    int readyThreads; //не управляемые выделенные

public:
    ThreadPool() {
        joinStop = false;
    }

    //переопределение size pool
    void new_count(int nthreads,std::deque<std::function<void()>>* tasks,
                   QTableWidget* table1) {
        readyThreads = 0;
        joinStop = true;
        condition.notify_all();
        del_thr();
        joinStop = false;
        add_thr(nthreads,tasks,table1);

    }

    void add_thr(int nthreads,std::deque<std::function<void()>>* tasks,
                 QTableWidget* table1) {
        for (int i = 0; i < nthreads; ++i) {
                                //VVV очередь лямд leak, очередь не хранит лишнего
            threads.emplace_back(std::thread([=] {this->dot(tasks,table1); }));
        }
    }

    void del_thr() {
        int num = (int)threads.size();
        for (int i = 0; i < num ; ++i) {
            if (threads.back().joinable()) {
                threads.back().join();
            }
            threads.pop_back();
        }
        const QString namel= "\n--- all treads have been reset ---";
        emit del_thread(namel);
    }

    void dot(std::deque<std::function<void()>>* tasks,
                QTableWidget* table1) {
        int nom = NULL;
        while (true) {
            std::function<void()> task; {

                std::unique_lock<std::mutex> lock(queue_mutex);
                while (!(joinStop || !tasks->empty())) {

                    //
                    std::stringstream ss;
                    ss << std::this_thread::get_id();
                    int id = std::stoull(ss.str());
                    const QString namel= "init thread --- "
                                         +QString::number(id)
                                         +" --- wait for";
                    emit init_thread(namel);
                    //
                    condition.wait(lock);
                }
                if (joinStop) {
                    readyThreads++;
                    return;
                }
                task = move(tasks->front());
                tasks->pop_front();
                nom = (int)table1->rowCount() - (int)tasks->size();
            }
            task();
            emit bar_pr(nom);

            if (joinStop) {
                readyThreads++;
                return;
            }
        }
    }

    void ad_task(std::function<void()> task,std::deque<std::function<void()>>* tasks,QTableWidget* table1) {
        std::unique_lock<std::mutex> lock(queue_mutex);

        table1->insertRow(0);//нужно, иначе придестяждать реквест для отображения или пропускать
        tasks->emplace_back(task);
        emit for_table();
        condition.notify_one();
    }

    // task/threads del
    void joinwait_del_threads(std::deque<std::function<void()>>* tasks) {
        joinStop = true;
        condition.notify_all();
        int num = (int)threads.size();
        while (num != readyThreads);// for wait
        tasks->clear();

        del_thr();
        readyThreads = 0;
    }

    // до выполняет task/потоки del
    void deltask(std::deque<std::function<void()>>* tasks) {
        tasks->clear();
        emit del_task();
    }

    ~ThreadPool() {
        condition.notify_all();
        del_thr();
    }
};


class ttasks: public QObject
{
    Q_OBJECT

signals:
    void s_fakt(const QString &namel);
    void s_fib(const QString &namel);
    void s_fsec(const QString &namel);

public:
    std::deque<std::function<void()>> deq;
    ttasks() {
    }

    void fakt(int x) {
        auto func1 = [](int x){
            int i;
            int res=1;
            for (i = 1; i <= x; i++) {
              res = res * i;
            }
            return res;
        };
        std::stringstream ss;
        ss << std::this_thread::get_id();
        int id = std::stoull(ss.str());
        const QString namel=" N -- " +  QString::number(x) + " --- zadacha "
                            +"facktorial" + " --- answer_"
                            +QString::number(func1(x)) + " --- thread - "
                            +QString::number(id);
        emit s_fakt(namel);
    }

    void fib(int x) {
        auto func2 = [](int x){
            int a = 0, res = 1, c, i;
            if(x == 0) return a;
            for(i = 2; i <= x; i++){
               c = a + res;
               a = res;
               res = c;
            }
            return res;
        };
        std::stringstream ss;
        ss << std::this_thread::get_id();
        int id = std::stoull(ss.str());
        const QString namel= " N -- " + QString::number(x) + " --- zadacha "
                             +"fibonachi" + " --- answer_"
                             +QString::number(func2(x)) + " --- thread - "
                             +QString::number(id);
        emit s_fib(namel);
    }

    void fsec(int x) {
        ////using namespace std::chrono_literals;
        auto func3 = [](void){std::this_thread::sleep_for(std::chrono::seconds(1));};
        func3();
        std::stringstream ss;
        ss << std::this_thread::get_id();
        int id = std::stoull(ss.str());
        const QString namel= " N -- " + QString::number(x) + " --- zadacha "
                             +"delay 1sec" +
                             " --- thread - "
                             +QString::number(id);
        emit s_fsec(namel);
    }

    ~ttasks() {
    }
};
