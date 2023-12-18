#include <iostream>

/**
 * Range provides a way to iterate over a range of numbers.
 */
template<typename T>
struct Range {

    /** Construct a range given a start and end. */
    Range(T start, T end) : start(start), end(end) {}

    /** Factory function to make a range given a start and length. */
    static Range<T> fromLength(T start, T length) {
        return Range<T>(start, start + length - 1);
    }

    /** The first value in the range. */
    T start;
    /** The last value in the range. */
    T end;
    /** The length of the range. */
    T length() const { return end - start + 1; }

    /** Is the range empty? */
    bool empty() const { return start > end; }

    /** Is the given value in the range? */
    bool contains(T value) const { return value >= start && value <= end; }

    /** Does this range intersect another range? */
    bool intersects(Range<T> const &other) const {
        return contains(other.start) || contains(other.end) || other.contains(start) || other.contains(end);
    }
};

template<typename T>
inline std::ostream &operator<<(std::ostream &Str, Range<T> const &v) {
    Str << "[" << v.start << ".." << v.end << "] " << v.length();
    return Str;
}