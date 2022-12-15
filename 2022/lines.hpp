#pragma once

#include <cmath>
#include <iostream>
#include "position.hpp"

/// <summary>Finds the orientation of ordered triplet</summary>
/// <returns>1 if clockwise, -1 if counterclockwise, and 0 if collinear.</returns>
int orientation(const Position& p, const Position& q, const Position& r)
{
	int o = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y);
	if (o == 0) return 0;
	return (o > 0) ? 1 : -1;
}

/// <returns>Is point q on line segment pr?</returns>
bool on_segment(const Position& p, const Position& q, const Position& r)
{
	return q.x <= std::max<int>(p.x, r.x) && q.x >= std::min<int>(p.x, r.x) && q.y <= std::max<int>(p.y, r.y) && q.y >= std::min<int>(p.y, r.y);
}

/// <returns>Do line segments pq1 and pq2 intersect?</returns>
bool do_intersect(const Position& p1, const Position& q1, const Position& p2, const Position& q2)
{
	int o1 = orientation(p1, q1, p2);
	int o2 = orientation(p1, q1, q2);
	int o3 = orientation(p2, q2, p1);
	int o4 = orientation(p2, q2, q1);

	// General case
	if (o1 != o2 && o3 != o4)
		return true;

	// Special cases
	// p1, q1 and p2 are collinear and p2 lies on segment p1q1
	if (o1 == 0 && on_segment(p1, p2, q1)) return true;
	
	// p1, q1 and q2 are collinear and q2 lies on segment p1q1
	if (o2 == 0 && on_segment(p1, q2, q1)) return true;
	
	// p2, q2 and p1 are collinear and p1 lies on segment p2q2
	if (o3 == 0 && on_segment(p2, p1, q2)) return true;
	
	// p2, q2 and q1 are collinear and q1 lies on segment p2q2
	if (o4 == 0 && on_segment(p2, q1, q2)) return true;
	
	return false; // Doesn't fall in any of the above cases
}

/// <summary>Calculates the intersection point between pq1 and pq2.</summary>
/// <returns>Position where lines intersect, or INT_MIN if no intersection.</returns>
Position intersection(const Position& p1, const Position& q1, const Position& p2, const Position& q2)
{
	if (!do_intersect(p1, q1, p2, q2))
	{
		//std::cout << "No intersect: " << p1 << q1 << p2 << q2 << std::endl;
		return Position(INT_MIN);
	}

	// They intersect. Find the intersection point.

	// Line pq1 as a1x + b1y = c1
	double a1 = q1.y - p1.y;
	double b1 = p1.x - q1.x;
	double c1 = a1 * p1.x + b1 * p1.y;

	// Line pq2 as a2x + b2y = c2
	double a2 = q2.y - p2.y;
	double b2 = p2.x - q2.x;
	double c2 = a2 * p2.x + b2 * p2.y;

	double determinant = a1 * b2 - a2 * b1;
	if (determinant == 0)
	{
		//std::cout << "Parallel." << p1 << q1 << p2 << q2 << std::endl;
		return Position(INT_MIN);
	}

	double ix = (b2 * c1 - b1 * c2) / determinant;
	double iy = (a1 * c2 - a2 * c1) / determinant;
	Position is(std::round(ix), std::round(iy));
	//std::cout << "INTERSECT @ " << is << " " << p1 << q1 << p2 << q2 << std::endl;
	return is;
	//outIntersection.x = (b2 * c1 - b1 * c2) / determinant;
	//outIntersection.y = (a1 * c2 - a2 * c1) / determinant;
}