#include <iostream>
using namespace std;
int main()
{
    int age = 18;
    bool issafe=true;
    char grade='a';
    int value=grade;
    double rate=100.89;
    int newprice=(int)rate;
    std::cout<<sizeof (age) << endl;
    std:cout<<issafe<<endl;
    cout<<value<<endl;
    cout<<newprice<<endl;

    return 0;
}