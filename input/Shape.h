#include <cmath>

// Any class annotated with this macro will be exposed and have all functions
// exposed.
// Any class deriving from an exposed class will have its constructors exposed.
#ifdef __clang__
#define C_API __attribute__((annotate("GENERATE_C_API")))
#else
#define C_API
#endif

struct Shape
{
  virtual ~Shape()
  {
  }
  virtual double area() const = 0;
  virtual double perimeter() const = 0;
  virtual const char* name() const = 0;
  virtual int sides() const = 0;
  virtual int is_equal(const Shape* s) const = 0;
} C_API;

static const double pi = 3.14159265359;

class Circle : public Shape
{
  const double radius_;

public:
  double area() const override
  {
    return pi * radius_ * radius_;
  }

  double perimeter() const override
  {
    return 2 * pi * radius_;
  }

  const char* name() const override
  {
    return "Circle";
  }

  int sides() const override { return 1; }

  int is_equal(const Shape* s) const override
  {
    if ( auto c = dynamic_cast<const Circle*>(s) )
      return c->radius_ == radius_;
    return false;
  }

  Circle(double radius) : radius_(radius)
  {
    if ( radius < 0 ) 
    { 
      std::string s = "Circle radius \"" + std::to_string(radius_) + "\" must be non-negative.";
      throw std::runtime_error(s);
    }
  }
};

class Square : public Shape
{
  const double side_;

public:
  double area() const override
  {
    return side_ * side_;
  }

  double perimeter() const override
  {
    return 4.0 * side_;
  }

  const char* name() const override
  {
    return "Square";
  }

  int sides() const override { return 4; }
  
  int is_equal(const Shape* s) const override
  {
    if ( auto sq = dynamic_cast<const Square*>(s) )
      return sq->side_ == side_;
    return false;
  }

  Square(double side) : side_(side)
  {
    if ( side_ <= 0.0 )
    {
      std::string s = "Square side \"" + std::to_string(side_) + "\" must be non-negative.";
      throw std::runtime_error(s);
    }
  }
};

class Pentagon : public Shape
{
  const double side_;

public:
  double area() const override
  {
    return 0.25 * sqrt(5. * (5. + 2. * sqrt(5.))) * side_ * side_;
  }

  double perimeter() const override
  {
    return 5.0 * side_;
  }

  const char* name() const override
  {
    return "Pentagon";
  }

  int sides() const override { return 5; }
  
  int is_equal(const Shape* s) const override
  {
    if ( auto p = dynamic_cast<const Pentagon*>(s) )
      return p->side_ == side_;
    return false;
  }

  Pentagon(double side) : side_(side)
  {
    if ( side_ <= 0.0 )
    {
      std::string s = "Pentagon side \"" + std::to_string(side_) + "\" must be non-negative.";
      throw std::runtime_error(s);
    }
  }
};
