#pragma once
#include "Window.h"
#include "Input.h"
#include "Camera.h"
#include "Renderer.h"

class Engine {
private:
    Window window;
    Input input;
    Camera camera;
    Renderer renderer;

    float lastFrameTime;
    float deltaTime;
    bool running;

public:
    Engine(int width, int height, const std::string& title);
    ~Engine();

    void init();
    void run();
    void update();
    void render();

    bool isRunning() const { return running; }
    float getDeltaTime() const { return deltaTime; }

    Window& getWindow() { return window; }
    Input& getInput() { return input; }
    Camera& getCamera() { return camera; }
    Renderer& getRenderer() { return renderer; }
};