#include <cmath>
#include <iostream>
using namespace std;
int main() {
  cout << "Enter the radius of the circle: ";
  double radius;
  cin >> radius;
  const double pi = 3.14;
  double area = pi * pow(radius, 2);
  cout << "The area of the circle is: " << area;
  return 0;
}