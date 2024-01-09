#include <bits/stdc++.h>
#include <conio.h>
#include <dirent.h>
#include <Windows.h>
using namespace std;

struct group
{
    string screen_name, followers;
    int id, post_id;
    char type;
    group() : id(-1), screen_name(""), followers("-1"), type('.') {}
    group(int _id, string sn, string fols, char ch) : id(_id), screen_name(sn), followers(fols), type(ch) {}
    friend istream& operator>>(istream& stream, group& g);
    friend ostream& operator<<(ostream& stream, group g);
};
vector<string> pools;
map<string, int> status;
set<string> pathsToDo;
// 0 - todo
// 1 - in progress
// 2 - done
string browser = "C:/Users/79150/AppData/Local/Yandex/YandexBrowser/Application/browser.exe";
//string browser = "C:/Users/hp291/AppData/Local/Yandex/YandexBrowser/Application/browser.exe";
//string browser = "C:/Users/NV/AppData/Local/Yandex/YandexBrowser/Application/browser.exe";
string vkLink = " https://vk.com/";
void getPools();
void setConsole();
void setColor(int);


int main()
{
    setlocale(0, "");
    setConsole();
    getPools();

    string path;
    ofstream fout;
    ifstream fin("do_not_open/execution_status.txt");
    if(!fin) {
        mkdir("do_not_open");
        mkdir("do_not_open/backup");
        for(int i = 0; i < pools.size(); ++i)
            status[pools[i]] = 0;
    }
    else {
        int progress;
        while(fin >> path >> progress) {
            status[path] = progress;
        }
        fin.close();
    }
    if(status.size() != pools.size()) { // если добавились новые файлы в Pools
        for(int i = 0; i < pools.size(); ++i) {
            if(status.find(pools[i]) == status.end())
                status[pools[i]] = 0;
        }
    }

    path = "";
    for(auto it = status.begin(); it != status.end(); ++it) {
        if(it->second != 2) pathsToDo.insert(it->first);
        if(it->second == 1) path = it->first;
    }
    if(!pathsToDo.size()) {
        cout << "\n\tВсе группы отсортированы!\n\n";
        system("pause");
        return 0;
    }
    vector<group> newPool;
    int startFrom = 0;
    group gr;
    if(path != "") {
        string progressFile = "do_not_open/" + path.substr(0, path.size() - 4) + "/progress.txt";
        fin.open(progressFile.c_str());
        if(fin) {
            fin >> startFrom;
            while(fin >> gr) newPool.push_back(gr);
            fin.close();
            remove(progressFile.c_str());
            progressFile.erase(progressFile.rfind("/"));
            RemoveDirectory(progressFile.c_str());
        }
        else {
            cout << "\n\tВ \"do_not_open\" нет папки \"" << path.substr(0, path.size() - 4) << "\"\n";
            system("pause");
            exit(-1);
        }
    }
    else path = *pathsToDo.begin();

    vector<group> initialPool;
    char choice;
    string path_demonstration;
    while(pathsToDo.size()) {
        initialPool.clear();
        fin.open(("Pools/" + path).c_str());
        if(!fin) {
            perror(("Ошибка в строке " + to_string(__LINE__)).c_str());
            system("pause");
            exit(-1);
        }
        while(fin >> gr) initialPool.push_back(gr);
        fin.close();

        ifstream currPool(("Pools/" + path).c_str(), ios::binary);
        ofstream backup(("do_not_open/backup/" + path).c_str(), ios::binary);
        backup << currPool.rdbuf();
        currPool.close();
        backup.close();

        for(int i = startFrom; i < initialPool.size(); ++i) {
            system((browser + vkLink + initialPool[i].screen_name).c_str());
            if(initialPool[i].followers == "-1") {
                string input;
                int amount;
                do {
                    system("cls");
                    cout << "\n\t" << i + 1 << ") Напиши количество подписчиков в группе\n\t";
                    string indent = "   ";
                    if(i + 1 >= 10) indent += ' ';
                    if(i + 1 >= 100) indent += ' ';
                    if(i + 1 >= 1000) indent += ' ';
                    setColor(6); cout << indent << initialPool[i].screen_name << "\n\n";
                    setColor(8);
                    cout << "\t(Это не обязательно, можешь проигнорировать.\n\tЕсли, например, сразу видно что группа не\n\t";
                    cout << "подходит, просто жми "; setColor(4); cout << "Tab"; setColor(8); cout << " и все. Если хочешь\n\t";
                    cout << "выйти, сразу жми "; setColor(4); cout << "backspace"; setColor(8); cout << ")\n\n\t";
                    setColor(15);
                    cout << "=> ";

                    char first_char = _getche();
                    if(first_char == 9 || first_char == 13 || first_char == 8 || first_char == 32) {
                        choice = first_char;
                        goto actions;
                    }
                    getline(cin, input);
                    input = string(1, first_char) + input;

                    while(input[0] == ' ') input.erase(0, 1);
                    if(input.size()) {
                        while(input.back() == ' ') input.pop_back();
                    }

                    if(input != "") {
                        initialPool[i].followers = input;
                        break;
                    }
                }while(1);
            }
            system("cls");
            path_demonstration = path.substr(0, path.size() - 4);
            for(int i = 0; i < path_demonstration.size(); ++i)
                if(path_demonstration[i] == '_') path_demonstration[i] = ' ';
            cout << "\n\tПул \"" << path_demonstration << "\" ("; setColor(11); cout << status.size() - pathsToDo.size() + 1; setColor(15);
            cout << " из "; setColor(11); cout << status.size(); setColor(15); cout << ")";
            cout << "\n\tКоличество групп в данном пуле: ";
            setColor(11); cout << initialPool.size(); setColor(15);
            cout << "\n\n\t" << i + 1 << ") " << "Оставляем данную группу?\n\t";
            setColor(6); cout << initialPool[i].screen_name; setColor(15);
            cout << "\n\n\t";
            setColor(4); cout << "Enter"; setColor(15);
            cout << " -- да\n\t";
            setColor(4); cout << "Tab"; setColor(15);
            cout << " -- убираем группу из пула\n\t";
            setColor(4); cout << "Backspace"; setColor(15);
            cout << " -- закрыть и сохранить\n\t";
            setColor(4); cout << "Пробел"; setColor(15);
            cout << " -- загрузить страницу еще раз\n\n\t";
            do choice = _getch();
            while(choice != 13 && choice != 9 && choice != 8 && choice != 32);
            actions:
            if(choice == 13) newPool.push_back(initialPool[i]);
            else if(choice == 32) {
                i--;
                continue;
            }
            else if(choice == 8) {
                if(i) { // сохраняем новые данные
                    mkdir(("do_not_open/" + path.substr(0, path.size() - 4)).c_str());
                    string progressFile = "do_not_open/" + path.substr(0, path.size() - 4) + "/progress.txt";
                    fout.open(progressFile.c_str());
                    fout << i << '\n';
                    for(auto x : newPool) fout << x;
                    fout.close();
                    status[path] = 1;
                }
                fout.open("do_not_open/execution_status.txt");
                for(auto it = status.begin(); it != status.end(); ++it)
                    fout << it->first << ' ' << it->second << '\n';
                fout.close();
                return 0;
            }
        }

        status[path] = 2;
        fout.open("do_not_open/execution_status.txt");
        for(auto it = status.begin(); it != status.end(); ++it)
            fout << it->first << ' ' << it->second << '\n';
        fout.close();
        fout.open(("Pools/" + path).c_str());
        for(int i = 0; i < newPool.size(); ++i)
            fout << newPool[i];
        fout.close();
        newPool.clear();

        pathsToDo.erase(path);
        if(!pathsToDo.size()) {
            system("cls");
            cout << "\n\tВсе группы отсортированы!\n\n";
            system("pause");
            return 0;
        }
        else path = *pathsToDo.begin();
        startFrom = 0;
    }

    return 0;
}

void getPools()
{
    DIR *dir = opendir("Pools");
    if(!dir) {
        cout << "\n\tНет папки Pools\n\n";
        system("pause");
        exit(-1);
    }
    dirent *entry;
    while((entry = readdir(dir)) != nullptr) {
        string s = entry->d_name;
        if(s != "." && s != "..") pools.push_back(s);
    }
}

void setConsole()
{
    // ширина и высота монитора компьютера в пикселях
    int monitorWidth = GetSystemMetrics(SM_CXSCREEN);
    int monitorHeight = GetSystemMetrics(SM_CYSCREEN);

    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    CONSOLE_FONT_INFOEX fontInfo;
    fontInfo.cbSize = sizeof(fontInfo);
    GetCurrentConsoleFontEx(hConsole, TRUE, &fontInfo);
    wcscpy(fontInfo.FaceName, L"Consolas");
    fontInfo.dwFontSize.Y = 24;
    SetCurrentConsoleFontEx(hConsole, TRUE, &fontInfo);
    HWND window_header = GetConsoleWindow();
    SetWindowPos(window_header, HWND_TOP, monitorWidth - 650, 85, 500, 500, NULL);
    system("mode con cols=60 lines=14");
}

void setColor(int text)
{
    HANDLE hStdOut = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hStdOut, (WORD) text);
}

istream& operator>>(istream& stream, group& g)
{
    stream >> g.id >> g.screen_name >> g.followers >> g.type;
    if(stream.peek() != '\n') stream >> g.post_id;
    else g.post_id = 0;
    return stream;
}
ostream& operator<<(ostream& stream, group g)
{
    stream << g.id << ' ' << g.screen_name << ' ' << g.followers << ' ' << g.type;
    if(g.post_id) stream << ' ' << g.post_id;
    stream << '\n';
    return stream;
}
