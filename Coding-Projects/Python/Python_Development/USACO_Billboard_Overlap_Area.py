board1 = list(map(int, input().split()))
board2 = list(map(int, input().split()))

# Lawn mower billboard
lx1, ly1, lx2, ly2 = board1
# Feed billboard
fx1, fy1, fx2, fy2 = board2

area1 = (lx2 - lx1) * (ly2 - ly1)
area2 = (fx2 - fx1) * (fy2 - fy1)
overlap_x1 = max(lx1, fx1)
overlap_y1 = max(ly1, fy1)
overlap_x2 = min(lx2, fx2)
overlap_y2 = min(ly2, fy2)
overlap_area = max(0, overlap_x2 - overlap_x1) * max(0, overlap_y2 - overlap_y1)
remaining_area_feedboard = area1 - overlap_area
if remaining_area_feedboard %2 == 0:
    print(remaining_area_feedboard)
else:
    print(area1)