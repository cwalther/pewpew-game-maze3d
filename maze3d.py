import pew
from micropython import const

_LOG_LEVEL_W = const(6)
_LOG_LEVEL_H = const(6)

def run():

	cos = [4,4,3,3,2,1,0,-1,-2,-3,-3,-4,-4,-4,-3,-3,-2,-1,0,1,2,3,3,4]
	sin = cos[18:]+cos[:18]

	with open('m3dlevel.bmp', 'rb') as f:
		f.seek(54)
		textures = f.read(64)
		textures = bytes(textures[4*i] for i in range(16))
		level = f.read()

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
		b = level[(y << (_LOG_LEVEL_W - 1 - 2)) & (((1 << _LOG_LEVEL_H) - 1) << (_LOG_LEVEL_W - 1)) | ((x >> 3) & ((1 << (_LOG_LEVEL_W - 1)) - 1))]
		return (b & 0xF) if (x & 4) else (b >> 4)

	pew.init()
	screen = pew.Pix()

	x = (1 << (_LOG_LEVEL_W + 1))
	y = (1 << (_LOG_LEVEL_H + 1))
	nx = None
	b = 6
	sb = sin[b]
	cb = cos[b]

	while pew.keys():
		pew.tick(0.1)
	while True:
		keys = pew.keys()
		if keys & pew.K_X:
			break
		if keys & pew.K_RIGHT:
			if keys & pew.K_O:
				nx = x + sb
				ny = y - cb
			else:
				b = (b + 23) % 24
				sb = sin[b]
				cb = cos[b]
				#print('xy:', x, y, 'b:', b)
		if keys & pew.K_LEFT:
			if keys & pew.K_O:
				nx = x - sb
				ny = y + cb
			else:
				b = (b + 1) % 24
				sb = sin[b]
				cb = cos[b]
				#print('xy:', x, y, 'b:', b)
		if keys & pew.K_UP:
			nx = x + cb
			ny = y + sb
		if keys & pew.K_DOWN:
			nx = x - cb
			ny = y - sb
		if nx is not None and lookup(nx, ny) == 0:
			x = nx
			y = ny
			nx = None
			#print('xy:', x, y, 'b:', b)
	
		rx = x + 16*cb - 14*sb
		ry = y + 16*sb + 14*cb
		for c in range(8):
			p = 0
			for bx, by in bresenham(x, y, rx, ry):
				p = lookup(bx, by)
				if p != 0:
					bxy = max(abs(bx - x), abs(by - y))
					rxy = max(abs(rx - x), abs(ry - y))
					for r in range(8):
						t = (7*rxy - 8*bxy*(5-2*r))//(4*rxy) - 1
						screen.pixel(c, r, 0 if t < 0 else 73 - 8*r if t >= 4 else ((textures[p] >> (t << 1)) & 3) + 4*(bxy*15//rxy))
					#if keys != 0:
					#	print(rx, ',', ry, ':', bx, ',', by, '=', p, 'z', 64*bxy/rxy)
					break
			else:
				for r in range(8):
					screen.pixel(c, r, 0 if r < 3 else 73 - 8*r)
		
			rx += 4*sb
			ry -= 4*cb
	
		pew.show(screen)
		pew.tick(0.06)

run()
