#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <stdint.h>
#include <math.h>
#include <chrono>

using namespace std;


void perlinNoise(int, double, double, double, double, double, int, uint8_t*, size_t);
double perlinHelper(double, double, double, double, double, double, int, uint8_t*);
double perlin(double, double, uint8_t*);
double fade(double);
double lerp(double, double, double);
double grad(int, double, double);

// Readable through .so via python.
extern "C"{
	void perlinNoise(int size, double scale, double f, double l, double a, double p, int o, uint8_t *perms, double* grid)
	{
			// Width and height
			int w = size;
			int h = size;
	
			// Create noise value for everything in the grid
			for(int y=0; y < h; y++)
			{
				for(int x = 0; x < w; x++)
				{
					grid[(y*w) + x] = perlinHelper((double)x/w/(double)scale, (double)y/h/(double)scale, f, l, a, p ,o, perms);
				}
			}
	}
}


double perlinHelper(double x, double y, double f, double l, double a, double p, int o, uint8_t*perms)
{
	double noiseVal = 0;
	for(int i=0; i < o; i++){
		noiseVal = noiseVal + (perlin(x*f, y*f, perms)*a);
		a = a*p;
		f = f * l;
	}
	return noiseVal/o;
}


double perlin(double x, double y, uint8_t* p)
{
	int cX = (int)floor(x) & 0xFF;
	int cY = (int)floor(y) & 0xFF;

	double pX = x - floor(x);
	double pY = y - floor(y);

	int g1 = (int)p[((int)p[cX] + cY) % 256];
	int g2 = (int)p[((int)p[cX+1] + cY) % 256];
	int g3 = (int)p[((int)p[cX] + cY+1) % 256];
	int g4 = (int)p[((int)p[cX+1] + cY+1) % 256];

	
	double d1 = grad(g1, pX, pY);
	double d2 = grad(g2, pX-1, pY);
	double d3 = grad(g3, pX, pY-1);
	double d4 = grad(g4, pX-1, pY-1);

	double u = fade(pX);
	double v = fade(pY);

	double ret =  lerp(v, lerp(u, d1, d2), lerp(u, d3, d4));
	return ret;
}


double fade(double t){
	return t * t * t * (t * (t * 6 - 15) + 10);
}


double lerp(double t, double a, double b){
	return a + (double)t * (b - a);
	
}


double grad(int permHash, double x, double y)
{
	int gradDir = permHash & 3;

	switch(gradDir){
		case(0):
			return x + y;
		case(1):
			return -x + y;
		case(2):
			return x - y;
		case (3):
			return -x - y;
		default:
			return 0;
	}
}


