number_cows = int(input(""))

line_a = input("").capitalize() 
list_a = list(line_a)

line_b = input("").capitalize()
list_b = list(line_b)
ans = 0
in_mismatch = False
for i in range(number_cows):
   if list_a[i] != list_b[i]:
       if not in_mismatch:
           ans += 1
           in_mismatch = True
   else:
       in_mismatch = False
print(ans)