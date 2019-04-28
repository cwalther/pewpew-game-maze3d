import pew

def bresenham(ax, ay, bx, by):
	x = ax
	y = ay
	dx = bx - ax
	if dx < 0:
		dx = -dx
		ix = -1
	else:
		ix = 1
	dy = by - ay
	if dy < 0:
		dy = -dy
		iy = -1
	else:
		iy = 1
	dx <<= 1
	dy <<= 1
	sx = dx
	sy = dy
	if dx >= dy:
		sx >>= 1
		while x != bx:
			if sx < sy:
				y += iy
				sx += dx
			x += ix
			sy += dy
			yield x, y
	else:
		sy >>= 1
		while y != by:
			if sy < sx:
				x += ix
				sy += dy
			y += iy
			sx += dx
			yield x, y

keyhistory = 0
def keyevents():
	global keyhistory
	keys = pew.keys()
	events = keys & (~keyhistory | (keyhistory & (keyhistory >> 8) & (keyhistory >> 16) & (keyhistory >> 24)))
	keyhistory = ((keyhistory & 0x3FFFFF) << 8) | keys
	return events

pew.init()
screen = pew.Pix()

x = [1, 6]
y = [1, 6]
active = 0
blink = 0
while True:
	keys = keyevents()
	if keys & pew.K_O:
		active ^= 1
	if keys & pew.K_X:
		break
	if keys & pew.K_RIGHT:
		x[active] = (x[active] + 1) & 7
	if keys & pew.K_LEFT:
		x[active] = (x[active] - 1) & 7
	if keys & pew.K_UP:
		y[active] = (y[active] - 1) & 7
	if keys & pew.K_DOWN:
		y[active] = (y[active] + 1) & 7
	blink = 0 if keys != 0 else (blink + 1) % 6
	
	screen.box(0)
	for px, py in bresenham(x[0], y[0], x[1], y[1]):
		screen.pixel(px, py, 3)
	screen.pixel(x[active^1], y[active^1], active+1)
	if blink < 2:
		screen.pixel(x[active], y[active], 2-active)
	
	pew.show(screen)
	pew.tick(0.06)
