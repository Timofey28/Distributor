#include <bits/stdc++.h>
#include <conio.h>
#include <Windows.h>
#include <dirent.h>
using namespace std;

struct group
{
    string screen_name;
    int followers, id;
    char type;
    group() : id(-1), screen_name(""), followers(-1), type('.') {}
    group(int _id, string sn, int fols, char ch) : id(_id), screen_name(sn), followers(fols), type(ch) {}
    friend istream& operator>>(istream& stream, group& g);
    friend ostream& operator<<(ostream& stream, group& g);
};
void getPools();
void writeBack();
void setColor(int);
vector<vector<group>> pools;
vector<string> paths;
vector<string> exclude; // screen_name групп

int main()
{
    setlocale(0, "");
    getPools();

    string input;
    bool found;
    while(1) {
        system("cls");
        cout << "\n\tУдаленные: ";
        setColor(4);
        if(!exclude.size()) cout << "пока нет";
        else if(exclude.size() == 1) cout << exclude[0];
        else if(exclude.size()) {
            for(int i = 0; i < exclude.size() - 1; ++i)
                cout << exclude[i] << ", ";
            cout << exclude.back();
        }
        setColor(15);
        cout << "\n\tВведи ссылку на группу, которую надо исключить из пула";
        cout << "\n\tЖми "; setColor(10); cout << "просто enter"; setColor(15);
        cout << " для безопасного выхода\n\n\t=> ";
        getline(cin, input);
        while(input[0] == ' ') input.erase(0, 1);
        while(input.back() == ' ') input.pop_back();
        if(input == "") break;
        if(input.find("https://") != string::npos) {
            input = input.substr(input.rfind("/") + 1);
        }
        found = 0;
        for(int i = 0; i < pools.size(); ++i) {
            for(auto x : pools[i]) {
                if(x.screen_name == input) {
                    found = 1;
                    if(find(exclude.begin(), exclude.end(), input) == exclude.end())
                        exclude.push_back(x.screen_name);
                    break;
                }
            }
            if(found) break;
        }
    }

    writeBack();

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
    group gr;
    while((entry = readdir(dir)) != nullptr) {
        string s = entry->d_name;
        if(s != "." && s != ".." && s.substr(0, 2) != "__" && s.substr(s.size() - 4) != ".txt") {
            paths.push_back(s);
            ifstream fin(("Pools/" + s).c_str());
            vector<group> temp;
            while(fin >> gr) temp.push_back(gr);
            fin.close();
            pools.push_back(temp);
        }
    }
}

void writeBack()
{
    DIR *dir = opendir("Pools");
    if(!dir) mkdir("Pools");
    else closedir(dir);
    ofstream fout;
    for(int i = 0; i < paths.size(); ++i) {
        fout.open(("Pools/" + paths[i]).c_str());
        for(auto x : pools[i]) {
            if(find(exclude.begin(), exclude.end(), x.screen_name) == exclude.end())
                fout << x;
        }
        fout.close();
    }
}

void setColor(int text)
{
    HANDLE hStdOut = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hStdOut, (WORD) text);
}

istream& operator>>(istream& stream, group& g)
{
    stream >> g.id >> g.screen_name >> g.followers >> g.type;
    return stream;
}
ostream& operator<<(ostream& stream, group& g)
{
    stream << g.id << ' ' << g.screen_name << ' ' << g.followers << ' ' << g.type << '\n';
    return stream;
}
