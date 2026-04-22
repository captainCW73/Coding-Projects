#include <iostream>
using namespace std;
int main() {
  cout << "Enter a temperature in Fahrenheit:";
  double fahrenheit;
  cin >> fahrenheit;
  double celsius = (fahrenheit - 32) * 5 / 9;
  cout << "The temperature in Celsius is: " << celsius;
  return 0;
}