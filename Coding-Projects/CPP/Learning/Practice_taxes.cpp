#include <iostream>
using namespace std;
int main() {
  double sales = 95000;
  double state_tax = sales * 0.04;
  double county_tax = sales * 0.02;
  double total_tax = state_tax + county_tax;
  double total_after_tax = sales - total_tax;
  cout << "Total sales: $" << sales << endl;
  cout << "State tax: $" << state_tax << endl;
  cout << "County tax: $" << county_tax << endl;
  cout << "Total tax: $" << total_tax << endl;
  cout << "Total after tax: $" << total_after_tax << endl;
  return 0;
}