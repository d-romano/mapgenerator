#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <stdint.h>
#include <time.h>
#include <math.h>
#include <algorithm>
using namespace std;

//void diamondSquare(int, double, double*, int);
void diamondStep(int, int, double, double*);
void squareStep(int, int, double, double*);
double getRandFloat(double);
void medianFilter(double *, int );

extern "C" void diamondSquare(int size, double rough, double* grid, int seed)
{
	// Seed random with time or provided seed.
	if (seed != 0)
		srand(seed);
	else
		srand(time(NULL));

	// Seed the grid
	grid[0] =  getRandFloat(rough);
	grid[size-1] = getRandFloat(rough);
	grid[size * (size-1)] = getRandFloat(rough);
	grid[(size*size) -1] =  getRandFloat(rough);
	
	int side = size - 1;
	double addVal = rough;
	// Fill entire grid with calculated values.
	while (side >= 2){
		squareStep(size, side, addVal, grid);
		diamondStep(size, side, addVal, grid);
		// Enrures rresidual noise
		addVal = (addVal / 2);
		side = side / 2;
	}

	// Apply median filter to smooth additional noise
	medianFilter(grid, size);
}


void squareStep(int size, int side, double rough, double* grid)
{
	// Find the center of each square and generate value
	int half_step = side / 2;
	int tl, tr, bl, br;

	double avg; 

	for (int r = 0; r < size-1; r += side){
		for(int c = 0; c < size-1; c += side){
			tl = (r*size) + c;
			tr = (r*size) + (c + side);
			bl = ((r + side) * size) + c;
			br = ((r + side) * size) + (c + side);

			avg = (grid[tl] + grid[tr] + grid[bl] + grid[br] ) / 4;
			grid[((r+half_step)*size) + (c+half_step)] = avg + getRandFloat(rough);
		}
	}
}


void diamondStep(int size, int side, double rough,  double* grid)
{
	//Find the center points of the squares and generate value.
	double avg;
	int t, ri, b, l;
	int half_step = side / 2;

	for (int r = 0; r <  size; r += half_step){
		for (int c = (r+half_step)%side; c < size; c+=side){	
			t = r-half_step <0 ? (((size-1) - half_step) * size) + c : ((r - half_step) * size) + c;
			ri = (r * size) + ((c + half_step) % size);
			b = (((r + half_step) % size)*size) + c;
			l = c - half_step <0 ? (r * size) + ((size-1) - half_step) : (r * size) + (c- half_step);
			 
			avg = (grid[t] + grid[ri] + grid[b] + grid[l]) / 4;
			//cout << t << " " << l << " " << b << " " << ri << "\n";
			// Avg + random val sent to grid.
			grid[(r*size) + c] = avg + getRandFloat(rough);
		}
	} 
}


// Used to sort in ascending order.
int compare(const void* a, const void* b){
	return ( *(double*)a - *(double*)b);
}

void medianFilter(double *grid, int size){
	//cout << "Median filter\n" ;
	// Creates a 3x3 kernel
	int kernelSize = 3;

	// Create a copy of the original image
	double* og_img = new double[size*size];
	copy(grid, grid+(size* size), og_img);

	int fX, fY;

	double medArry[9];

	 for (int r = 1; r < size-1; r++){
	 	for (int c = 1; c < size-1; c++){
			for (int m = 0; m < kernelSize; m++){
				for (int n = 0;  n < kernelSize; n++){
					fX = ((c - 1) + n) % size;
					fY = ((r - 1) + m) % size;
					medArry[(m*3)+n] = og_img[(fY*size) + fX];		
				}
			}
			qsort(medArry, 9, sizeof(double), compare);
			grid[(r*size) + c] = medArry[4];
		}
	}
}

// Generate a random float between -mVal and mVal
double getRandFloat(double mVal)
{
	return (((double)rand() / (double)(RAND_MAX)) * (mVal*2)) - mVal;
}