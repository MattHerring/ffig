#ifdef __clang__
#define C_API __attribute__((annotate("GENERATE_C_API")))
#else
#define C_API
#endif

struct Asset
{
  virtual double PV() const = 0;
  virtual ~Asset() = default;
} C_API;

struct CDO : Asset
{
  CDO() {}

  double PV() const { return 0.0; }
};

