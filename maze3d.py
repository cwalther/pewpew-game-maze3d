import pew

def run():

	cos = [4,4,3,3,2,1,0,-1,-2,-3,-3,-4,-4,-4,-3,-3,-2,-1,0,1,2,3,3,4]
	sin = cos[18:]+cos[:18]

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

	def lookup(x, y):
		x >>= 2
		y >>= 2
		if 18 <= x < 22:
			if 18 <= y < 22:
				return 2 + ((x+y) & 1)
			elif 10 <= y < 14:
				return 3
		elif 10 <= x < 14:
			if 18 <= y < 22:
				return 2
			elif 10 <= y < 14:
				return 1
		return 0

	pew.init()
	screen = pew.Pix()

	x = 64
	y = 64
	b = 6

	while pew.keys():
		pew.tick(0.1)
	while True:
		keys = pew.keys()
		if keys & pew.K_O:
			pass
		if keys & pew.K_X:
			break
		if keys & pew.K_RIGHT:
			b = (b + 23) % 24
			#print('xy:', x, y, 'b:', b)
		if keys & pew.K_LEFT:
			b = (b + 1) % 24
			#print('xy:', x, y, 'b:', b)
		if keys & pew.K_UP:
			nx = x + cos[b]
			ny = y + sin[b]
			if lookup(nx, ny) == 0:
				x = nx
				y = ny
			#print('xy:', x, y, 'b:', b)
		if keys & pew.K_DOWN:
			nx = x - cos[b]
			ny = y - sin[b]
			if lookup(nx, ny) == 0:
				x = nx
				y = ny
			#print('xy:', x, y, 'b:', b)
	
		rx = x + 16*cos[b] - 14*sin[b]
		ry = y + 16*sin[b] + 14*cos[b]
		for c in range(8):
			p = 0
			for bx, by in bresenham(x, y, rx, ry):
				p = lookup(bx, by)
				if p != 0:
					bxy = max(abs(bx - x), abs(by - y))
					rxy = max(abs(rx - x), abs(ry - y))
					for r in range(8):
						t = (7*rxy - 8*bxy*(5-2*r))//(4*rxy) - 1
						screen.pixel(c, r, 0 if t < 0 else 1 if t >= 4 else 2+(t&1) if p == 1 else p)
					#if keys != 0:
					#	print(rx, ',', ry, ':', bx, ',', by, '=', p, 'z', 64*bxy/rxy)
					break
			else:
				for r in range(8):
					screen.pixel(c, r, 0 if r < 3 else 1)
		
			rx += 4*sin[b]
			ry -= 4*cos[b]
	
		pew.show(screen)
		pew.tick(0.06)

run()
