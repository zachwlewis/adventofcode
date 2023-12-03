#pragma once

#include <sstream>
#include <cmath>

struct Position
{
  Position() : x(0), y(0) {}
  Position(int inX, int inY) : x(inX), y(inY) {}
  Position(int inValue) : x(inValue), y(inValue) {}
  int x = 0;
  int y = 0;
  Position& operator+=(const Position& rhs)
  {
    x += rhs.x;
    y += rhs.y;
    return *this;
  }
  Position& operator -=(const Position& rhs)
  {
    x -= rhs.x;
    y -= rhs.y;
    return *this;
  }
  friend Position operator+(Position lhs, const Position& rhs)
  {
    lhs += rhs;
    return lhs;
  }
  friend Position operator-(Position lhs, const Position& rhs)
  {
    lhs -= rhs;
    return lhs;
  }
  friend bool operator<(const Position& lhs, const Position& rhs) { return lhs.x < rhs.x || (lhs.x==rhs.x && lhs.y < rhs.y); }
  friend bool operator>(const Position& lhs, const Position& rhs) { return rhs < lhs; }
  friend bool operator<=(const Position& lhs, const Position& rhs) { return !(lhs > rhs); }
  friend bool operator>=(const Position& lhs, const Position& rhs) { return !(lhs < rhs); }
  friend bool operator==(const Position& lhs, const Position& rhs) { return lhs.x == rhs.x && lhs.y == rhs.y; }
  friend bool operator!=(const Position& lhs, const Position& rhs) { return !(lhs == rhs); }
  
  Position normalize() const
  {
    Position out;
    out.x = x == 0 ? 0 : x / std::abs(x);
    out.y = y == 0 ? 0 : y / std::abs(y);
    return out;
  }
  Position size() const { return {std::abs(x), std::abs(y)}; }
  std::string tostring() const
  {
    std::stringstream ss;
    ss << "{" << x << ", " << y << "}";
    return ss.str();
  }

  int manhattan(const Position& other) const { return std::abs(x - other.x) + std::abs(y - other.y); }
};

inline std::ostream & operator<<(std::ostream & Str, Position const & v) { 
  Str << v.tostring();
  return Str;
}
