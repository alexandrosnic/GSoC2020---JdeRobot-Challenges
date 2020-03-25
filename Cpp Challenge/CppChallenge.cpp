/**
 * Author: Alexandros Nicolaou
 * Solution: Labyrinth, find the largest pathway
 */

#include <iostream>
#include <fstream>
#include <vector>
#include <cstdlib>
#include <string>

using namespace std;

int dirX[] = { -1, 0, 1,  0 };
int dirY[] = { 0, 1, 0, -1 };

void DFS(int x, int y, vector<string>& matrix, vector<vector<bool> >& visited, int& curLen, bool finalPath)
{
	if (finalPath) {
		matrix[x][y] = curLen + '0';
	}

	for (int i = 0; i < 4; ++i) {
		// Move along 4 directions as [up, right, down, left]
		int newX = x + dirX[i];
		int newY = y + dirY[i];
		if (newX >= 0 && newX < matrix.size() &&
			newY >= 0 && newY < matrix[0].length() &&
			matrix[newX][newY] == '.' &&
			visited[newX][newY] == false) {
			// Visit the node
			visited[newX][newY] = true;
			curLen = curLen + 1;
			DFS(newX, newY, matrix, visited, curLen, finalPath);
		}
	}
}

int main()
{

	// Read in the Labyrinth
	ifstream file("map.txt");
	string row, newRow;
	int col = 0;
	vector<string> matrix;
	while (getline(file, row))
	{
		newRow = row;
		matrix.push_back(row);
		col += 1;
	}
	file.close();

	// Write the map
	cout << "The Labyrinth map is:" << endl;
	for (int i = 0; i < matrix.size(); ++i) {
		for (int j = 0; j < matrix[0].length(); ++j) {
			cout << matrix[i][j];
		}
		cout << endl;
	}
	cout << endl;

	// Initialize visited points
	vector<vector<bool> > visited;
	for (int i = 0; i < matrix.size(); ++i) {
		vector<bool> rowBool;
		visited.push_back(rowBool);
		for (int j = 0; j < matrix[0].length(); ++j) {
			visited[i].push_back(false);
		}
	}

	// Find the path
	vector<string> finalPath = matrix;
	vector<vector<bool> > outputVisited = visited;
	int xCoord, yCoord;
	int maxLen = 0;
	int curLen;
	for (int i = 0; i < matrix.size(); ++i) {
		for (int j = 0; j < matrix[0].length(); ++j) {
			if (matrix[i][j] == '#' || visited[i][j] == true) continue;
			curLen = 1;
			visited[i][j] = true;
			DFS(i, j, matrix, visited, curLen, false);
			if (curLen > maxLen) {
				maxLen = curLen;
				xCoord = i;
				yCoord = j;
			}
		}
	}

	// Print the final path
	curLen = 1;
	outputVisited[xCoord][yCoord] = true;
	DFS(xCoord, yCoord, finalPath, outputVisited, curLen, true);
	cout << "The final path is:" << endl;
	for (int i = 0; i < matrix.size(); ++i) {
		for (int j = 0; j < matrix[0].length(); ++j) {
			cout << finalPath[i][j];
		}
		cout << endl;
	}

	return 0;
}