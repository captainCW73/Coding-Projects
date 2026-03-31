fence_posts = int(input(""))
xs = []
ys = []
matchingx = ""
matchingy = ""
for i in range(fence_posts):
    coordinates = input("").split()
    xs.append(int(coordinates[0]))
    ys.append(int(coordinates[1]))

max_area_2 = 0
for i in range(fence_posts):
    for j in range(i + 1, fence_posts):
        for k in range(j + 1, fence_posts):
            if xs[i] == xs[j] and ys[i] == ys[k]:
                height = abs(ys[i] - ys[j])
                width = abs(xs[i] - xs[k])
                
                current_area_2 = width * height
                
                if current_area_2 > max_area_2:
                    max_area_2 = current_area_2

print(max_area_2)