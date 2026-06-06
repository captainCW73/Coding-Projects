ax1, ay1, ax2, ay2 = map(int, input().split())
bx1, by1, bx2, by2 = map(int, input().split())


full_area = (ax2 - ax1) * (ay2 - ay1)


ox1 = max(ax1, bx1)
oy1 = max(ay1, by1)
ox2 = min(ax2, bx2)
oy2 = min(ay2, by2)
if ox1>=ox2 or oy1>=oy2:
    print(full_area)
    exit()
covers_width = (ox1 <= ax1 and ox2 >= ax2)

covers_height = (oy1 <= ay1 and oy2 >= ay2)

if not covers_width and not covers_height:
    print(full_area)
else:
    
    min_x = ax2
    max_x = ax2
    min_y = ay1
    max_y = ay2

    if covers_width:
        # can shrink vertically
        if oy1 > ay1:
            max_y = oy1
        else:
            min_y = oy2

    if covers_height:
        # can shrink horizontally
        if ox1 > ax1:
            max_x = ox1
        else:
            min_x = ox2

    print((max_x - min_x) * (max_y - min_y))
