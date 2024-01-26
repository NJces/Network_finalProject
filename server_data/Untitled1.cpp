#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>

std::mutex mtx;
std::condition_variable cv;
int current_number = 1;

void write(const std::string& message) {
    std::unique_lock<std::mutex> lock(mtx);
    // Wait until it's the turn for the current number
    cv.wait(lock, [message] { return std::stoi(message) == current_number; });

    // Output the message
    std::cout << message << std::endl;

    // Increment the current number
    ++current_number;

    // Notify other waiting threads
    cv.notify_all();
}

int main() {
    std::thread P1([&]() {
        write("1");
        write("2");
    });

    std::thread P2([&]() {
        write("3");
        write("4");
    });

    std::thread P3([&]() {
        write("5");
        write("6");
    });

    P1.join();
    P2.join();
    P3.join();

    return 0;
}

