#pragma once
#include <string>
#include <glad/glad.h>
#include <GLFW/glfw3.h>

class Window {
private:
    GLFWwindow* window;
    int width, height;
    std::string title;

public:
    Window(int width, int height, const std::string& title);
    ~Window();

    bool init();
    void update();
    bool shouldClose() const;
    void setShouldClose(bool value);

    GLFWwindow* getHandle() const { return window; }
    int getWidth() const { return width; }
    int getHeight() const { return height; }
};