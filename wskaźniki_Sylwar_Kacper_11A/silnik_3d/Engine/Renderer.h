#pragma once
#include "Shader.h"
#include "Mesh.h"
#include "Light.h"
#include "Camera.h"
#include <vector>
#include <memory>

class Renderer {
private:
    std::vector<std::shared_ptr<Mesh>> meshes;
    std::vector<std::shared_ptr<Light>> lights;
    std::shared_ptr<Shader> defaultShader;
    bool lightingEnabled;
    bool shadingEnabled;

public:
    Renderer();
    ~Renderer();

    void init();
    void render(const Camera& camera);

    void addMesh(std::shared_ptr<Mesh> mesh);
    void addLight(std::shared_ptr<Light> light);

    void setLightingEnabled(bool enabled) { lightingEnabled = enabled; }
    void setShadingEnabled(bool enabled) { shadingEnabled = enabled; }

    bool isLightingEnabled() const { return lightingEnabled; }
    bool isShadingEnabled() const { return shadingEnabled; }
};