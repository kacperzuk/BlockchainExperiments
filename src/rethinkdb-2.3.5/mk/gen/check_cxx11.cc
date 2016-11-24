
// Verify that std::map uses the move constructor

#include <map>

struct C {
    C(const C&) = delete;

    C() { }
    C(C &&) { }
};

int main() {
    std::map<int, C> m;
    m.insert(std::make_pair(0, C()));
}


